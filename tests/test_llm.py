"""Tests for LLM module — extract_json, ClaudeCLI, load_prompt_template."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from qadris_datasourcediscovery.exceptions import LLMError
from qadris_datasourcediscovery.llm import (
    ClaudeCLI,
    _fix_malformed_json,
    extract_json,
    load_prompt_template,
)


# =====================================================================
# _fix_malformed_json
# =====================================================================


class TestFixMalformedJson:
    def test_trailing_comma_in_object(self) -> None:
        assert _fix_malformed_json('{"a": 1, "b": 2,}') == '{"a": 1, "b": 2}'

    def test_trailing_comma_in_array(self) -> None:
        assert _fix_malformed_json("[1, 2, 3,]") == "[1, 2, 3]"

    def test_no_trailing_comma(self) -> None:
        s = '{"a": 1}'
        assert _fix_malformed_json(s) == s

    def test_nested_trailing_commas(self) -> None:
        s = '{"a": [1, 2,], "b": {"c": 3,},}'
        result = _fix_malformed_json(s)
        assert ",}" not in result
        assert ",]" not in result


# =====================================================================
# extract_json
# =====================================================================


class TestExtractJson:
    def test_plain_json(self) -> None:
        result = extract_json('{"key": "value"}')
        assert result == {"key": "value"}

    def test_json_with_markdown_fence(self) -> None:
        text = 'Here is the result:\n```json\n{"tags": ["price"]}\n```\nDone.'
        result = extract_json(text)
        assert result == {"tags": ["price"]}

    def test_json_with_generic_fence(self) -> None:
        text = 'Result:\n```\n{"a": 1}\n```'
        result = extract_json(text)
        assert result == {"a": 1}

    def test_json_embedded_in_text(self) -> None:
        text = 'The answer is {"domain_tags": ["revenue"]} as shown.'
        result = extract_json(text)
        assert result == {"domain_tags": ["revenue"]}

    def test_json_with_trailing_comma(self) -> None:
        text = '{"tags": ["a", "b",],}'
        result = extract_json(text)
        assert result == {"tags": ["a", "b"]}

    def test_no_json_raises(self) -> None:
        with pytest.raises(LLMError, match="Cannot extract JSON"):
            extract_json("This is just plain text with no JSON")

    def test_returns_dict_not_list(self) -> None:
        # If the JSON is a list, extract_json should fail since it expects dict
        with pytest.raises(LLMError):
            extract_json("[1, 2, 3]")


# =====================================================================
# load_prompt_template
# =====================================================================


class TestLoadPromptTemplate:
    def test_load_and_format(self, tmp_path: Path) -> None:
        template = tmp_path / "test.txt"
        template.write_text("Hello {name}, source={source}")
        result = load_prompt_template(template, name="World", source="twse")
        assert result == "Hello World, source=twse"

    def test_missing_file(self, tmp_path: Path) -> None:
        with pytest.raises(LLMError, match="not found"):
            load_prompt_template(tmp_path / "missing.txt")

    def test_missing_variable(self, tmp_path: Path) -> None:
        template = tmp_path / "test.txt"
        template.write_text("Hello {name} {missing}")
        with pytest.raises(LLMError, match="Missing template variable"):
            load_prompt_template(template, name="World")


# =====================================================================
# ClaudeCLI
# =====================================================================


class TestClaudeCLI:
    def test_name_with_model(self) -> None:
        cli = ClaudeCLI(model="claude-haiku-4-5-20251001")
        assert "claude-haiku" in cli.name

    def test_name_without_model(self) -> None:
        cli = ClaudeCLI()
        assert cli.name == "claude-cli"

    def test_prompt_success(self) -> None:
        cli = ClaudeCLI()
        mock_result = type(
            "Result", (), {"returncode": 0, "stdout": "hello", "stderr": ""}
        )()
        with patch("subprocess.run", return_value=mock_result):
            result = cli.prompt("test")
        assert result == "hello"

    def test_prompt_nonzero_exit(self) -> None:
        cli = ClaudeCLI()
        mock_result = type(
            "Result",
            (),
            {"returncode": 1, "stdout": "", "stderr": "error occurred"},
        )()
        with patch("subprocess.run", return_value=mock_result):
            with pytest.raises(LLMError, match="exited with code 1"):
                cli.prompt("test")

    def test_prompt_empty_response(self) -> None:
        cli = ClaudeCLI()
        mock_result = type(
            "Result", (), {"returncode": 0, "stdout": "   ", "stderr": ""}
        )()
        with patch("subprocess.run", return_value=mock_result):
            with pytest.raises(LLMError, match="empty response"):
                cli.prompt("test")

    def test_prompt_timeout(self) -> None:
        cli = ClaudeCLI(timeout=1)
        import subprocess

        with patch(
            "subprocess.run", side_effect=subprocess.TimeoutExpired("cmd", 1)
        ):
            with pytest.raises(LLMError, match="timed out"):
                cli.prompt("test")

    def test_prompt_not_found(self) -> None:
        cli = ClaudeCLI(command="nonexistent-cmd")
        with patch("subprocess.run", side_effect=FileNotFoundError):
            with pytest.raises(LLMError, match="not found"):
                cli.prompt("test")

    def test_prompt_json_success(self) -> None:
        cli = ClaudeCLI()
        mock_result = type(
            "Result",
            (),
            {
                "returncode": 0,
                "stdout": '{"domain_tags": ["price"]}',
                "stderr": "",
            },
        )()
        with patch("subprocess.run", return_value=mock_result):
            result = cli.prompt_json("test")
        assert result == {"domain_tags": ["price"]}

    def test_prompt_with_model_flag(self) -> None:
        cli = ClaudeCLI(model="test-model")
        mock_result = type(
            "Result", (), {"returncode": 0, "stdout": "ok", "stderr": ""}
        )()
        with patch("subprocess.run", return_value=mock_result) as mock_run:
            cli.prompt("test")
        cmd = mock_run.call_args[0][0]
        assert "--model" in cmd
        assert "test-model" in cmd

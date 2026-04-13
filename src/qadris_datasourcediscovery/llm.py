"""LLM CLI wrapper — claude -p 封裝。

基於 InvestLitBase 的 claude_cli.py，適配本套件使用。
"""

import json
import logging
import re
import subprocess
from pathlib import Path

from qadris_datasourcediscovery.exceptions import LLMError

logger = logging.getLogger(__name__)


class ClaudeCLI:
    """Claude Code CLI wrapper（claude -p）"""

    def __init__(
        self, command: str = "claude", model: str = "", timeout: int = 120
    ) -> None:
        self._command = command
        self._model = model
        self._default_timeout = timeout

    def prompt(self, text: str, timeout: int | None = None) -> str:
        """送出 prompt，回傳 raw text 回應。"""
        t = timeout or self._default_timeout
        try:
            cmd = [self._command, "-p", text]
            if self._model:
                cmd.extend(["--model", self._model])
            logger.debug(
                "Calling %s -p (model=%s, timeout=%ds)",
                self._command,
                self._model or "default",
                t,
            )
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=t,
            )
            if result.returncode != 0:
                stderr = result.stderr.strip()
                raise LLMError(
                    f"{self._command} exited with code {result.returncode}: {stderr}"
                )
            response = result.stdout.strip()
            if not response:
                raise LLMError(f"{self._command} returned empty response")
            logger.debug("LLM response length: %d chars", len(response))
            return response
        except subprocess.TimeoutExpired as e:
            raise LLMError(f"{self._command} timed out after {t}s") from e
        except FileNotFoundError as e:
            raise LLMError(
                f"{self._command} not found. Is it installed and in PATH?"
            ) from e

    def prompt_json(self, text: str, timeout: int | None = None) -> dict:
        """送出 prompt，解析並回傳 JSON 回應。"""
        raw = self.prompt(text, timeout=timeout)
        return extract_json(raw)

    @property
    def name(self) -> str:
        if self._model:
            return f"{self._command}-cli({self._model})"
        return f"{self._command}-cli"


def load_prompt_template(template_path: Path, **kwargs: str) -> str:
    """載入 prompt 模板並填入變數。

    模板使用 {variable_name} 格式的佔位符。
    """
    if not template_path.exists():
        raise LLMError(f"Prompt template not found: {template_path}")
    template = template_path.read_text(encoding="utf-8")
    try:
        return template.format(**kwargs)
    except KeyError as e:
        raise LLMError(f"Missing template variable: {e}") from e


def _fix_malformed_json(s: str) -> str:
    """修復 LLM 常見的 JSON 格式錯誤。"""
    s = re.sub(r',\s*"[^"]*"\s*([}\]])', r"\1", s)
    s = re.sub(r',\s*"[^"]*\s*([}\]])', r"\1", s)
    s = re.sub(r",\s*([}\]])", r"\1", s)
    return s


def extract_json(text: str) -> dict:
    """從 LLM 回應中擷取 JSON。"""
    text = text.strip()

    def _try_parse(s: str) -> dict | None:
        try:
            return json.loads(s)
        except json.JSONDecodeError:
            pass
        try:
            return json.loads(_fix_malformed_json(s))
        except json.JSONDecodeError:
            return None

    if (result := _try_parse(text)) is not None:
        return result

    if "```json" in text:
        start = text.index("```json") + len("```json")
        end = text.index("```", start)
        json_str = text[start:end].strip()
        if (result := _try_parse(json_str)) is not None:
            return result

    if "```" in text:
        start = text.index("```") + len("```")
        end = text.index("```", start)
        json_str = text[start:end].strip()
        if (result := _try_parse(json_str)) is not None:
            return result

    first_brace = text.find("{")
    last_brace = text.rfind("}")
    if first_brace != -1 and last_brace != -1:
        json_str = text[first_brace : last_brace + 1]
        if (result := _try_parse(json_str)) is not None:
            return result

    raise LLMError(f"Cannot extract JSON from LLM response:\n{text[:500]}")

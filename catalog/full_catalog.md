# Taiwan Official Financial Data Source Catalog

**Total: 433 endpoints**

## Summary Statistics

| Source | Type | Total | OK | Empty | Error | History |
|--------|------|-------|----|-------|-------|---------|
| TWSE | openapi | 143 | 120 | 23 | 0 | 0 |
| TWSE | web | 20 | 20 | 0 | 0 | 20 |
| TPEx | openapi | 225 | 207 | 18 | 0 | 0 |
| TPEx | web | 15 | 3 | 0 | 12 | 15 |
| MOPS | web | 30 | 28 | 0 | 2 | 28 |

## TWSE (Taiwan Stock Exchange)

### OpenAPI (143 endpoints)

#### 公司治理

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/opendata/t187ap46_L_21` | 上市公司企業ESG資訊揭露彙總資料-職業安全衛生 | empty | N | 0 |  |
| `/opendata/t187ap45_L` | 上市公司股利分派情形 | ok | N | 1014 | 出表日期, 公司代號, 公司名稱, 決議（擬議）進度, 股利年度 |
| `/opendata/t187ap46_L_20` | 上市公司企業ESG資訊揭露彙總資料-反競爭行為法律訴訟 | empty | N | 0 |  |
| `/opendata/t187ap46_L_19` | 上市公司企業ESG資訊揭露彙總資料-風險管理政策 | empty | N | 0 |  |
| `/opendata/t187ap46_L_18` | 上市公司企業ESG資訊揭露彙總資料-持股及控制力 | empty | N | 0 |  |
| `/opendata/t187ap46_L_17` | 上市公司企業ESG資訊揭露彙總資料-普惠金融 | empty | N | 0 |  |
| `/opendata/t187ap46_L_16` | 上市公司企業ESG資訊揭露彙總資料-資訊安全 | empty | N | 0 |  |
| `/opendata/t187ap46_L_15` | 上市公司企業ESG資訊揭露彙總資料-社區關係 | empty | N | 0 |  |
| `/opendata/t187ap46_L_14` | 上市公司企業ESG資訊揭露彙總資料-產品品質與安全 | empty | N | 0 |  |
| `/opendata/t187ap46_L_13` | 上市公司企業ESG資訊揭露彙總資料-供應鏈管理 | empty | N | 0 |  |
| `/opendata/t187ap46_L_12` | 上市公司企業ESG資訊揭露彙總資料-食品安全 | empty | N | 0 |  |
| `/opendata/t187ap46_L_11` | 上市公司企業ESG資訊揭露彙總資料-產品生命週期 | empty | N | 0 |  |
| `/opendata/t187ap46_L_10` | 上市公司企業ESG資訊揭露彙總資料-燃料管理 | empty | N | 0 |  |
| `/opendata/t187ap46_L_9` | 上市公司企業ESG資訊揭露彙總資料-功能性委員會 | empty | N | 0 |  |
| `/opendata/t187ap46_L_8` | 上市公司企業ESG資訊揭露彙總資料-氣候相關議題管理 | empty | N | 0 |  |
| `/opendata/t187ap05_P` | 公開發行公司每月營業收入彙總表 | ok | N | 299 | 出表日期, 資料年月, 公司代號, 公司名稱, 產業別 |
| `/opendata/t187ap46_L_7` | 上市公司企業ESG資訊揭露彙總資料-投資人溝通 | empty | N | 0 |  |
| `/opendata/t187ap46_L_6` | 上市公司企業ESG資訊揭露彙總資料-董事會 | empty | N | 0 |  |
| `/opendata/t187ap46_L_5` | 上市公司企業ESG資訊揭露彙總資料-人力發展 | empty | N | 0 |  |
| `/opendata/t187ap46_L_4` | 上市公司企業ESG資訊揭露彙總資料-廢棄物管理 | empty | N | 0 |  |
| `/opendata/t187ap46_L_3` | 上市公司企業ESG資訊揭露彙總資料-水資源管理 | empty | N | 0 |  |
| `/opendata/t187ap46_L_2` | 上市公司企業ESG資訊揭露彙總資料-能源管理 | empty | N | 0 |  |
| `/opendata/t187ap46_L_1` | 上市公司企業ESG資訊揭露彙總資料-溫室氣體排放 | empty | N | 0 |  |
| `/company/applylistingForeign` | 外國公司向證交所申請第一上市之公司 | ok | N | 123 | No, Code, Company, ApplicationDate, Chairman |
| `/company/newlisting` | 最近上市公司 | ok | N | 777 | Code, Company, ApplicationDate, Chairman, Amoun... |
| `/company/suspendListingCsvAndHtml` | 終止上市公司 | ok | N | 263 | DelistingDate, Company, Code |
| `/company/applylistingLocal` | 申請上市之本國公司 | ok | N | 685 | Code, Company, ApplicationDate, Chairman, Amoun... |
| `/opendata/t187ap04_L` | 上市公司每日重大訊息 | ok | N | 103 | 出表日期, 發言日期, 發言時間, 公司代號, 公司名稱 |
| `/opendata/t187ap03_L` | 上市公司基本資料 | ok | N | 1081 | 出表日期, 公司代號, 公司名稱, 公司簡稱, 外國企業註冊地國 |
| `/opendata/t187ap02_L` | 上市公司持股逾 10% 大股東名單 | ok | N | 946 | 出表日期, 公司代號, 公司名稱, 大股東名稱 |
| `/opendata/t187ap14_L` | 上市公司各產業EPS統計資訊 | ok | N | 1070 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap08_L` | 上市公司董事、監察人持股不足法定成數彙總表 | ok | N | 30 | 出表日期, 公司代號, 公司名稱, 已發行股份總額, 全體董事應持有股數 |
| `/opendata/t187ap11_L` | 上市公司董監事持股餘額明細資料 | ok | N | 27224 | 出表日期, 資料年月, 公司代號, 公司名稱, 職稱 |
| `/opendata/t187ap12_L` | 上市公司每日內部人持股轉讓事前申報表-持股轉讓日報表 | ok | N | 3 | 出表日期, 公司代號, 公司名稱, 申報人身分, 姓名 |
| `/opendata/t187ap13_L` | 上市公司每日內部人持股轉讓事前申報表-持股未轉讓日報表 | ok | N | 3 | 出表日期, 公司代號, 公司名稱, 申報人身分, 姓名 |
| `/opendata/t187ap22_L` | 上市公司金管會證券期貨局裁罰案件專區 | ok | N | 10 | 出表日期, 發函日期, 股票代號, 公司名稱, 違規事由 |
| `/opendata/t187ap30_L` | 上市公司獨立董監事兼任情形彙總表 | ok | N | 14121 | 出表日期, 序號, 公司代號, 公司名稱, 職稱 |
| `/opendata/t187ap29_A_L` | 上市公司董事酬金相關資訊  | ok | N | 972 | 出表日期, 產業類別, 公司代號, 公司名稱, 董事酬金-前年支付 |
| `/opendata/t187ap29_B_L` | 上市公司監察人酬金相關資訊  | ok | N | 7 | 出表日期, 產業類別, 公司代號, 公司名稱, 監察人酬金-前年支付 |
| `/opendata/t187ap29_C_L` | 上市公司合併報表董事酬金相關資訊  | ok | N | 999 | 出表日期, 產業類別, 公司代號, 公司名稱, 董事酬金-前年支付 |
| `/opendata/t187ap29_D_L` | 上市公司合併報表監察人酬金相關資訊  | ok | N | 6 | 出表日期, 產業類別, 公司代號, 公司名稱, 監察人酬金-前年支付 |
| `/opendata/t187ap23_L` | 上市公司違反資訊申報、重大訊息及說明記者會規定專區 | ok | N | 11 | 出表日期, 發函日期, 股票代號, 公司名稱, 違規事由 |
| `/opendata/t187ap03_P` | 公開發行公司基本資料 | ok | N | 301 | 出表日期, 公司代號, 公司名稱, 公司簡稱, 外國企業註冊地國 |
| `/announcement/punish` | 集中市場公布處置股票 | ok | N | 7 | Number, Date, Code, Name, NumberOfAnnouncement |
| `/opendata/t187ap10_L` | 上市公司董事、監察人持股不足法定成數連續達3個月以上彙總表 | ok | N | 14 | 出表日期, 連續不足達3個月, 連續不足達4個月, 連續不足達5個月, 連續不足達6個月 |
| `/opendata/t187ap38_L` | 上市公司股東會公告-召集股東常(臨時)會公告資料彙總表(95年度起適用) | ok | N | 1074 | 出表日期, 公司代號, 公司名稱, 股東常(臨時)會日期-常或臨時, 股東常(臨時)會日期-日期 |
| `/opendata/t187ap24_L` | 上市公司經營權及營業範圍異(變)動專區-經營權異動公司 | ok | N | 12 | 出表日期, 公司代號, 公司名稱, 經營權異動日期, 經營權異動說明 |
| `/opendata/t187ap26_L` | 上市公司經營權及營業範圍異(變)動專區-經營權異動且營業範圍重大變更停止買賣公司 | empty | N | 0 |  |
| `/opendata/t187ap41_L` | 上市公司召開股東常 (臨時) 會日期、地點及採用電子投票情形等資料彙總表 | ok | N | 1074 | 出表日期, 公司代號, 公司名稱, 公司地址, 股東常(臨時)會 |
| `/opendata/t187ap25_L` | 上市公司經營權及營業範圍異(變)動專區-營業範圍重大變更公司 | ok | N | 1 | 出表日期, 序號, 年度, 季別, 公司代號 |
| `/opendata/t187ap27_L` | 上市公司經營權及營業範圍異(變)動專區-經營權異動且營業範圍重大變更列為變更交易公司 | empty | N | 0 |  |
| `/opendata/t187ap32_L` | 上市公司公司治理之相關規程規則 | ok | N | 10927 | 出表日期, 公司代號, 公司名稱, 公司治理之相關規程規則 |
| `/opendata/t187ap33_L` | 上市公司董事長是否兼任總經理 | ok | N | 1081 | 出表日期, 公司代號, 公司名稱, 董事長, 總經理 |
| `/opendata/t187ap09_L` | 上市公司董事、監察人質權設定占董事及監察人實際持有股數彙總表 | ok | N | 9 | 出表日期, 百分比, 公司名稱 |
| `/opendata/t187ap34_L` | 上市公司採累積投票制、全額連記法、候選人提名制選任董監事及當選資料彙總表 | ok | N | 2656 | 出表日期, 公司代號, 公司名稱, 股東常(臨時)會日期-常或臨時, 股東常(臨時)會日期-日期 |
| `/opendata/t187ap35_L` | 上市公司股東行使提案權情形彙總表 | ok | N | 404 | 出表日期, 公司代號, 公司名稱, 召開股東會日期, 股東依公司法第172條之1行使提案權-提... |

#### 其他

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/opendata/t187ap47_L` | 基金基本資料彙總表 | ok | N | 251 | 出表日期, 基金代號, 基金簡稱, 基金類型, 基金中文名稱 |
| `/news/eventList` | 證交所活動訊息 | ok | N | 45 | No, Title, Details |
| `/news/newsList` | 證交所新聞 | ok | N | 200 | Title, Url, Date |
| `/exchangeReport/BFI61U` | 中央登錄公債補息資料表 | ok | N | 282 | Code, Name, IssuedDate, StartingDate, CouponRate |

#### 券商資料

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/ETFReport/ETFRank` | 定期定額交易戶數統計排行月報表 | ok | N | 20 | No, STOCKsSecurityCode, STOCKsName, STOCKsNumbe... |
| `/brokerService/secRegData` | 開辦定期定額業務證券商名單 | ok | N | 21 | SecuritiesFirmCode, Name, BrokerageBusinessStar... |
| `/brokerService/brokerList` | 證券商總公司基本資料 | ok | N | 64 | Code, Name, EstablishmentDate, Address, Telephone |
| `/opendata/t187ap01` | 券商業務別人員數 | ok | N | 4 | 出表日期, 職位, 受託買賣, 受託買賣（衍生性商品銷售）, 內部稽核 |
| `/opendata/t187ap20` | 各券商每月月計表 | ok | N | 47515 | 出表日期, 券商代號, 券商名稱, 科目, 會計科目名稱 |
| `/opendata/t187ap21` | 各券商收支概況表資料 | ok | N | 19175 | 出表日期, 券商代號, 券商名稱, 科目, 會計科目名稱 |
| `/opendata/t187ap18` | 證券商基本資料 | ok | N | 66 | 出表日期, 證券代號, 券商(證券IB)簡稱, 登記資本額（仟元）, 實收資本額（仟元） |
| `/opendata/OpenData_BRK01` | 證券商營業員男女人數統計資料 | ok | N | 860 | 出表日期, 證券商代號, 男性員工人數, 女性員工人數, 總人數 |
| `/opendata/OpenData_BRK02` | 證券商分公司基本資料 | ok | N | 868 | 出表日期, 證券商代號, 證券商名稱, 開業日, 地址 |

#### 指數

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/exchangeReport/MI_INDEX4` | 每日上市上櫃跨市場成交資訊 | ok | N | 5 | Date, TradeValue, FormosaIndex, Change |
| `/indicesReport/FRMSA` | 寶島股價指數歷史資料 | ok | N | 5 | Date, FormosaIndex, FormosaTotalReturnIndex |
| `/indicesReport/TAI50I` | 臺灣 50 指數歷史資料 | ok | N | 5 | Date, Taiwan50Index, Taiwan50TotalReturnIndex |
| `/indicesReport/MI_5MINS_HIST` | 發行量加權股價指數歷史資料 | ok | N | 5 | Date, OpeningIndex, HighestIndex, LowestIndex, ... |
| `/indicesReport/MFI94U` | 發行量加權股價報酬指數 | ok | N | 5 | Date, TAIEXTotalReturnIndex |

#### 權證

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/opendata/t187ap36_L` | 上市認購(售)權證年度發行量概況統計表 | ok | N | 54321 | 出表日期, 發行人代號, 發行人名稱, 權證代號, 名稱 |
| `/opendata/t187ap43_L` | 上市認購(售)權證交易人數檔 | ok | N | 1 | 出表日期, 日期, 人數 |
| `/opendata/t187ap42_L` | 上市認購(售)權證每日成交資料檔 | ok | N | 32435 | 出表日期, 交易日期, 權證代號, 權證名稱, 成交金額 |

#### 證券交易

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/exchangeReport/BWIBBU_ALL` | 上市個股日本益比、殖利率及股價淨值比（依代碼查詢） | ok | N | 1070 | Date, Code, Name, PEratio, DividendYield |
| `/exchangeReport/STOCK_DAY_AVG_ALL` | 上市個股日收盤價及月平均價 | ok | N | 21944 | Date, Code, Name, ClosingPrice, MonthlyAverageP... |
| `/exchangeReport/STOCK_DAY_ALL` | 上市個股日成交資訊 | ok | N | 1349 | Date, Code, Name, TradeVolume, TradeValue |
| `/exchangeReport/FMSRFK_ALL` | 上市個股月成交資訊 | ok | N | 30623 | Month, Code, Name, HighestPrice, LowestPrice |
| `/exchangeReport/FMNPTK_ALL` | 上市個股年成交資訊 | ok | N | 72048 | Year, Code, Name, TradeVolume, TradeValue |
| `/exchangeReport/MI_INDEX` | 每日收盤行情-大盤統計資訊 | ok | N | 267 | 日期, 指數, 收盤指數, 漲跌, 漲跌點數 |
| `/fund/MI_QFIIS_cat` | 集中市場外資及陸資投資類股持股比率表 | ok | N | 36 | IndustryCat, Numbers, ShareNumber, ForeignMainl... |
| `/fund/MI_QFIIS_sort_20` | 集中市場外資及陸資持股前 20 名彙總表 | ok | N | 20 | Rank, Code, Name, ShareNumber, AvailableShare |
| `/exchangeReport/TWT88U` | 上市個股首五日無漲跌幅 | ok | N | 2 | SecurCode, SecurName, 1stTradingDate, 5thTradin... |
| `/Announcement/BFZFZU_T` | 投資理財節目異常推介個股 | ok | N | 1 | Number, Code, Name, Date |
| `/exchangeReport/TWTB4U` | 上市股票每日當日沖銷交易標的及統計 | ok | N | 1194 | Date, Code, Name, Suspension |
| `/exchangeReport/TWTBAU1` | 集中市場暫停先賣後買當日沖銷交易標的預告表 | ok | N | 466 | Code, Name, StartDate, EndDate, Reason |
| `/exchangeReport/TWTBAU2` | 集中市場暫停先賣後買當日沖銷交易歷史查詢 | ok | N | 137 | Code, Name, StartDate, EndDate, Reason |
| `/exchangeReport/MI_5MINS` | 每 5 秒委託成交統計 | ok | N | 3241 | Time, AccBidOrders, AccBidVolume, AccAskOrders,... |
| `/exchangeReport/FMTQIK` | 集中市場每日市場成交資訊 | ok | N | 5 | Date, TradeVolume, TradeValue, Transaction, TAIEX |
| `/exchangeReport/MI_INDEX20` | 集中市場每日成交量前二十名證券 | ok | N | 20 | Date, Rank, Code, Name, TradeVolume |
| `/exchangeReport/TWT53U` | 集中市場零股交易行情單 | ok | N | 1333 | Code, Name, TradeVolume, Transaction, TradeValue |
| `/exchangeReport/TWTAWU` | 集中市場暫停交易證券 | ok | N | 1 | Number, Code, Name, TradingHaltDate, TradingHal... |
| `/exchangeReport/BFT41U` | 集中市場盤後定價交易 | ok | N | 15575 | Code, Name, TradeVolume, Transaction, TradeValue |
| `/exchangeReport/BFI84U` | 集中市場停資停券預告表 | ok | N | 371 | Code, Name, StartDate, EndDate, Reason |
| `/exchangeReport/MI_MARGN` | 集中市場融資融券餘額 | ok | N | 1259 | 股票代號, 股票名稱, 融資買進, 融資賣出, 融資現金償還 |
| `/block/BFIAUU_d` | 集中市場鉅額交易日成交量值統計 | ok | N | 20 | Date, Class, Type, TradeVolume, MarketSharePer |
| `/block/BFIAUU_m` | 集中市場鉅額交易月成交量值統計 | ok | N | 8 | Month, Class, TradeVolume, MarketSharePer, Trad... |
| `/block/BFIAUU_y` | 集中市場鉅額交易年成交量值統計 | ok | N | 22 | Month, TradeVolume, MarketSharePer, TradeValue |
| `/exchangeReport/STOCK_FIRST` | 每日第一上市外國股票成交量值 | ok | N | 90 | Code, Name, TradeVolume, Transaction, TradeValue |
| `/exchangeReport/TWT85U` | 集中市場證券變更交易 | ok | N | 40 | Code, Name, PeriodicCallAuctionTrading |
| `/holidaySchedule/holidaySchedule` | 有價證券集中交易市場開（休）市日期 | ok | N | 27 | Name, Date, Weekday, Description |
| `/exchangeReport/BWIBBU_d` | 上市個股日本益比、殖利率及股價淨值比（依日期查詢） | ok | N | 1070 | Date, Code, Name, ClosePrice, DividendYield |
| `/SBL/TWT96U` | 上市上櫃股票當日可借券賣出股數 | ok | N | 1203 | TWSECode, TWSEAvailableVolume, GRETAICode, GRET... |
| `/exchangeReport/TWT84U` | 上市個股股價升降幅度 | ok | N | 33420 | Code, Name, TodayLimitUp, TodayOpeningRefPrice,... |
| `/opendata/twtazu_od` | 集中市場漲跌證券數統計表 | ok | N | 2 | 出表日期, 類型, 上漲, 漲停, 下跌 |
| `/opendata/t187ap19` | 電子式交易統計資訊 | ok | N | 1 | 出表日期, 成交月份, 本月新增戶數, 本月註銷戶數, 累計開戶數 |
| `/opendata/t187ap37_L` | 上市權證基本資料彙總表 | ok | N | 43204 | 出表日期, 權證代號, 權證簡稱, 權證類型, 類別 |
| `/announcement/notetrans` | 集中市場公布注意累計次數異常資訊 | ok | N | 6 | Code, Name, RecentlyMetAttentionSecuritiesCriteria |
| `/announcement/notice` | 集中市場當日公布注意股票 | ok | N | 1 | Number, Code, Name, NumberOfAnnouncement, Tradi... |
| `/exchangeReport/TWT48U_ALL` | 上市股票除權除息預告表 | ok | N | 73 | Date, Code, Name, Exdividend, StockDividendRatio |

#### 財務報表

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/opendata/t187ap07_X_ci` | 公發公司資產負債表-一般業 | ok | N | 87 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap07_X_mim` | 公發公司資產負債表-異業 | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap06_X_basi` | 公發公司綜合損益表-金融業 | ok | N | 34 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap06_X_bd` | 公發公司綜合損益表-證券期貨業 | ok | N | 27 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap06_X_ci` | 公發公司綜合損益表-一般業 | ok | N | 87 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap06_X_fh` | 公發公司綜合損益表-金控業 | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap06_X_ins` | 公發公司綜合損益表-保險業 | ok | N | 16 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap06_X_mim` | 公發公司綜合損益表-異業 | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap05_L` | 上市公司每月營業收入彙總表 | ok | N | 1070 | 出表日期, 資料年月, 公司代號, 公司名稱, 產業別 |
| `/opendata/t187ap15_L` | 上市公司截至各季綜合損益財測達成情形(簡式) | ok | N | 4 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap16_L` | 上市公司當季綜合損益經會計師查核(核閱)數與當季預測數差異達百分之十以上者，或截至當季累計差異達百分之二十以上者(簡式) | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap17_L` | 上市公司營益分析查詢彙總表(全體公司彙總報表) | ok | N | 1040 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap31_L` | 上市公司財務報告經監察人承認情形 | ok | N | 1068 | 出表日期, 公司代號, 公司名稱, 是否設置審計委員會, 出具本次財務報告審查報告書之監察人姓名 |
| `/opendata/t187ap06_L_bd` | 上市公司綜合損益表(證券期貨業) | ok | N | 3 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap06_L_ci` | 上市公司綜合損益表(一般業) | ok | N | 1034 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap06_L_fh` | 上市公司綜合損益表(金控業) | ok | N | 13 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap06_L_ins` | 上市公司綜合損益表(保險業) | ok | N | 6 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap06_L_mim` | 上市公司綜合損益表(異業) | ok | N | 4 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap07_L_bd` | 上市公司資產負債表(證券期貨業) | ok | N | 3 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap07_L_ci` | 上市公司資產負債表(一般業) | ok | N | 1034 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap07_L_fh` | 上市公司資產負債表(金控業) | ok | N | 13 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap07_L_ins` | 上市公司資產負債表(保險業) | ok | N | 6 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap07_L_mim` | 上市公司資產負債表(異業) | ok | N | 4 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap07_X_basi` | 公發公司資產負債表-金融業 | ok | N | 34 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap07_X_bd` | 公發公司資產負債表-證券期貨業 | ok | N | 27 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap07_X_fh` | 公發公司資產負債表-金控業 | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap07_X_ins` | 公發公司資產負債表-保險業 | ok | N | 16 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap11_P` | 公發公司董監事持股餘額明細 | ok | N | 6559 | 出表日期, 資料年月, 公司代號, 公司名稱, 職稱 |
| `/opendata/t187ap06_L_basi` | 上市公司綜合損益表(金融業) | ok | N | 10 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap07_L_basi` | 上市公司資產負債表(金融業) | ok | N | 10 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |

### Web (20 endpoints)

#### 信用交易

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/exchangeReport/MI_MARGN` | 融資融券餘額 | ok | Y | 2 |  |
| `/exchangeReport/TWTASU` | 信用交易統計 | ok | Y | 1234 | 證券名稱, 數量, 金額, 數量, 金額 |
| `/exchangeReport/BFI84U` | 停資停券預告表 | ok | Y | 371 | 股票代號, 股票名稱, 停券起日(最後回補日), 停券迄日, 原因 |

#### 借券

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/exchangeReport/TWT93U` | 借券成交明細 | ok | Y | 1199 | 代號, 名稱, 前日餘額, 賣出, 買進 |

#### 基本面

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/exchangeReport/BWIBBU` | 個股本益比、殖利率及股價淨值比 | ok | Y | 20 | 日期, 殖利率(%), 股利年度, 本益比, 股價淨值比 |
| `/exchangeReport/TWT48U` | 除權除息預告表 | ok | Y | 73 | 除權除息日期, 股票代號, 名稱, 除權息, 無償配股率 |

#### 指數

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/indicesReport/MI_5MINS_HIST` | 發行量加權股價指數歷史資料 | ok | Y | 20 | 日期, 開盤指數, 最高指數, 最低指數, 收盤指數 |

#### 法人

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/fund/T86` | 三大法人買賣超日報 | ok | Y | 4095 | 證券代號, 證券名稱, 外陸資買進股數(不含外資自營商), 外陸資賣出股數(不含外資自營商),... |
| `/fund/MI_QFIIS` | 外資及陸資投資持股統計 | ok | Y | 1261 | 證券代號, 證券名稱, 國際證券編碼, 發行股數, 外資及陸資尚可投資股數 |
| `/fund/TWT38U` | 三大法人買賣金額統計表 | ok | Y | 1096 | , 證券代號, 證券名稱, 買進股數, 賣出股數 |

#### 行情

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/exchangeReport/STOCK_DAY` | 個股日成交資訊 | ok | Y | 20 | 日期, 成交股數, 成交金額, 開盤價, 最高價 |
| `/exchangeReport/MI_INDEX` | 每日收盤行情（大盤統計） | ok | Y | 10 |  |
| `/exchangeReport/FMTQIK` | 每日成交量值 | ok | Y | 20 | 日期, 成交股數, 成交金額, 成交筆數, 發行量加權股價指數 |
| `/exchangeReport/MI_INDEX20` | 每日成交量前二十名證券 | ok | Y | 20 | 排名, 證券代號, 證券名稱, 成交股數, 成交筆數 |
| `/exchangeReport/STOCK_DAY_AVG` | 個股月均價 | ok | Y | 21 | 日期, 收盤價 |
| `/exchangeReport/FMSRFK` | 個股月成交資訊 | ok | Y | 12 | 年度, 月份, 最高價, 最低價, 加權(A/B)平均價 |
| `/exchangeReport/TWT84U` | 個股股價升降幅度 | ok | Y | 1285 | 證券代號, 證券名稱, 漲停價, 開盤競價基準, 跌停價 |
| `/exchangeReport/TWT53U` | 零股交易行情 | ok | Y | 1267 | 證券代號, 證券名稱, 成交股數, 成交筆數, 成交金額 |
| `/exchangeReport/BFT41U` | 盤後定價交易 | ok | Y | 9 | 證券代號, 證券名稱, 成交數量, 成交筆數, 成交金額 |
| `/exchangeReport/TWTB4U` | 當日沖銷交易標的及統計 | ok | Y | 2 |  |

## TPEx (Taipei Exchange)

### OpenAPI (225 endpoints)

#### 上櫃

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/tpex_mainborad_highlight` | 上櫃股票市場現況 | ok | N | 1 | Date, ListedCompanyNumbers, AuthorizedCapital, ... |
| `/tpex_securities` | 上櫃股票現股當沖交易標的資訊 | ok | N | 816 | 資料日期, 證券代號, 證券名稱, 暫停現股賣出後現款買進當沖註記 |
| `/tpex_spendi_today` | 上櫃當日公布暫停/恢復交易股票 | ok | N | 1 | Date, SecuritiesCompanyCode, CompanyName, 暫停交易,... |
| `/tpex_spendi_history` | 上櫃歷史公布暫停/恢復交易股票 | ok | N | 26 | Date, Serial, SecuritiesCompanyCode, CompanyNam... |
| `/tpex_mainboard_daily_close_quotes` | 上櫃股票行情 | ok | N | 10711 | Date, SecuritiesCompanyCode, CompanyName, Close... |
| `/tpex_mainboard_quotes` | 上櫃股票收盤行情 | ok | N | 998 | Date, SecuritiesCompanyCode, CompanyName, Close... |
| `/tpex_mainboard_peratio_analysis` | 上櫃股票個股本益比、殖利率、股價淨值比 | ok | N | 878 | Date, SecuritiesCompanyCode, CompanyName, Price... |
| `/tpex_mainboard_margin_balance` | 上櫃股票融資融券餘額 | ok | N | 892 | Date, SecuritiesCompanyCode, CompanyName, Margi... |
| `/tpex_intraday_trading_statistics` | 上櫃股票現股當沖交易統計資訊 | ok | N | 5 | Date, DayTradingVolume, DayTradingVolumeOfTheMa... |
| `/tpex_active_broker_volume` | 上櫃股票熱門股證券商進出排行 | ok | N | 300 | Date, StockRanking, SecuritiesCompanyCodeAndCom... |
| `/tpex_margin_sbl` | 上櫃股票融券借券賣出餘額 | ok | N | 909 | Date, SecuritiesCompanyCode, CompanyName, SaleB... |
| `/tpex_exright_daily` | 上櫃股票除權除息計算結果表 | ok | N | 4 | Date, SecuritiesCompanyCode, CompanyName, Close... |
| `/tpex_exright_prepost` | 上櫃股票除權除息預告表 | ok | N | 100 | ExRrightsExDividendDate, SecuritiesCompanyCode,... |
| `/tpex_cmode` | 上櫃股票變更交易、分盤交易、管理股票與停止交易資訊 | ok | N | 20 | Date, SecuritiesCompanyCode, CompanyName, Alter... |
| `/tpex_odd_stock` | 上櫃股票零股交易資訊 | ok | N | 991 | Date, SecuritiesCompanyCode, CompanyName, Trade... |
| `/tpex_off_market` | 上櫃股票盤後定價行情 | ok | N | 10711 | Date, SecuritiesCompanyCode, CompanyName, BidTr... |
| `/tpex_esb_applicant_companies` | 申請上櫃公司 | ok | N | 788 | Date, SecuritiesCompanyCode, CompanyName, Chair... |
| `/tpex_trading_warning_information` | 上櫃公布注意股票資訊 | ok | N | 31 | Date, SecuritiesCompanyCode, CompanyName, Tradi... |
| `/tpex_disposal_information` | 上櫃處置有價證券資訊 | ok | N | 41 | Date, SecuritiesCompanyCode, CompanyName, Dispo... |
| `/tpex_trading_warning_note` | 上櫃公布注意累計次數異常資訊 | ok | N | 1 | Date, SecuritiesCompanyCode, CompanyName, Accum... |
| `/tpex_margin_trading_term` | 上櫃融資融券暫停融券賣出預告表 | ok | N | 317 | Date, SecuritiesCompanyCode, CompanyName, Short... |
| `/tpex_margin_trading_adjust` | 上櫃融資融券調整成數 | ok | N | 242 | Date, SecuritiesCompanyCode, CompanyName, Reduc... |
| `/tpex_margin_trading_lend` | 上櫃融資融券標借 | ok | N | 2 | Date, DateOfTheCompetitiveDids, SecuritiesCompa... |
| `/tpex_margin_trading_marginspot` | 上櫃信用交易餘額概況表 | ok | N | 35 | Month, Ranking, SecuritiesCompanyCode, CompanyN... |
| `/tpex_margin_trading_margin_mark` | 上櫃平盤下得融(借)券賣出之證券名單 | ok | N | 809 | Date, SecuritiesCompanyCode, CompanyName, Banne... |
| `/tpex_margin_trading_margin_used` | 上櫃融資融券使用率報表 | ok | N | 20 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |
| `/tpex_margin_trading_short_sell` | 上櫃融資融券增減排行表 | ok | N | 20 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |
| `/tpex_3insti_qfii` | 上櫃僑外資及陸資持股比例排行表 | ok | N | 882 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |
| `/tpex_3insti_qfii_industry` | 上櫃各類股僑外資及陸資持股比例表 | ok | N | 28 | Date, Industry, NumberOfCompanies, NumberOfShar... |
| `/tpex_3insti_daily_trading` | 上櫃股票三大法人買賣明細資訊 | ok | N | 915 | Date, SecuritiesCompanyCode, CompanyName, Forei... |
| `/tpex_3insti_dealer_trading` | 上櫃股票自營商買賣超彙總表 | ok | N | 2528 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |
| `/tpex_ceil_non_trading` | 上櫃漲跌停未成交資訊 | ok | N | 39 | Date, SecuritiesCompanyCode, CompanyName, Closi... |
| `/tpex_daily_trading_index` | 上櫃日成交量值指數 | ok | N | 6 | Date, TradeVolume, TradeAmount, NumberOfTransac... |
| `/tpex_short_sell` | 上櫃當日融券賣出與借券賣出成交量值 | ok | N | 990 | Date, SecuritiesCompanyCode, CompanyName, Short... |
| `/tpex_daily_broker1` | 上櫃各券商當日營業金額統計表 | ok | N | 895 | Date, Ranking, PreviousDayRanking, Code, Name |
| `/tpex_active_dollar_volume` | 上櫃盤中個股成交金額排行 | ok | N | 30 | Date, SecuritiesCompanyCode, CompanyName, Numbe... |
| `/tpex_active_advanced` | 上櫃盤中個股漲幅排行 | ok | N | 30 | Date, SecuritiesCompanyCode, CompanyName, Closi... |
| `/tpex_active_declined` | 上櫃盤中個股跌幅排行 | ok | N | 30 | Date, SecuritiesCompanyCode, CompanyName, Closi... |
| `/tpex_intraday_fee` | 上櫃應付現股當日沖銷券差借券費率 | ok | N | 157 | Date, SecuritiesCompanyCode, CompanyName,  Lend... |
| `/tpex_intraday_trading_pre` | 上櫃暫停先賣後買當日沖銷交易標的預告表 | ok | N | 255 | Date, SecuritiesCompanyCode, CompanyName, First... |
| `/tpex_intraday_trading_his` | 上櫃暫停先賣後買當日沖銷交易歷史查詢 | ok | N | 137 | Date, SecuritiesCompanyCode, CompanyName, First... |
| `/tpex_daily_market_value` | 上櫃歷史個股市值排行 | ok | N | 879 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |
| `/tpex_daily_turnover` | 上櫃歷史個股週轉率排行 | ok | N | 879 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |
| `/tpex_trading_volumes_avg` | 上櫃歷史個股日均量排行 | ok | N | 866 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |
| `/tpex_trading_amount_avg` | 上櫃歷史個股日均值排行 | ok | N | 866 | Date, Rank, StockCode, StockName, AverageDailyT... |
| `/tpex_trading_volume_ratio` | 上櫃歷史類股成交價量比重 | ok | N | 28 | Date, Sector, TradeAmount, TradeWeight,  Number... |
| `/tpex_pe_ratio_top10` | 上櫃歷史個股本益比排行 | ok | N | 878 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |
| `/tpex_daily_qutoes_block` | 上櫃鉅額交易日成交資訊 | ok | N | 1 | Date, TransactionType, SettlementPeriod, Code, ... |
| `/tpex_daily_trading_block` | 上櫃個股單一證券鉅額交易日成交資訊 | ok | N | 250 | TradingDate, Name, NumberOfSharesTraded, Tradin... |
| `/tpex_daily_trading_summary_odd` | 上櫃鉅額交易日成交量值統計 | ok | N | 20 | TradingDate, Type, NumberOfTransactions, Number... |
| `/tpex_monthly_trading_summary_block` | 上櫃鉅額交易月成交量值統計 | ok | N | 16 | Month, Type, NumberOfTransactions, NumberOfShar... |
| `/tpex_yearly_trading_summary_block` | 上櫃鉅額交易年成交量值統計 | ok | N | 4 | Year, Type, NumberOfTransactions, NumberOfShare... |
| `/tpex_volume_rank` | 上櫃歷史個股成交量排行 | ok | N | 879 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |
| `/tpex_amount_rank` | 上櫃歷史個股成交值排行 | ok | N | 879 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |
| `/tpex_prvol` | 上櫃股票等價系統成交分價表 | ok | N | 63 | Date, SecuritiesCompanyCode, CompanyNam, Tradin... |
| `/tpex_3insti_summary` | 上櫃股票三大法人買賣金額彙總表 | ok | N | 8 | Date, Investor, PurchaseAmount, SaleAmount, Net |
| `/tpex_3insti_trading` | 上櫃股票投信買賣超彙總表 | ok | N | 16 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |
| `/tpex_daily_trade_block_day` | 鉅額交易歷史成交資訊 | ok | N | 250 | TradingDate, Name, NumberOfSharesTraded, Tradin... |
| `/tpex_delayed_stock_open` | 上櫃每日暫緩開盤股票 | ok | N | 100 | Date, SecuritiesCompanyCode, CompanyName |
| `/tpex_delayed_stock_close` | 上櫃每日暫緩收盤股票 | ok | N | 6 | Date, SecuritiesCompanyCode, CompanyName |
| `/tpex_ipo_no_limit` | 上櫃首五日無漲跌幅資訊 | ok | N | 1 | Date, SecuritiesCompanyCode, CompanyName, Start... |
| `/tpex_3insti_qfii_trading` | 上櫃股票外資及陸資買賣超彙總表 | ok | N | 428 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |
| `/mopsfin_t187ap19_O` | 電子式交易統計資訊(上櫃) | ok | N | 1 | 出表日期, 成交月份, 本月新增戶數, 本月註銷戶數, 累計開戶數 |

#### 債券

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/tpex_dpsp_monthly_CBmcs007` | 可轉債資產交換ASO及ASW銀行承作餘額 | ok | N | 17 | Date, FinancialInstitutionsCode, FinancialInsti... |
| `/tpex_international_bond_quotes` | 國際債券當日盤中報價行情表(含寶島債) | ok | N | 32 | Date, Time, BondCode, BondName, BidYieldPrice |
| `/tpex_international_bond_trade` | 國際債券當日盤中成交行情表(含寶島債) | ok | N | 1 | Date, Time, BondCode, BondName, LastField |
| `/tpex_international_bond_issue_investor` | 國際債券(一般投資人) | ok | N | 7 | Date, BondCode, ShortName, Issuer, IssuingDate |
| `/tpex_international_bond_issue_org` | 國際債券(僅售予專業投資人者) | ok | N | 940 | Date, BondCode, ShortName, Issuer, IssuingDate |
| `/BDdos216UTF` | 美元固定利率不可贖回國際債券理論價格 | ok | N | 27 | 資料日期, 債券代碼, 債券簡稱, 發行人, 發行日 |
| `/BDdos215UTF` | 美元附息固定利率可贖回國際債券理論價格 | ok | N | 128 | 資料日期, 債券代碼, 債券簡稱, 發行人, 發行日 |
| `/BDdos209UTF` | 美元零息可贖回國際債券理論價格 | ok | N | 277 | 資料日期, 債券代碼, 債券簡稱, 發行人, 發行日 |
| `/bond_cb_daily` | 轉(交)換公司債買賣斷券商買賣日報表 | ok | N | 1 | Date, FinancialInstitutionsCode, FinancialInsti... |
| `/bond_ISSBD1_data` | 公債發行資料下載 | ok | N | 191 | Date, IssuerCode, IssuerName, BondCode, BondType |
| `/bond_ISSBD2_data` | 外國金融債發行資料下載 | ok | N | 1 | Date, IssuerCode, IssuerName, BondCode, BondType |
| `/bond_ISSBD3_data` | 金融債發行資料下載 | ok | N | 431 | Date, IssuerCode, IssuerName, BondCode, BondType |
| `/bond_ISSBD4_data` | 普通債發行資料下載 | ok | N | 1867 | Date, IssuerCode, IssuerName, BondCode, BondType |
| `/bond_ISSBD5_data` | 轉(交)換債發行資料下載 | ok | N | 397 | Date, IssuerCode, IssuerName, BondCode, BondType |
| `/bond_ISSBD6_data` | 海外轉換債發行資料下載 | ok | N | 19 | Date, IssuerCode, IssuerName, BondCode, BondType |
| `/bond_ISSBD7_data` | 附認股權公司債發行資料下載 | ok | N | 1 | Date, IssuerCode, IssuerName, BondCode, BondType |
| `/bond_ISSBD8_data` | 海外附認股權公司債發行資料下載 | ok | N | 1 | Date, IssuerCode, IssuerName, BondCode, BondType |
| `/bond_ISSBD9_data` | 海外普通債發行資料下載 | ok | N | 1 | Date, IssuerCode, IssuerName, BondCode, BondType |
| `/bond_ISSBD10_data` | 國際債券(寶島債券)-本國發行人及第一、二上市(櫃)公司之外國發行人發行資料下載 | ok | N | 181 | Date, IssuerCode, IssuerName, BondCode, BondType |
| `/bond_ISSBD11_data` | 國際債券(寶島債券)-外國發行人(在我國未公開發行股權商品者)發行資料下載 | ok | N | 1 | Date, IssuerCode, IssuerName, BondCode, BondName |

#### 公司治理

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/tpex_esb_eps_rank` | 本國興櫃公司EPS排名 | ok | N | 345 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |
| `/tpex_esb_capitals_rank` | 興櫃公司資本額排名 | ok | N | 345 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |
| `/t187ap46_O_21` | 上櫃公司企業ESG資訊揭露彙總資料-職業安全衛生 | empty | N | 0 |  |
| `/t187ap46_O_9` | 上櫃公司企業ESG資訊揭露彙總資料-功能性委員會 | empty | N | 0 |  |
| `/t187ap46_O_8` | 上櫃公司企業ESG資訊揭露彙總資料-氣候相關議題管理 | empty | N | 0 |  |
| `/t187ap46_O_20` | 上櫃公司企業ESG資訊揭露彙總資料-反競爭行為法律訴訟  | empty | N | 0 |  |
| `/t187ap46_O_19` | 上櫃公司企業ESG資訊揭露彙總資料-風險管理政策  | empty | N | 0 |  |
| `/t187ap46_O_15` | 上櫃公司企業ESG資訊揭露彙總資料-社區關係  | empty | N | 0 |  |
| `/t187ap46_O_13` | 上櫃公司企業ESG資訊揭露彙總資料-供應鏈管理  | empty | N | 0 |  |
| `/t187ap46_O_12` | 上櫃公司企業ESG資訊揭露彙總資料-食品安全 | empty | N | 0 |  |
| `/t187ap46_O_14` | 上櫃公司企業ESG資訊揭露彙總資料-產品品質與安全 | empty | N | 0 |  |
| `/t187ap41_O` | 上櫃公司召開股東常 (臨時) 會日期、地點及採用電子投票情形等資料彙總表 | ok | N | 887 | 出表日期, 公司代號, 公司名稱, 公司地址, 股東常(臨時)會 |
| `/t187ap05_R` | 興櫃公司每月營業收入彙總表 | ok | N | 360 | 出表日期, 資料年月, 公司代號, 公司名稱, 產業別 |
| `/t187ap46_O_4` | 上櫃公司企業ESG資訊揭露彙總資料-廢棄物管理 | empty | N | 0 |  |
| `/t187ap46_O_2` | 上櫃公司企業ESG資訊揭露彙總資料-能源管理 | empty | N | 0 |  |
| `/t187ap46_O_7` | 上櫃公司企業ESG資訊揭露彙總資料-投資人溝通 | empty | N | 0 |  |
| `/t187ap46_O_1` | 上櫃公司企業ESG資訊揭露彙總資料-溫室氣體排放 | empty | N | 0 |  |
| `/t187ap46_O_6` | 上櫃公司企業ESG資訊揭露彙總資料-董事會 | empty | N | 0 |  |
| `/t187ap46_O_5` | 上櫃公司企業ESG資訊揭露彙總資料-人力發展 | empty | N | 0 |  |
| `/t187ap46_O_3` | 上櫃公司企業ESG資訊揭露彙總資料-水資源管理 | empty | N | 0 |  |
| `/mopsfin_t187ap05_OA` | 二十九大類股營收變化統計表 | ok | N | 879 | 出表日期, 資料年月, 公司代號, 公司名稱, 產業別 |
| `/mopsfin_t187ap05_OB` | 發行公司營收創新高一覽表(上櫃) | ok | N | 879 | 出表日期, 資料年月, 公司代號, 公司名稱, 產業別 |
| `/mopsfin_t187ap35_O` | 上櫃公司股東行使提案權情形彙總表 | ok | N | 870 | Date, SecuritiesCompanyCode, CompanyName, 召開股東會... |
| `/mopsfin_t187ap32_O` | 上櫃公司公司治理之相關規程規則 | ok | N | 8787 | Date, SecuritiesCompanyCode, CompanyName, 公司治理之... |
| `/mopsfin_t187ap34_O` | 上櫃公司採累積投票制、全額連記法、候選人提名制選任董監事及當選資料彙總表 | ok | N | 1907 | Date, SecuritiesCompanyCode, CompanyName, 股東常(臨... |
| `/mopsfin_t187ap33_O` | 上櫃公司董事長是否兼任總經理 | ok | N | 881 | Date, SecuritiesCompanyCode, CompanyName, Chair... |
| `/mopsfin_t187ap31_O` | 上櫃公司財務報告經監察人承認情形 | ok | N | 881 | Date, SecuritiesCompanyCode, CompanyName, 是否設置審... |
| `/mopsfin_t187ap09_O` | 上櫃公司董事、監察人質權設定占董事及監察人實際持有股數彙總表 | ok | N | 9 | Date, Percent, CompanyName |
| `/mopsfin_t187ap10_O` | 上櫃公司董事、監察人持股不足法定成數連續達3個月以上彙總表 | ok | N | 19 | 出表日期, 連續不足達3個月, 107/10-12連續不足達4個月, 107/09-12連續不... |
| `/mopsfin_t187ap24_O` | 上櫃公司經營權及營業範圍異(變)動專區-經營權異動公司 | ok | N | 27 | Date, SecuritiesCompanyCode, CompanyName, 經營權異動... |
| `/mopsfin_t187ap25_O` | 上櫃公司經營權及營業範圍異(變)動專區-營業範圍重大變更公司 | ok | N | 1 | Date, 序號, 年度, 季別, SecuritiesCompanyCode |
| `/mopsfin_t187ap03_O` | 上櫃股票基本資料 | ok | N | 881 | Date, SecuritiesCompanyCode, CompanyName, Compa... |
| `/mopsfin_t187ap03_R` | 興櫃公司基本資料 | ok | N | 354 | Date, SecuritiesCompanyCode, CompanyName, Compa... |
| `/mopsfin_t187ap04_O` | 上櫃公司每日重大訊息 | ok | N | 82 | Date, 發言日期, 發言時間, SecuritiesCompanyCode, Compan... |
| `/mopsfin_t187ap02_O` | 上櫃公司持股逾 10% 大股東名單 | ok | N | 976 | Date, SecuritiesCompanyCode, CompanyName, 大股東名稱 |
| `/mopsfin_t187ap26_O` | 上櫃公司經營權及營業範圍異(變)動專區-經營權異動且營業範圍重大變更停止買賣公司 | empty | N | 0 |  |
| `/mopsfin_t187ap27_O` | 上櫃公司經營權及營業範圍異(變)動專區-經營權異動且營業範圍重大變更列為變更交易公司 | empty | N | 0 |  |
| `/mopsfin_t187ap05_O` | 上櫃公司每月營業收入彙總表 | ok | N | 879 | 出表日期, 資料年月, 公司代號, 公司名稱, 產業別 |
| `/mopsfin_t187ap39_O` | 上櫃股利分派情形-董事會通過 | ok | N | 2483 | 出表日期, 公司代號, 公司名稱, 股利年度, 期別 |
| `/mopsfin_t187ap11_R` | 興櫃公司董監事持股餘額明細資料 | ok | N | 6829 | Date, 資料年月, SecuritiesCompanyCode, CompanyName, 職稱 |
| `/mopsfin_t187ap14_O` | 上櫃公司各產業EPS統計資訊 | ok | N | 881 | Date, Year, 季別, SecuritiesCompanyCode, CompanyName |
| `/mopsfin_t187ap08_O` | 上櫃公司董事、監察人持股不足法定成數彙總表 | ok | N | 32 | 出表日期, 公司代號, 公司名稱, 已發行股份總額, 全體董事不包含獨立董事應持有股數 |
| `/mopsfin_t187ap11_O` | 上櫃公司董監事持股餘額明細資料 | ok | N | 17216 | 出表日期, 資料年月, 公司代號, 公司名稱, 職稱 |
| `/mopsfin_t187ap12_O` | 上櫃公司每日內部人持股轉讓事前申報表-持股轉讓日報表 | ok | N | 1 | Date, SecuritiesCompanyCode, CompanyName, 申請人身分... |
| `/mopsfin_t187ap13_O` | 上櫃公司每日內部人持股轉讓事前申報表-持股未轉讓日報表 | ok | N | 1 | Date, SecuritiesCompanyCode, CompanyName, 申請人身分... |
| `/mopsfin_t187ap22_O` | 上櫃公司金管會證券期貨局裁罰案件專區 | ok | N | 7 | Date, 發函日期, SecuritiesCompanyCode, CompanyName,... |
| `/mopsfin_t187ap30_O` | 上櫃公司獨立董監事兼任情形彙總表 | ok | N | 10350 | Date, 序號, SecuritiesCompanyCode, CompanyName, 職稱 |
| `/mopsfin_t187ap29_A_O` | 上櫃公司董事酬金相關資訊 | ok | N | 846 | Date, 產業類別, SecuritiesCompanyCode, CompanyName,... |
| `/mopsfin_t187ap29_B_O` | 上櫃公司監察人酬金相關資訊 | ok | N | 10 | Date, 產業類別, SecuritiesCompanyCode, CompanyName,... |
| `/mopsfin_t187ap29_C_O` | 上櫃公司合併報表董事酬金相關資訊 | ok | N | 768 | Date, 產業類別, SecuritiesCompanyCode, CompanyName,... |
| `/mopsfin_t187ap29_D_O` | 上櫃公司合併報表監察人酬金相關資訊 | ok | N | 7 | Date, 產業類別, SecuritiesCompanyCode, CompanyName,... |
| `/mopsfin_t187ap23_O` | 上櫃公司違反資訊申報、重大訊息及說明記者會規定專區 | ok | N | 6 | Date, 發函日期, SecuritiesCompanyCode, CompanyName,... |

#### 券商資料

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mopsfin_t187ap01` | 券商業務別人員數 | ok | N | 4 | 出表日期, 職位, 受託買賣, 受託買賣（衍生性商品銷售）, 內部稽核 |
| `/tpex_daily_broker2` | 上櫃股票各券商總公司當日營業金額統計表 | ok | N | 63 | Date, Ranking, PreviousDayRanking, FinancialIns... |

#### 創櫃

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/tpex_gisa_highlight` | 創櫃板公司市場現況 | ok | N | 1 | Date, CumulativeNumberOfCompaniesApplyingForGIS... |
| `/tpex_gisa_company` | 創櫃板公司資訊 | ok | N | 135 | Date, SecuritiesCompanyCode, CompanyName, Industry |
| `/tpex_gisa_financing_before` | 於登錄創櫃板前辦理籌資資訊 | ok | N | 260 | Date, SecuritiesCompanyCode, CompanyName, 現金增資期... |
| `/tpex_gisa_financing_history` | 創櫃板公司透過籌資系統辦理籌資資訊 | ok | N | 3 | Date, SecuritiesCompanyCode, CompanyName, 現金增資期... |
| `/tpex_gisa_financing_in_process` | 創櫃板辦理中籌資資訊 | ok | N | 1 | Date, SecuritiesCompanyCode, CompanyName, 現金增資期... |

#### 指數系列

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/tpex_index` | 櫃買指數歷史資料 | ok | N | 6 | Date, Open, High, Low, Close |
| `/tpex50_index` | 富櫃50指數歷史收盤指數 | ok | N | 6 | Date, TPEx50Index, TPEx50TotalReturnIndex |
| `/tpex200_change` | 櫃買「富櫃200指數」當日收盤指數 | ok | N | 2 | 資料日期, 指數, 收盤指數, 漲跌, 漲跌點數 |
| `/tpcgi_constituents` | 上櫃公司治理指數當日成分股資訊 | ok | N | 60 | Date, SecuritiesCompanyCode, CompanyName |
| `/tpcgi_reward_index` | 上櫃公司治理指數歷史收盤指數 | ok | N | 6 | Date, TPExCorporateGovernanceIndex, TPExCorpora... |
| `/tpcgi_change` | 上櫃公司治理指數當日收盤指數 | ok | N | 2 | Date, Name, Index, Change |
| `/tpex_index_consti` | 櫃買指數成分股 | ok | N | 881 | Date, SecuritiesCompanyCode, CompanyName, Capit... |
| `/tpex_reward_index` | 櫃買指數與報酬指數之收市指數 | ok | N | 6 | Date, TPExIndex, TPExTotalReturnIndex |
| `/tpex50_constituents` | 櫃買「富櫃50指數」當日成分股 | ok | N | 50 | Date, SecuritiesCompanyCode, CompanyName |
| `/tpex50_change` | 櫃買「富櫃50指數」當日收盤指數 | ok | N | 2 | Date, Name, Index, Change |
| `/tphd_constituents` | 櫃買「高殖利率指數」當日成分股 | ok | N | 60 | Date, SecuritiesCompanyCode, CompanyName |
| `/tphd_change` | 櫃買「高殖利率指數」當日收盤指數 | ok | N | 2 | Date, Name, Index, Change |
| `/tpci_constituents` | 櫃買「薪酬指數」當日成分股 | ok | N | 88 | Date, SecuritiesCompanyCode, CompanyName |
| `/tpci_change` | 櫃買「薪酬指數」當日收盤指數 | ok | N | 2 | Date, Name, Index, Change |
| `/tpci_reward_index` | 櫃買「薪酬指數」歷史收盤指數 | ok | N | 6 | Date, GTSMCompensationIndex, GTSMCompensationTo... |
| `/tpex_emp88_constituents` | 櫃買「勞工就業88指數」當日成分股 | ok | N | 88 | Date, SecuritiesCompanyCode, CompanyName |
| `/tpex_emp88_change` | 櫃買「勞工就業88指數」當日收盤指數 | ok | N | 2 | Date, Name, Index, Change |
| `/tpex_emp88_reward_index` | 櫃買「勞工就業88指數」歷史收盤指數 | ok | N | 6 | Date, GretaiLaborEmployment88Index, GretaiLabor... |
| `/tpex200_constituents` | 櫃買「富櫃200指數」當日成分股 | ok | N | 200 | 資料日期, 股票代號, 股票名稱 |
| `/tphd_index` | 高殖利率指數歷史收盤指數 | ok | N | 6 | Date, TPExHighDividendYieldIndex, TPExHighDivid... |

#### 權證

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/tpex_warrant_gold` | 黃金現貨權證發行基本資料 | ok | N | 2 | Date, Code, Name, ListedDate, ExpiryDate |
| `/tpex_warrant_gold_quts` | 黃金現貨權證收盤行情 | ok | N | 1 | Date, Code, Name, Open, High |
| `/tpex_warrant_daily_quts` | 上櫃權證收盤行情日報表 | ok | N | 9836 | Date, Code, Name, Open, High |
| `/tpex_warrant_monthly_quts` | 上櫃權證收盤行情月報表 | ok | N | 10364 | Date, Code, Name, Open, High |
| `/tpex_warrant_issue` | 上櫃權證發行基本資料 | ok | N | 9847 | Date, Code, Name, ListedDate, ExpiryDate |
| `/tpex_warrant_wcb_daily_quts` | 上櫃牛熊證收盤行情(不含展延型牛熊證)日報表 | ok | N | 1 | Date, Code, Name, Open, High |
| `/tpex_warrant_wcb_monthly_quts` | 上櫃牛熊證收盤行情(不含展延型牛熊證)月報表 | ok | N | 1 | Date, Code, Name, Open, High |
| `/tpex_warrant_wcb_issue` | 上櫃牛熊證發行基本資料(不含展延型牛熊證) | ok | N | 1 | Date, Code, Name, ListedDate, ExpiryDate |
| `/tpex_warrant_wxy_daily_quts` | 上櫃展延型牛熊證收盤行情日報表 | ok | N | 1 | Date, Code, Name, Open, High |
| `/tpex_warrant_wxy_monthly_quts` | 上櫃展延型牛熊證收盤行情月報表 | ok | N | 1 | Date, Code, Name, Open, High |
| `/tpex_warrant_wxy_issue` | 上櫃展延型牛熊證發行基本資料 | ok | N | 1 | Date, Code, Name, ListedDate, ExpiryDate |
| `/tpex_warrant_quts` | 單筆權證成交資料 | ok | N | 9836 | Date, Code, Name, Open, High |
| `/tpex_warrant_statistics` | 每日權證交易人數(上櫃) | ok | N | 8 | Date, Category, Statistics |
| `/tpex_warrant` | 上櫃股票權證資訊 | ok | N | 9931 | Date, Item, Code, Name, UnderlyingCode |
| `/tpex_warrant_suspend_today` | 上櫃權證當日暫停/恢復交易資訊 | ok | N | 5 | Date, WarrantCode, WarrantName, SecuritiesCompa... |
| `/tpex_warrant_suspend_history` | 上櫃權證歷史暫停/恢復交易資訊 | ok | N | 12 | Year, No., Date, WarrantCode, WarrantName |
| `/mopsfin_t187ap37_O` | 上櫃權證基本資料彙總表 | ok | N | 13709 | 出表日期, 權證代號, 權證簡稱, 權證類型, 類別 |
| `/mopsfin_t187ap42_O` | 上櫃認購(售)權證每日成交資料檔 | ok | N | 9836 | Date, 交易日期, 權證代號, 權證名稱, 成交金額 |
| `/mopsfin_t187ap36_O` | 上櫃認購(售)權證年度發行量概況統計表 | ok | N | 17351 | Date, 發行人代號, 發行人名稱, 權證代號, 名稱 |

#### 興櫃

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/tpex_esb_disposal_information` | 興櫃處置有價證券資訊 | ok | N | 2 | 公布日期, 證券代號, 證券名稱, 處置起訖時間, 處置原因 |
| `/tpex_esb_warning_information` | 興櫃公布注意有價證券資訊 | ok | N | 1 | 公告日期, 證券代號, 證券名稱, 注意交易資訊, 收盤價 |
| `/tpex_esb_recommended_dealer` | 興櫃推薦證券商與推薦之股票 | ok | N | 1137 | Date, SecuritiesCompanyCode, CompanyName, Recom... |
| `/tpex_esb_latest_statistics` | 興櫃股票當日行情表 | ok | N | 352 | Date, Time, SecuritiesCompanyCode, CompanyName,... |
| `/tpex_esb_highlight` | 興櫃股票市場現況 | ok | N | 1 | Date, RegisteredStocksNumber, TotalPaidinCapita... |

#### 財務報表

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mopsfin_t187ap07_O_basi` | 上櫃公司資產負債表(金融業) | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap07_O_bd` | 上櫃公司資產負債表(證券期貨業) | ok | N | 7 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap07_O_ci` | 上櫃公司資產負債表(一般業) | ok | N | 874 | Date, 年度, 季別, SecuritiesCompanyCode, CompanyName |
| `/mopsfin_t187ap07_O_fh` | 上櫃公司資產負債表(金控業) | ok | N | 1 | Date, Year, Season, SecuritiesCompanyCode, Comp... |
| `/mopsfin_t187ap07_O_ins` | 上櫃公司資產負債表(保險業) | ok | N | 1 | Date, Year, Season, SecuritiesCompanyCode, Comp... |
| `/mopsfin_t187ap07_O_mim` | 上櫃公司資產負債表(異業) | ok | N | 1 | Date, Year, Season, SecuritiesCompanyCode, Comp... |
| `/mopsfin_t187ap06_O_basi` | 上櫃公司綜合損益表(金融業) | ok | N | 1 | Date, Year, Season, SecuritiesCompanyCode, Comp... |
| `/mopsfin_t187ap06_O_bd` | 上櫃公司綜合損益表(證券期貨業) | ok | N | 7 | Date, 年度, 季別, 公司代號, CompanyName |
| `/mopsfin_t187ap06_O_ci` | 上櫃公司綜合損益表(一般業) | ok | N | 874 | Date, Year, Season, SecuritiesCompanyCode, Comp... |
| `/mopsfin_t187ap06_O_fh` | 上櫃公司綜合損益表(金控業) | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap06_O_ins` | 上櫃公司綜合損益表(保險業) | ok | N | 1 | Date, Year, Season, SecuritiesCompanyCode, Comp... |
| `/mopsfin_t187ap06_O_mim` | 上櫃公司綜合損益表(異業) | ok | N | 1 | Date, Year, Season, SecuritiesCompanyCode, Comp... |
| `/mopsfin_t187ap06_O_basiA` | 上櫃公司財報資訊(金融業) | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap06_O_bdA` | 上櫃公司財報資訊(證券期貨業) | ok | N | 7 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap06_O_ciA` | 上櫃公司財報資訊( 一般業) | ok | N | 874 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap06_O_fhA` | 上櫃公司財報資訊(金控業) | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap06_O_insA` | 上櫃公司財報資訊(保險業) | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap06_O_mimA` | 上櫃公司財報資訊(異業) | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap07_U_bd` | 興櫃公司資產負債表-證券期貨業 | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap07_U_ci` | 興櫃公司資產負債表-一般業 | ok | N | 145 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap07_U_fh` | 興櫃公司資產負債表-金控業 | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap07_U_ins` | 興櫃公司資產負債表-保險業 | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap07_U_mim` | 興櫃公司資產負債表-異業 | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap06_U_basi` | 興櫃公司綜合損益表-金融業 | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap06_U_bd` | 興櫃公司綜合損益表-證券期貨業 | ok | N | 1 | Date, 年度, 季別, SecuritiesCompanyCode, CompanyName |
| `/mopsfin_t187ap06_U_ci` | 興櫃公司綜合損益表-一般業 | ok | N | 145 | Date, 年度, 季別, SecuritiesCompanyCode, CompanyName |
| `/mopsfin_t187ap06_U_fh` | 興櫃公司綜合損益表-金控業 | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap06_U_ins` | 興櫃公司綜合損益表-保險業 | ok | N | 1 | Date, 年度, 季別, SecuritiesCompanyCode, CompanyName |
| `/mopsfin_t187ap06_U_mim` | 興櫃公司綜合損益表-異業 | ok | N | 1 | Date, 年度, 季別, SecuritiesCompanyCode, CompanyName |
| `/mopsfin_t187ap07_U_basi` | 興櫃公司資產負債表-金融業 | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap15_O` | 上櫃公司截至各季綜合損益財測達成情形(簡式) | ok | N | 1 | Date, Year, 季別, SecuritiesCompanyCode, CompanyName |
| `/mopsfin_t187ap16_O` | 上櫃公司當季綜合損益經會計師查核(核閱)數與當季預測數差異達百分之十以上者，或截至當季累計差異達百分之二十以上者(簡式) | ok | N | 1 | Date, Year, 季別, SecuritiesCompanyCode, CompanyName |
| `/mopsfin_187ap17_O` | 上櫃公司營益分析查詢彙總表(全體公司彙總報表) | ok | N | 874 | Date, Year, 季別, SecuritiesCompanyCode, CompanyName |

#### 開放式基金

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/tpex_opfund_latest` | 開放式基金當日行情表 | ok | N | 3 | Date, Time, SecurityCode, ListedOpenEndedFund, ... |
| `/tpex_opfund_recommended_dealer` | 開放式基金受益憑證造市商與造市之基金 | ok | N | 3 | Date, SecurityCode, SecurityName, No., MarketMa... |
| `/tpex_opfund_market_highlight` | 開放式基金市場現況 | ok | N | 1 | Date, NumberOfFunds, TotalTradingAmount, TotalT... |

#### 黃金現貨

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/tpex_gold_market_highlight` | 黃金現貨市場現況 | ok | N | 1 | Date, NumberOfRegisteredGold, TotalTradingAmoun... |
| `/tpex_gold_recommended_dealer` | 造市商與造市之黃金現貨 | ok | N | 2 | Date, GoldCode, GoldName, No., MarketMakerCode |
| `/tpex_gold_latest` | 黃金現貨當日行情表 | ok | N | 2 | Date, Time, GoldCode, GoldShortName, QuotedBuyi... |

### Web (15 endpoints)

#### 信用交易

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/www/zh-tw/marginTrading/balance` | 融資融券餘額 | error | Y | 0 |  |
| `/www/zh-tw/marginTrading/marginSbl` | 融券借券賣出餘額 | error | Y | 0 |  |

#### 基本面

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/www/zh-tw/afterTrading/peRatio` | 個股本益比、殖利率、股價淨值比 | error | Y | 0 |  |
| `/www/zh-tw/exRight/dailyQuote` | 除權除息日程 | error | Y | 0 |  |

#### 指數

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/www/zh-tw/indexInfo/minuteIndex` | 上櫃指數歷史資料 | error | Y | 0 |  |

#### 法人

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/www/zh-tw/insti/dailyTrade` | 三大法人買賣明細 | ok | Y | 0 |  |
| `/www/zh-tw/insti/summary` | 三大法人買賣金額統計 | ok | Y | 8 | 單位名稱, 買進金額(元), 賣出金額(元), 買賣超(元) |
| `/www/zh-tw/insti/qfiiTrade` | 外資及陸資買賣明細 | error | Y | 0 |  |

#### 行情

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/www/zh-tw/afterTrading/dailyQuotes` | 上櫃股票每日收盤行情 | ok | Y | 10711 | 代號, 名稱, 收盤, 漲跌, 開盤 |
| `/www/zh-tw/afterTrading/dailyTradingInfo` | 每日市場成交資訊 | error | Y | 0 |  |
| `/www/zh-tw/afterTrading/monthlyTrade` | 個股月成交資訊 | error | Y | 0 |  |
| `/www/zh-tw/afterTrading/brokerTrading` | 證券商成交量值 | error | Y | 0 |  |
| `/www/zh-tw/afterTrading/oddLot` | 零股交易行情 | error | Y | 0 |  |
| `/www/zh-tw/afterTrading/blockTrading` | 鉅額交易 | error | Y | 0 |  |
| `/www/zh-tw/afterTrading/dayTrading` | 當日沖銷交易統計 | error | Y | 0 |  |

## MOPS (Market Observation Post System)

### Web (30 endpoints)

#### API Architecture

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mops/api/{endpoint_name}` | MOPS SPA backend API architecture note | ok | N | 0 |  |

#### Announcement

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mops/web/ajax_t05sr01_1` | Real-time material information | error | Y | 0 |  |

#### Dividend

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mops/web/ajax_t05st09_2` | Dividend distribution | error | Y | 0 |  |

#### Financial

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mops/web/ajax_t164sb04` | Financial statements (Income statement) | ok | Y | 48 | ('民國113年第3季', '單位：新台幣仟元', '會計項目', 'Unnamed: 0_l... |
| `/mops/web/ajax_t164sb03` | Financial statements (Balance sheet) | ok | Y | 71 | ('民國113年第3季', '單位：新台幣仟元', '會計項目', 'Unnamed: 0_l... |
| `/mops/web/ajax_t164sb05` | Financial statements (Cash flow statement) | ok | Y | 80 | ('民國113年第3季', '單位：新台幣仟元', '會計項目', 'Unnamed: 0_l... |
| `/mops/web/t05st10_ifrs` | Profitability analysis (IFRS) | ok | Y | 9 | 0 |

#### Revenue

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mops/web/ajax_t21sc04_ifrs` | Monthly revenue summary (IFRS) - Listed | ok | Y | 1137 | ('Unnamed: 0_level_0', '���q �N��'), ('Unnamed:... |
| `/mops/web/ajax_t21sc04_ifrs` | Monthly revenue summary (IFRS) - OTC | ok | Y | 939 | ('Unnamed: 0_level_0', '���q �N��'), ('Unnamed:... |

#### SPA Page

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `#/web/t05sr01_1` | Real-time material information | ok | Y | 0 |  |
| `#/web/t05st02` | Today's material information | ok | Y | 0 |  |
| `#/web/t05st01` | Historical material information | ok | Y | 0 |  |
| `#/web/t146sb10` | Announcement query | ok | Y | 0 |  |
| `#/web/t146sb05` | Company overview | ok | Y | 0 |  |
| `#/web/t05st03` | Company basic info | ok | Y | 0 |  |
| `#/web/t164sb00` | Consolidated/individual reports (XBRL) | ok | Y | 0 |  |
| `#/web/t163sb01` | Financial report announcements | ok | Y | 0 |  |
| `#/web/t57sb01_q1` | Financial reports | ok | Y | 0 |  |
| `#/web/t05st10_ifrs` | Monthly revenue | ok | Y | 0 |  |
| `#/web/t05st15` | Mainland investment info | ok | Y | 0 |  |
| `#/web/t108sb19` | Ex-dividend announcements | ok | Y | 0 |  |
| `#/web/t108sb16_q1` | Shareholder meetings | ok | Y | 0 |  |
| `#/web/t05st09_2` | Dividend distribution | ok | Y | 0 |  |
| `#/web/stapap1` | Director/supervisor holdings | ok | Y | 0 |  |
| `#/web/query6_1` | Insider holding changes | ok | Y | 0 |  |
| `#/web/t100sb03_1` | Functional committees | ok | Y | 0 |  |
| `#/web/t51sb10` | Latest announcements | ok | Y | 0 |  |

#### XBRL

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mops/web/ajax_t203sb01` | XBRL instance document query (single company) | ok | Y | 82 | 0, 1, 2, 3 |
| `/mops/web/ajax_t203sb02` | XBRL instance document batch download | ok | Y | 29 | 0, 1, 2, 3, 4 |
| `/mops/web/t203sb03` | XBRL taxonomy download | ok | N | 10 | tifrs-20200630.zip, tifrs-20190331.zip, tifrs-2... |

## Technical Notes

### TWSE
- **OpenAPI**: `https://openapi.twse.com.tw/v1` — real-time, current day only
- **Web**: `https://www.twse.com.tw` — historical, add `&response=json` for JSON
- Date format: `YYYYMMDD`
- Rate limit: OpenAPI 1s, Web 3s

### TPEx
- **OpenAPI**: `https://www.tpex.org.tw/openapi/v1` — real-time, current day only
- **Web**: `https://www.tpex.org.tw/www/zh-tw/` — new API, partial JSON
- Date format: OpenAPI `YYYYMMDD`, old web ROC year `YYY/MM/DD`

### MOPS
- **New SPA**: `https://mops.twse.com.tw/mops/` — Vue SPA, requires Selenium
- **Old**: `https://mopsov.twse.com.tw` — still works via requests + AJAX
- **API**: `https://mops.interinfo.com.tw:8443` — browser Worker only
- Monthly revenue via `/nas/t21/{type}/` static HTML
- Financial statements return HTML tables directly
- Date format: ROC calendar year

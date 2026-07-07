# Official Financial Data Source Catalog (TW/JP)

**Total: 1154 endpoints**

## Summary Statistics

| Market | Source | Type | Total | OK | Empty | Error | History |
|--------|--------|------|-------|----|-------|-------|---------|
| tw | TWSE | openapi | 133 | 110 | 23 | 0 | 0 |
| tw | TWSE | web | 137 | 121 | 2 | 14 | 103 |
| tw | TPEx | openapi | 225 | 207 | 18 | 0 | 0 |
| tw | TPEx | web | 194 | 94 | 20 | 80 | 126 |
| tw | MOPS | web | 101 | 75 | 0 | 26 | 9 |
| tw | TDCC | openapi | 134 | 97 | 37 | 0 | 0 |
| jp | J-Quants | openapi | 28 | 16 | 0 | 0 | 23 |
| jp | EDINET | openapi | 28 | 25 | 3 | 0 | 28 |
| jp | TDnet | web | 8 | 8 | 0 | 0 | 7 |
| jp | JPX | web | 166 | 166 | 0 | 0 | 106 |

## Taiwan Stock Exchange (TWSE)

### OpenAPI (133 endpoints)

#### 公司治理

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/announcement/punish` | 集中市場公布處置股票 | ok | N | 7 | Number, Date, Code, Name, NumberOfAnnouncement |
| `/company/applylistingForeign` | 外國公司向證交所申請第一上市之公司 | ok | N | 123 | No, Code, Company, ApplicationDate, Chairman |
| `/company/applylistingLocal` | 申請上市之本國公司 | ok | N | 685 | Code, Company, ApplicationDate, Chairman, Amoun... |
| `/company/newlisting` | 最近上市公司 | ok | N | 777 | Code, Company, ApplicationDate, Chairman, Amoun... |
| `/company/suspendListingCsvAndHtml` | 終止上市公司 | ok | N | 263 | DelistingDate, Company, Code |
| `/opendata/t187ap02_L` | 上市公司持股逾 10% 大股東名單 | ok | N | 946 | 出表日期, 公司代號, 公司名稱, 大股東名稱 |
| `/opendata/t187ap03_L` | 上市公司基本資料 | ok | N | 1081 | 出表日期, 公司代號, 公司名稱, 公司簡稱, 外國企業註冊地國 |
| `/opendata/t187ap03_P` | 公開發行公司基本資料 | ok | N | 301 | 出表日期, 公司代號, 公司名稱, 公司簡稱, 外國企業註冊地國 |
| `/opendata/t187ap04_L` | 上市公司每日重大訊息 | ok | N | 103 | 出表日期, 發言日期, 發言時間, 公司代號, 公司名稱 |
| `/opendata/t187ap05_P` | 公開發行公司每月營業收入彙總表 | ok | N | 299 | 出表日期, 資料年月, 公司代號, 公司名稱, 產業別 |
| `/opendata/t187ap08_L` | 上市公司董事、監察人持股不足法定成數彙總表 | ok | N | 30 | 出表日期, 公司代號, 公司名稱, 已發行股份總額, 全體董事應持有股數 |
| `/opendata/t187ap09_L` | 上市公司董事、監察人質權設定占董事及監察人實際持有股數彙總表 | ok | N | 9 | 出表日期, 百分比, 公司名稱 |
| `/opendata/t187ap10_L` | 上市公司董事、監察人持股不足法定成數連續達3個月以上彙總表 | ok | N | 14 | 出表日期, 連續不足達3個月, 連續不足達4個月, 連續不足達5個月, 連續不足達6個月 |
| `/opendata/t187ap11_L` | 上市公司董監事持股餘額明細資料 | ok | N | 27224 | 出表日期, 資料年月, 公司代號, 公司名稱, 職稱 |
| `/opendata/t187ap12_L` | 上市公司每日內部人持股轉讓事前申報表-持股轉讓日報表 | ok | N | 3 | 出表日期, 公司代號, 公司名稱, 申報人身分, 姓名 |
| `/opendata/t187ap13_L` | 上市公司每日內部人持股轉讓事前申報表-持股未轉讓日報表 | ok | N | 3 | 出表日期, 公司代號, 公司名稱, 申報人身分, 姓名 |
| `/opendata/t187ap14_L` | 上市公司各產業EPS統計資訊 | ok | N | 1070 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap22_L` | 上市公司金管會證券期貨局裁罰案件專區 | ok | N | 10 | 出表日期, 發函日期, 股票代號, 公司名稱, 違規事由 |
| `/opendata/t187ap23_L` | 上市公司違反資訊申報、重大訊息及說明記者會規定專區 | ok | N | 11 | 出表日期, 發函日期, 股票代號, 公司名稱, 違規事由 |
| `/opendata/t187ap24_L` | 上市公司經營權及營業範圍異(變)動專區-經營權異動公司 | ok | N | 12 | 出表日期, 公司代號, 公司名稱, 經營權異動日期, 經營權異動說明 |
| `/opendata/t187ap25_L` | 上市公司經營權及營業範圍異(變)動專區-營業範圍重大變更公司 | ok | N | 1 | 出表日期, 序號, 年度, 季別, 公司代號 |
| `/opendata/t187ap26_L` | 上市公司經營權及營業範圍異(變)動專區-經營權異動且營業範圍重大變更停止買賣公司 | empty | N | 0 |  |
| `/opendata/t187ap27_L` | 上市公司經營權及營業範圍異(變)動專區-經營權異動且營業範圍重大變更列為變更交易公司 | empty | N | 0 |  |
| `/opendata/t187ap29_A_L` | 上市公司董事酬金相關資訊  | ok | N | 972 | 出表日期, 產業類別, 公司代號, 公司名稱, 董事酬金-前年支付 |
| `/opendata/t187ap29_B_L` | 上市公司監察人酬金相關資訊  | ok | N | 7 | 出表日期, 產業類別, 公司代號, 公司名稱, 監察人酬金-前年支付 |
| `/opendata/t187ap29_C_L` | 上市公司合併報表董事酬金相關資訊  | ok | N | 999 | 出表日期, 產業類別, 公司代號, 公司名稱, 董事酬金-前年支付 |
| `/opendata/t187ap29_D_L` | 上市公司合併報表監察人酬金相關資訊  | ok | N | 6 | 出表日期, 產業類別, 公司代號, 公司名稱, 監察人酬金-前年支付 |
| `/opendata/t187ap30_L` | 上市公司獨立董監事兼任情形彙總表 | ok | N | 14121 | 出表日期, 序號, 公司代號, 公司名稱, 職稱 |
| `/opendata/t187ap32_L` | 上市公司公司治理之相關規程規則 | ok | N | 10927 | 出表日期, 公司代號, 公司名稱, 公司治理之相關規程規則 |
| `/opendata/t187ap33_L` | 上市公司董事長是否兼任總經理 | ok | N | 1081 | 出表日期, 公司代號, 公司名稱, 董事長, 總經理 |
| `/opendata/t187ap34_L` | 上市公司採累積投票制、全額連記法、候選人提名制選任董監事及當選資料彙總表 | ok | N | 2656 | 出表日期, 公司代號, 公司名稱, 股東常(臨時)會日期-常或臨時, 股東常(臨時)會日期-日期 |
| `/opendata/t187ap35_L` | 上市公司股東行使提案權情形彙總表 | ok | N | 404 | 出表日期, 公司代號, 公司名稱, 召開股東會日期, 股東依公司法第172條之1行使提案權-提... |
| `/opendata/t187ap38_L` | 上市公司股東會公告-召集股東常(臨時)會公告資料彙總表(95年度起適用) | ok | N | 1074 | 出表日期, 公司代號, 公司名稱, 股東常(臨時)會日期-常或臨時, 股東常(臨時)會日期-日期 |
| `/opendata/t187ap41_L` | 上市公司召開股東常 (臨時) 會日期、地點及採用電子投票情形等資料彙總表 | ok | N | 1074 | 出表日期, 公司代號, 公司名稱, 公司地址, 股東常(臨時)會 |
| `/opendata/t187ap45_L` | 上市公司股利分派情形 | ok | N | 1014 | 出表日期, 公司代號, 公司名稱, 決議（擬議）進度, 股利年度 |
| `/opendata/t187ap46_L_1` | 上市公司企業ESG資訊揭露彙總資料-溫室氣體排放 | empty | N | 0 |  |
| `/opendata/t187ap46_L_10` | 上市公司企業ESG資訊揭露彙總資料-燃料管理 | empty | N | 0 |  |
| `/opendata/t187ap46_L_11` | 上市公司企業ESG資訊揭露彙總資料-產品生命週期 | empty | N | 0 |  |
| `/opendata/t187ap46_L_12` | 上市公司企業ESG資訊揭露彙總資料-食品安全 | empty | N | 0 |  |
| `/opendata/t187ap46_L_13` | 上市公司企業ESG資訊揭露彙總資料-供應鏈管理 | empty | N | 0 |  |
| `/opendata/t187ap46_L_14` | 上市公司企業ESG資訊揭露彙總資料-產品品質與安全 | empty | N | 0 |  |
| `/opendata/t187ap46_L_15` | 上市公司企業ESG資訊揭露彙總資料-社區關係 | empty | N | 0 |  |
| `/opendata/t187ap46_L_16` | 上市公司企業ESG資訊揭露彙總資料-資訊安全 | empty | N | 0 |  |
| `/opendata/t187ap46_L_17` | 上市公司企業ESG資訊揭露彙總資料-普惠金融 | empty | N | 0 |  |
| `/opendata/t187ap46_L_18` | 上市公司企業ESG資訊揭露彙總資料-持股及控制力 | empty | N | 0 |  |
| `/opendata/t187ap46_L_19` | 上市公司企業ESG資訊揭露彙總資料-風險管理政策 | empty | N | 0 |  |
| `/opendata/t187ap46_L_2` | 上市公司企業ESG資訊揭露彙總資料-能源管理 | empty | N | 0 |  |
| `/opendata/t187ap46_L_20` | 上市公司企業ESG資訊揭露彙總資料-反競爭行為法律訴訟 | empty | N | 0 |  |
| `/opendata/t187ap46_L_21` | 上市公司企業ESG資訊揭露彙總資料-職業安全衛生 | empty | N | 0 |  |
| `/opendata/t187ap46_L_3` | 上市公司企業ESG資訊揭露彙總資料-水資源管理 | empty | N | 0 |  |
| `/opendata/t187ap46_L_4` | 上市公司企業ESG資訊揭露彙總資料-廢棄物管理 | empty | N | 0 |  |
| `/opendata/t187ap46_L_5` | 上市公司企業ESG資訊揭露彙總資料-人力發展 | empty | N | 0 |  |
| `/opendata/t187ap46_L_6` | 上市公司企業ESG資訊揭露彙總資料-董事會 | empty | N | 0 |  |
| `/opendata/t187ap46_L_7` | 上市公司企業ESG資訊揭露彙總資料-投資人溝通 | empty | N | 0 |  |
| `/opendata/t187ap46_L_8` | 上市公司企業ESG資訊揭露彙總資料-氣候相關議題管理 | empty | N | 0 |  |
| `/opendata/t187ap46_L_9` | 上市公司企業ESG資訊揭露彙總資料-功能性委員會 | empty | N | 0 |  |

#### 其他

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/exchangeReport/BFI61U` | 中央登錄公債補息資料表 | ok | N | 282 | Code, Name, IssuedDate, StartingDate, CouponRate |
| `/news/eventList` | 證交所活動訊息 | ok | N | 45 | No, Title, Details |
| `/news/newsList` | 證交所新聞 | ok | N | 200 | Title, Url, Date |
| `/opendata/t187ap47_L` | 基金基本資料彙總表 | ok | N | 251 | 出表日期, 基金代號, 基金簡稱, 基金類型, 基金中文名稱 |

#### 券商資料

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/ETFReport/ETFRank` | 定期定額交易戶數統計排行月報表 | ok | N | 20 | No, STOCKsSecurityCode, STOCKsName, STOCKsNumbe... |
| `/brokerService/brokerList` | 證券商總公司基本資料 | ok | N | 64 | Code, Name, EstablishmentDate, Address, Telephone |
| `/brokerService/secRegData` | 開辦定期定額業務證券商名單 | ok | N | 21 | SecuritiesFirmCode, Name, BrokerageBusinessStar... |
| `/opendata/OpenData_BRK01` | 證券商營業員男女人數統計資料 | ok | N | 860 | 出表日期, 證券商代號, 男性員工人數, 女性員工人數, 總人數 |
| `/opendata/OpenData_BRK02` | 證券商分公司基本資料 | ok | N | 868 | 出表日期, 證券商代號, 證券商名稱, 開業日, 地址 |
| `/opendata/t187ap01` | 券商業務別人員數 | ok | N | 4 | 出表日期, 職位, 受託買賣, 受託買賣（衍生性商品銷售）, 內部稽核 |
| `/opendata/t187ap18` | 證券商基本資料 | ok | N | 66 | 出表日期, 證券代號, 券商(證券IB)簡稱, 登記資本額（仟元）, 實收資本額（仟元） |
| `/opendata/t187ap20` | 各券商每月月計表 | ok | N | 47515 | 出表日期, 券商代號, 券商名稱, 科目, 會計科目名稱 |
| `/opendata/t187ap21` | 各券商收支概況表資料 | ok | N | 19175 | 出表日期, 券商代號, 券商名稱, 科目, 會計科目名稱 |

#### 指數

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/exchangeReport/MI_INDEX4` | 每日上市上櫃跨市場成交資訊 | ok | N | 5 | Date, TradeValue, FormosaIndex, Change |
| `/indicesReport/FRMSA` | 寶島股價指數歷史資料 | ok | N | 5 | Date, FormosaIndex, FormosaTotalReturnIndex |
| `/indicesReport/MFI94U` | 發行量加權股價報酬指數 | ok | N | 5 | Date, TAIEXTotalReturnIndex |
| `/indicesReport/TAI50I` | 臺灣 50 指數歷史資料 | ok | N | 5 | Date, Taiwan50Index, Taiwan50TotalReturnIndex |

#### 權證

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/opendata/t187ap36_L` | 上市認購(售)權證年度發行量概況統計表 | ok | N | 54321 | 出表日期, 發行人代號, 發行人名稱, 權證代號, 名稱 |
| `/opendata/t187ap42_L` | 上市認購(售)權證每日成交資料檔 | ok | N | 32435 | 出表日期, 交易日期, 權證代號, 權證名稱, 成交金額 |
| `/opendata/t187ap43_L` | 上市認購(售)權證交易人數檔 | ok | N | 1 | 出表日期, 日期, 人數 |

#### 證券交易

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/Announcement/BFZFZU_T` | 投資理財節目異常推介個股 | ok | N | 1 | Number, Code, Name, Date |
| `/SBL/TWT96U` | 上市上櫃股票當日可借券賣出股數 | ok | N | 1203 | TWSECode, TWSEAvailableVolume, GRETAICode, GRET... |
| `/announcement/notetrans` | 集中市場公布注意累計次數異常資訊 | ok | N | 6 | Code, Name, RecentlyMetAttentionSecuritiesCriteria |
| `/announcement/notice` | 集中市場當日公布注意股票 | ok | N | 1 | Number, Code, Name, NumberOfAnnouncement, Tradi... |
| `/block/BFIAUU_d` | 集中市場鉅額交易日成交量值統計 | ok | N | 20 | Date, Class, Type, TradeVolume, MarketSharePer |
| `/block/BFIAUU_m` | 集中市場鉅額交易月成交量值統計 | ok | N | 8 | Month, Class, TradeVolume, MarketSharePer, Trad... |
| `/block/BFIAUU_y` | 集中市場鉅額交易年成交量值統計 | ok | N | 22 | Month, TradeVolume, MarketSharePer, TradeValue |
| `/exchangeReport/BWIBBU_ALL` | 上市個股日本益比、殖利率及股價淨值比（依代碼查詢） | ok | N | 1070 | Date, Code, Name, PEratio, DividendYield |
| `/exchangeReport/BWIBBU_d` | 上市個股日本益比、殖利率及股價淨值比（依日期查詢） | ok | N | 1070 | Date, Code, Name, ClosePrice, DividendYield |
| `/exchangeReport/FMNPTK_ALL` | 上市個股年成交資訊 | ok | N | 72048 | Year, Code, Name, TradeVolume, TradeValue |
| `/exchangeReport/FMSRFK_ALL` | 上市個股月成交資訊 | ok | N | 30623 | Month, Code, Name, HighestPrice, LowestPrice |
| `/exchangeReport/MI_5MINS` | 每 5 秒委託成交統計 | ok | N | 3241 | Time, AccBidOrders, AccBidVolume, AccAskOrders,... |
| `/exchangeReport/STOCK_DAY_ALL` | 上市個股日成交資訊 | ok | N | 1349 | Date, Code, Name, TradeVolume, TradeValue |
| `/exchangeReport/STOCK_DAY_AVG_ALL` | 上市個股日收盤價及月平均價 | ok | N | 21944 | Date, Code, Name, ClosingPrice, MonthlyAverageP... |
| `/exchangeReport/STOCK_FIRST` | 每日第一上市外國股票成交量值 | ok | N | 90 | Code, Name, TradeVolume, Transaction, TradeValue |
| `/exchangeReport/TWT48U_ALL` | 上市股票除權除息預告表 | ok | N | 73 | Date, Code, Name, Exdividend, StockDividendRatio |
| `/exchangeReport/TWT85U` | 集中市場證券變更交易 | ok | N | 40 | Code, Name, PeriodicCallAuctionTrading |
| `/exchangeReport/TWT88U` | 上市個股首五日無漲跌幅 | ok | N | 2 | SecurCode, SecurName, 1stTradingDate, 5thTradin... |
| `/exchangeReport/TWTAWU` | 集中市場暫停交易證券 | ok | N | 1 | Number, Code, Name, TradingHaltDate, TradingHal... |
| `/exchangeReport/TWTBAU1` | 集中市場暫停先賣後買當日沖銷交易標的預告表 | ok | N | 466 | Code, Name, StartDate, EndDate, Reason |
| `/exchangeReport/TWTBAU2` | 集中市場暫停先賣後買當日沖銷交易歷史查詢 | ok | N | 137 | Code, Name, StartDate, EndDate, Reason |
| `/fund/MI_QFIIS_cat` | 集中市場外資及陸資投資類股持股比率表 | ok | N | 36 | IndustryCat, Numbers, ShareNumber, ForeignMainl... |
| `/fund/MI_QFIIS_sort_20` | 集中市場外資及陸資持股前 20 名彙總表 | ok | N | 20 | Rank, Code, Name, ShareNumber, AvailableShare |
| `/holidaySchedule/holidaySchedule` | 有價證券集中交易市場開（休）市日期 | ok | N | 27 | Name, Date, Weekday, Description |
| `/opendata/t187ap19` | 電子式交易統計資訊 | ok | N | 1 | 出表日期, 成交月份, 本月新增戶數, 本月註銷戶數, 累計開戶數 |
| `/opendata/t187ap37_L` | 上市權證基本資料彙總表 | ok | N | 43204 | 出表日期, 權證代號, 權證簡稱, 權證類型, 類別 |
| `/opendata/twtazu_od` | 集中市場漲跌證券數統計表 | ok | N | 2 | 出表日期, 類型, 上漲, 漲停, 下跌 |

#### 財務報表

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/opendata/t187ap05_L` | 上市公司每月營業收入彙總表 | ok | N | 1070 | 出表日期, 資料年月, 公司代號, 公司名稱, 產業別 |
| `/opendata/t187ap06_L_basi` | 上市公司綜合損益表(金融業) | ok | N | 10 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap06_L_bd` | 上市公司綜合損益表(證券期貨業) | ok | N | 3 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap06_L_ci` | 上市公司綜合損益表(一般業) | ok | N | 1034 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap06_L_fh` | 上市公司綜合損益表(金控業) | ok | N | 13 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap06_L_ins` | 上市公司綜合損益表(保險業) | ok | N | 6 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap06_L_mim` | 上市公司綜合損益表(異業) | ok | N | 4 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap06_X_basi` | 公發公司綜合損益表-金融業 | ok | N | 34 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap06_X_bd` | 公發公司綜合損益表-證券期貨業 | ok | N | 27 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap06_X_ci` | 公發公司綜合損益表-一般業 | ok | N | 87 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap06_X_fh` | 公發公司綜合損益表-金控業 | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap06_X_ins` | 公發公司綜合損益表-保險業 | ok | N | 16 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap06_X_mim` | 公發公司綜合損益表-異業 | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap07_L_basi` | 上市公司資產負債表(金融業) | ok | N | 10 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap07_L_bd` | 上市公司資產負債表(證券期貨業) | ok | N | 3 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap07_L_ci` | 上市公司資產負債表(一般業) | ok | N | 1034 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap07_L_fh` | 上市公司資產負債表(金控業) | ok | N | 13 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap07_L_ins` | 上市公司資產負債表(保險業) | ok | N | 6 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap07_L_mim` | 上市公司資產負債表(異業) | ok | N | 4 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap07_X_basi` | 公發公司資產負債表-金融業 | ok | N | 34 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap07_X_bd` | 公發公司資產負債表-證券期貨業 | ok | N | 27 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap07_X_ci` | 公發公司資產負債表-一般業 | ok | N | 87 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap07_X_fh` | 公發公司資產負債表-金控業 | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap07_X_ins` | 公發公司資產負債表-保險業 | ok | N | 16 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap07_X_mim` | 公發公司資產負債表-異業 | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap11_P` | 公發公司董監事持股餘額明細 | ok | N | 6559 | 出表日期, 資料年月, 公司代號, 公司名稱, 職稱 |
| `/opendata/t187ap15_L` | 上市公司截至各季綜合損益財測達成情形(簡式) | ok | N | 4 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap16_L` | 上市公司當季綜合損益經會計師查核(核閱)數與當季預測數差異達百分之十以上者，或截至當季累計差異達百分之二十以上者(簡式) | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap17_L` | 上市公司營益分析查詢彙總表(全體公司彙總報表) | ok | N | 1040 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/opendata/t187ap31_L` | 上市公司財務報告經監察人承認情形 | ok | N | 1068 | 出表日期, 公司代號, 公司名稱, 是否設置審計委員會, 出具本次財務報告審查報告書之監察人姓名 |

### Web (137 endpoints)

#### 上市公司

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/zh/listed/listed/apply-listing.html` | 申請上市公司 | ok | Y | 853 | 索引, 公司代號, 公司簡稱, 申請日期, 董事長 |
| `/zh/listed/listed/apply-tdr.html` | 向本公司申請發行臺灣存託憑證公司 | ok | N | 57 | 公司
代號, 公司簡稱, 申請日期, 董事長, 預計發行
單位數 |
| `/zh/listed/listed/change-listing.html` | 申請改列公司 | ok | N | 5 | 索引, 公司代號, 公司簡稱, 申請日期, 董事長 |
| `/zh/listed/listed/ipo-seo.html` | 向本公司申請辦理首次公開發行、初次上市前及改列上市前現金增資案件彙總表 | ok | N | 320 | 證券代號, 公司型態, 結案類型
(說明1), 公司名稱, 承銷商 |
| `/zh/listed/listed/new-listing.html` | 最近上市公司 | ok | N | 777 | 公司代號, 公司簡稱, 申請日期, 董事長, 申請時股本(仟元) |
| `/zh/listed/suspend-listing.html` | 終止上市公司 | error | N | 0 | 終止上市日期, 公司名稱, 上市編號 |
| `/zh/listed/violations/change.html` | 變更交易及併採行分盤集合競價交易 | ok | N | 17 | 證券代號, 證券名稱, 違反營業細則條款, 變更交易原因, 變更交易開始日 |
| `/zh/listed/violations/stop.html` | 停止買賣 | ok | N | 1 | 證券代號, 證券名稱, 違反營業細則條款, 停止買賣原因, 停止買賣開始日期 |

#### 上市證券

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/zh/products/broker/month-rank.html` | 定期定額交易戶數統計排行月報表 | ok | N | 20 |  , 代號, 名稱, 交易戶數, 代號 |
| `...roducts/etf-registration-processing-status.html` | ETF受理申報案件情形 | error | N | 0 | 收文日期, 案件狀態, 公司名稱, ETF名稱, 案件類別 |
| `/zh/products/sbl/disclosures/info.html` | 借券資訊 | error | Y | 0 | 名稱, 市場別, 開盤參考價, 限制出借(詳說明2)[可擔保證券明細]
代號, 名稱 |
| `/zh/products/securities/etf/news.html` | ETF | error | Y | 0 | 證券名稱, 成交金額, 成交股數, 成交筆數, 開盤價 |
| `...ducts/securities/etn/overview/introduction.html` | ETN | error | Y | 0 | 證券名稱, 成交金額, 成交股數, 成交筆數, 開盤價 |
| `/zh/products/securities/warrant/rank/amount.html` | 權證發行金額排行 | ok | N | 12 | 排行, 證券商代號, 證券商名稱, 發行金額 |
| `...roducts/securities/warrant/rank/securities.html` | 發行標的證券排行 | ok | N | 220 | 排行, 權證標的代號, 權證標的名稱, 發行檔數 |
| `/zh/products/securities/warrant/rank/symbol.html` | 權證發行檔數排行 | ok | N | 12 | 排行, 證券商代號, 證券商名稱, 發行檔數 |
| `/zh/products/securities/warrant/rank/trading.html` | 受託買賣權證成交金額排行 | ok | N | 52 | 排行, 證券商代號, 證券商名稱, 交易金額 |

#### 交易資訊

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/zh/trading/bfib8u.html` | 標借 | ok | Y | 9 | 標借日期, 證券代號, 證券名稱, 證金公司, 不足數量 |
| `/zh/trading/block/bfiauu-day.html` | 鉅額交易日成交量值統計 | ok | Y | 30 | 日期, 交易別, 類別, 成交股數, 成交股數占市場比重% |
| `/zh/trading/block/bfiauu-month.html` | 鉅額交易月成交量值統計 | ok | Y | 12 | 成交月份, 交易別, 成交股數, 成交股數占市場比重%, 成交金額 |
| `/zh/trading/block/bfiauu-stock.html` | 個股單一證券鉅額交易日成交資訊 | empty | Y | 0 | 日期, 交易別, 成交股數, 成交金額, 最高價 |
| `/zh/trading/block/bfiauu-year.html` | 鉅額交易年成交量值統計 | ok | N | 22 | 成交年度, 成交股數, 成交股數占市場比重%, 成交金額, 成交金額占市場比重% |
| `/zh/trading/block/bfiauu.html` | 鉅額交易日成交資訊 | ok | N | 27 | 證券代號, 證券名稱, 交易別, 成交價, 成交股數 |
| `/zh/trading/day-trading.html` | 每日當日沖銷交易標的 | ok | Y | 1191 | 證券代號, 證券名稱, 暫停現股賣出後
現款買進當沖註記 |
| `/zh/trading/day-trading/bfif8u.html` | 應付現股當日沖銷券差借券費率 | ok | Y | 667 | 券差日期, 證券代號, 證券名稱, 投資人借券股數, 投資人借券費率 |
| `/zh/trading/day-trading/twtb4u-month.html` | 每月當日沖銷交易標的及統計 | ok | Y | 6 | 日期, 當日沖銷交易總成交股數, 當日沖銷交易總成交股數占市場比重%, 當日沖銷交易總買進成交... |
| `/zh/trading/day-trading/twtbau-history.html` | 暫停先賣後買當日沖銷交易歷史查詢 | ok | Y | 204 | 股票代號, 股票名稱, 停止先賣後買開始日, 停止先賣後買結束日, 原因 |
| `/zh/trading/day-trading/twtbau.html` | 暫停先賣後買當日沖銷交易標的預告表 | ok | N | 351 | 證券代號, 證券名稱, 停止先賣後買開始日, 停止先賣後買結束日, 原因 |
| `/zh/trading/delivery/twt84u.html` | 股價升降幅度 | ok | Y | 1350 | 證券代號, 證券名稱, 漲停價, 開盤競價基準, 跌停價 |
| `/zh/trading/delivery/twt88u.html` | 首五日無漲跌幅 | ok | Y | 2 | 證券代號, 證券名稱, 執行起始日, 執行到期日, 承銷價 |
| `/zh/trading/foreign/bfi82u.html` | 三大法人買賣金額統計表 | ok | Y | 6 | 單位名稱, 買進金額, 賣出金額, 買賣差額 |
| `/zh/trading/foreign/fmgdrk.html` | 國內上市公司發行海外存託憑證彙總表 | ok | N | 48 | 上市公司名稱, 國際證券辨識號碼, 上市地點, 存託機構, 保管銀行 |
| `/zh/trading/foreign/mi-qfiis-cat.html` | 外資及陸資投資類股持股比率表 | ok | N | 36 | 產業別, 家數, 總發行股數, 僑外資及陸資持有總股數, 僑外資及陸資持股比率 |
| `/zh/trading/foreign/mi-qfiis.html` | 外資及陸資投資持股統計 | ok | Y | 8 | 證券代號, 證券名稱, 國際證券編碼, 發行股數, 外資及陸資尚可投資股數 |
| `/zh/trading/foreign/mi-qfiis20.html` | 外資及陸資持股前20名彙總表 | ok | Y | 20 | 排行, 證券代號, 證券名稱, 發行股數, 外資及陸資尚可投資股數 |
| `/zh/trading/foreign/t86.html` | 三大法人買賣超日報 | ok | Y | 8 | 證券代號, 證券名稱, 外陸資買進股數(不含外資自營商), 外陸資賣出股數(不含外資自營商),... |
| `/zh/trading/foreign/twt38u.html` | 外資及陸資買賣超彙總表 | error | Y | 0 | 證券代號, 證券名稱, 賣出股數, 買賣超股數, 賣出股數 |
| `/zh/trading/foreign/twt43u.html` | 自營商買賣超彙總表 | ok | Y | 14982 | 證券代號, 證券名稱, 買進股數, 賣出股數, 買賣超股數 |
| `/zh/trading/foreign/twt44u.html` | 投信買賣超彙總表 | ok | Y | 340 | , 證券代號, 證券名稱, 買進股數, 賣出股數 |
| `/zh/trading/foreign/twt47u.html` | 三大法人買賣超月報 | ok | Y | 8 | 證券代號, 證券名稱, 外陸資買進股數(不含外資自營商), 外陸資賣出股數(不含外資自營商),... |
| `/zh/trading/foreign/twt54u.html` | 三大法人買賣超週報 | ok | Y | 8 | 證券代號, 證券名稱, 外陸資買進股數(不含外資自營商), 外陸資賣出股數(不含外資自營商),... |
| `/zh/trading/government/abp010.html` | 中央登錄公債行情單 | error | N | 0 | 債券代號, 債券名稱, 成交量   成交金額(不含息), 成交筆數, 開盤價 |
| `/zh/trading/government/bfi61u.html` | 中央登錄公債補息資料表 | ok | N | 282 | 債券代號, 債券簡稱, 發行日期, 起息日, 票面利率 |
| `/zh/trading/historical/bfiamu.html` | 各類指數日成交量值 | ok | Y | 34 | 分類指數名稱, 成交股數, 成交金額, 成交筆數, 漲跌指數 |
| `/zh/trading/historical/bft41u.html` | 盤後定價交易 | ok | Y | 9 | 證券代號, 證券名稱, 成交數量, 成交筆數, 成交金額 |
| `/zh/trading/historical/bwibbu-day.html` | 個股日本益比、殖利率及股價淨值比（依日期查詢） | ok | Y | 1070 | 證券代號, 證券名稱, 收盤價, 殖利率(%), 股利年度 |
| `/zh/trading/historical/bwibbu.html` | 個股日本益比、殖利率及股價淨值比（依代碼查詢） | error | Y | 0 | 日期, 殖利率(%), 股利年度, 本益比, 股價淨值比 |
| `/zh/trading/historical/fmnptk.html` | 個股年成交資訊 | error | Y | 0 | 年度, 成交股數, 成交金額, 成交筆數, 最高價 |
| `/zh/trading/historical/fmsrfk.html` | 個股月成交資訊 | error | Y | 0 | 年度, 月份, 最高價, 最低價, 加權(A/B)平均價 |
| `/zh/trading/historical/fmtqik.html` | 每日市場成交資訊 | error | Y | 0 | 日期, 成交股數, 成交金額, 成交筆數, 發行量加權股價指數 |
| `/zh/trading/historical/mi-5mins.html` | 每5秒委託成交統計 | ok | Y | 3241 | 時間, 累積委託買進筆數, 累積委託買進數量, 累積委託賣出筆數, 累積委託賣出數量 |
| `/zh/trading/historical/mi-index.html` | 每日收盤行情 | ok | Y | 22 | 成交統計, 成交金額(元), 成交股數(股), 成交筆數 |
| `/zh/trading/historical/mi-stock-first.html` | 每日第一上市外國股票成交量值 | ok | Y | 91 | 證券代號, 證券名稱, 成交股數, 成交筆數, 成交金額 |
| `/zh/trading/historical/mi-stock-tib.html` | 每日創新板股票成交量值 | ok | Y | 25 | 證券代號, 證券名稱, 成交股數, 成交筆數, 成交金額 |
| `/zh/trading/historical/mi-stock20.html` | 每日成交量前二十名證券 | ok | Y | 20 | 排名, 證券代號, 證券名稱, 成交股數, 成交筆數 |
| `/zh/trading/historical/stock-day-avg.html` | 個股日收盤價及月平均價 | error | Y | 0 | 日期, 收盤價
備註：該月份各交易日及其收盤價 |
| `/zh/trading/historical/stock-day.html` | 個股日成交資訊 | error | Y | 0 | 日期, 成交股數, 成交金額, 開盤價, 最高價 |
| `/zh/trading/historical/twt53u.html` | 盤後零股交易行情單 | ok | Y | 1335 | 證券代號, 證券名稱, 成交股數, 成交筆數, 成交金額 |
| `/zh/trading/historical/twtasu.html` | 當日融券賣出與借券賣出成交量值 | ok | Y | 1301 | 證券名稱, 數量, 金額, 數量, 金額 |
| `/zh/trading/historical/twtawu.html` | 暫停交易證券 | ok | Y | 1 | 編號, 證券代號, 證券名稱, 暫停交易日期, 暫停交易時間 |
| `/zh/trading/historical/twtc7u.html` | 盤中零股交易行情單 | ok | Y | 1335 | 證券代號, 證券名稱, 成交股數, 成交筆數, 成交金額 |
| `/zh/trading/margin/bfi84u-history.html` | 停券歷史查詢 | ok | Y | 5 | 股票代號, 股票名稱, 停券起日(最後回補日), 停券迄日, 原因 |
| `/zh/trading/margin/bfi84u.html` | 停券預告表 | ok | N | 367 | 股票代號, 股票名稱, 停券起日(最後回補日), 停券迄日, 原因 |
| `/zh/trading/margin/bfib9u.html` | 調整成數 | ok | Y | 271 | 編號, 證券代號, 證券名稱, 調整成數原因, 調整成數起日 |
| `/zh/trading/margin/mi-margn.html` | 融資融券餘額 | ok | Y | 3 | 項目, 買進, 賣出, 現金(券)償還, 前日餘額 |
| `/zh/trading/margin/twt92u.html` | 平盤下得融(借)券賣出之證券名單 | ok | Y | 1187 | 證券代號, 證券名稱, 暫停融券賣出, 暫停借券賣出, 前一交易日收盤價跌停本日禁止平盤下融券... |
| `/zh/trading/margin/twt93u.html` | 融券借券賣出餘額 | ok | Y | 1268 | 代號, 名稱, 前日餘額, 賣出, 買進 |
| `/zh/trading/margin/twt96u.html` | 當日可借券賣出股數 | ok | N | 1204 | 證券代號, 可借券賣出股數, 證券代號, 可借券賣出股數 |
| `/zh/trading/margin/twta1u.html` | 借貸款項擔保品管制餘額 | ok | Y | 2148 | 代號, 名稱, 前日餘額, 買進, 賣出 |
| `/zh/trading/statistics/index01.html` | 股價指數月報 | ok | Y | 4 | 報表名稱, 1月, 2月, 3月, 4月 |
| `/zh/trading/statistics/index02.html` | 市場交易月報 | ok | Y | 4 | 報表名稱, 1月, 2月, 3月, 4月 |
| `/zh/trading/statistics/index03.html` | 證券商月報 | ok | Y | 4 | 報表名稱, 1月, 2月, 3月, 4月 |
| `/zh/trading/statistics/index04.html` | 上市公司月報 | ok | Y | 4 | 報表名稱, 1月, 2月, 3月, 4月 |
| `/zh/trading/statistics/index05.html` | 上市公司季報 | ok | Y | 4 | 報表名稱, 1月, 2月, 3月, 4月 |
| `/zh/trading/statistics/index06.html` | 國際主要股市月報 | ok | Y | 4 | 報表名稱, 1月, 2月, 3月, 4月 |
| `/zh/trading/statistics/index07.html` | 證券統計資料年報 | ok | Y | 4 | 報表名稱, 1月, 2月, 3月, 4月 |
| `/zh/trading/statistics/week.html` | 市值週報 | ok | Y | 1 | 文件名稱, 下載 |
| `/zh/trading/twt85u.html` | 變更交易 | ok | Y | 40 | 證券代號, 證券名稱, 分盤集合競價(以**表示) |

#### 信用交易

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/exchangeReport/BFI84U` | 停資停券預告表 | ok | Y | 371 | 股票代號, 股票名稱, 停券起日(最後回補日), 停券迄日, 原因 |
| `/exchangeReport/MI_MARGN` | 融資融券餘額 | ok | Y | 1196 | 項目, 買進, 賣出, 現金(券)償還, 前日餘額 |
| `/exchangeReport/TWTASU` | 信用交易統計 | ok | Y | 1234 | 證券名稱, 數量, 金額, 數量, 金額 |

#### 借券

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/exchangeReport/TWT93U` | 借券成交明細 | ok | Y | 1199 | 代號, 名稱, 前日餘額, 賣出, 買進 |

#### 公告資訊

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/zh/announcement/auction.html` | 競價拍賣公告-投標日程表 | ok | N | 42 | 序號, 開標日期, 證券名稱, 證券代號, 發行市場 |
| `/zh/announcement/bfigtu.html` | 1.證券商申報投資人違約金額2.個股達違約資訊揭露標準之證券資訊 | ok | N | 1 | 申報日期, 買進、賣出合計總金額, 買進、賣出相抵後金額 |
| `/zh/announcement/bfzfzu-t.html` | 投資理財節目異常推介個股 | ok | N | 1 | 編號, 證券代號, 證券名稱, 日期 |
| `/zh/announcement/bfzfzu-u.html` | 特殊異常有價證券 | empty | N | 0 | 編號, 證券代號, 證券名稱, 日期 |
| `/zh/announcement/change/twtb7u.html` | 變更股票面額預告表 | ok | N | 1 | 停止買賣日期, 股票代號, 名稱, 恢復買賣日期, 變更股票面額換股率 |
| `/zh/announcement/change/twtb8u.html` | 變更股票面額恢復買賣參考價格 | ok | N | 1 | 恢復買賣日期, 股票代號, 名稱, 停止買賣前收盤價格, 恢復買賣參考價 |
| `/zh/announcement/ex-right/twt48u.html` | 預告表 | ok | N | 67 | 除權除息日期, 股票代號, 名稱, 除權息, 無償配股率 |
| `/zh/announcement/ex-right/twt49u.html` | 計算結果表 | ok | Y | 2 | 資料日期, 股票代號, 股票名稱, 除權息前收盤價, 除權息參考價 |
| `/zh/announcement/notetrans.html` | 公布注意累計次數異常資訊 | ok | N | 13 | 編號, 證券代號, 證券名稱, 近期達本公司「公布注意交易資訊」標準之情形 |
| `/zh/announcement/notice.html` | 公布注意有價證券 | ok | Y | 38 | 編號, 證券代號, 證券名稱, 累計次數, 注意交易資訊 |
| `/zh/announcement/public.html` | 公開申購公告-抽籤日程表 | ok | Y | 93 | 序號, 抽籤日期, 證券名稱, 證券代號, 發行市場 |
| `/zh/announcement/punish.html` | 公布處置有價證券 | ok | Y | 14 | 編號, 公布日期, 證券代號, 證券名稱, 累計 |
| `/zh/announcement/reduction/twtauu.html` | 股票減資恢復買賣參考價格 | ok | N | 1 | 恢復買賣日期, 股票代號, 名稱, 停止買賣前收盤價格, 恢復買賣參考價 |
| `/zh/announcement/split/twtc9u.html` | ETF分割(反分割)預告表 | ok | N | 1 | 停止買賣日期, ETF代號, 名稱, 分割(反分割), 恢復買賣日期 |
| `/zh/announcement/split/twtcau.html` | ETF分割(反分割)恢復買賣參考價格 | ok | N | 1 | 恢復買賣日期, ETF代號, 名稱, 分割(反分割), 停止買賣前收盤價格 |

#### 基本面

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/exchangeReport/BWIBBU` | 個股本益比、殖利率及股價淨值比 | ok | Y | 20 | 日期, 殖利率(%), 股利年度, 本益比, 股價淨值比 |
| `/exchangeReport/TWT48U` | 除權除息預告表 | ok | Y | 73 | 除權除息日期, 股票代號, 名稱, 除權息, 無償配股率 |

#### 市場焦點

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/zh/focus/lt185-dtr.html` | 上市普通股股數／TDR單位數增減公告 | ok | N | 3 | 公司代號, 公司簡稱, 公告種類, 申報序號, 主旨 |

#### 指數

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/indicesReport/MI_5MINS_HIST` | 發行量加權股價指數歷史資料 | ok | Y | 20 | 日期, 開盤指數, 最高指數, 最低指數, 收盤指數 |

#### 指數資訊

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/zh/indices/cross/frmsa.html` | 寶島股價指數歷史資料 | ok | Y | 7 | 日期, 寶島股價指數, 寶島股價報酬指數 |
| `/zh/indices/cross/mi-index4.html` | 每日上市上櫃跨市場成交資訊 | ok | Y | 7 | 日期, 成交金額(元), 寶島股價指數, 漲跌點數 |
| `/zh/indices/ftse/bfm44u-tai100i.html` | 臺灣中型100指數月平均價差 | ok | Y | 3 | 年度, 月份, 成交值(仟元), 成交量(交易單位) , 成交筆數 |
| `/zh/indices/ftse/bfm44u-tai50i.html` | 臺灣50指數月平均價差 | ok | Y | 3 | 年度, 月份, 成交值(仟元), 成交量(交易單位) , 成交筆數 |
| `/zh/indices/ftse/bfm44u-taidividi.html` | 臺灣高股息指數月平均價差 | ok | Y | 3 | 年度, 月份, 成交值(仟元), 成交量(交易單位) , 成交筆數 |
| `/zh/indices/ftse/bfm44u-taiei.html` | 臺灣發達指數月平均價差 | ok | Y | 3 | 年度, 月份, 成交值(仟元), 成交量(交易單位) , 成交筆數 |
| `/zh/indices/ftse/bfm44u-taiinti.html` | 臺灣資訊科技指數月平均價差 | ok | Y | 3 | 年度, 月份, 成交值(仟元), 成交量(交易單位) , 成交筆數 |
| `/zh/indices/ftse/tai100i.html` | 臺灣中型100指數歷史資料 | ok | Y | 7 | 日期, 臺灣中型100指數, 臺灣中型100報酬指數 |
| `/zh/indices/ftse/tai50i.html` | 臺灣50指數歷史資料 | ok | Y | 7 | 日期, 臺灣50指數, 臺灣50報酬指數 |
| `/zh/indices/ftse/taidividi.html` | 臺灣高股息指數歷史資料 | ok | Y | 7 | 日期, 臺灣高股息指數, 臺灣高股息報酬指數 |
| `/zh/indices/ftse/taiei.html` | 臺灣發達指數歷史資料 | ok | Y | 7 | 日期, 臺灣發達指數, 臺灣發達報酬指數 |
| `/zh/indices/ftse/taiinti.html` | 臺灣資訊科技指數歷史資料 | ok | Y | 7 | 日期, 臺灣資訊科技指數, 臺灣資訊科技報酬指數 |
| `/zh/indices/research/emp99.html` | 臺灣就業99指數歷史資料 | error | Y | 0 | 日期, 臺灣就業99指數, 臺灣就業99報酬指數 |
| `/zh/indices/research/hc100.html` | 臺灣高薪100指數歷史資料 | ok | Y | 7 | 日期, 臺灣高薪100指數, 臺灣高薪100報酬指數 |
| `/zh/indices/taiex/cg100.html` | 臺灣公司治理100指數歷史資料 | ok | Y | 7 | 日期, 臺灣公司治理100指數, 臺灣公司治理100報酬指數 |
| `/zh/indices/taiex/eftri-hist.html` | 電子類指數及金融保險類指數 | ok | Y | 7 | 日　期, 電子類指數, 半導體類指數, 電腦及週邊設備類指數, 光電類指數 |
| `/zh/indices/taiex/eftri.html` | 電子類報酬指數及金融保險類報酬指數 | ok | Y | 7 | 日　期, 電子類報酬指數, 半導體類報酬指數, 電腦及週邊設備類報酬指數, 光電類報酬指數 |
| `/zh/indices/taiex/mfi94u.html` | 發行量加權股價報酬指數 | ok | Y | 7 | 日　期, 發行量加權股價報酬指數 |
| `/zh/indices/taiex/mi-5min-hist.html` | 發行量加權股價指數歷史資料 | ok | Y | 7 | 日期, 開盤指數, 最高指數, 最低指數, 收盤指數 |
| `/zh/indices/taiex/mi-5min-indices.html` | 每5秒指數盤後統計 | ok | Y | 3241 | 時間, 發行量加權股價指數, 未含金融保險股指數, 未含電子股指數, 未含金融電子股指數 |
| `/zh/indices/taiex/sc300.html` | 小型股300指數歷史資料 | ok | Y | 7 | 日期, 小型股300指數, 小型股300報酬指數 |
| `/zh/indices/taiex/ttdr.html` | 臺指槓桿及反向指數歷史資料 | ok | Y | 7 | 日期, 臺指日報酬兩倍指數, 臺指反向一倍指數 |
| `/zh/indices/taiex/twt91u.html` | 未含金融電子股指數歷史資料 | ok | Y | 7 | 日　期, 未含金融電子股指數, 未含金融電子股報酬指數 |

#### 法人

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/fund/MI_QFIIS` | 外資及陸資投資持股統計 | ok | Y | 1261 | 證券代號, 證券名稱, 國際證券編碼, 發行股數, 外資及陸資尚可投資股數 |
| `/fund/T86` | 三大法人買賣超日報 | ok | Y | 4095 | 證券代號, 證券名稱, 外陸資買進股數(不含外資自營商), 外陸資賣出股數(不含外資自營商),... |
| `/fund/TWT38U` | 三大法人買賣金額統計表 | ok | Y | 1096 | , 證券代號, 證券名稱, 買進股數, 賣出股數 |

#### 行情

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/exchangeReport/BFT41U` | 盤後定價交易 | ok | Y | 9 | 證券代號, 證券名稱, 成交數量, 成交筆數, 成交金額 |
| `/exchangeReport/FMSRFK` | 個股月成交資訊 | ok | Y | 12 | 年度, 月份, 最高價, 最低價, 加權(A/B)平均價 |
| `/exchangeReport/FMTQIK` | 每日成交量值 | ok | Y | 20 | 日期, 成交股數, 成交金額, 成交筆數, 發行量加權股價指數 |
| `/exchangeReport/MI_INDEX` | 每日收盤行情（大盤統計） | ok | Y | 22 | 成交統計, 成交金額(元), 成交股數(股), 成交筆數 |
| `/exchangeReport/MI_INDEX20` | 每日成交量前二十名證券 | ok | Y | 20 | 排名, 證券代號, 證券名稱, 成交股數, 成交筆數 |
| `/exchangeReport/STOCK_DAY` | 個股日成交資訊 | ok | Y | 20 | 日期, 成交股數, 成交金額, 開盤價, 最高價 |
| `/exchangeReport/STOCK_DAY_AVG` | 個股月均價 | ok | Y | 21 | 日期, 收盤價 |
| `/exchangeReport/TWT53U` | 零股交易行情 | ok | Y | 1267 | 證券代號, 證券名稱, 成交股數, 成交筆數, 成交金額 |
| `/exchangeReport/TWT84U` | 個股股價升降幅度 | ok | Y | 1285 | 證券代號, 證券名稱, 漲停價, 開盤競價基準, 跌停價 |
| `/exchangeReport/TWTB4U` | 當日沖銷交易標的及統計 | ok | Y | 1125 | 當日沖銷交易總成交股數, 當日沖銷交易總成交股數占市場比重%, 當日沖銷交易總買進成交金額, ... |

## Taipei Exchange (TPEx)

### OpenAPI (225 endpoints)

#### 上櫃

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mopsfin_t187ap19_O` | 電子式交易統計資訊(上櫃) | ok | N | 1 | 出表日期, 成交月份, 本月新增戶數, 本月註銷戶數, 累計開戶數 |
| `/tpex_3insti_daily_trading` | 上櫃股票三大法人買賣明細資訊 | ok | N | 915 | Date, SecuritiesCompanyCode, CompanyName, Forei... |
| `/tpex_3insti_dealer_trading` | 上櫃股票自營商買賣超彙總表 | ok | N | 2528 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |
| `/tpex_3insti_qfii` | 上櫃僑外資及陸資持股比例排行表 | ok | N | 882 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |
| `/tpex_3insti_qfii_industry` | 上櫃各類股僑外資及陸資持股比例表 | ok | N | 28 | Date, Industry, NumberOfCompanies, NumberOfShar... |
| `/tpex_3insti_qfii_trading` | 上櫃股票外資及陸資買賣超彙總表 | ok | N | 428 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |
| `/tpex_3insti_summary` | 上櫃股票三大法人買賣金額彙總表 | ok | N | 8 | Date, Investor, PurchaseAmount, SaleAmount, Net |
| `/tpex_3insti_trading` | 上櫃股票投信買賣超彙總表 | ok | N | 16 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |
| `/tpex_active_advanced` | 上櫃盤中個股漲幅排行 | ok | N | 30 | Date, SecuritiesCompanyCode, CompanyName, Closi... |
| `/tpex_active_broker_volume` | 上櫃股票熱門股證券商進出排行 | ok | N | 300 | Date, StockRanking, SecuritiesCompanyCodeAndCom... |
| `/tpex_active_declined` | 上櫃盤中個股跌幅排行 | ok | N | 30 | Date, SecuritiesCompanyCode, CompanyName, Closi... |
| `/tpex_active_dollar_volume` | 上櫃盤中個股成交金額排行 | ok | N | 30 | Date, SecuritiesCompanyCode, CompanyName, Numbe... |
| `/tpex_amount_rank` | 上櫃歷史個股成交值排行 | ok | N | 879 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |
| `/tpex_ceil_non_trading` | 上櫃漲跌停未成交資訊 | ok | N | 39 | Date, SecuritiesCompanyCode, CompanyName, Closi... |
| `/tpex_cmode` | 上櫃股票變更交易、分盤交易、管理股票與停止交易資訊 | ok | N | 20 | Date, SecuritiesCompanyCode, CompanyName, Alter... |
| `/tpex_daily_broker1` | 上櫃各券商當日營業金額統計表 | ok | N | 895 | Date, Ranking, PreviousDayRanking, Code, Name |
| `/tpex_daily_market_value` | 上櫃歷史個股市值排行 | ok | N | 879 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |
| `/tpex_daily_qutoes_block` | 上櫃鉅額交易日成交資訊 | ok | N | 1 | Date, TransactionType, SettlementPeriod, Code, ... |
| `/tpex_daily_trade_block_day` | 鉅額交易歷史成交資訊 | ok | N | 250 | TradingDate, Name, NumberOfSharesTraded, Tradin... |
| `/tpex_daily_trading_block` | 上櫃個股單一證券鉅額交易日成交資訊 | ok | N | 250 | TradingDate, Name, NumberOfSharesTraded, Tradin... |
| `/tpex_daily_trading_index` | 上櫃日成交量值指數 | ok | N | 6 | Date, TradeVolume, TradeAmount, NumberOfTransac... |
| `/tpex_daily_trading_summary_odd` | 上櫃鉅額交易日成交量值統計 | ok | N | 20 | TradingDate, Type, NumberOfTransactions, Number... |
| `/tpex_daily_turnover` | 上櫃歷史個股週轉率排行 | ok | N | 879 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |
| `/tpex_delayed_stock_close` | 上櫃每日暫緩收盤股票 | ok | N | 6 | Date, SecuritiesCompanyCode, CompanyName |
| `/tpex_delayed_stock_open` | 上櫃每日暫緩開盤股票 | ok | N | 100 | Date, SecuritiesCompanyCode, CompanyName |
| `/tpex_disposal_information` | 上櫃處置有價證券資訊 | ok | N | 41 | Date, SecuritiesCompanyCode, CompanyName, Dispo... |
| `/tpex_esb_applicant_companies` | 申請上櫃公司 | ok | N | 788 | Date, SecuritiesCompanyCode, CompanyName, Chair... |
| `/tpex_exright_daily` | 上櫃股票除權除息計算結果表 | ok | N | 4 | Date, SecuritiesCompanyCode, CompanyName, Close... |
| `/tpex_exright_prepost` | 上櫃股票除權除息預告表 | ok | N | 100 | ExRrightsExDividendDate, SecuritiesCompanyCode,... |
| `/tpex_intraday_fee` | 上櫃應付現股當日沖銷券差借券費率 | ok | N | 157 | Date, SecuritiesCompanyCode, CompanyName,  Lend... |
| `/tpex_intraday_trading_his` | 上櫃暫停先賣後買當日沖銷交易歷史查詢 | ok | N | 137 | Date, SecuritiesCompanyCode, CompanyName, First... |
| `/tpex_intraday_trading_pre` | 上櫃暫停先賣後買當日沖銷交易標的預告表 | ok | N | 255 | Date, SecuritiesCompanyCode, CompanyName, First... |
| `/tpex_intraday_trading_statistics` | 上櫃股票現股當沖交易統計資訊 | ok | N | 5 | Date, DayTradingVolume, DayTradingVolumeOfTheMa... |
| `/tpex_ipo_no_limit` | 上櫃首五日無漲跌幅資訊 | ok | N | 1 | Date, SecuritiesCompanyCode, CompanyName, Start... |
| `/tpex_mainboard_daily_close_quotes` | 上櫃股票行情 | ok | N | 10711 | Date, SecuritiesCompanyCode, CompanyName, Close... |
| `/tpex_mainboard_margin_balance` | 上櫃股票融資融券餘額 | ok | N | 892 | Date, SecuritiesCompanyCode, CompanyName, Margi... |
| `/tpex_mainboard_peratio_analysis` | 上櫃股票個股本益比、殖利率、股價淨值比 | ok | N | 878 | Date, SecuritiesCompanyCode, CompanyName, Price... |
| `/tpex_mainboard_quotes` | 上櫃股票收盤行情 | ok | N | 998 | Date, SecuritiesCompanyCode, CompanyName, Close... |
| `/tpex_mainborad_highlight` | 上櫃股票市場現況 | ok | N | 1 | Date, ListedCompanyNumbers, AuthorizedCapital, ... |
| `/tpex_margin_sbl` | 上櫃股票融券借券賣出餘額 | ok | N | 909 | Date, SecuritiesCompanyCode, CompanyName, SaleB... |
| `/tpex_margin_trading_adjust` | 上櫃融資融券調整成數 | ok | N | 242 | Date, SecuritiesCompanyCode, CompanyName, Reduc... |
| `/tpex_margin_trading_lend` | 上櫃融資融券標借 | ok | N | 2 | Date, DateOfTheCompetitiveDids, SecuritiesCompa... |
| `/tpex_margin_trading_margin_mark` | 上櫃平盤下得融(借)券賣出之證券名單 | ok | N | 809 | Date, SecuritiesCompanyCode, CompanyName, Banne... |
| `/tpex_margin_trading_margin_used` | 上櫃融資融券使用率報表 | ok | N | 20 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |
| `/tpex_margin_trading_marginspot` | 上櫃信用交易餘額概況表 | ok | N | 35 | Month, Ranking, SecuritiesCompanyCode, CompanyN... |
| `/tpex_margin_trading_short_sell` | 上櫃融資融券增減排行表 | ok | N | 20 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |
| `/tpex_margin_trading_term` | 上櫃融資融券暫停融券賣出預告表 | ok | N | 317 | Date, SecuritiesCompanyCode, CompanyName, Short... |
| `/tpex_monthly_trading_summary_block` | 上櫃鉅額交易月成交量值統計 | ok | N | 16 | Month, Type, NumberOfTransactions, NumberOfShar... |
| `/tpex_odd_stock` | 上櫃股票零股交易資訊 | ok | N | 991 | Date, SecuritiesCompanyCode, CompanyName, Trade... |
| `/tpex_off_market` | 上櫃股票盤後定價行情 | ok | N | 10711 | Date, SecuritiesCompanyCode, CompanyName, BidTr... |
| `/tpex_pe_ratio_top10` | 上櫃歷史個股本益比排行 | ok | N | 878 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |
| `/tpex_prvol` | 上櫃股票等價系統成交分價表 | ok | N | 63 | Date, SecuritiesCompanyCode, CompanyNam, Tradin... |
| `/tpex_securities` | 上櫃股票現股當沖交易標的資訊 | ok | N | 816 | 資料日期, 證券代號, 證券名稱, 暫停現股賣出後現款買進當沖註記 |
| `/tpex_short_sell` | 上櫃當日融券賣出與借券賣出成交量值 | ok | N | 990 | Date, SecuritiesCompanyCode, CompanyName, Short... |
| `/tpex_spendi_history` | 上櫃歷史公布暫停/恢復交易股票 | ok | N | 26 | Date, Serial, SecuritiesCompanyCode, CompanyNam... |
| `/tpex_spendi_today` | 上櫃當日公布暫停/恢復交易股票 | ok | N | 1 | Date, SecuritiesCompanyCode, CompanyName, 暫停交易,... |
| `/tpex_trading_amount_avg` | 上櫃歷史個股日均值排行 | ok | N | 866 | Date, Rank, StockCode, StockName, AverageDailyT... |
| `/tpex_trading_volume_ratio` | 上櫃歷史類股成交價量比重 | ok | N | 28 | Date, Sector, TradeAmount, TradeWeight,  Number... |
| `/tpex_trading_volumes_avg` | 上櫃歷史個股日均量排行 | ok | N | 866 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |
| `/tpex_trading_warning_information` | 上櫃公布注意股票資訊 | ok | N | 31 | Date, SecuritiesCompanyCode, CompanyName, Tradi... |
| `/tpex_trading_warning_note` | 上櫃公布注意累計次數異常資訊 | ok | N | 1 | Date, SecuritiesCompanyCode, CompanyName, Accum... |
| `/tpex_volume_rank` | 上櫃歷史個股成交量排行 | ok | N | 879 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |
| `/tpex_yearly_trading_summary_block` | 上櫃鉅額交易年成交量值統計 | ok | N | 4 | Year, Type, NumberOfTransactions, NumberOfShare... |

#### 債券

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/BDdos209UTF` | 美元零息可贖回國際債券理論價格 | ok | N | 277 | 資料日期, 債券代碼, 債券簡稱, 發行人, 發行日 |
| `/BDdos215UTF` | 美元附息固定利率可贖回國際債券理論價格 | ok | N | 128 | 資料日期, 債券代碼, 債券簡稱, 發行人, 發行日 |
| `/BDdos216UTF` | 美元固定利率不可贖回國際債券理論價格 | ok | N | 27 | 資料日期, 債券代碼, 債券簡稱, 發行人, 發行日 |
| `/bond_ISSBD10_data` | 國際債券(寶島債券)-本國發行人及第一、二上市(櫃)公司之外國發行人發行資料下載 | ok | N | 181 | Date, IssuerCode, IssuerName, BondCode, BondType |
| `/bond_ISSBD11_data` | 國際債券(寶島債券)-外國發行人(在我國未公開發行股權商品者)發行資料下載 | ok | N | 1 | Date, IssuerCode, IssuerName, BondCode, BondName |
| `/bond_ISSBD1_data` | 公債發行資料下載 | ok | N | 191 | Date, IssuerCode, IssuerName, BondCode, BondType |
| `/bond_ISSBD2_data` | 外國金融債發行資料下載 | ok | N | 1 | Date, IssuerCode, IssuerName, BondCode, BondType |
| `/bond_ISSBD3_data` | 金融債發行資料下載 | ok | N | 431 | Date, IssuerCode, IssuerName, BondCode, BondType |
| `/bond_ISSBD4_data` | 普通債發行資料下載 | ok | N | 1867 | Date, IssuerCode, IssuerName, BondCode, BondType |
| `/bond_ISSBD5_data` | 轉(交)換債發行資料下載 | ok | N | 397 | Date, IssuerCode, IssuerName, BondCode, BondType |
| `/bond_ISSBD6_data` | 海外轉換債發行資料下載 | ok | N | 19 | Date, IssuerCode, IssuerName, BondCode, BondType |
| `/bond_ISSBD7_data` | 附認股權公司債發行資料下載 | ok | N | 1 | Date, IssuerCode, IssuerName, BondCode, BondType |
| `/bond_ISSBD8_data` | 海外附認股權公司債發行資料下載 | ok | N | 1 | Date, IssuerCode, IssuerName, BondCode, BondType |
| `/bond_ISSBD9_data` | 海外普通債發行資料下載 | ok | N | 1 | Date, IssuerCode, IssuerName, BondCode, BondType |
| `/bond_cb_daily` | 轉(交)換公司債買賣斷券商買賣日報表 | ok | N | 1 | Date, FinancialInstitutionsCode, FinancialInsti... |
| `/tpex_dpsp_monthly_CBmcs007` | 可轉債資產交換ASO及ASW銀行承作餘額 | ok | N | 17 | Date, FinancialInstitutionsCode, FinancialInsti... |
| `/tpex_international_bond_issue_investor` | 國際債券(一般投資人) | ok | N | 7 | Date, BondCode, ShortName, Issuer, IssuingDate |
| `/tpex_international_bond_issue_org` | 國際債券(僅售予專業投資人者) | ok | N | 940 | Date, BondCode, ShortName, Issuer, IssuingDate |
| `/tpex_international_bond_quotes` | 國際債券當日盤中報價行情表(含寶島債) | ok | N | 32 | Date, Time, BondCode, BondName, BidYieldPrice |
| `/tpex_international_bond_trade` | 國際債券當日盤中成交行情表(含寶島債) | ok | N | 1 | Date, Time, BondCode, BondName, LastField |

#### 公司治理

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mopsfin_t187ap02_O` | 上櫃公司持股逾 10% 大股東名單 | ok | N | 976 | Date, SecuritiesCompanyCode, CompanyName, 大股東名稱 |
| `/mopsfin_t187ap03_O` | 上櫃股票基本資料 | ok | N | 881 | Date, SecuritiesCompanyCode, CompanyName, Compa... |
| `/mopsfin_t187ap03_R` | 興櫃公司基本資料 | ok | N | 354 | Date, SecuritiesCompanyCode, CompanyName, Compa... |
| `/mopsfin_t187ap04_O` | 上櫃公司每日重大訊息 | ok | N | 82 | Date, 發言日期, 發言時間, SecuritiesCompanyCode, Compan... |
| `/mopsfin_t187ap05_O` | 上櫃公司每月營業收入彙總表 | ok | N | 879 | 出表日期, 資料年月, 公司代號, 公司名稱, 產業別 |
| `/mopsfin_t187ap05_OA` | 二十九大類股營收變化統計表 | ok | N | 879 | 出表日期, 資料年月, 公司代號, 公司名稱, 產業別 |
| `/mopsfin_t187ap05_OB` | 發行公司營收創新高一覽表(上櫃) | ok | N | 879 | 出表日期, 資料年月, 公司代號, 公司名稱, 產業別 |
| `/mopsfin_t187ap08_O` | 上櫃公司董事、監察人持股不足法定成數彙總表 | ok | N | 32 | 出表日期, 公司代號, 公司名稱, 已發行股份總額, 全體董事不包含獨立董事應持有股數 |
| `/mopsfin_t187ap09_O` | 上櫃公司董事、監察人質權設定占董事及監察人實際持有股數彙總表 | ok | N | 9 | Date, Percent, CompanyName |
| `/mopsfin_t187ap10_O` | 上櫃公司董事、監察人持股不足法定成數連續達3個月以上彙總表 | ok | N | 19 | 出表日期, 連續不足達3個月, 107/10-12連續不足達4個月, 107/09-12連續不... |
| `/mopsfin_t187ap11_O` | 上櫃公司董監事持股餘額明細資料 | ok | N | 17216 | 出表日期, 資料年月, 公司代號, 公司名稱, 職稱 |
| `/mopsfin_t187ap11_R` | 興櫃公司董監事持股餘額明細資料 | ok | N | 6829 | Date, 資料年月, SecuritiesCompanyCode, CompanyName, 職稱 |
| `/mopsfin_t187ap12_O` | 上櫃公司每日內部人持股轉讓事前申報表-持股轉讓日報表 | ok | N | 1 | Date, SecuritiesCompanyCode, CompanyName, 申請人身分... |
| `/mopsfin_t187ap13_O` | 上櫃公司每日內部人持股轉讓事前申報表-持股未轉讓日報表 | ok | N | 1 | Date, SecuritiesCompanyCode, CompanyName, 申請人身分... |
| `/mopsfin_t187ap14_O` | 上櫃公司各產業EPS統計資訊 | ok | N | 881 | Date, Year, 季別, SecuritiesCompanyCode, CompanyName |
| `/mopsfin_t187ap22_O` | 上櫃公司金管會證券期貨局裁罰案件專區 | ok | N | 7 | Date, 發函日期, SecuritiesCompanyCode, CompanyName,... |
| `/mopsfin_t187ap23_O` | 上櫃公司違反資訊申報、重大訊息及說明記者會規定專區 | ok | N | 6 | Date, 發函日期, SecuritiesCompanyCode, CompanyName,... |
| `/mopsfin_t187ap24_O` | 上櫃公司經營權及營業範圍異(變)動專區-經營權異動公司 | ok | N | 27 | Date, SecuritiesCompanyCode, CompanyName, 經營權異動... |
| `/mopsfin_t187ap25_O` | 上櫃公司經營權及營業範圍異(變)動專區-營業範圍重大變更公司 | ok | N | 1 | Date, 序號, 年度, 季別, SecuritiesCompanyCode |
| `/mopsfin_t187ap26_O` | 上櫃公司經營權及營業範圍異(變)動專區-經營權異動且營業範圍重大變更停止買賣公司 | empty | N | 0 |  |
| `/mopsfin_t187ap27_O` | 上櫃公司經營權及營業範圍異(變)動專區-經營權異動且營業範圍重大變更列為變更交易公司 | empty | N | 0 |  |
| `/mopsfin_t187ap29_A_O` | 上櫃公司董事酬金相關資訊 | ok | N | 846 | Date, 產業類別, SecuritiesCompanyCode, CompanyName,... |
| `/mopsfin_t187ap29_B_O` | 上櫃公司監察人酬金相關資訊 | ok | N | 10 | Date, 產業類別, SecuritiesCompanyCode, CompanyName,... |
| `/mopsfin_t187ap29_C_O` | 上櫃公司合併報表董事酬金相關資訊 | ok | N | 768 | Date, 產業類別, SecuritiesCompanyCode, CompanyName,... |
| `/mopsfin_t187ap29_D_O` | 上櫃公司合併報表監察人酬金相關資訊 | ok | N | 7 | Date, 產業類別, SecuritiesCompanyCode, CompanyName,... |
| `/mopsfin_t187ap30_O` | 上櫃公司獨立董監事兼任情形彙總表 | ok | N | 10350 | Date, 序號, SecuritiesCompanyCode, CompanyName, 職稱 |
| `/mopsfin_t187ap31_O` | 上櫃公司財務報告經監察人承認情形 | ok | N | 881 | Date, SecuritiesCompanyCode, CompanyName, 是否設置審... |
| `/mopsfin_t187ap32_O` | 上櫃公司公司治理之相關規程規則 | ok | N | 8787 | Date, SecuritiesCompanyCode, CompanyName, 公司治理之... |
| `/mopsfin_t187ap33_O` | 上櫃公司董事長是否兼任總經理 | ok | N | 881 | Date, SecuritiesCompanyCode, CompanyName, Chair... |
| `/mopsfin_t187ap34_O` | 上櫃公司採累積投票制、全額連記法、候選人提名制選任董監事及當選資料彙總表 | ok | N | 1907 | Date, SecuritiesCompanyCode, CompanyName, 股東常(臨... |
| `/mopsfin_t187ap35_O` | 上櫃公司股東行使提案權情形彙總表 | ok | N | 870 | Date, SecuritiesCompanyCode, CompanyName, 召開股東會... |
| `/mopsfin_t187ap39_O` | 上櫃股利分派情形-董事會通過 | ok | N | 2483 | 出表日期, 公司代號, 公司名稱, 股利年度, 期別 |
| `/t187ap05_R` | 興櫃公司每月營業收入彙總表 | ok | N | 360 | 出表日期, 資料年月, 公司代號, 公司名稱, 產業別 |
| `/t187ap41_O` | 上櫃公司召開股東常 (臨時) 會日期、地點及採用電子投票情形等資料彙總表 | ok | N | 887 | 出表日期, 公司代號, 公司名稱, 公司地址, 股東常(臨時)會 |
| `/t187ap46_O_1` | 上櫃公司企業ESG資訊揭露彙總資料-溫室氣體排放 | empty | N | 0 |  |
| `/t187ap46_O_12` | 上櫃公司企業ESG資訊揭露彙總資料-食品安全 | empty | N | 0 |  |
| `/t187ap46_O_13` | 上櫃公司企業ESG資訊揭露彙總資料-供應鏈管理  | empty | N | 0 |  |
| `/t187ap46_O_14` | 上櫃公司企業ESG資訊揭露彙總資料-產品品質與安全 | empty | N | 0 |  |
| `/t187ap46_O_15` | 上櫃公司企業ESG資訊揭露彙總資料-社區關係  | empty | N | 0 |  |
| `/t187ap46_O_19` | 上櫃公司企業ESG資訊揭露彙總資料-風險管理政策  | empty | N | 0 |  |
| `/t187ap46_O_2` | 上櫃公司企業ESG資訊揭露彙總資料-能源管理 | empty | N | 0 |  |
| `/t187ap46_O_20` | 上櫃公司企業ESG資訊揭露彙總資料-反競爭行為法律訴訟  | empty | N | 0 |  |
| `/t187ap46_O_21` | 上櫃公司企業ESG資訊揭露彙總資料-職業安全衛生 | empty | N | 0 |  |
| `/t187ap46_O_3` | 上櫃公司企業ESG資訊揭露彙總資料-水資源管理 | empty | N | 0 |  |
| `/t187ap46_O_4` | 上櫃公司企業ESG資訊揭露彙總資料-廢棄物管理 | empty | N | 0 |  |
| `/t187ap46_O_5` | 上櫃公司企業ESG資訊揭露彙總資料-人力發展 | empty | N | 0 |  |
| `/t187ap46_O_6` | 上櫃公司企業ESG資訊揭露彙總資料-董事會 | empty | N | 0 |  |
| `/t187ap46_O_7` | 上櫃公司企業ESG資訊揭露彙總資料-投資人溝通 | empty | N | 0 |  |
| `/t187ap46_O_8` | 上櫃公司企業ESG資訊揭露彙總資料-氣候相關議題管理 | empty | N | 0 |  |
| `/t187ap46_O_9` | 上櫃公司企業ESG資訊揭露彙總資料-功能性委員會 | empty | N | 0 |  |
| `/tpex_esb_capitals_rank` | 興櫃公司資本額排名 | ok | N | 345 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |
| `/tpex_esb_eps_rank` | 本國興櫃公司EPS排名 | ok | N | 345 | Date, Rank, SecuritiesCompanyCode, CompanyName,... |

#### 券商資料

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mopsfin_t187ap01` | 券商業務別人員數 | ok | N | 4 | 出表日期, 職位, 受託買賣, 受託買賣（衍生性商品銷售）, 內部稽核 |
| `/tpex_daily_broker2` | 上櫃股票各券商總公司當日營業金額統計表 | ok | N | 63 | Date, Ranking, PreviousDayRanking, FinancialIns... |

#### 創櫃

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/tpex_gisa_company` | 創櫃板公司資訊 | ok | N | 135 | Date, SecuritiesCompanyCode, CompanyName, Industry |
| `/tpex_gisa_financing_before` | 於登錄創櫃板前辦理籌資資訊 | ok | N | 260 | Date, SecuritiesCompanyCode, CompanyName, 現金增資期... |
| `/tpex_gisa_financing_history` | 創櫃板公司透過籌資系統辦理籌資資訊 | ok | N | 3 | Date, SecuritiesCompanyCode, CompanyName, 現金增資期... |
| `/tpex_gisa_financing_in_process` | 創櫃板辦理中籌資資訊 | ok | N | 1 | Date, SecuritiesCompanyCode, CompanyName, 現金增資期... |
| `/tpex_gisa_highlight` | 創櫃板公司市場現況 | ok | N | 1 | Date, CumulativeNumberOfCompaniesApplyingForGIS... |

#### 指數系列

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/tpcgi_change` | 上櫃公司治理指數當日收盤指數 | ok | N | 2 | Date, Name, Index, Change |
| `/tpcgi_constituents` | 上櫃公司治理指數當日成分股資訊 | ok | N | 60 | Date, SecuritiesCompanyCode, CompanyName |
| `/tpcgi_reward_index` | 上櫃公司治理指數歷史收盤指數 | ok | N | 6 | Date, TPExCorporateGovernanceIndex, TPExCorpora... |
| `/tpci_change` | 櫃買「薪酬指數」當日收盤指數 | ok | N | 2 | Date, Name, Index, Change |
| `/tpci_constituents` | 櫃買「薪酬指數」當日成分股 | ok | N | 88 | Date, SecuritiesCompanyCode, CompanyName |
| `/tpci_reward_index` | 櫃買「薪酬指數」歷史收盤指數 | ok | N | 6 | Date, GTSMCompensationIndex, GTSMCompensationTo... |
| `/tpex200_change` | 櫃買「富櫃200指數」當日收盤指數 | ok | N | 2 | 資料日期, 指數, 收盤指數, 漲跌, 漲跌點數 |
| `/tpex200_constituents` | 櫃買「富櫃200指數」當日成分股 | ok | N | 200 | 資料日期, 股票代號, 股票名稱 |
| `/tpex50_change` | 櫃買「富櫃50指數」當日收盤指數 | ok | N | 2 | Date, Name, Index, Change |
| `/tpex50_constituents` | 櫃買「富櫃50指數」當日成分股 | ok | N | 50 | Date, SecuritiesCompanyCode, CompanyName |
| `/tpex50_index` | 富櫃50指數歷史收盤指數 | ok | N | 6 | Date, TPEx50Index, TPEx50TotalReturnIndex |
| `/tpex_emp88_change` | 櫃買「勞工就業88指數」當日收盤指數 | ok | N | 2 | Date, Name, Index, Change |
| `/tpex_emp88_constituents` | 櫃買「勞工就業88指數」當日成分股 | ok | N | 88 | Date, SecuritiesCompanyCode, CompanyName |
| `/tpex_emp88_reward_index` | 櫃買「勞工就業88指數」歷史收盤指數 | ok | N | 6 | Date, GretaiLaborEmployment88Index, GretaiLabor... |
| `/tpex_index` | 櫃買指數歷史資料 | ok | N | 6 | Date, Open, High, Low, Close |
| `/tpex_index_consti` | 櫃買指數成分股 | ok | N | 881 | Date, SecuritiesCompanyCode, CompanyName, Capit... |
| `/tpex_reward_index` | 櫃買指數與報酬指數之收市指數 | ok | N | 6 | Date, TPExIndex, TPExTotalReturnIndex |
| `/tphd_change` | 櫃買「高殖利率指數」當日收盤指數 | ok | N | 2 | Date, Name, Index, Change |
| `/tphd_constituents` | 櫃買「高殖利率指數」當日成分股 | ok | N | 60 | Date, SecuritiesCompanyCode, CompanyName |
| `/tphd_index` | 高殖利率指數歷史收盤指數 | ok | N | 6 | Date, TPExHighDividendYieldIndex, TPExHighDivid... |

#### 權證

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mopsfin_t187ap36_O` | 上櫃認購(售)權證年度發行量概況統計表 | ok | N | 17351 | Date, 發行人代號, 發行人名稱, 權證代號, 名稱 |
| `/mopsfin_t187ap37_O` | 上櫃權證基本資料彙總表 | ok | N | 13709 | 出表日期, 權證代號, 權證簡稱, 權證類型, 類別 |
| `/mopsfin_t187ap42_O` | 上櫃認購(售)權證每日成交資料檔 | ok | N | 9836 | Date, 交易日期, 權證代號, 權證名稱, 成交金額 |
| `/tpex_warrant` | 上櫃股票權證資訊 | ok | N | 9931 | Date, Item, Code, Name, UnderlyingCode |
| `/tpex_warrant_daily_quts` | 上櫃權證收盤行情日報表 | ok | N | 9836 | Date, Code, Name, Open, High |
| `/tpex_warrant_gold` | 黃金現貨權證發行基本資料 | ok | N | 2 | Date, Code, Name, ListedDate, ExpiryDate |
| `/tpex_warrant_gold_quts` | 黃金現貨權證收盤行情 | ok | N | 1 | Date, Code, Name, Open, High |
| `/tpex_warrant_issue` | 上櫃權證發行基本資料 | ok | N | 9847 | Date, Code, Name, ListedDate, ExpiryDate |
| `/tpex_warrant_monthly_quts` | 上櫃權證收盤行情月報表 | ok | N | 10364 | Date, Code, Name, Open, High |
| `/tpex_warrant_quts` | 單筆權證成交資料 | ok | N | 9836 | Date, Code, Name, Open, High |
| `/tpex_warrant_statistics` | 每日權證交易人數(上櫃) | ok | N | 8 | Date, Category, Statistics |
| `/tpex_warrant_suspend_history` | 上櫃權證歷史暫停/恢復交易資訊 | ok | N | 12 | Year, No., Date, WarrantCode, WarrantName |
| `/tpex_warrant_suspend_today` | 上櫃權證當日暫停/恢復交易資訊 | ok | N | 5 | Date, WarrantCode, WarrantName, SecuritiesCompa... |
| `/tpex_warrant_wcb_daily_quts` | 上櫃牛熊證收盤行情(不含展延型牛熊證)日報表 | ok | N | 1 | Date, Code, Name, Open, High |
| `/tpex_warrant_wcb_issue` | 上櫃牛熊證發行基本資料(不含展延型牛熊證) | ok | N | 1 | Date, Code, Name, ListedDate, ExpiryDate |
| `/tpex_warrant_wcb_monthly_quts` | 上櫃牛熊證收盤行情(不含展延型牛熊證)月報表 | ok | N | 1 | Date, Code, Name, Open, High |
| `/tpex_warrant_wxy_daily_quts` | 上櫃展延型牛熊證收盤行情日報表 | ok | N | 1 | Date, Code, Name, Open, High |
| `/tpex_warrant_wxy_issue` | 上櫃展延型牛熊證發行基本資料 | ok | N | 1 | Date, Code, Name, ListedDate, ExpiryDate |
| `/tpex_warrant_wxy_monthly_quts` | 上櫃展延型牛熊證收盤行情月報表 | ok | N | 1 | Date, Code, Name, Open, High |

#### 興櫃

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/tpex_esb_disposal_information` | 興櫃處置有價證券資訊 | ok | N | 2 | 公布日期, 證券代號, 證券名稱, 處置起訖時間, 處置原因 |
| `/tpex_esb_highlight` | 興櫃股票市場現況 | ok | N | 1 | Date, RegisteredStocksNumber, TotalPaidinCapita... |
| `/tpex_esb_latest_statistics` | 興櫃股票當日行情表 | ok | N | 352 | Date, Time, SecuritiesCompanyCode, CompanyName,... |
| `/tpex_esb_recommended_dealer` | 興櫃推薦證券商與推薦之股票 | ok | N | 1137 | Date, SecuritiesCompanyCode, CompanyName, Recom... |
| `/tpex_esb_warning_information` | 興櫃公布注意有價證券資訊 | ok | N | 1 | 公告日期, 證券代號, 證券名稱, 注意交易資訊, 收盤價 |

#### 財務報表

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mopsfin_187ap17_O` | 上櫃公司營益分析查詢彙總表(全體公司彙總報表) | ok | N | 874 | Date, Year, 季別, SecuritiesCompanyCode, CompanyName |
| `/mopsfin_t187ap06_O_basi` | 上櫃公司綜合損益表(金融業) | ok | N | 1 | Date, Year, Season, SecuritiesCompanyCode, Comp... |
| `/mopsfin_t187ap06_O_basiA` | 上櫃公司財報資訊(金融業) | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap06_O_bd` | 上櫃公司綜合損益表(證券期貨業) | ok | N | 7 | Date, 年度, 季別, 公司代號, CompanyName |
| `/mopsfin_t187ap06_O_bdA` | 上櫃公司財報資訊(證券期貨業) | ok | N | 7 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap06_O_ci` | 上櫃公司綜合損益表(一般業) | ok | N | 874 | Date, Year, Season, SecuritiesCompanyCode, Comp... |
| `/mopsfin_t187ap06_O_ciA` | 上櫃公司財報資訊( 一般業) | ok | N | 874 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap06_O_fh` | 上櫃公司綜合損益表(金控業) | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap06_O_fhA` | 上櫃公司財報資訊(金控業) | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap06_O_ins` | 上櫃公司綜合損益表(保險業) | ok | N | 1 | Date, Year, Season, SecuritiesCompanyCode, Comp... |
| `/mopsfin_t187ap06_O_insA` | 上櫃公司財報資訊(保險業) | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap06_O_mim` | 上櫃公司綜合損益表(異業) | ok | N | 1 | Date, Year, Season, SecuritiesCompanyCode, Comp... |
| `/mopsfin_t187ap06_O_mimA` | 上櫃公司財報資訊(異業) | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap06_U_basi` | 興櫃公司綜合損益表-金融業 | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap06_U_bd` | 興櫃公司綜合損益表-證券期貨業 | ok | N | 1 | Date, 年度, 季別, SecuritiesCompanyCode, CompanyName |
| `/mopsfin_t187ap06_U_ci` | 興櫃公司綜合損益表-一般業 | ok | N | 145 | Date, 年度, 季別, SecuritiesCompanyCode, CompanyName |
| `/mopsfin_t187ap06_U_fh` | 興櫃公司綜合損益表-金控業 | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap06_U_ins` | 興櫃公司綜合損益表-保險業 | ok | N | 1 | Date, 年度, 季別, SecuritiesCompanyCode, CompanyName |
| `/mopsfin_t187ap06_U_mim` | 興櫃公司綜合損益表-異業 | ok | N | 1 | Date, 年度, 季別, SecuritiesCompanyCode, CompanyName |
| `/mopsfin_t187ap07_O_basi` | 上櫃公司資產負債表(金融業) | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap07_O_bd` | 上櫃公司資產負債表(證券期貨業) | ok | N | 7 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap07_O_ci` | 上櫃公司資產負債表(一般業) | ok | N | 874 | Date, 年度, 季別, SecuritiesCompanyCode, CompanyName |
| `/mopsfin_t187ap07_O_fh` | 上櫃公司資產負債表(金控業) | ok | N | 1 | Date, Year, Season, SecuritiesCompanyCode, Comp... |
| `/mopsfin_t187ap07_O_ins` | 上櫃公司資產負債表(保險業) | ok | N | 1 | Date, Year, Season, SecuritiesCompanyCode, Comp... |
| `/mopsfin_t187ap07_O_mim` | 上櫃公司資產負債表(異業) | ok | N | 1 | Date, Year, Season, SecuritiesCompanyCode, Comp... |
| `/mopsfin_t187ap07_U_basi` | 興櫃公司資產負債表-金融業 | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap07_U_bd` | 興櫃公司資產負債表-證券期貨業 | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap07_U_ci` | 興櫃公司資產負債表-一般業 | ok | N | 145 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap07_U_fh` | 興櫃公司資產負債表-金控業 | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap07_U_ins` | 興櫃公司資產負債表-保險業 | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap07_U_mim` | 興櫃公司資產負債表-異業 | ok | N | 1 | 出表日期, 年度, 季別, 公司代號, 公司名稱 |
| `/mopsfin_t187ap15_O` | 上櫃公司截至各季綜合損益財測達成情形(簡式) | ok | N | 1 | Date, Year, 季別, SecuritiesCompanyCode, CompanyName |
| `/mopsfin_t187ap16_O` | 上櫃公司當季綜合損益經會計師查核(核閱)數與當季預測數差異達百分之十以上者，或截至當季累計差異達百分之二十以上者(簡式) | ok | N | 1 | Date, Year, 季別, SecuritiesCompanyCode, CompanyName |

#### 開放式基金

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/tpex_opfund_latest` | 開放式基金當日行情表 | ok | N | 3 | Date, Time, SecurityCode, ListedOpenEndedFund, ... |
| `/tpex_opfund_market_highlight` | 開放式基金市場現況 | ok | N | 1 | Date, NumberOfFunds, TotalTradingAmount, TotalT... |
| `/tpex_opfund_recommended_dealer` | 開放式基金受益憑證造市商與造市之基金 | ok | N | 3 | Date, SecurityCode, SecurityName, No., MarketMa... |

#### 黃金現貨

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/tpex_gold_latest` | 黃金現貨當日行情表 | ok | N | 2 | Date, Time, GoldCode, GoldShortName, QuotedBuyi... |
| `/tpex_gold_market_highlight` | 黃金現貨市場現況 | ok | N | 1 | Date, NumberOfRegisteredGold, TotalTradingAmoun... |
| `/tpex_gold_recommended_dealer` | 造市商與造市之黃金現貨 | ok | N | 2 | Date, GoldCode, GoldName, No., MarketMakerCode |

### Web (194 endpoints)

#### 上櫃公司

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/zh-tw/mainboard/listed/company.html` | 上櫃公司查詢 | ok | Y | 8 | 股票代號, 公司名稱, 最近一季每股淨值(元), 產業類別 |
| `/zh-tw/mainboard/listed/delisted.html` | 終止上櫃公司 | ok | Y | 6 | 股票代號, 公司名稱, 終止上櫃日期, 終止上櫃原因, 公司資料網址 |
| `...tw/mainboard/listed/financial/rank-capital.html` | 上櫃資本額排名 | ok | Y | 851 | 排名, 公司代號, 公司名稱, 資本額(百萬), 公司代號網址 |
| `/zh-tw/mainboard/listed/financial/rank-pe.html` | 上櫃EPS排名 | ok | Y | 851 | 排名, 公司代號, 公司名稱, EPS, 公司代號網址 |
| `...tw/mainboard/listed/financial/rank-revenue.html` | 上櫃營收額排名 | ok | Y | 40 | 排行, 股票代號, 公司名稱, 本月營收(仟元), 上月營收(仟元) |
| `/zh-tw/mainboard/listed/financial/summary.html` | 上櫃公司季報 | ok | Y | 5 | 資料日期, XLS下載, ODS下載 |
| `/zh-tw/mainboard/listed/flexible-face-value.html` | 採彈性面額之上(興)櫃公司資訊 | error | N | 0 |  |
| `/zh-tw/mainboard/listed/latest.html` | 近期上櫃公司 | ok | Y | 42 | 索引, 股票代號, 公司名稱, 上櫃日期, 每股面額 |
| `/zh-tw/mainboard/listed/month/fundamentals.html` | 獲利及股利分派情形 | ok | Y | 12 | 資料月份, XLS檔案下載, ODS檔案下載 |
| `/zh-tw/mainboard/listed/month/funding.html` | 櫃買市場募集資金相關資訊 | ok | Y | 24 | 日期, 下載, 下載ODS |
| `/zh-tw/mainboard/listed/month/revenue.html` | 營業額及背書保證金額彙總表 | ok | Y | 24 | 資料日期, XLS下載, ODS下載 |

#### 交易資訊

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/zh-tw/mainboard/trading/block-trading/day.html` | 鉅額交易日成交量值統計 | ok | Y | 28 | 成交日期, 類別, 成交筆數, 成交股數, 成交股數占全市場比重(%) |
| `/zh-tw/mainboard/trading/block-trading/month.html` | 鉅額交易月成交量值統計 | ok | Y | 16 | 成交月份, 類別, 成交筆數, 成交股數, 成交股數占全市場比重(%) |
| `...tw/mainboard/trading/block-trading/pricing.html` | 鉅額交易日成交資訊 | ok | Y | 3 | 交易型態, 交割期別, 代號, 名稱, 成交價格(元) |
| `...nboard/trading/block-trading/stock-pricing.html` | 個股單一證券鉅額交易日成交資訊 | ok | Y | 254 | 證券代號, 名 稱, 成交日期, 成交股數, 成交金額 |
| `/zh-tw/mainboard/trading/block-trading/year.html` | 鉅額交易年成交量值統計 | ok | Y | 4 | 成交年度, 類別, 成交筆數, 成交股數, 成交股數占全市場比重(%) |
| `/zh-tw/mainboard/trading/day-trading/fee.html` | 應付現股當日沖銷券差借券費率 | ok | Y | 229 | 券差日期, 證券代號, 證券名稱, 借券股數 (股), 借券費率 (%) |
| `/zh-tw/mainboard/trading/day-trading/rules.html` | 制度介紹 | error | N | 0 |  |
| `...w/mainboard/trading/day-trading/securities.html` | 現股當沖交易標的 | ok | Y | 817 | 證券代號, 證券名稱, 暫停現股賣出後現款買進當沖註記 |
| `...inboard/trading/day-trading/statistics/day.html` | 現股當沖交易統計資訊 | error | N | 0 |  |
| `...oard/trading/day-trading/suspended-annouce.html` | 暫停先賣後買當日沖銷交易標的預告表 | empty | Y | 0 | 股票代號, 股票名稱, 停止先賣後買開始日, 恢復先賣後買日, 原因 |
| `...d/trading/day-trading/suspended-historical.html` | 暫停先賣後買當日沖銷交易歷史查詢 | ok | Y | 122 | 股票代號, 股票名稱, 停止先賣後買開始日, 停止先賣後買結束日, 原因 |
| `...w/mainboard/trading/historical/advance/day.html` | 個股漲幅排行 | error | N | 0 |  |
| `...ainboard/trading/historical/avg-amount/day.html` | 個股日均值排行 | error | N | 0 |  |
| `...ainboard/trading/historical/avg-volume/day.html` | 個股日均量排行 | ok | Y | 869 | 排 行,  股票代號,  股票名稱,  日均張數 |
| `...tw/mainboard/trading/historical/broker-amt.html` | 熱門股證券商進出排行(依成交金額) | ok | Y | 449 | 排行 - 股票名稱(代號), 排行, 證商名稱, 買進金額(仟元), 賣出金額(仟元) |
| `...tw/mainboard/trading/historical/broker-vol.html` | 熱門股證券商進出排行 (依成交量) | ok | Y | 450 | 排行 - 股票名稱(代號), 排行, 證商名稱, 總買量(張), 總賣量(張) |
| `...w/mainboard/trading/historical/decline/day.html` | 個股跌幅排行 | error | N | 0 |  |
| `.../mainboard/trading/historical/market-value.html` | 個股市值排行 | ok | Y | 881 | 排名, 股票代號, 股票名稱, 發行股數, 收盤價 |
| `/zh-tw/mainboard/trading/historical/pe.html` | 個股本益比排行 | ok | Y | 880 | 排名, 股票代號, 股票名稱, 收盤價(元), 每股盈餘(元) |
| `...inboard/trading/historical/rank-amount/day.html` | 個股成交值排行 | error | N | 0 |  |
| `...inboard/trading/historical/rank-volume/day.html` | 個股成交量排行 | error | N | 0 |  |
| `...oard/trading/historical/turnover-ratio/day.html` | 個股週轉率排行 | error | N | 0 |  |
| `/zh-tw/mainboard/trading/historical/weekly.html` | 證券行情週報表 | ok | Y | 11408 | 代號, 名稱, 參考價, 漲停, 跌停 |
| `/zh-tw/mainboard/trading/historical/weights.html` | 類股成交價量比重 | ok | Y | 28 | 類股名稱,  成交金額(元),  成交比重(%),   成交股數,  成交比重(%) |
| `/zh-tw/mainboard/trading/info/altered.html` | 變更交易、分盤交易、管理股票與停止交易資訊 | ok | Y | 18 | 證券代號, 證券名稱, 變更交易, 分盤交易, 屬管理股票 |
| `/zh-tw/mainboard/trading/info/daily-indices.html` | 日成交量值指數 | ok | Y | 7 | 日期, 成交張數, 金額（仟元）, 筆數, 櫃買指數 |
| `/zh-tw/mainboard/trading/info/daily-pe.html` | 個股本益比、殖利率及股價淨值比(依日期查詢) | ok | Y | 880 | 股票代號, 公司名稱, 本益比, 每股股利, 股利年度 |
| `/zh-tw/mainboard/trading/info/highlight.html` | 上櫃股票市場現況 | ok | Y | 1 | 上櫃家數, 總資本額(佰萬元), 總市值(佰萬元), 本日總成交值(佰萬元), 本日總成交股數... |
| `/zh-tw/mainboard/trading/info/indices-pricing.html` | 上櫃股價指數收盤行情 | ok | Y | 75 | 指數, 收市指數, 漲跌, 漲跌幅度(%), 大盤資訊連結 |
| `/zh-tw/mainboard/trading/info/mi-pricing.html` | 每日收盤行情(不含定價) | empty | Y | 0 | 代號, 名稱, 收盤 , 漲跌, 開盤  |
| `/zh-tw/mainboard/trading/info/no-limit.html` | 首五日無漲跌幅資訊 | empty | Y | 0 | 代號, 名稱, 穩定操作起始日, 穩定操作截止日, 承銷價格(元) |
| `...oard/trading/info/odd-lot/post-pricing/day.html` | 盤後零股每日收盤行情 | error | N | 0 |  |
| `/zh-tw/mainboard/trading/info/odd-lot/pricing.html` | 盤中零股每日收盤行情 | ok | Y | 948 | 代號, 名稱, 最後成交價, 漲跌, 首筆成交價 |
| `...nboard/trading/info/odd-lot/statistics/day.html` | 零股交易成交統計 | error | N | 0 |  |
| `/zh-tw/mainboard/trading/info/post.html` | 盤後定價行情 | ok | Y | 10675 | 代號, 名稱, 委買筆數, 委買張數, 委賣筆數 |
| `/zh-tw/mainboard/trading/info/pricing.html` | 上櫃股票行情 | ok | Y | 10675 | 代號, 名稱, 收盤, 漲跌, 開盤 |
| `/zh-tw/mainboard/trading/info/sec-summary.html` | 各券商總公司當日營業金額統計表 | ok | Y | 63 | 排名, 前日排名, 券商, 名稱, 家數 |
| `/zh-tw/mainboard/trading/info/sec-trading.html` | 各券商當日營業金額統計表 | ok | Y | 895 | 排名,  前日排名, 券商, 名稱, 成交金額(仟元) |
| `/zh-tw/mainboard/trading/info/short.html` | 當日融券賣出與借券賣出成交量值 | ok | Y | 992 | 代號, 名稱, 融券賣出成交張數, 融券賣出成交金額(元), 借券賣出成交張數 |
| `/zh-tw/mainboard/trading/info/statistics/day.html` | 上櫃證券成交統計 | error | N | 0 |  |
| `/zh-tw/mainboard/trading/info/stock-month.html` | 個股月成交資訊 | empty | Y | 0 | 年, 月, 收市最高價, 收市最低價, 收市平均價 |
| `/zh-tw/mainboard/trading/info/stock-pe.html` | 個股本益比、殖利率及股價淨值比(依代碼查詢) | ok | Y | 1 | 日期, 本益比, 殖利率(%), 股利年度, 股價淨值比 |
| `/zh-tw/mainboard/trading/info/stock-pricing.html` | 個股日成交資訊 | empty | Y | 0 | 日 期, 成交張數, 成交仟元, 開盤, 最高 |
| `/zh-tw/mainboard/trading/info/stock-year.html` | 個股年成交資訊 | empty | Y | 0 | 年度, 成交張數(A), 金額(仟元)(B), 筆數(仟), 加權平均價(B/A) |
| `/zh-tw/mainboard/trading/info/volume-profile.html` | 等價系統成交分價表 | ok | Y | 58 | 股票代號,   名稱 ,  成交價 , 價格註記,   成交張數 |
| `...ard/trading/major-institutional/dealer/day.html` | 自營商買賣超彙總表 | error | N | 0 |  |
| `...ard/trading/major-institutional/detail/day.html` | 三大法人買賣明細資訊 | error | N | 0 |  |
| `...ding/major-institutional/domestic-inst/day.html` | 投信買賣超彙總表 | error | N | 0 |  |
| `...rd/trading/major-institutional/foreign/day.html` | 外資及陸資買賣超彙總表 | error | N | 0 |  |
| `...rd/trading/major-institutional/sector-ocfi.html` | 各類股僑外資及陸資持股比例表 | ok | Y | 28 | 類股, 家數, 總發行股數(A), 僑外資及陸資持有總股數(B), 僑外資及陸資持股比率(%)... |
| `...ard/trading/major-institutional/stock-ocfi.html` | 僑外資及陸資持股比例排行表 | ok | Y | 882 | 排行, 代號, 名稱, 發行股數(A), 僑外資及陸資尚可投資股數B=A*F-C |
| `...rd/trading/major-institutional/summary/day.html` | 三大法人買賣金額彙總表 | ok | Y | 8 | 單位名稱, 買進金額(元), 賣出金額(元), 買賣超(元) |
| `...mainboard/trading/margin-trading/adjusting.html` | 調整成數 | ok | Y | 247 | 證券代號, 證券名稱, 降成日, 恢復日, 連續五日 |
| `.../mainboard/trading/margin-trading/announce.html` | 信用交易公告 | empty | Y | 0 | 公告日期, 股票代號 |
| `...mainboard/trading/margin-trading/borrowing.html` | 標借 | ok | Y | 2 | 標借日期, 股票代號, 股票名稱, 證金公司, 標借張數 |
| `.../mainboard/trading/margin-trading/exempted.html` | 平盤下得融(借)券賣出之證券名單 | ok | Y | 812 | 證券代號, 證券名稱, 暫停融券賣出, 暫停借券賣出, 前一交易日收盤價跌停本日禁止平盤下融(... |
| `...mainboard/trading/margin-trading/highlight.html` | 信用交易餘額概況表 | ok | Y | 35 | 排名, 代號, 名稱, 月均融資餘額(元), 市場佔有率 |
| `.../mainboard/trading/margin-trading/rank/day.html` | 融資融券增減排行表 | error | N | 0 |  |
| `/zh-tw/mainboard/trading/margin-trading/sbl.html` | 融券借券賣出餘額 | ok | Y | 910 | 股票代號, 股票名稱, 前日餘額, 賣出, 買進 |
| `...ainboard/trading/margin-trading/suspension.html` | 暫停融券賣出預告表 | ok | Y | 322 | 證券代號, 證券名稱, 停券起日(最後回補日), 停券迄日, 原因 |
| `...nboard/trading/margin-trading/transactions.html` | 融資融券餘額表 | ok | Y | 893 | 代號, 名稱, 前資餘額(張), 資買, 資賣 |
| `...mainboard/trading/margin-trading/usage/day.html` | 融資融券使用率報表 | error | N | 0 |  |
| `/zh-tw/mainboard/trading/realtime/advance.html` | 個股漲幅排行 | ok | Y | 30 | 代號, 名稱, 收盤價(元), 上漲金額(元), 漲幅百分比(%) |
| `/zh-tw/mainboard/trading/realtime/amount.html` | 個股成交金額排行 | ok | Y | 30 | 代號, 名稱, 成交張數, 成交值(仟元) |
| `/zh-tw/mainboard/trading/realtime/broker-amt.html` | 熱門股證券商進出排行(依成交金額) | ok | Y | 300 | 排行 - 股票名稱(代號), 排行, 證券商名稱, 買進金額(仟元), 賣出金額(仟元) |
| `/zh-tw/mainboard/trading/realtime/broker-vol.html` | 熱門股證券商進出排行(依成交量) | ok | Y | 300 | 排行 - 股票名稱(代號), 排行, 證券商名稱, 總買量(張), 總賣量(張) |
| `/zh-tw/mainboard/trading/realtime/decline.html` | 個股跌幅排行 | ok | Y | 30 | 代號, 名稱, 收盤價(元), 下跌金額(元), 跌幅百分比(%) |
| `...w/mainboard/trading/realtime/delayed-close.html` | 暫緩收盤個股資訊 | ok | Y | 6 | 交易日期, 股票代碼, 股票名稱 |
| `...tw/mainboard/trading/realtime/delayed-open.html` | 暫緩開盤個股資訊 | ok | Y | 74 | 交易日期, 股票代碼, 股票名稱 |
| `/zh-tw/mainboard/trading/rules/ccp.html` | 櫃買中心金融市場基本架構原則資訊揭露報告（CCP&SSS） | ok | Y | 1 | 公告日期, 揭露報告, 檔案下載, 檔案下載 (ODS) |
| `/zh-tw/mainboard/trading/rules/continuous.html` | 盤中全面逐筆交易專區 | error | N | 0 |  |
| `/zh-tw/mainboard/trading/rules/fixed-term.html` | 定期定額投資股票及ETF專區 | error | N | 0 |  |
| `.../mainboard/trading/rules/fluctuation-limit.html` | 放寬漲跌幅度專區 | error | N | 0 |  |
| `/zh-tw/mainboard/trading/rules/maker.html` | 股票造市者制度專區 | error | N | 0 |  |
| `/zh-tw/mainboard/trading/rules/odd-lot.html` | 盤中零股交易專區 | error | N | 0 |  |
| `...tw/mainboard/trading/rules/opening-closing.html` | 開收盤前資訊揭露配套措施專區 | error | N | 0 |  |
| `/zh-tw/mainboard/trading/rules/res-fund.html` | 共同責任制給付結算基金簡介 | error | N | 0 |  |
| `/zh-tw/mainboard/trading/rules/system.html` | 上櫃有價證券交易系統簡介 | error | N | 0 |  |
| `/zh-tw/mainboard/trading/statistics/highlight.html` | 櫃買市場重要指標 | ok | Y | 14 | 文件名稱, XLS檔案下載, ODS檔案下載, 更新日期 |
| `...rd/trading/statistics/indices/constituents.html` | 股價指數採樣股票一覽表 | error | N | 0 |  |
| `...ard/trading/statistics/indices/daily-major.html` | 股價指數及指數平均數一覽表 | error | N | 0 |  |
| `...rd/trading/statistics/indices/daily-sector.html` | 產業分類股價指數一覽表 | error | N | 0 |  |
| `...inboard/trading/statistics/indices/summary.html` | 股價指數概要 | error | N | 0 |  |
| `/zh-tw/mainboard/trading/statistics/month.html` | 市場交易日報 | error | N | 0 |  |
| `.../mainboard/trading/statistics/month/listed.html` | 上櫃股票統計 | ok | Y | 3 | 日期, 下載XLS, 下載ODS |
| `.../mainboard/trading/statistics/month/market.html` | 市場交易月報 | error | N | 0 |  |
| `...w/mainboard/trading/statistics/month/value.html` | 上櫃公司市值、本益比、殖利率、投資報酬率一覽表 | ok | Y | 3 | 日期, 下載XLS, 下載ODS |
| `...rading/statistics/securities-firms/summary.html` | 櫃檯買賣股票營業彙總表 | ok | Y | 3 | 日期, 下載XLS, 下載ODS |
| `...statistics/securities-firms/trading-amount.html` | 證券商成交金額 | empty | Y | 0 | 資料日期, XLS下載, ODS下載 |
| `...g/statistics/securities-firms/trading-area.html` | 證券商成交金額統計表-地區別 | empty | Y | 0 | 資料日期, XLS下載, ODS下載 |
| `...statistics/securities-firms/trading-status.html` | 證券商成交金額彙計表 | empty | Y | 0 | 資料日期, XLS下載, ODS下載 |
| `/zh-tw/mainboard/trading/statistics/year.html` | 市場交易年報 | ok | Y | 7 | 報表名稱, 下載CSV |

#### 信用交易

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/www/zh-tw/marginTrading/balance` | 融資融券餘額 | error | Y | 0 |  |
| `/www/zh-tw/marginTrading/marginSbl` | 融券借券賣出餘額 | error | Y | 0 |  |

#### 公告資訊

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/zh-tw/announce/market/announce.html` | 公告查詢 | ok | Y | 4 | 項次, 資料日期, 發文字號, 主旨, 詳細資料 |
| `/zh-tw/announce/market/attention.html` | 上櫃公布注意有價證券資訊 | ok | Y | 46 | 編號, 證券代號, 證券名稱, 累計, 注意交易資訊 |
| `/zh-tw/announce/market/change.html` | 變更股票面額預告表 | ok | Y | 1 | 證券代號, 證券名稱, 停止買賣日期, 變更股票面額換股率, 變更前股票面額 |
| `/zh-tw/announce/market/change/reference.html` | 變更股票面額恢復交易參考價 | ok | Y | 1 | 恢復買賣日期, 證券代號, 證券名稱, 最後交易日之收盤價格, 恢復買賣開始參考價 |
| `/zh-tw/announce/market/default.html` | 違約公告專區 | ok | Y | 2 | 申報日期, 類別, 買進、賣出合計總金額, 買進、賣出相抵後金額 |
| `/zh-tw/announce/market/disposal.html` | 上櫃處置有價證券資訊 | ok | Y | 42 | 編號, 公布日期, 證券代號, 證券名稱, 累計 |
| `/zh-tw/announce/market/download.html` | 公告資料下載 | empty | Y | 0 | 資料日期, 檔案下載 |
| `/zh-tw/announce/market/employee.html` | 員工認股權憑證、可轉換特別股、海外轉換公司債暨興櫃公司國內轉換公司債情形公告 | ok | Y | 12 | 資料月份, XLS檔案下載, ODS檔案下載 |
| `/zh-tw/announce/market/esb-attention.html` | 興櫃達通知標準及公布注意股票資訊 | ok | Y | 18 | 編號, 證券代號, 證券名稱, 累計, 注意交易資訊 |
| `/zh-tw/announce/market/esb-disposal.html` | 興櫃處置股票資訊 | ok | Y | 2 | 編號, 公布日期, 證券代號, 證券名稱, 累計 |
| `/zh-tw/announce/market/esb-warning.html` | 興櫃公布累積次數異常資訊 | ok | Y | 5 | 編號, 證券代號, 證券名稱, 近期達本公司「公布注意交易資訊」標準之情形 |
| `/zh-tw/announce/market/etf-rev-split.html` | ETF反分割預告表 | empty | Y | 0 | 證券代號, 證券名稱, 停止買賣日期, ETF分割率, 分割前ETF淨值 |
| `...tw/announce/market/etf-rev-split/reference.html` | ETF反分割恢復交易參考價 | empty | Y | 0 | 恢復買賣日期, 證券代號, 證券名稱, 最後交易日之收盤價格, 恢復買賣開始參考價 |
| `/zh-tw/announce/market/etf-split.html` | ETF分割預告表 | empty | Y | 0 | 證券代號, 證券名稱, 停止買賣日期, ETF分割率, 分割前ETF淨值 |
| `/zh-tw/announce/market/etf-split/reference.html` | ETF分割恢復交易參考價 | empty | Y | 0 | 恢復買賣日期, 證券代號, 證券名稱, 最後交易日之收盤價格, 恢復買賣開始參考價 |
| `/zh-tw/announce/market/ex/announce.html` | 除權除息預告表 | ok | Y | 90 | 除權息日期, 代號, 名稱, 除權息, 每股無償配股率 |
| `/zh-tw/announce/market/ex/cal.html` | 除權除息計算結果表 | empty | Y | 0 | 除權息日期, 代號, 名稱, 除權息前收盤價, 除權息參考價 |
| `/zh-tw/announce/market/halt.html` | 公布暫停/恢復交易有價證券 | error | N | 0 |  |
| `/zh-tw/announce/market/holiday.html` | 開休市日期表 | empty | Y | 0 |  |
| `/zh-tw/announce/market/reduction-tdr.html` | 股票增減資上櫃掛牌（興櫃登錄）公告暨TDR再發行及註銷公告 | ok | Y | 20 | 項次, 公司代號, 公司簡稱, 公告種類, 申報序號 |
| `/zh-tw/announce/market/reduction.html` | 減資預告表 | empty | Y | 0 | 代號, 名稱, 停止買賣日期, 減資換股率, 每股退還股款(元) |
| `/zh-tw/announce/market/reduction/reference.html` | 減資恢復交易參考價 | empty | Y | 0 | 恢復買賣日期, 股票代號, 名稱, 最後交易日之收盤價格, 減資恢復買賣開始日參考價格 |
| `/zh-tw/announce/market/specific.html` | 特殊異常有價證券 | ok | Y | 1 | 編號, 證券代號, 證券名稱, 累計, 公告日期 |
| `/zh-tw/announce/market/unusual.html` | 投資理財節目異常推介有價證券 | ok | Y | 1 | 編號, 證券代號, 證券名稱, 累計, 公告日期 |
| `/zh-tw/announce/market/warning.html` | 上櫃公布注意累計次數異常資訊 | ok | Y | 17 | 編號, 證券代號, 證券名稱, 近期達本公司「公布注意交易資訊」標準之情形 |

#### 基本面

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/www/zh-tw/afterTrading/peRatio` | 個股本益比、殖利率、股價淨值比 | error | Y | 0 |  |
| `/www/zh-tw/exRight/dailyQuote` | 除權除息日程 | error | Y | 0 |  |

#### 指數

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/www/zh-tw/indexInfo/minuteIndex` | 上櫃指數歷史資料 | error | Y | 0 |  |

#### 指數資訊

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/zh-tw/indices/bond-index/benchmark/licensing.html` | 指數之授權 | error | N | 0 |  |
| `/zh-tw/indices/bond-index/benchmark/method.html` | 指數編製基本規則 | error | N | 0 |  |
| `...tw/indices/bond-index/benchmark/report/day.html` | 指數報表 | error | N | 0 |  |
| `/zh-tw/indices/bond-index/boc/introduction.html` | 指數簡介 | error | N | 0 |  |
| `/zh-tw/indices/bond-index/boc/methodology.html` | 指數編製原則 | error | N | 0 |  |
| `/zh-tw/indices/bond-index/gov-bond/method.html` | 指數編製基本規則 | error | N | 0 |  |
| `/zh-tw/indices/bond-index/gov-bond/report/day.html` | 指數報表 | error | N | 0 |  |
| `/zh-tw/indices/co-branded/bloomberg-list.html` | TPEx & 彭博聯名指數 | error | N | 0 |  |
| `/zh-tw/indices/co-branded/ice-list.html` | TPEx & ICE聯名指數 | error | N | 0 |  |
| `/zh-tw/indices/gold-index/spot/AU9901-spot.html` | 櫃買臺灣黃金現貨指數 | error | N | 0 |  |
| `/zh-tw/indices/gold-index/spot/tpex-gold-spot.html` | 櫃買黃金現貨指數 | error | N | 0 |  |
| `/zh-tw/indices/stock-index/announcement.html` | 技術通知 | ok | Y | 13 | 公布日期, 摘要, 檔案下載 |
| `/zh-tw/indices/stock-index/boc/consti.html` | 指數當日成分債 | error | N | 0 |  |
| `/zh-tw/indices/stock-index/cross-market.html` | 跨市場指數 | ok | Y | 55 | 合作機構, 指數名稱, 基期, 發布日, 基期指數 |
| `/zh-tw/indices/stock-index/factset/IR0203.html` | TPEx FactSet半導體氣候淨零優選報酬指數 | error | N | 0 |  |
| `/zh-tw/indices/stock-index/factset/IX0201.html` | TPEx FactSet氣候韌性指數 | error | N | 0 |  |
| `/zh-tw/indices/stock-index/factset/IX0202.html` | TPEx FactSet半導體氣候韌性指數 | error | N | 0 |  |
| `/zh-tw/indices/stock-index/industrial/consti.html` | 櫃買指數成分股 | ok | Y | 881 | 代號, 名稱, 發行仟股數, 收市價, 產業類別 |
| `/zh-tw/indices/stock-index/industrial/idxsm.html` | 產業分類指數及其報酬指數(月查詢) | ok | Y | 40 | 日期, 紡織纖維, 電機機械, 鋼鐵工業, 電子工業 |
| `/zh-tw/indices/stock-index/industrial/intro.html` | 指數簡介 | error | N | 0 |  |
| `/zh-tw/indices/stock-index/industrial/inxh.html` | 櫃買指數(月查詢) | ok | Y | 7 | 日期, 開市, 最高, 最低, 收市 |
| `/zh-tw/indices/stock-index/industrial/inxsect.html` | 櫃買指數暨產業分類指數(日查詢) | ok | Y | 23 | 類股名稱, 收市, 漲跌, 開市, 最高 |
| `/zh-tw/indices/stock-index/industrial/method.html` | 指數編製要點 | error | N | 0 |  |
| `/zh-tw/indices/stock-index/industrial/roe.html` | 櫃買指數與報酬指數(月查詢) | ok | Y | 7 | 日期, 櫃買指數, 櫃買報酬指數(基期:94/12/30) |
| `/zh-tw/indices/stock-index/industrial/sec.html` | 每5秒盤後統計 | ok | Y | 3242 | 時 間, 紡纖纖維, 電機機械, 鋼鐵工業, 建材營造 |
| `/zh-tw/indices/stock-index/serial_esg.html` | 更多指數 | error | N | 0 |  |
| `/zh-tw/indices/stock-index/serial_etf_etn.html` | ESG ETF | error | N | 0 |  |
| `/zh-tw/indices/stock-index/serial_factset.html` | 更多指數 | error | N | 0 |  |
| `...indices/stock-index/sustainability//IX0177.html` | 上櫃ESG 30指數 | error | N | 0 |  |
| `.../indices/stock-index/sustainability/IR0173.html` | 特選上櫃ESG永續高股息報酬指數 | error | N | 0 |  |
| `.../indices/stock-index/sustainability/IR0200.html` | 特選上櫃ESG龍頭報酬指數 | error | N | 0 |  |
| `.../indices/stock-index/sustainability/IX0134.html` | 臺灣上櫃永續指數 | error | N | 0 |  |
| `/zh-tw/indices/stock-index/thematic/IR0140.html` | 櫃買半導體領航報酬指數 | error | N | 0 |  |
| `/zh-tw/indices/stock-index/thematic/IR0141.html` | 櫃買富櫃200報酬正向2倍指數 | error | N | 0 |  |
| `/zh-tw/indices/stock-index/thematic/IX0060.html` | 富櫃50指數 | error | N | 0 |  |
| `/zh-tw/indices/stock-index/thematic/IX0118.html` | 富櫃200指數 | error | N | 0 |  |
| `/zh-tw/indices/stock-index/thematic/list.html` | 更多指數 | ok | Y | 19 | 指數名稱, 指數基期, 基期指數, 發布日, 最近指數 |

#### 法人

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/www/zh-tw/insti/dailyTrade` | 三大法人買賣明細 | empty | Y | 0 |  |
| `/www/zh-tw/insti/qfiiTrade` | 外資及陸資買賣明細 | error | Y | 0 |  |
| `/www/zh-tw/insti/summary` | 三大法人買賣金額統計 | ok | Y | 8 | 單位名稱, 買進金額(元), 賣出金額(元), 買賣超(元) |

#### 興櫃交易

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/zh-tw/esb/trading/ex/ex-dividend.html` | 除權除息 | ok | Y | 42 | 代號, 名稱, 除權除息日期, 種類, 現金股利 |
| `/zh-tw/esb/trading/halt/today.html` | 興櫃交易時間內股價異常波動達暫停交易標準之興櫃股票查詢 | error | N | 0 |  |
| `/zh-tw/esb/trading/highlight.html` | 興櫃股票市場現況 | ok | Y | 3 | 登錄興櫃家數, 總資本額(佰萬元), 總市值(佰萬元), 本日總成交值(佰萬元), 本日總成交... |
| `/zh-tw/esb/trading/info/historical/day.html` | 歷史行情(日統計) | ok | Y | 13 | 文件名稱, 資料日期, 下載, 檢視網頁, 備註 |
| `/zh-tw/esb/trading/info/historical/month.html` | 歷史行情(月統計) | ok | Y | 9 | 文件名稱, 資料月份, 下載, 檢視網頁, 備註 |
| `/zh-tw/esb/trading/info/historical/week.html` | 歷史行情(週統計) | ok | Y | 7 | 文件名稱, 資料日期, 下載, 檢視網頁, 備註 |
| `/zh-tw/esb/trading/info/historical/year.html` | 歷史行情(年統計) | ok | Y | 10 | 文件名稱, 資料年份, 下載, 備註 |
| `/zh-tw/esb/trading/info/pricing.html` | 當日行情表 | ok | Y | 352 | 代號, 名稱, 前日均價, 報買價, 報買量 |
| `/zh-tw/esb/trading/info/stock-pricing.html` | 個股歷史行情 | error | N | 0 |  |
| `/zh-tw/esb/trading/rules/education.html` | 相關文件下載 | error | N | 0 |  |
| `/zh-tw/esb/trading/rules/overview.html` | 制度說明 | error | N | 0 |  |
| `/zh-tw/esb/trading/rules/qa.html` | 問與答 | error | N | 0 |  |
| `/zh-tw/esb/trading/rules/regulations.html` | 規章公告 | error | N | 0 |  |
| `/zh-tw/esb/trading/statistics/day.html` | 興櫃股票成交統計 | error | N | 0 |  |

#### 行情

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/www/zh-tw/afterTrading/blockTrading` | 鉅額交易 | error | Y | 0 |  |
| `/www/zh-tw/afterTrading/brokerTrading` | 證券商成交量值 | error | Y | 0 |  |
| `/www/zh-tw/afterTrading/dailyQuotes` | 上櫃股票每日收盤行情 | ok | Y | 10711 | 代號, 名稱, 收盤, 漲跌, 開盤 |
| `/www/zh-tw/afterTrading/dailyTradingInfo` | 每日市場成交資訊 | error | Y | 0 |  |
| `/www/zh-tw/afterTrading/dayTrading` | 當日沖銷交易統計 | error | Y | 0 |  |
| `/www/zh-tw/afterTrading/monthlyTrade` | 個股月成交資訊 | error | Y | 0 |  |
| `/www/zh-tw/afterTrading/oddLot` | 零股交易行情 | error | Y | 0 |  |

## Market Observation Post System (MOPS)

### Web (101 endpoints)

#### Announcement

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mops/web/ajax_t05sr01_1` | Real-time material information | ok | Y | 240 | 公司代號, 公司簡稱, 發言日期, 發言時間, 主旨 |

#### Dividend

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mops/web/ajax_t05st09_2` | Dividend distribution | error | Y | 0 |  |

#### Financial

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mops/web/ajax_t164sb03` | Financial statements (Balance sheet) | ok | Y | 71 | ('民國113年第3季', '單位：新台幣仟元', '會計項目', 'Unnamed: 0_l... |
| `/mops/web/ajax_t164sb04` | Financial statements (Income statement) | ok | Y | 48 | ('民國113年第3季', '單位：新台幣仟元', '會計項目', 'Unnamed: 0_l... |
| `/mops/web/ajax_t164sb05` | Financial statements (Cash flow statement) | ok | Y | 80 | ('民國113年第3季', '單位：新台幣仟元', '會計項目', 'Unnamed: 0_l... |
| `/mops/web/t05st10_ifrs` | Profitability analysis (IFRS) | ok | Y | 9 | 0 |

#### Revenue

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mops/web/ajax_t21sc04_ifrs` | Monthly revenue summary (IFRS) - OTC | ok | Y | 939 | ('Unnamed: 0_level_0', '���q �N��'), ('Unnamed:... |

#### SPA Page

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mops/web/t05sr01_1` | 即時重大訊息 | ok | N | 48 | 公司代號, 公司簡稱, 發言日期, 發言時間, 主旨 |
| `/mops/web/t05st01` | 歷史重大訊息 | ok | N | 22 | 公司代號, 公司名稱, 發言日期, 發言時間, 主旨 |
| `/mops/web/t05st02` | 今日重大訊息 | ok | N | 12 | 發言日期, 發言時間, 公司代號, 公司名稱, 主旨 |
| `/mops/web/t05st09_2` | 股利分派情形 | ok | N | 6 | ('決議（擬議） 進度', '決議（擬議） 進度', '決議（擬議） 進度'), ('股利所屬... |
| `/mops/web/t05st15` | 大陸投資資訊 | ok | N | 16 | 0 |
| `/mops/web/t100sb03_1` | 功能性委員會 | ok | N | 3 | ('公司代號', '公司代號'), ('公司名稱', '公司名稱'), ('成立日期', '成... |
| `/mops/web/t108sb16_q1` | 股東會 | ok | N | 5 | 0 |
| `/mops/web/t108sb19` | 除權息公告 | ok | N | 1 | 公告日期, 申報序號, 主旨, 種類, 內容 |
| `/mops/web/t146sb10` | 公告查詢 | error | N | 0 |  |
| `/mops/web/t163sb01` | 財報公告 | ok | N | 65 | 0, 1, 2, 3 |
| `/mops/web/t164sb00` | 合併/個別報表 (XBRL) | error | N | 0 |  |
| `/mops/web/t51sb10` | 最新公告 | ok | N | 10 | 0 |

#### XBRL

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mops/web/ajax_t203sb01` | XBRL instance document query (single company) | ok | Y | 82 | 0, 1, 2, 3 |
| `/mops/web/ajax_t203sb02` | XBRL instance document batch download | ok | Y | 29 | 0, 1, 2, 3, 4 |
| `/mops/web/t203sb03` | XBRL taxonomy download | ok | N | 10 | tifrs-20200630.zip, tifrs-20190331.zip, tifrs-2... |

#### 內部人持股轉讓事前申報彙總表

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mops/web/t56sb21_q3` | 持股轉讓日報表 | ok | N | 399 | ('異動情形', '異動情形'), ('申報日期', '申報日期'), ('公司 代號', '... |
| `/mops/web/t56sb21_q4` | 持股未轉讓日報表 | ok | N | 40 | ('申報日期', '申報日期'), ('公司代號', '公司代號'), ('公司名稱', '公... |

#### 內部人持股轉讓事前申報表(個別公司)

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mops/web/t56sb21_q1` | 持股轉讓日報表 | ok | N | 27 | ('異動情形', '異動情形'), ('申報日期', '申報日期'), ('公司 代號', '... |
| `/mops/web/t56sb21_q2` | 持股未轉讓日報表 | ok | N | 1 | ('申報日期', '申報日期'), ('公司代號', '公司代號'), ('公司名稱', '公... |

#### 內部人設質解質彙總公告

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mops/web/STAMAK03_1` | 內部人設質解質公告(個別公司) | ok | N | 115 | 公司代號, 公司名稱, 設質人身份別, 設質人姓名, 質設異動發生日期 |
| `/mops/web/STAMAK03_q1` | 依照日期排序 | ok | N | 327 | ('股票代號', '金融控股公司名稱'), ('公司名稱', '金融控股公司名稱'), ('設... |
| `/mops/web/STAMAK03_q2` | 依照公司代號排序 | ok | N | 327 | ('股票代號', '金融控股公司名稱'), ('公司名稱', '金融控股公司名稱'), ('設... |

#### 員工認股權憑證

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mops/web/t158sb01` | 員工認股權憑證年度經理人、部門及分支機構主管與前十大員工之取得及認購情形資訊 | ok | N | 23 | 0, 1, 2, 3, 4 |
| `/mops/web/t158sb02` | 員工認股權憑證發行次日暨經理人、部門及分支機構主管取得認股權憑證情形之申報資訊 | ok | N | 10 | 0, 1, 2 |
| `/mops/web/t158sb03` | 員工認股權憑證經理人、部門及分支機構主管認購情形之資訊－認購次日內申報(自102年起免申報) | ok | N | 19 | 認購日期, Unnamed: 1 |
| `/mops/web/t158sb04_new` | 員工認股權憑證經理人、部門及分支機構主管當季認購認股權情形資料－按季結束十日內申報 | ok | N | 9 | 0, 1 |
| `/mops/web/t158sb05_new` | 員工認股權憑證發行期間屆滿次日暨經理人、部門及分支機構主管取得認股權憑證情形之申報資訊 | error | N | 0 |  |
| `/mops/web/t47sb09` | 員工認股權憑證基本資料查詢 | ok | N | 4 | 主管機關核准日期, Unnamed: 1 |
| `/mops/web/t47sc18` | 員工認股權憑證年度已執行及未執行資訊 | ok | N | 10 | 主管機關核准日期, 發行日期, 年度 （例如：90）, Unnamed: 3 |

#### 國內有價證券

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mops/web/t144sb01` | 分離後認股權憑證發行基本資料查詢 | ok | N | 3 | 0 |
| `/mops/web/t47sb05` | 附認股權特別股基本資料查詢 | error | N | 0 |  |
| `/mops/web/t47sb06` | 一般公司債基本資料查詢 | ok | N | 84 | 期別, 券別, Unnamed: 2 |
| `/mops/web/t47sb07` | 轉換公司債基本資料查詢 | error | N | 0 |  |
| `/mops/web/t47sb08` | 附認股權公司債基本資料查詢 | error | N | 0 |  |
| `/mops/web/t47sb11` | 附認股權公司債利率查詢 | error | N | 0 |  |
| `/mops/web/t47sb12` | 特別股權利基本資料查詢 | ok | N | 2 | 0 |
| `/mops/web/t47sb17` | 一般公司債月報表查詢 | ok | N | 84 | 期別, 券別, 資料年月, Unnamed: 3 |
| `/mops/web/t47sb18` | 轉換公司債月報表查詢 | ok | N | 1 | 0 |
| `/mops/web/t47sb19` | 附認股權公司債月報表查詢 | ok | N | 1 | 0 |
| `/mops/web/t47sb20` | 金融債券月報表查詢 | ok | N | 1 | 0 |

#### 基本資料

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mops/web/t05st03` | 公司基本資料 | ok | N | 33 | 0, 1, 2, 3, 4 |
| `/mops/web/t146sb05` | 精華版3.0 | ok | N | 50 | 0, 1, 2, 3, 4 |

#### 海外有價證券

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mops/web/t47sb03_q1` | 海外股票基本資料查詢 | ok | N | 1 | 0 |
| `/mops/web/t47sb03_q2` | 海外存託憑證基本資料查詢 | ok | N | 2 | 0 |
| `/mops/web/t47sb03_q3` | 海外一般公司債基本資料查詢 | ok | N | 1 | 0 |
| `/mops/web/t47sb03_q4` | 海外轉換公司債基本資料查詢 | ok | N | 1 | 0 |
| `/mops/web/t47sb03_q5` | 海外附認股權公司債基本資料查詢 | ok | N | 1 | 0 |
| `/mops/web/t47sb21` | 海外一般公司債異動情形報表查詢 | ok | N | 1 | 0 |
| `/mops/web/t47sb22` | 海外轉換公司債異動情形報表查詢 | ok | N | 1 | 0 |
| `/mops/web/t47sb23` | 海外附認股權公司債異動情形報表查詢 | ok | N | 1 | 0 |
| `/mops/web/t47sb24` | 海外股票流通餘額報表 | ok | N | 1 | 0 |
| `/mops/web/t47sb25` | 海外存託憑證暨其所表彰有價證券流通餘額查詢 | ok | N | 2 | 0 |

#### 股權轉讓資料查詢

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mops/web/IRB100` | 董事、監察人持股不足法定成數彙總表 | ok | N | 13 | 0, 1, 2, 3, 4 |
| `/mops/web/IRB210` | 董事、監察人持股不足法定成數連續達3個月以上彙總表 | ok | N | 1 | 連續持股 不足之期間, 連續不足 達3個月 113/10-12, 連續不足 達4個月 113/... |
| `/mops/web/t56sb12_q1` | 上市公司持股轉讓日報表 | error | N | 0 |  |
| `/mops/web/t56sb12_q2` | 上櫃公司持股轉讓日報表 | error | N | 0 |  |
| `/mops/web/t56sb12_q3` | 興櫃公司持股轉讓日報表 | error | N | 0 |  |
| `/mops/web/t56sb12_q4` | 公開發行公司持股轉讓日報表 | error | N | 0 |  |
| `/mops/web/t56sb12_q5` | 上市公司持股未轉讓日報表 | error | N | 0 |  |
| `/mops/web/t56sb12_q6` | 上櫃公司持股未轉讓日報表 | error | N | 0 |  |
| `/mops/web/t56sb12_q7` | 興櫃公司持股未轉讓日報表 | error | N | 0 |  |
| `/mops/web/t93sb06` | 公司董事、監察人及持股10%以上大股東為法人之彙總查詢 | ok | N | 2324 | 公司代號, 公司名稱, 董事監察人或大股東姓名, 身分, Unnamed: 4 |
| `/mops/web/t93sb06_1` | 持股10%以上大股東最近異動情形 | ok | N | 1050 | 0, 1, 2, 3, 4 |

#### 董監事股權異動統計彙總表

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mops/web/IRB110` | 董事、監察人、經理人及百分之十以上大股東股權異動彙總表 | ok | N | 1036 | 0, 1, 2, 3, 4 |
| `/mops/web/IRB130` | 董事、監察人、經理人及百分之十以上大股東質權設定彙總表 | ok | N | 1036 | 0, 1, 2, 3, 4 |
| `/mops/web/IRB140` | 轉讓持股達100萬股以上者彙總表 | ok | N | 20 | 0, 1, 2, 3 |
| `/mops/web/IRB150` | 取得股份達100萬股以上者彙總表 | ok | N | 23 | 0, 1, 2, 3 |
| `/mops/web/IRB160` | 公司增減資表 | ok | N | 105 | 0, 1 |
| `/mops/web/IRB170` | 新公司彙總表 | ok | N | 6 | 0, 1 |
| `/mops/web/IRB180` | 董事、監察人質權設定佔董事及監察人實際持有股數彙總表 | ok | N | 262 | 0, 1, 2, 3, 4 |
| `/mops/web/IRB190` | 董事、監察人質權設定在100萬股以上彙總表 | ok | N | 18 | 0, 1, 2, 3 |
| `/mops/web/IRB200` | 董事、監察人質權解除在100萬股以上彙總表 | ok | N | 12 | 0, 1, 2, 3 |
| `/mops/web/query6_1` | 內部人持股異動事後申報表 | ok | N | 103 | ('資料年月：11503', '身份別'), ('資料年月：11503', '姓\u3000名... |

#### 董監大股東持股、質押、轉讓

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mops/web/stapap1` | 董監事持股餘額明細資料 | ok | N | 62 | 0, 1, 2, 3, 4 |
| `/mops/web/stapap1_all` | 董事、監察人、經理人及大股東持股餘額彙總表 | ok | N | 1069 | 公司代號, 公司簡稱, Unnamed: 2 |

#### 買回臺灣存託憑證

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mops/web/t05st05` | 歷年變更登記 | ok | N | 75 | 0, 1 |
| `/mops/web/t16sn02` | 股權分散表 | ok | N | 37 | 0, 1, 2, 3, 4 |
| `/mops/web/t35sb08` | 買回臺灣存託憑證基本資料 | error | N | 0 |  |
| `/mops/web/t35sb09` | 查詢買回臺灣存託憑證期間屆滿或執行完畢 | error | N | 0 |  |
| `/mops/web/t35sb10` | 買回臺灣存託憑證達一定標準 | ok | N | 1 | 0 |
| `/mops/web/t98sb04` | 國內海外有價證券轉換情形 | error | N | 0 |  |

#### 重要子公司基本資料

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mops/web/t102sb01` | 被投資控股公司基本資料 | error | N | 0 |  |
| `/mops/web/t79sb02` | 重要子公司基本資料 | ok | N | 18 | 0 |
| `/mops/web/t79sb03` | 重要子公司異動說明 | ok | N | 19 | 0 |

#### 限制員工權利新股

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mops/web/t132sb20` | 外國發行人之股票、臺灣存託憑證、債券流通情形 | error | N | 0 |  |
| `/mops/web/t160sb01` | 限制員工權利新股發行辦法及對股東權益可能稀釋情形(包含變更發行辦法、實際發行資料) | ok | N | 5 | 0, 1 |
| `/mops/web/t160sb02` | 員工達成既得條件之解除限制資訊 | ok | N | 9 | 0, 1, 2, 3 |
| `/mops/web/t98sb02` | 僑外及大陸地區投資人投資持股情形統計表 | ok | N | 2 | 0, 1, 2, 3 |

#### 電子書

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/mops/web/t57sb01_q1` | 財務報告書 | error | N | 11 |  |
| `/mops/web/t57sb01_q10` | 關係企業三書表專區 | error | N | 8 |  |
| `/mops/web/t57sb01_q2` | 財務預測書 | error | N | 0 |  |
| `/mops/web/t57sb01_q3` | 公開說明書 | error | N | 110 |  |
| `/mops/web/t57sb01_q5` | 年報及股東會相關資料(含存託憑證資料) | error | N | 12 |  |
| `/mops/web/t57sb01_q8` | 年度自結財務資訊專區 | error | N | 0 |  |

## Taiwan Depository & Clearing Corporation (TDCC)

### OpenAPI (134 endpoints)

#### TAIBIR 資訊

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/v1/opendata/2-15` | TAIBIR當日最近初級發行利率報價 | ok | N | 23 | 30天期, 120天期, ﻿資料日期時間, 票券公司, 60天期 |
| `/v1/opendata/2-16` | TAIBIR當日最近次級買賣利率報價 | ok | N | 23 | 365天期買入小計, ﻿資料日期時間, 30天期賣出小計, 20天期賣出小計, 60天期賣出小計 |
| `/v1/opendata/2-17` | TAIBIR 01當日初級發行利率報價定盤利率 | ok | N | 23 | 20天期小計, 120天期小計, ﻿資料日期時間, 票券公司, 180天期小計 |
| `/v1/opendata/2-18` | TAIBIR 02當日次級買賣利率報價定盤利率 | ok | N | 23 | 365天期買入小計, ﻿資料日期時間, 30天期賣出小計, 20天期賣出小計, 60天期賣出小計 |
| `/v1/opendata/2-19` | TAIBIR 01歷史初級發行利率報價定盤利率 | ok | N | 30 | 30天期, 120天期, 60天期, 150天期, ﻿資料日期 |
| `/v1/opendata/2-20` | TAIBIR 02歷史次級買賣利率報價定盤利率 | ok | N | 30 | 30天期, 120天期, 60天期, 150天期, ﻿資料日期 |
| `/v1/opendata/2-21` | TAIBIR 02上線前歷史次級買賣利率報價定盤利率 | ok | N | 701 | 30天期, 120天期, 60天期, 150天期, ﻿資料日期 |

#### 固定收益類 統計資訊

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/v1/opendata/2-11` | 次級市場ABCP | ok | N | 8 | 365天期買入小計, ﻿資料日期時間, 30天期賣出小計, 20天期賣出小計, 60天期賣出小計 |
| `/v1/opendata/2-12` | ABCP成交資訊 | ok | N | 9 | ﻿資料日期時間, 加權平均利率, 成交量(佰萬元), 天期 |
| `/v1/opendata/2-13` | 國庫券成交資訊 | ok | N | 9 | 附條件成交量(小計), ﻿資料日期時間, 天期(小計), 買賣斷成交量(小計), 買賣斷加權平... |
| `/v1/opendata/2-14` | 國庫券買賣斷成交行情資訊 | ok | N | 8 | 買賣斷成交利率(最低), ﻿資料日期時間, 買賣斷成交利率(加權平均), 國庫券名稱, 距到期天期 |
| `/v1/opendata/2-30` | 票券保管結算交割系統各類短期票券流通餘額表 | ok | N | 6 | ﻿﻿資料年月, 幣別, 票劵別, 當月底持有餘額, 比率 |
| `/v1/opendata/2-31` | 票券保管結算交割系統結算交割時間統計 | ok | N | 1 | ﻿﻿資料年月, 合計比率, 09:00~14:30, 16:30之後, 14:30~16:30 |
| `/v1/opendata/2-32` | 票券保管結算交割系統參加單位一覽表 | ok | N | 143 | 參加單位代號, ﻿﻿資料年月, 參加單位類別, 參加單位名稱 |
| `/v1/opendata/2-33` | 票券保管結算交割系統票券部位別統計月報表 | ok | N | 6 | ﻿﻿資料年月, 附賣回部位, 附買回部位, 出質部位, 質權部位 |
| `/v1/opendata/2-34` | 固定收益商品債券存摺開立統計月報表 | ok | N | 12 | 數額, ﻿年月, 筆數 |
| `/v1/opendata/2-35` | 固定收益商品債券存摺開立統計年報表 | ok | N | 1 | 數額, ﻿年, 筆數 |
| `/v1/opendata/2-36` | 票券保管結算交割系統票券撥轉月報表 | ok | N | 6 | 前一日帳簿餘額, 承銷/配銷, RP賣出, 賣斷, 跨系統撥轉淨額 |
| `/v1/opendata/2-37` | 票券保管結算交割系統次級交易央清款項清算交割統計月報 | ok | N | 2 | 14:31 ~ 15:30金額, 15:31 ~ 16:30比例, 項次, 超過 16:30金... |
| `/v1/opendata/2-38` | 票券保管結算交割系統次級交易央清款項清算交割統計月報 | ok | N | 2 | 14:31 ~ 15:30金額, 15:31 ~ 16:30比例, 項次, 超過 16:30金... |

#### 境外基金資訊

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/v1/opendata/3-1` | 境外基金總代理資訊 | ok | N | 63 | 核准基金筆數, 總代理網址, 總代理名稱, 總代理信箱, ﻿資料日期 |
| `/v1/opendata/3-10` | 境外基金市場資訊-基金類別 | ok | N | 853 | 買回總金額, 淨申贖總金額, 基金筆數, ﻿年月, 基金類別 |
| `/v1/opendata/3-11` | 境外基金市場資訊-投資區域別 | ok | N | 4722 | 買回總金額, 淨申贖總金額, 投資區域細項, 基金筆數, ﻿年月 |
| `/v1/opendata/3-12` | 境外基金資訊傳輸暨款項收付平台使用機構查詢 | ok | N | 599 | 身份別, 銷售基金檔數, ﻿資料時間, 境外基金機構, 使用機構名稱 |
| `/v1/opendata/3-13` | 境外基金資訊傳輸暨款項收付平台款項收付銀行查詢 | ok | N | 10 | 收付銀行機構代號, ﻿資料時間, 收付銀行機構名稱 |
| `/v1/opendata/3-14` | 境外基金資訊傳輸暨款項收付平台全國性繳費稅金融機構查詢 | ok | N | 228 | 金融機構代號, ﻿資料時間, 金融機構名稱 |
| `/v1/opendata/3-15` | 境外基金短線交易與反稀釋等相關資訊 | ok | N | 5215 | 基金名稱, ﻿資料時間, ISIN Code, 公開說明書網址, 有無反稀釋條款 |
| `/v1/opendata/3-16` | 境外基金基金總覽-美元計價基金 | ok | N | 3352 | 淨值日期, 最新淨值小計(總額), 境外基金機構, ﻿資料日期, 計價幣別 |
| `/v1/opendata/3-17` | 境外基金基金總覽-歐元計價基金 | ok | N | 955 | 淨值日期, 最新淨值小計(總額), 境外基金機構, ﻿資料日期, 計價幣別 |
| `/v1/opendata/3-18` | 境外基金基金總覽-日圓計價基金 | ok | N | 157 | 淨值日期, 最新淨值小計(總額), 境外基金機構, ﻿資料日期, 計價幣別 |
| `/v1/opendata/3-19` | 境外基金基金總覽-其他計價幣別基金 | ok | N | 750 | 淨值日期, 最新淨值小計(總額), 境外基金機構, ﻿資料日期, 計價幣別 |
| `/v1/opendata/3-2` | 境外基金基本資料 | ok | N | 5214 | 保管機構短期信評, 境外基金機構, 基金規模幣別, ﻿資料日期, 基金英文名稱 |
| `/v1/opendata/3-20` | 境外基金基金總覽-全球型基金 | ok | N | 2911 | 淨值日期, 最新淨值小計(總額), 境外基金機構, ﻿資料日期, 計價幣別 |
| `/v1/opendata/3-21` | 境外基金基金總覽-單一國家型基金 | ok | N | 961 | 淨值日期, 最新淨值小計(總額), 境外基金機構, ﻿資料日期, 計價幣別 |
| `/v1/opendata/3-22` | 境外基金基金總覽-區域型基金 | ok | N | 1342 | 淨值日期, 最新淨值小計(總額), 境外基金機構, ﻿資料日期, 計價幣別 |
| `/v1/opendata/3-23` | 境外基金投資人服務及保護-公平價格調整機制 | ok | N | 5028 | 基金名稱, 總代理人, ﻿資料日期, 備註, 公平價格調整機制資料內容 |
| `/v1/opendata/3-25` | 境外基金基金總覽-股票型基金 | ok | N | 2694 | 基金名稱, 淨值日期, 最新淨值小計(總額), 基金種類, 投資細項 |
| `/v1/opendata/3-26` | 境外基金基金總覽-固定收益型 | ok | N | 2050 | 基金名稱, 淨值日期, 最新淨值小計(總額), 基金種類, 投資細項 |
| `/v1/opendata/3-27` | 境外基金基金總覽-平衡型 | ok | N | 426 | 基金名稱, 淨值日期, 最新淨值小計(總額), 基金種類, 投資細項 |
| `/v1/opendata/3-28` | 境外基金基金總覽-貨幣市場型 | ok | N | 32 | 基金名稱, 淨值日期, 最新淨值小計(總額), 基金種類, 投資細項 |
| `/v1/opendata/3-29` | 境外基金基金總覽-指數股票型(ETF) | ok | N | 1 | 基金名稱, 淨值日期, 最新淨值小計(總額), 檢查日期, 基金種類 |
| `/v1/opendata/3-3` | 境外基金機構基本資料 | ok | N | 112 | ﻿總機構代碼, 電話, 公司名稱, 地址, 負責人 |
| `/v1/opendata/3-4` | 境外基金淨值 | ok | N | 22697 | 基金名稱, 日期, 總代理機構, 境外基金機構, ﻿基金代碼 |
| `/v1/opendata/3-5` | 境外基金配息資訊 | ok | N | 9173 | 境外基金機構, 配息頻率, ﻿資料日期, 可分配淨利益/配息, 配息發放日 |
| `/v1/opendata/3-6` | 境外基金報價日及營業日查詢 | ok | N | 28535 | 基金名稱, 日期類型, 基金ISIN CODE, 日期, 基金代號 |
| `/v1/opendata/3-7` | 境外基金銷售機構查詢 | ok | N | 1335 | 基金總代理, ﻿資料時間, 銷售機構 |
| `/v1/opendata/3-8` | 境外基金市場資訊-彙總 | ok | N | 3745 | ﻿年月, 統計類型, 項目, 金額 |
| `/v1/opendata/3-9` | 境外基金市場資訊-計價幣別 | ok | N | 1786 | 買回總金額, 淨申贖總金額, 計價幣別, 基金筆數, ﻿年月 |

#### 境外結構型商品資訊

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/v1/opendata/4-1` | 境外結構型商品發行人/總代理人資訊 | ok | N | 13 | 發行人/總代理人身分別, ﻿資料日期, 所屬發行機構, 所屬保證機構, 境外結構型商品名稱 |
| `/v1/opendata/4-10` | 境外結構型商品配息資訊查詢（已到期） | empty | N | 0 |  |
| `/v1/opendata/4-11` | 境外結構型商品受託或銷售金額每月累計統計表（連結標的-股權） | empty | N | 0 |  |
| `/v1/opendata/4-12` | 境外結構型商品受託或銷售金額每月累計統計表（連結標的-利率） | empty | N | 0 |  |
| `/v1/opendata/4-13` | 境外結構型商品受託或銷售金額每月累計統計表（連結標的-匯率） | empty | N | 0 |  |
| `/v1/opendata/4-14` | 境外結構型商品受託或銷售金額每月累計統計表（連結標的-指數） | empty | N | 0 |  |
| `/v1/opendata/4-15` | 境外結構型商品受託或銷售金額每月累計統計表（連結標的-商品） | ok | N | 1 | 商品數, ﻿年月, 金額(百萬台幣) |
| `/v1/opendata/4-16` | 境外結構型商品受託或銷售金額每月累計統計表（連結標的-信用事件） | ok | N | 1 | 商品數, ﻿年月, 金額(百萬台幣) |
| `/v1/opendata/4-17` | 境外結構型商品受託或銷售金額每月累計統計表（連結標的-其他利益) | ok | N | 1 | 商品數, ﻿年月, 金額(百萬台幣) |
| `/v1/opendata/4-18` | 境外結構型商品受託或銷售金額每月累計統計表（澳幣） | empty | N | 0 |  |
| `/v1/opendata/4-19` | 境外結構型商品受託或銷售金額每月累計統計表（加幣） | empty | N | 0 |  |
| `/v1/opendata/4-2` | 境外結構型商品商品總覽 | ok | N | 35956 | 連結標的類別, 總代理, 投資人類別, ISIN_Common Code, ﻿資料日期 |
| `/v1/opendata/4-20` | 境外結構型商品受託或銷售金額每月累計統計表（人民幣） | empty | N | 0 |  |
| `/v1/opendata/4-21` | 境外結構型商品受託或銷售金額每月累計統計表（歐元） | empty | N | 0 |  |
| `/v1/opendata/4-22` | 境外結構型商品受託或銷售金額每月累計統計表（英鎊） | empty | N | 0 |  |
| `/v1/opendata/4-23` | 境外結構型商品受託或銷售金額每月累計統計表（港幣） | empty | N | 0 |  |
| `/v1/opendata/4-24` | 境外結構型商品受託或銷售金額每月累計統計表（日圓） | empty | N | 0 |  |
| `/v1/opendata/4-25` | 境外結構型商品受託或銷售金額每月累計統計表（紐西蘭幣） | empty | N | 0 |  |
| `/v1/opendata/4-26` | 境外結構型商品受託或銷售金額每月累計統計表（美元） | empty | N | 0 |  |
| `/v1/opendata/4-27` | 境外結構型商品受託或銷售金額每月累計統計表（南非幣） | empty | N | 0 |  |
| `/v1/opendata/4-28` | 境外結構型商品受託或銷售金額每月累計統計表（瑞士法郎） | empty | N | 0 |  |
| `/v1/opendata/4-29` | 境外結構型商品受託或銷售金額每月累計統計表（瑞典克朗） | empty | N | 0 |  |
| `/v1/opendata/4-3` | 境外結構型商品機構基本資料查詢 | ok | N | 78 | 機構代碼, 電話, ﻿資料日期, 公司名稱, 地址 |
| `/v1/opendata/4-4` | 境外結構型商品受託或銷售機構查詢 | ok | N | 35956 | 類別, ﻿資料日期, 受託或銷售之商品代號, 總機構代碼, 受託或銷售之商品名稱 |
| `/v1/opendata/4-5` | 境外結構型商品參考價格查詢 | ok | N | 20000 | 商品名稱, 日期, ﻿資料日期, 商品代號, 參考價格 |
| `/v1/opendata/4-6` | 境外結構型商品配息資訊查詢 | ok | N | 30004 | 商品名稱, 發行機構, 發行人/總代理人, ﻿資料日期, 配息率 |
| `/v1/opendata/4-7` | 境外結構型商品公告訊息 | empty | N | 0 |  |
| `/v1/opendata/4-8` | 境外結構型商品商品總覽（已到期） | empty | N | 0 |  |
| `/v1/opendata/4-9` | 境外結構型商品參考價格查詢（已到期） | empty | N | 0 |  |

#### 期信基金資訊

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/v1/opendata/3-30` | 境外基金基金總覽-其他基金類型 | ok | N | 12 | 基金名稱, 淨值日期, 基金種類, 投資細項, 境外基金機構 |
| `/v1/opendata/3-31` | 境外基金投資人服務及保護-反稀釋機制 | ok | N | 9628 | 更新日期, 總代理人, 日期, 內容, 備註 |
| `/v1/opendata/5-1` | 期貨信託基金總覽 | empty | N | 0 |  |
| `/v1/opendata/5-10` | 期信基金機構資訊統計 | empty | N | 0 |  |
| `/v1/opendata/5-11` | 期信基金募集統計 | empty | N | 0 |  |
| `/v1/opendata/5-12` | 期信基金銷售統計 | empty | N | 0 |  |
| `/v1/opendata/5-13` | 期貨信託基金投資概況-投資標的 | empty | N | 0 |  |
| `/v1/opendata/5-16` | 期信基金對特定人募集之基金統計表 | empty | N | 0 |  |
| `/v1/opendata/5-2` | 期貨信託基金基本資料 | empty | N | 0 |  |
| `/v1/opendata/5-3` | 期貨信託基金銷售機構資訊 | empty | N | 0 |  |
| `/v1/opendata/5-4` | 期貨信託基金淨值 | empty | N | 0 |  |
| `/v1/opendata/5-5` | 期貨信託基金投資概況 | empty | N | 0 |  |
| `/v1/opendata/5-6` | 期信事業資訊 | empty | N | 0 |  |
| `/v1/opendata/5-7` | 期信基金公告訊息查詢 | empty | N | 0 |  |
| `/v1/opendata/5-8` | 期貨信託契約 | empty | N | 0 |  |
| `/v1/opendata/5-9` | 期信基金非營業日查詢 | empty | N | 0 |  |

#### 權益證券類 統計資訊

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/v1/opendata/2-1` | 集中保管有價證券業務概況表 | ok | N | 36 | 總開戶數, 解約數, ﻿資料年月, 累計開戶數, 新開戶數 |
| `/v1/opendata/2-10` | 票券保管結算交割統計表 | ok | N | 12 | 初級市場承銷/首買, 次級市場小計, 次級市場附條件交易, ﻿資料年月, 次級市場附條件履約 |
| `/v1/opendata/2-2` | 集中保管債券收付統計表 | ok | N | 12 | 收存/登錄交付加項(張數), 付出/登錄交付減項(張數), 餘額(數量), 收存/登錄交付加項... |
| `/v1/opendata/2-22` | 有價證券集中保管個別股票異動月分析表－上市證券 | ok | N | 1342 | 股票名稱, 本月底保管千股數, 增減數額, 增減百分比, ﻿資料年月 |
| `/v1/opendata/2-23` | 有價證券集中保管個別股票異動月分析表－上櫃證券 | ok | N | 1000 | 股票名稱, 本月底保管千股數, 增減數額, 增減百分比, ﻿資料年月 |
| `/v1/opendata/2-24` | 有價證券集中保管個別股票異動月分析表－興櫃證券 | ok | N | 350 | 股票名稱, 本月底保管千股數, 增減數額, 增減百分比, ﻿資料年月 |
| `/v1/opendata/2-25` | 上市保管有價證券週餘額表 | ok | N | 31471 | 股票名稱, 增減數額, 增減比率, 上週餘額, ﻿資料日期 |
| `/v1/opendata/2-26` | 上櫃保管有價證券週餘額表 | ok | N | 10884 | 股票名稱, 增減數額, 增減比率, 上週餘額, ﻿資料日期 |
| `/v1/opendata/2-27` | 上櫃保管有價證券週餘額表 | ok | N | 349 | 股票名稱, 增減數額, 增減比率, 上週餘額, ﻿資料日期 |
| `/v1/opendata/2-28` | 上市櫃檯合併保管有價證券週餘額表 | ok | N | 42707 | 股票名稱, 增減數額, 增減比率, 上週餘額, ﻿資料日期 |
| `/v1/opendata/2-29` | 上市櫃檯合併保管有價證券週餘額表 | ok | N | 2002 | 股票名稱, 增減數額, 增減比率, 上週餘額, ﻿資料日期 |
| `/v1/opendata/2-3` | 集中保管債券收付統計表 | ok | N | 12 | 實體保管(佔總保管股數比例), 總保管股數(上市櫃股數), 總保管股數(合計), 實體保管(張... |
| `/v1/opendata/2-39` | 境外結構型商品受託或銷售金額每月累計統計表 | ok | N | 1 | 商品數, ﻿年月, 金額 |
| `/v1/opendata/2-4` | 集中保管有價證券帳簿劃撥統計表 | ok | N | 12 | 興櫃證券平均每日成交量, 店頭議價債券平均每日成交金額, ﻿資料年月, 上櫃證券平均每日成交量... |
| `/v1/opendata/2-41` | 集中保管ETF月分析表 | ok | N | 339 | 增減數額, 發行單位數, 證券名稱, 證券代號, 增減百分比 |
| `/v1/opendata/2-42` | 集中保管開放式受益憑證月分析表 | ok | N | 3 | 增減數額, 增減百分比, ﻿資料年月, 開放式受益憑證名稱, 本月底保管數 |
| `/v1/opendata/2-43` | 集中保管黃金現貨月分析表 | ok | N | 2 | 黃金現貨名稱, ﻿資料年月, 集保戶數, 黃金現貨代號 |
| `/v1/opendata/2-44` | 集中保管TDR月分析表 | ok | N | 11 | 增減數額, 發行單位數, 證券名稱, 證券代號, 增減百分比 |
| `/v1/opendata/2-5` | 帳簿劃撥配發新股統計表 | ok | N | 12 | 家次, 簽約家數, ﻿資料年月, 戶次, 股數 |
| `/v1/opendata/2-6` | 集中保管有價證券帳簿劃撥設質交付統計表 | ok | N | 12 | 設質餘額(股數), 質權設定(股數), 質權解除/實行質權(股數), ﻿資料年月, 質權解除/... |
| `/v1/opendata/2-7` | 境外基金交易平台業務量統計表 | ok | N | 12 | 轉換(筆數), ﻿資料年月, 申購(筆數), 申購(金額), 轉換(金額) |
| `/v1/opendata/2-8` | 可轉換公司債月分析表 | ok | N | 369 | 增減數額, 可轉換公司債代號, 增減百分比, 發行張數, ﻿資料年月 |
| `/v1/opendata/2-9` | 認購售權證月分析表 | ok | N | 40359 | 增減數額, 發行單位數, 增減百分比, 認購售權證代號, ﻿資料年月 |

#### 股務資訊

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/v1/opendata/1-1` | 證券基本資料 | ok | N | 144462 | ﻿證券代號, 每股面額(元), 更新日期, 證券名稱, 限制部分帳簿劃撥功能註記 |
| `/v1/opendata/1-10` | 私募有價證券無實體登錄資料查詢：特別股 | ok | N | 11 | 特別股代號, ﻿資料日期, 特別股名稱, 登錄數額 |
| `/v1/opendata/1-11` | 私募有價證券無實體登錄資料查詢：公司債 | ok | N | 2 | 公司債券代號, ﻿資料日期, 公司債券名稱, 登錄數額 |
| `/v1/opendata/1-12` | 私募有價證券無實體登錄資料查詢：轉換公司債 | ok | N | 13 | 轉換公司債券代號, ﻿資料日期, 轉換公司債券名稱, 登錄數額 |
| `/v1/opendata/1-13` | 有價證券轉(交)換/認股價格變更資料查詢 | ok | N | 346 | 證券名稱, 證券代號, 轉(交)換後證券代號, ﻿資料日期, 轉(交)換價格 |
| `/v1/opendata/1-14` | 有價證券董事收購相關資訊 | ok | N | 1 | 收購起日, 收購迄日, 證券名稱, 證券代號, 收購價格 |
| `/v1/opendata/1-2` | 公司股務單位資料 | ok | N | 142036 | 證券名稱, 證券代號, 電話, ﻿資料日期, 市場別 |
| `/v1/opendata/1-3` | 固定收益證券發行資料 | ok | N | 4973 | 發行機構名稱, 債券代號, 債券簡稱, ﻿資料日期, 發行辦法檔案網址(http://www.... |
| `/v1/opendata/1-4` | 發行人董監分戶保管 | ok | N | 99 | 強制集保總股數, 證券名稱, 發行仟股數, 證券代號, ﻿資料日期 |
| `/v1/opendata/1-5` | 集保戶股權分散表 | ok | N | 67813 | 證券代號, 占集保庫存數比例%, 人數, ﻿資料日期, 股數 |
| `/v1/opendata/1-6` | 債券持有對象分析 | ok | N | 2980 | 債券代號, 法人戶持有比率, 自營商持有比率, 其他持有比率, ﻿資料年月 |
| `/v1/opendata/1-7` | 有價證券帳簿劃撥配發交付日期一覽表 | ok | N | 634 | ﻿證券代號, 證券名稱, 交付原因, 交付日期 |
| `/v1/opendata/1-8-1` | 債券基本資料 | ok | N | 4398 | 發行日期, 利率別, 登錄機構, 債券簡稱, ﻿資料日期 |
| `/v1/opendata/1-8-2` | 債券還本付息明細資料 | ok | N | 67419 | 還本付息日, 付息金額, 債券代號, 還本金額, 實際付款日 |
| `/v1/opendata/1-9` | 私募有價證券無實體登錄資料查詢：普通股 | ok | N | 354 | 證券名稱, 證券代號, ﻿資料日期, 登錄數額 |

#### 股東e票通

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/v1/opendata/6-1` | 股東常會電子投票公司資訊 | empty | N | 0 |  |
| `/v1/opendata/6-2` | 股東臨時會電子投票公司資訊 | empty | N | 0 |  |
| `/v1/opendata/6-3` | 發行公司電子投票比率統計資訊 | empty | N | 0 |  |

## J-Quants API (JPX official)

### OpenAPI (28 endpoints)

#### Bulk

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/bulk/get` | Get File Download URL（CSV ファイル取得 URL） | skipped | N | 0 | url |
| `/bulk/list` | List of Downloadable Files（CSV 一括DL可能ファイル一覧） | ok | N | 125 | Key, LastModified, Size |

#### Derivatives

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/derivatives/bars/daily/futures` | Futures OHLC（先物四本値） | skipped | Y | 0 | Code, ProdCat, Date, O, H |
| `/derivatives/bars/daily/options` | Options OHLC（オプション四本値） | skipped | Y | 0 | Code, ProdCat, UndSSO, Date, O |
| `/derivatives/bars/daily/options/225` | Nikkei 225 Index Option OHLC（日経225オプション四本値） | ok | Y | 8494 | Date, Code, O, H, L |

#### EDINET

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/edinet/cross-shareholdings` | Cross-Shareholdings from EDINET（政策保有株式，有報由来） | ok | Y | 130 | DocId, Code, EdinetCode, FilerName, FilerNameEn |
| `/edinet/major-shareholders` | Major Shareholders from EDINET（大株主状況，有報由来） | ok | Y | 181 | DocId, Code, EdinetCode, FilerName, FilerNameEn |

#### Equities

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/equities/bars/daily` | Stock Prices OHLC（株価四本値，含調整價與 AdjFactor） | ok | Y | 4451 | Date, Code, O, H, L |
| `/equities/bars/daily/am` | Morning Session Stock Prices（前場四本値） | skipped | Y | 0 | Date, Code, MO, MH, ML |
| `/equities/bars/minute` | Minute Stock Prices OHLC（分足） | skipped | Y | 0 | Date, Time, Code, O, H |
| `/equities/earnings-calendar` | Earnings Calendar（決算発表予定日） | ok | N | 14 | Date, Code, CoName, FY, SectorNm |
| `/equities/investor-types` | Trading by Type of Investors（投資部門別売買状況，週次） | ok | Y | 223 | PubDate, StDate, EnDate, Section, PropSell |
| `/equities/master` | Listed Issue Master（上場銘柄一覧，point-in-time） | ok | Y | 4451 | Date, Code, CoName, CoNameEn, S17 |
| `/equities/trades` | Stock Prices Tick（ティックデータ） | skipped | Y | 0 |  |

#### Financials

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/fins/details` | Financial Statement Data BS/PL/CF（財務諸表明細） | skipped | Y | 0 | DiscDate, DiscTime, Code, DiscNo, DocType |
| `/fins/dividend` | Cash Dividend Data（配当金明細） | skipped | Y | 0 | PubDate, PubTime, Code, RefNo, StatCode |
| `/fins/summary` | Financial Data Summary（決算短信サマリ財務情報） | ok | Y | 19 | DiscDate, DiscTime, Code, DiscNo, DocType |

#### Indices

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/indices/bars/daily` | Indices OHLC（指数四本値） | ok | Y | 79 | Date, Code, O, H, L |
| `/indices/bars/daily/topix` | TOPIX Prices OHLC（TOPIX指数四本値） | ok | Y | 2441 | Date, O, H, L, C |

#### Markets

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/markets/breakdown` | Breakdown Trading Data(売買内訳データ) | skipped | Y | 0 | Date, Code, LongSellVa, ShrtNoMrgnVa, MrgnSellN... |
| `/markets/calendar` | Trading Calendar（取引カレンダー） | ok | Y | 4195 | Date, HolDiv |
| `/markets/margin-alert` | Margin Trading Outstanding — daily publication（日々公表信用取引残高） | ok | Y | 293 | PubDate, Code, AppDate, PubReason, ShrtOut |
| `/markets/margin-interest` | Margin Trading Outstandings（信用取引週末残高） | ok | Y | 4257 | Date, Code, ShrtVol, LongVol, ShrtNegVol |
| `/markets/short-ratio` | Short Sale Value and Ratio by Sector（業種別空売り比率） | ok | Y | 34 | Date, S33, SellExShortVa, ShrtWithResVa, ShrtNo... |
| `/markets/short-sale-report` | Outstanding Short Selling Positions（空売り残高報告，≥0.5% 部位） | ok | Y | 794 | DiscDate, CalcDate, Code, SSName, SSAddr |

#### TDnet

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/td/bulk` | TDnet/Company Disclosure Index CSV Download（インデックス一括DL） | skipped | N | 0 | lastUpdated, url |
| `/td/files` | TDnet/Company Disclosure Files（開示資料ファイル取得） | skipped | N | 0 | discNo, files, files.pdf, files.summaryPdf, fil... |
| `/td/list` | TDnet/Company Disclosure Index List（適時開示インデックス一覧） | skipped | Y | 0 | DiscNo, Code, Name, DiscDate, DiscTime |

## EDINET API v2 (Financial Services Agency)

### OpenAPI (28 endpoints)

#### 半期報告書

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/documents/{docID}?type=1#docTypeCode=160` | 半期報告書 — XBRL 取得 | ok | Y | 27 |  |
| `/documents/{docID}?type=2#docTypeCode=160` | 半期報告書 — PDF 取得 | ok | Y | 47 |  |
| `/documents/{docID}?type=5#docTypeCode=160` | 半期報告書 — CSV 取得 | ok | Y | 27 |  |

#### 四半期報告書

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/documents/{docID}?type=1#docTypeCode=140` | 四半期報告書 — XBRL 取得 | empty | Y | 0 |  |
| `/documents/{docID}?type=2#docTypeCode=140` | 四半期報告書 — PDF 取得 | empty | Y | 0 |  |
| `/documents/{docID}?type=5#docTypeCode=140` | 四半期報告書 — CSV 取得 | empty | Y | 0 |  |

#### 大量保有報告書

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/documents/{docID}?type=1#docTypeCode=350` | 大量保有報告書 — XBRL 取得 | ok | Y | 305 |  |
| `/documents/{docID}?type=2#docTypeCode=350` | 大量保有報告書 — PDF 取得 | ok | Y | 305 |  |
| `/documents/{docID}?type=5#docTypeCode=350` | 大量保有報告書 — CSV 取得 | ok | Y | 305 |  |

#### 書類一覧

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/documents.json` | 書類一覧 API（提出書類一覧及びメタデータ） | ok | Y | 2051 | seqNumber, docID, edinetCode, secCode, JCN |

#### 有価証券報告書

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/documents/{docID}?type=1#docTypeCode=120` | 有価証券報告書 — XBRL 取得 | ok | Y | 102 |  |
| `/documents/{docID}?type=2#docTypeCode=120` | 有価証券報告書 — PDF 取得 | ok | Y | 170 |  |
| `/documents/{docID}?type=5#docTypeCode=120` | 有価証券報告書 — CSV 取得 | ok | Y | 102 | 要素ID, 項目名, コンテキストID, 相対年度, 連結・個別 |

#### 臨時報告書

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/documents/{docID}?type=1#docTypeCode=180` | 臨時報告書 — XBRL 取得 | ok | Y | 820 |  |
| `/documents/{docID}?type=2#docTypeCode=180` | 臨時報告書 — PDF 取得 | ok | Y | 824 |  |
| `/documents/{docID}?type=5#docTypeCode=180` | 臨時報告書 — CSV 取得 | ok | Y | 820 |  |

#### 訂正半期報告書

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/documents/{docID}?type=1#docTypeCode=170` | 訂正半期報告書 — XBRL 取得 | ok | Y | 2 |  |
| `/documents/{docID}?type=2#docTypeCode=170` | 訂正半期報告書 — PDF 取得 | ok | Y | 2 |  |
| `/documents/{docID}?type=5#docTypeCode=170` | 訂正半期報告書 — CSV 取得 | ok | Y | 2 |  |

#### 訂正四半期報告書

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/documents/{docID}?type=1#docTypeCode=150` | 訂正四半期報告書 — XBRL 取得 | ok | Y | 1 |  |
| `/documents/{docID}?type=2#docTypeCode=150` | 訂正四半期報告書 — PDF 取得 | ok | Y | 1 |  |
| `/documents/{docID}?type=5#docTypeCode=150` | 訂正四半期報告書 — CSV 取得 | ok | Y | 1 |  |

#### 訂正大量保有報告書

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/documents/{docID}?type=1#docTypeCode=360` | 訂正大量保有報告書 — XBRL 取得 | ok | Y | 34 |  |
| `/documents/{docID}?type=2#docTypeCode=360` | 訂正大量保有報告書 — PDF 取得 | ok | Y | 34 |  |
| `/documents/{docID}?type=5#docTypeCode=360` | 訂正大量保有報告書 — CSV 取得 | ok | Y | 34 |  |

#### 訂正有価証券報告書

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/documents/{docID}?type=1#docTypeCode=130` | 訂正有価証券報告書 — XBRL 取得 | ok | Y | 31 |  |
| `/documents/{docID}?type=2#docTypeCode=130` | 訂正有価証券報告書 — PDF 取得 | ok | Y | 33 |  |
| `/documents/{docID}?type=5#docTypeCode=130` | 訂正有価証券報告書 — CSV 取得 | ok | Y | 31 |  |

## TDnet Timely Disclosure (Tokyo Stock Exchange)

### Web (8 endpoints)

#### 檔案取得

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/inbs/0812{YYYYMMDD}{seq}.zip` | 決算短信等 XBRL zip 取得（XBRLData/Summary＋Attachment） | ok | Y | 11 | XBRLData/Summary/tse-*-ixbrl.htm, XBRLData/Summ... |
| `/inbs/1401{YYYYMMDD}{seq}.pdf` | 開示資料 PDF 取得（一覧/検索結果的表題連結） | ok | Y | 100 |  |

#### 開示一覧

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/inbs/I_list_{page}_{YYYYMMDD}.html` | 指定日開示一覧（每頁 100 件，頁碼 001 起） | ok | Y | 170 | 時刻, コード, 会社名, 表題, XBRL |
| `/inbs/I_main_00.html` | 適時開示閲覧サービス首頁（嵌入本日最新一覧） | ok | N | 1 |  |

#### 開示検索

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/onsf/TDJFSearch/TDJFSearch#facet=code` | 開示検索 — 按銘柄コード | ok | Y | 1 | 時刻, コード, 会社名, 表題, XBRL |
| `/onsf/TDJFSearch/TDJFSearch#facet=code-window` | 開示検索 — 按銘柄コード（全 31 天窗，個股開示歷史） | ok | Y | 1 | 時刻, コード, 会社名, 表題, XBRL |
| `/onsf/TDJFSearch/TDJFSearch#facet=company` | 開示検索 — 按会社名 | ok | Y | 1 | 時刻, コード, 会社名, 表題, XBRL |
| `/onsf/TDJFSearch/TDJFSearch#facet=disclosure-type` | 開示検索 — 按開示種別キーワード（如「決算短信」） | ok | Y | 484 | 時刻, コード, 会社名, 表題, XBRL |

## Japan Exchange Group statistics (JPX)

### Web (166 endpoints)

#### ETF受益者情報調査

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `...tistics-equities/examination/02.html#ETF*-j.pdf` | ETF受益者情報調査 — ETF*-j.pdf | ok | Y | 1 |  |
| `...tatistics-equities/examination/02.html#ETF*.xls` | ETF受益者情報調査 — ETF*.xls | ok | Y | 33 | 表 １, 所有者別受益者数, 1ページ |
| `...atistics-equities/examination/02.html#ETF*.xlsx` | ETF受益者情報調査 — ETF*.xlsx | ok | Y | 22 | 表 １, 所有者別受益者数, Number of Beneficiaries by Holde... |
| `...atistics-equities/examination/02.html#ETF*j.pdf` | ETF受益者情報調査 — ETF*j.pdf | ok | Y | 1 |  |
| `...istics-equities/examination/02.html#ETF_*-j.pdf` | ETF受益者情報調査 — ETF_*-j.pdf | ok | Y | 1 |  |
| `...atistics-equities/examination/02.html#ETF_*.xls` | ETF受益者情報調査 — ETF_*.xls | ok | Y | 34 | 表 １, 所有者別受益者数, 1ページ |
| `...atistics-equities/examination/02.html#jETF*.pdf` | ETF受益者情報調査 — jETF*.pdf | ok | Y | 1 |  |
| `...tistics-equities/examination/02.html#jETF_*.pdf` | ETF受益者情報調査 — jETF_*.pdf | ok | Y | 1 |  |

#### REIT投資主情報調査

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `...istics-equities/examination/03.html#REIT*-j.pdf` | REIT投資主情報調査 — REIT*-j.pdf | ok | Y | 1 |  |
| `...atistics-equities/examination/03.html#REIT*.xls` | REIT投資主情報調査 — REIT*.xls | ok | Y | 33 | 表 １, 所有者別投資主数, 1ページ |
| `...tistics-equities/examination/03.html#REIT*.xlsx` | REIT投資主情報調査 — REIT*.xlsx | ok | Y | 41 | 表 １, 所有者別投資主数, 1ページ |
| `...stics-equities/examination/03.html#REIT*_HP.pdf` | REIT投資主情報調査 — REIT*_HP.pdf | ok | Y | 1 |  |
| `...stics-equities/examination/03.html#REIT_*-j.pdf` | REIT投資主情報調査 — REIT_*-j.pdf | ok | Y | 1 |  |

#### プログラム売買・裁定取引

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/markets/statistics-equities/program/01.html#*.pdf` | プログラム売買 — *.pdf | ok | Y | 1 |  |
| `/markets/statistics-equities/program/01.html#*.xls` | プログラム売買 — *.xls | ok | Y | 46 | 株　　数, 353605, 410799, 28781, 27864 |
| `.../statistics-equities/program/01.html#gaiyou.pdf` | プログラム売買 — gaiyou.pdf | ok | N | 1 |  |
| `...ts/statistics-equities/program/index.html#*.pdf` | 裁定取引 — *.pdf | ok | Y | 1 |  |
| `...ts/statistics-equities/program/index.html#*.xls` | 裁定取引 — *.xls | ok | Y | 43 | 株　　数, 10172, 4909, 15081, 671476 |

#### 上場会社資金調達額

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `...tics-equities/misc/06.html#historical-sikin.xls` | 上場会社資金調達額 — historical-sikin.xls | ok | N | 340 | 1998-01-31 00:00:00, －, －, －, － |

#### 上場投資信託（ETF）

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `...stics-equities/investor-type/02.html#etf_m*.pdf` | 月間 — etf_m*.pdf | ok | Y | 1 |  |
| `...stics-equities/investor-type/02.html#etf_m*.xls` | 月間 — etf_m*.xls | ok | Y | 63 | Proprietary, 買い, Purchases, 2,317,248, 3.71 |
| `...tor-type/02.html#revision_information_etf_j.xls` | 月間 — revision_information_etf_j.xls | ok | N | 3 | 訂正日付, 対象資料, 対象商品, 対象データ |

#### 不動産投資信託証券（REIT）

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `...tics-equities/investor-type/03.html#reit_m*.pdf` | 月間 — reit_m*.pdf | ok | Y | 1 |  |
| `...tics-equities/investor-type/03.html#reit_m*.xls` | 月間 — reit_m*.xls | ok | Y | 63 | Proprietary, 買い, Purchases, 2,248,980, 22.47 |

#### 信用取引残高等

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `...cs-equities/margin/01.html#Premium_Charges.xlsx` | 品貸料 — Premium_Charges.xlsx | ok | N | 1054 | 約定日 Trade Date, コード Code, 銘柄名 Issue Name, 取引所区分... |
| `...tistics-equities/margin/02.html#tvdivq*ttjj.pdf` | 信用取引売買比率 — tvdivq*ttjj.pdf | ok | Y | 1 |  |
| `...tatistics-equities/margin/03.html#mtgaisan*.pdf` | 信用取引現在高(一般信用取引・制度信用取引別) — mtgaisan*.pdf | ok | Y | 1 |  |
| `...tatistics-equities/margin/03.html#mtgaisan*.xls` | 信用取引現在高(一般信用取引・制度信用取引別) — mtgaisan*.xls | ok | Y | 29 | 合計, 東京 Tokyo, 株数 Shs., 498570, 60598 |
| `...tistics-equities/margin/03.html#t13vrt*chwn.pdf` | 信用取引現在高(一般信用取引・制度信用取引別) — t13vrt*chwn.pdf | ok | Y | 1 |  |
| `...tistics-equities/margin/03.html#t13vrt*ixc8.pdf` | 信用取引現在高(一般信用取引・制度信用取引別) — t13vrt*ixc8.pdf | ok | Y | 1 |  |
| `...tatistics-equities/margin/04.html#mtseisan*.pdf` | 信用取引現在高 — mtseisan*.pdf | ok | Y | 1 |  |
| `...tatistics-equities/margin/04.html#mtseisan*.xls` | 信用取引現在高 — mtseisan*.xls | ok | Y | 38 | 二市場計 Total, 株数Shs., 370571, 59597, 3939461 |
| `...tistics-equities/margin/04.html#t13vrt*chxp.pdf` | 信用取引現在高 — t13vrt*chxp.pdf | ok | Y | 1 |  |
| `...tistics-equities/margin/04.html#t13vrt*ixdk.pdf` | 信用取引現在高 — t13vrt*ixdk.pdf | ok | Y | 1 |  |
| `...tatistics-equities/margin/05.html#syumatsu*.pdf` | 銘柄別信用取引週末残高 — syumatsu*.pdf | ok | Y | 1 |  |
| `...tistics-equities/margin/05.html#t13vrt*ci1v.pdf` | 銘柄別信用取引週末残高 — t13vrt*ci1v.pdf | ok | Y | 1 |  |
| `...tistics-equities/margin/05.html#t13vrt*ixeg.pdf` | 銘柄別信用取引週末残高 — t13vrt*ixeg.pdf | ok | Y | 1 |  |
| `.../statistics-equities/margin/06.html#tvdivq*.pdf` | 信用取引現在高　過去推移表 — tvdivq*.pdf | ok | Y | 1 |  |
| `.../statistics-equities/margin/06.html#tvdivq*.xls` | 信用取引現在高　過去推移表 — tvdivq*.xls | ok | Y | 1218 | 2002-08-02 00:00:00, 784204, 562477, 2613903, 1... |
| `...statistics-equities/margin/06.html#tvdivq*x.pdf` | 信用取引現在高　過去推移表 — tvdivq*x.pdf | ok | Y | 1 |  |
| `...statistics-equities/margin/06.html#tvdivq*z.xls` | 信用取引現在高　過去推移表 — tvdivq*z.xls | ok | Y | 1217 | 2002-08-02 00:00:00, 1254269, 1004839, 2615658,... |
| `...tistics-equities/margin/07.html#nlsgeu*octp.pdf` | 公表スケジュール — nlsgeu*octp.pdf | ok | Y | 1 |  |
| `...istics-equities/margin/index.html#mtdailyk*.pdf` | 個別銘柄信用取引残高表 — mtdailyk*.pdf | ok | Y | 1 |  |
| `...istics-equities/margin/index.html#mtdailyk*.xls` | 個別銘柄信用取引残高表 — mtdailyk*.xls | ok | Y | 236 | B, 日, 株, イメージ　ワン　普通株式, スタンダード |
| `...tics-equities/margin/index.html#t13vrt*coh2.pdf` | 個別銘柄信用取引残高表 — t13vrt*coh2.pdf | ok | Y | 1 |  |
| `...tics-equities/margin/index.html#t13vrt*ix4e.pdf` | 個別銘柄信用取引残高表 — t13vrt*ix4e.pdf | ok | Y | 1 |  |

#### 市場別時価総額

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `...tics-equities/misc/02.html#historical-jika.xlsx` | 市場別時価総額 — historical-jika.xlsx | ok | N | 51 | 月末 End of Month, プライム Prime, スタンダード Standard, グ... |

#### 従業員持株会状況調査

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `...ics-equities/examination/04.html#employee_*.pdf` | 従業員持株会状況調査 — employee_*.pdf | ok | Y | 1 |  |
| `...equities/examination/04.html#employee_*.pdf.pdf` | 従業員持株会状況調査 — employee_*.pdf.pdf | ok | Y | 1 |  |
| `...cs-equities/examination/04.html#employee_18.pdf` | 従業員持株会状況調査 — employee_18.pdf | ok | N | 1 |  |
| `...cs-equities/examination/04.html#employee_19.pdf` | 従業員持株会状況調査 — employee_19.pdf | ok | N | 1 |  |
| `...cs-equities/examination/04.html#employee_20.pdf` | 従業員持株会状況調査 — employee_20.pdf | ok | N | 1 |  |

#### 投資部門別売買状況

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `...tics-equities/investor-type/06.html#stock_*.pdf` | 資料の見方 — stock_*.pdf | ok | Y | 1 |  |

#### 時価総額順位表

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/markets/statistics-equities/misc/08.html#*-j.pdf` | 時価総額順位表 — *-j.pdf | ok | Y | 1 |  |
| `/markets/statistics-equities/misc/08.html#*_r.pdf` | 時価総額順位表 — *_r.pdf | ok | Y | 1 |  |

#### 東京証券取引所日報

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/markets/statistics-equities/daily/03.html#*.pdf` | 株価情報（過去分） — *.pdf | ok | Y | 1 |  |
| `.../statistics-equities/daily/index.html#boq_*.pdf` | 東京証券取引所日報 — boq_*.pdf | ok | Y | 1 |  |
| `...tistics-equities/daily/index.html#est-set_*.pdf` | 東京証券取引所日報 — est-set_*.pdf | ok | Y | 1 |  |
| `.../statistics-equities/daily/index.html#stq_*.pdf` | 東京証券取引所日報 — stq_*.pdf | ok | Y | 1 |  |

#### 東証上場銘柄一覧

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `...ets/statistics-equities/misc/01.html#data_j.xls` | 東証上場銘柄一覧 — data_j.xls | ok | N | 4437 | 日付, コード, 銘柄名, 市場・商品区分, 33業種コード |

#### 株価平均・株式平均利回り

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `...s-equities/misc/03.html#JPChangeStockPrices.pdf` | 株価平均・株式平均利回り — JPChangeStockPrices.pdf | ok | N | 1 |  |
| `...tistics-equities/misc/03.html#historical-sp.xls` | 株価平均・株式平均利回り — historical-sp.xls | ok | N | 50 | 2022-04-30 00:00:00, 2328.23, 2411.55, 783.6, 1... |
| `...atistics-equities/misc/03.html#historical-y.xls` | 株価平均・株式平均利回り — historical-y.xls | ok | N | 50 | 2022-04-30 00:00:00, 1.88, 2.03, 2.03, 2.05 |

#### 株式

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `...s-equities/investor-type/00-01.html#kiroku*.pdf` | 月間 — kiroku*.pdf | ok | Y | 1 |  |
| `...ies/investor-type/00-01.html#stock_val_1_m*.pdf` | 月間 — stock_val_1_m*.pdf | ok | Y | 1 |  |
| `...ies/investor-type/00-01.html#stock_val_1_m*.xls` | 月間 — stock_val_1_m*.xls | ok | Y | 64 | Proprietary, 買い, Purchases, 21,112,795,829, 8.2 |
| `...ies/investor-type/00-01.html#stock_vol_1_m*.pdf` | 月間 — stock_vol_1_m*.pdf | ok | Y | 1 |  |
| `...ies/investor-type/00-01.html#stock_vol_1_m*.xls` | 月間 — stock_vol_1_m*.xls | ok | Y | 65 | 自己計, 売り, Sales, 6,693,289, 11.7 |
| `...-equities/investor-type/00-02.html#kiroku25.pdf` | 年間 — kiroku25.pdf | ok | N | 1 |  |
| `...es/investor-type/00-02.html#stock_val_1_y16.pdf` | 年間 — stock_val_1_y16.pdf | ok | N | 1 |  |
| `...es/investor-type/00-02.html#stock_val_1_y16.xls` | 年間 — stock_val_1_y16.xls | ok | N | 64 | Proprietary, 買い, Purchases, 101,701,677,122, 16.2 |
| `...es/investor-type/00-02.html#stock_val_1_y17.pdf` | 年間 — stock_val_1_y17.pdf | ok | N | 1 |  |
| `...es/investor-type/00-02.html#stock_val_1_y17.xls` | 年間 — stock_val_1_y17.xls | ok | N | 64 | Proprietary, 買い, Purchases, 113,270,673,801, 17.0 |
| `...es/investor-type/00-02.html#stock_val_1_y18.pdf` | 年間 — stock_val_1_y18.pdf | ok | N | 1 |  |
| `...es/investor-type/00-02.html#stock_val_1_y18.xls` | 年間 — stock_val_1_y18.xls | ok | N | 64 | Proprietary, 買い, Purchases, 117,834,602,837, 16.3 |
| `...es/investor-type/00-02.html#stock_val_1_y19.pdf` | 年間 — stock_val_1_y19.pdf | ok | N | 1 |  |
| `...es/investor-type/00-02.html#stock_val_1_y19.xls` | 年間 — stock_val_1_y19.xls | ok | N | 64 | Proprietary, 買い, Purchases, 96,111,439,756, 16.4 |
| `...es/investor-type/00-02.html#stock_val_1_y20.pdf` | 年間 — stock_val_1_y20.pdf | ok | N | 1 |  |
| `...es/investor-type/00-02.html#stock_val_1_y20.xls` | 年間 — stock_val_1_y20.xls | ok | N | 64 | Proprietary, 買い, Purchases, 92,685,814,447, 14.1 |
| `...es/investor-type/00-02.html#stock_val_1_y21.pdf` | 年間 — stock_val_1_y21.pdf | ok | N | 1 |  |
| `...es/investor-type/00-02.html#stock_val_1_y21.xls` | 年間 — stock_val_1_y21.xls | ok | N | 64 | Proprietary, 買い, Purchases, 104,849,244,849, 13.9 |
| `...es/investor-type/00-02.html#stock_val_1_y22.pdf` | 年間 — stock_val_1_y22.pdf | ok | N | 1 |  |
| `...es/investor-type/00-02.html#stock_val_1_y22.xls` | 年間 — stock_val_1_y22.xls | ok | N | 65 | 自己計, 売り, Sales, 82,384,335,251, 13.7 |
| `...es/investor-type/00-02.html#stock_val_1_y23.pdf` | 年間 — stock_val_1_y23.pdf | ok | N | 1 |  |
| `...es/investor-type/00-02.html#stock_val_1_y23.xls` | 年間 — stock_val_1_y23.xls | ok | N | 64 | Proprietary, 買い, Purchases, 110,665,536,872, 11.9 |
| `...es/investor-type/00-02.html#stock_val_1_y24.pdf` | 年間 — stock_val_1_y24.pdf | ok | N | 1 |  |
| `...es/investor-type/00-02.html#stock_val_1_y24.xls` | 年間 — stock_val_1_y24.xls | ok | N | 64 | Proprietary, 買い, Purchases, 133,891,949,881, 10.8 |
| `...es/investor-type/00-02.html#stock_val_1_y25.pdf` | 年間 — stock_val_1_y25.pdf | ok | N | 1 |  |
| `...es/investor-type/00-02.html#stock_val_1_y25.xls` | 年間 — stock_val_1_y25.xls | ok | N | 65 | 自己計, 売り, Sales, 155,701,993,283, 11.1 |
| `...es/investor-type/00-02.html#stock_vol_1_y16.pdf` | 年間 — stock_vol_1_y16.pdf | ok | N | 1 |  |
| `...es/investor-type/00-02.html#stock_vol_1_y16.xls` | 年間 — stock_vol_1_y16.xls | ok | N | 64 | Proprietary, 買い, Purchases, 82,913,489, 14.6 |
| `...es/investor-type/00-02.html#stock_vol_1_y17.pdf` | 年間 — stock_vol_1_y17.pdf | ok | N | 1 |  |
| `...es/investor-type/00-02.html#stock_vol_1_y17.xls` | 年間 — stock_vol_1_y17.xls | ok | N | 64 | Proprietary, 買い, Purchases, 67,934,776, 14.4 |
| `...es/investor-type/00-02.html#stock_vol_1_y18.pdf` | 年間 — stock_vol_1_y18.pdf | ok | N | 1 |  |
| `...es/investor-type/00-02.html#stock_vol_1_y18.xls` | 年間 — stock_vol_1_y18.xls | ok | N | 64 | Proprietary, 買い, Purchases, 54,859,072, 14.0 |
| `...es/investor-type/00-02.html#stock_vol_1_y19.pdf` | 年間 — stock_vol_1_y19.pdf | ok | N | 1 |  |
| `...es/investor-type/00-02.html#stock_vol_1_y19.xls` | 年間 — stock_vol_1_y19.xls | ok | N | 64 | Proprietary, 買い, Purchases, 47,496,621, 14.8 |
| `...es/investor-type/00-02.html#stock_vol_1_y20.pdf` | 年間 — stock_vol_1_y20.pdf | ok | N | 1 |  |
| `...es/investor-type/00-02.html#stock_vol_1_y20.xls` | 年間 — stock_vol_1_y20.xls | ok | N | 64 | Proprietary, 買い, Purchases, 46,679,201, 13.0 |
| `...es/investor-type/00-02.html#stock_vol_1_y21.pdf` | 年間 — stock_vol_1_y21.pdf | ok | N | 1 |  |
| `...es/investor-type/00-02.html#stock_vol_1_y21.xls` | 年間 — stock_vol_1_y21.xls | ok | N | 64 | Proprietary, 買い, Purchases, 42,196,953, 12.8 |
| `...es/investor-type/00-02.html#stock_vol_1_y22.pdf` | 年間 — stock_vol_1_y22.pdf | ok | N | 1 |  |
| `...es/investor-type/00-02.html#stock_vol_1_y22.xls` | 年間 — stock_vol_1_y22.xls | ok | N | 65 | 自己計, 売り, Sales, 33,717,269, 13.5 |
| `...es/investor-type/00-02.html#stock_vol_1_y23.pdf` | 年間 — stock_vol_1_y23.pdf | ok | N | 1 |  |
| `...es/investor-type/00-02.html#stock_vol_1_y23.xls` | 年間 — stock_vol_1_y23.xls | ok | N | 64 | Proprietary, 買い, Purchases, 45,816,873, 12.1 |
| `...es/investor-type/00-02.html#stock_vol_1_y24.pdf` | 年間 — stock_vol_1_y24.pdf | ok | N | 1 |  |
| `...es/investor-type/00-02.html#stock_vol_1_y24.xls` | 年間 — stock_vol_1_y24.xls | ok | N | 64 | Proprietary, 買い, Purchases, 54,088,040, 10.7 |
| `...es/investor-type/00-02.html#stock_vol_1_y25.pdf` | 年間 — stock_vol_1_y25.pdf | ok | N | 1 |  |
| `...es/investor-type/00-02.html#stock_vol_1_y25.xls` | 年間 — stock_vol_1_y25.xls | ok | N | 65 | 自己計, 売り, Sales, 65,977,074, 11.5 |
| `...s-equities/investor-type/index.html#kiroku*.pdf` | 週間 — kiroku*.pdf | ok | Y | 1 |  |
| `...stor-type/index.html#revision_information_j.xls` | 週間 — revision_information_j.xls | ok | N | 19 | 訂正日付, 対象資料, 対象商品, 対象データ, 対象市場 |
| `...ties/investor-type/index.html#stock_val_1_*.pdf` | 週間 — stock_val_1_*.pdf | ok | Y | 1 |  |
| `...ties/investor-type/index.html#stock_val_1_*.xls` | 週間 — stock_val_1_*.xls | ok | Y | 64 | Proprietary, 買い, Purchases, 5,197,495,592, 7.8 |
| `...ties/investor-type/index.html#stock_vol_1_*.pdf` | 週間 — stock_vol_1_*.pdf | ok | Y | 1 |  |
| `...ties/investor-type/index.html#stock_vol_1_*.xls` | 週間 — stock_vol_1_*.xls | ok | Y | 65 | 自己計, 売り, Sales, 1,714,199, 11.8 |

#### 株式分布状況調査

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `...stics-equities/examination/01.html#j-bunpu*.pdf` | 株式分布状況調査 — j-bunpu*.pdf | ok | Y | 1 |  |
| `...tics-equities/examination/01.html#j-bunpu*.xlsx` | 株式分布状況調査 — j-bunpu*.xlsx | ok | Y | 22 | 表 １, 所有者別株主数, 2 |

#### 業種別時価総額

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/markets/statistics-equities/misc/07.html#*.pdf` | 業種別時価総額 — *.pdf | ok | Y | 1 |  |

#### 決算短信集計結果

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `...s-equities/examination/index.html#gaiyou*_3.pdf` | 決算短信集計結果 — gaiyou*_3.pdf | ok | Y | 1 |  |
| `...s/examination/index.html#renketsu_Growth*_3.pdf` | 決算短信集計結果 — renketsu_Growth*_3.pdf | ok | Y | 1 |  |
| `.../examination/index.html#renketsu_Growth*_3.xlsx` | 決算短信集計結果 — renketsu_Growth*_3.xlsx | ok | Y | 49 | 全産業, 154, 1360853, 17.48, 1158364 |
| `...es/examination/index.html#renketsu_Prime*_3.pdf` | 決算短信集計結果 — renketsu_Prime*_3.pdf | ok | Y | 1 |  |
| `...s/examination/index.html#renketsu_Prime*_3.xlsx` | 決算短信集計結果 — renketsu_Prime*_3.xlsx | ok | Y | 49 | 全産業, 959, 741258041, 2.94, 720100841 |
| `...examination/index.html#renketsu_Standard*_3.pdf` | 決算短信集計結果 — renketsu_Standard*_3.pdf | ok | Y | 1 |  |
| `...xamination/index.html#renketsu_Standard*_3.xlsx` | 決算短信集計結果 — renketsu_Standard*_3.xlsx | ok | Y | 49 | 全産業, 869, 31527754, 4.44, 30187879 |
| `...s/examination/index.html#renketsu_goukei*_3.pdf` | 決算短信集計結果 — renketsu_goukei*_3.pdf | ok | Y | 1 |  |
| `.../examination/index.html#renketsu_goukei*_3.xlsx` | 決算短信集計結果 — renketsu_goukei*_3.xlsx | ok | Y | 49 | 全産業, 1982, 774146648, 3.02, 751447084 |

#### 海外投資家地域別株券

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `...-equities/investor-type/04.html#region_1_m*.pdf` | 月間 — region_1_m*.pdf | ok | Y | 1 |  |
| `...-equities/investor-type/04.html#region_1_m*.xls` | 月間 — region_1_m*.xls | ok | Y | 28 | 北      米, 売り, Sales, 3,788,833, 9.03 |

#### 空売り集計

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `...statistics-equities/short-selling/01.html#*.pdf` | 月間集計 — *.pdf | ok | Y | 1 |  |
| `...stics-equities/short-selling/index.html#*-g.pdf` | 日次集計 — *-g.pdf | ok | Y | 1 |  |
| `...stics-equities/short-selling/index.html#*-m.pdf` | 日次集計 — *-m.pdf | ok | Y | 1 |  |

#### 統計情報（株式関連）

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `/markets/statistics-equities/misc/index.html#*.pdf` | 売買代金順位表・売買高・売買代金 — *.pdf | ok | Y | 1 |  |
| `...uities/misc/index.html#historical-genbutsu.xlsx` | 売買代金順位表・売買高・売買代金 — historical-genbutsu.xlsx | ok | N | 50 | 2022-04-30 00:00:00, 20, 24354567, 1281819, 576... |
| `...quities/misc/index.html#historical-toushin.xlsx` | 売買代金順位表・売買高・売買代金 — historical-toushin.xlsx | ok | N | 380 | 売買高 Trading Volume, 売買代金 Trading Value, 売買高 Tra... |
| `...ics-equities/monthly/index.html#*newmarket.xlsx` | 統計月報 — *newmarket.xlsx | ok | Y | 3770 | コード, 会社名, 旧市場区分, 新市場区分 |
| `...tics-equities/monthly/index.html#01_sokatu*.pdf` | 統計月報 — 01_sokatu*.pdf | ok | Y | 1 |  |
| `...tics-equities/monthly/index.html#02_baibai*.pdf` | 統計月報 — 02_baibai*.pdf | ok | Y | 1 |  |
| `...istics-equities/monthly/index.html#03_sisu*.pdf` | 統計月報 — 03_sisu*.pdf | ok | Y | 1 |  |
| `...tics-equities/monthly/index.html#04_jikaso*.pdf` | 統計月報 — 04_jikaso*.pdf | ok | Y | 1 |  |
| `...stics-equities/monthly/index.html#05_yield*.pdf` | 統計月報 — 05_yield*.pdf | ok | Y | 1 |  |
| `...tics-equities/monthly/index.html#06_perpbr*.pdf` | 統計月報 — 06_perpbr*.pdf | ok | Y | 1 |  |
| `...tistics-equities/monthly/index.html#07_etf*.pdf` | 統計月報 — 07_etf*.pdf | ok | Y | 1 |  |
| `...tics-equities/monthly/index.html#08_saiken*.pdf` | 統計月報 — 08_saiken*.pdf | ok | Y | 1 |  |
| `...tics-equities/monthly/index.html#09_t-kabu*.pdf` | 統計月報 — 09_t-kabu*.pdf | ok | Y | 1 |  |
| `...stics-equities/monthly/index.html#10_t-etf*.pdf` | 統計月報 — 10_t-etf*.pdf | ok | Y | 1 |  |
| `...tics-equities/monthly/index.html#11_kaigai*.pdf` | 統計月報 — 11_kaigai*.pdf | ok | Y | 1 |  |
| `...tics-equities/monthly/index.html#12_sinyou*.pdf` | 統計月報 — 12_sinyou*.pdf | ok | Y | 1 |  |
| `...tics-equities/monthly/index.html#13_kabusu*.pdf` | 統計月報 — 13_kabusu*.pdf | ok | Y | 1 |  |
| `...tics-equities/monthly/index.html#14_tansin*.pdf` | 統計月報 — 14_tansin*.pdf | ok | Y | 1 |  |
| `...stics-equities/monthly/index.html#15_allse*.pdf` | 統計月報 — 15_allse*.pdf | ok | Y | 1 |  |
| `...istics-equities/monthly/index.html#16_idou*.pdf` | 統計月報 — 16_idou*.pdf | ok | Y | 1 |  |
| `...stics-equities/monthly/index.html#17_kenri*.pdf` | 統計月報 — 17_kenri*.pdf | ok | Y | 1 |  |
| `...tistics-equities/monthly/index.html#geppou*.pdf` | 統計月報 — geppou*.pdf | ok | Y | 1 |  |
| `...statistics-equities/price/index.html#ivt_*.xlsx` | 月間相場表 — ivt_*.xlsx | ok | Y | 532 | 年月, 銘柄コード, 銘柄名称, Issues, 銘柄属性 |
| `.../statistics-equities/price/index.html#sb_*.xlsx` | 月間相場表 — sb_*.xlsx | ok | Y | 405 | 年月, 証券種別名, Securities, 銘柄コード, 銘柄名称 |
| `...statistics-equities/price/index.html#st_*-2.pdf` | 月間相場表 — st_*-2.pdf | ok | Y | 1 |  |
| `...s/statistics-equities/price/index.html#st_*.pdf` | 月間相場表 — st_*.pdf | ok | Y | 1 |  |

#### 統計月報

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `...ics-equities/monthly/01.html#koumokusyousai.pdf` | ご利用の手引き — koumokusyousai.pdf | ok | N | 1 |  |
| `...stics-equities/monthly/02.html#osirase-kako.pdf` | お知らせ — osirase-kako.pdf | ok | N | 1 |  |
| `...tistics-equities/monthly/03.html#b7gje*a9cd.pdf` | 訂正情報 — b7gje*a9cd.pdf | ok | Y | 1 |  |
| `...tatistics-equities/monthly/03.html#teisei-*.pdf` | 訂正情報 — teisei-*.pdf | ok | Y | 1 |  |

#### 規模別・業種別PER・PBR

| Path | Description | Status | History | Count | Fields |
|------|-------------|--------|---------|-------|--------|
| `...statistics-equities/misc/04.html#*PERPBRHPj.pdf` | 規模別・業種別PER・PBR — *PERPBRHPj.pdf | ok | Y | 1 |  |
| `...ics-equities/misc/04.html#longrange-perpbr.xlsx` | 規模別・業種別PER・PBR — longrange-perpbr.xlsx | ok | N | 50 | 2022, 4.0, 1821, 20.4, 1.2 |
| `...s/statistics-equities/misc/04.html#oshirase.pdf` | 規模別・業種別PER・PBR — oshirase.pdf | ok | N | 1 |  |
| `...s/statistics-equities/misc/04.html#perpbr*.xlsx` | 規模別・業種別PER・PBR — perpbr*.xlsx | ok | Y | 115 | 年月, 市場区分名, Section, 種別, Industry |

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

### TDCC
- **OpenAPI**: `https://openapi.tdcc.com.tw` — snapshot only, no history

### J-Quants (JP)
- **API**: `https://api.jquants.com/v2` — JPX official REST API, requires API key (`x-api-key` header, RSR_JQUANTS_API_KEY)
- Rate limit: Free plan 5 req/min; plan tier per endpoint noted in `notes`
- Date format: `YYYY-MM-DD`; pagination via `pagination_key`

### EDINET (JP)
- **API v2**: `https://api.edinet-fsa.go.jp/api/v2` — requires `Subscription-Key` query param (RSR_EDINET_API_KEY, free registration)
- Document list by filing date; document fetch by docID + type (1=XBRL zip, 2=PDF, 5=CSV zip)

### TDnet (JP)
- **Web**: `https://www.release.tdnet.info` — free window is **last 31 days only**; no official free API
- Daily list pages: `/inbs/I_list_{page}_{YYYYMMDD}.html`

### JPX (JP)
- **Web**: `https://www.jpx.co.jp` statistics pages — mostly Excel downloads; some tables PDF-only
- File URLs contain random CMS paths — must re-crawl listing pages, never hardcode file URLs
- Cloud-hosted clients get HTTP 403 (independent of User-Agent); fetch from a residential/local machine

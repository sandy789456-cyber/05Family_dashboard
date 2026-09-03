# Roadmap

## V1 — 已完成
- [x] Streamlit Dashboard
- [x] Google Sheets API
- [x] Service Account
- [x] Render Environment Variables
- [x] Git / GitHub
- [x] Docker / Render
- [x] 基本資料讀取與 append
- [x] 月份／孩子／類別篩選
- [x] 基本統計與圖表

## V1.1 — 報告與 UX
- [ ] 各分頁「匯出報告」真正功能
- [ ] Excel 報告格式最佳化
- [ ] PDF 報告
- [ ] 匯出目前篩選結果
- [ ] 報告摘要／孩子比較／類別統計
- [ ] 檔名自動加入月份

## V1.2 — 資料管理
- [ ] 編輯紀錄
- [ ] 刪除紀錄
- [ ] 防止重複提交
- [ ] Google Sheets 資料驗證
- [ ] schema 檢查
- [ ] CSV / Excel 批次匯入

## V1.3 — Dashboard 強化
- [ ] 日／週／月趨勢
- [ ] 孩子長期趨勢
- [ ] 類別完成率
- [ ] 點數排行榜
- [ ] 連續完成天數
- [ ] 未完成任務提醒
- [ ] 目標達成率

## V1.4 — 使用者與權限
- [ ] 登入
- [ ] 家長／孩子角色
- [ ] 權限控制
- [ ] 操作紀錄
- [ ] 管理員功能

## V2 — 自動化
- [ ] 自動週報
- [ ] 自動月報
- [ ] Email / 通知
- [ ] Google Sheets 備份
- [ ] 排程任務
- [ ] 異常資料提醒

## V3 — 架構升級
資料量或多人同時使用增加後再考慮：
- [ ] SQLite / PostgreSQL
- [ ] REST API
- [ ] 前後端分離
- [ ] 正式資料庫 schema
- [ ] CI/CD
- [ ] Automated testing
- [ ] Monitoring / logging

## 開發原則
1. 優先處理實際使用需求。
2. 不要過早把 Google Sheets 換成資料庫。
3. 每完成一個版本就 Git commit。
4. 每次 Render 部署後做實際寫入測試。

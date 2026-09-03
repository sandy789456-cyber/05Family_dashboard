# 家庭家事 Dashboard

以 Streamlit 建立的家庭家事紀錄與分析 Dashboard。

## 功能
- 線上填寫家事紀錄
- 孩子／類別／任務／次數／完成狀態／點數
- 月份與孩子篩選
- 統計與圖表
- Google Sheets 雲端資料儲存
- Docker + Render 部署
- Excel 報告匯出（持續擴充）

## 架構
```text
User → Streamlit/app.py → sheets_db.py → Google Sheets API → Google Sheets
Git → GitHub → Render → Docker → Streamlit
```

## 專案結構
```text
dashboard/
├── app.py
├── sheets_db.py
├── requirements.txt
├── Dockerfile
├── .gitignore
├── .env.example
└── sample_data/
    └── housework_month_sampele.csv
```

`google-service-account.json` 僅供本機使用，不加入 Git。

## 本機執行
```powershell
python -m venv env_dash
.\env_dash\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Google Sheets 欄位
```text
date, child, category, task, times, completed, points, mood, recorder, note, created_at
```

## Render Environment Variables
```text
GOOGLE_SPREADSHEET_ID
GOOGLE_SHEET_NAME
GOOGLE_SERVICE_ACCOUNT_JSON
```

## Docker
```powershell
docker build -t family-housework-dashboard .
docker run --rm -p 8501:8501 -e PORT=8501 family-housework-dashboard
```

## Git
```powershell
git add .
git commit -m "Update project"
git push
```

## 安全
不要提交：
```text
google-service-account.json
.env
.streamlit/secrets.toml
```

若 credential 曾公開，應撤銷並重新建立 key。

## 部署驗證
1. 開啟 Render URL
2. 新增一筆測試資料
3. 確認 Google Sheets 出現
4. 確認 Dashboard 讀回
5. 確認最近紀錄與統計正常

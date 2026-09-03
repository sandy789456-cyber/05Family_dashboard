
### `專案流程_家庭家事Dashboard.md`

````markdown
# 家庭家事 Dashboard — 專案流程與部署說明

> 版本：V1  
> 技術：Streamlit + Google Sheets API + Docker + Render

---

## 一、專案整體架構

本專案使用 Streamlit 建立家庭家事紀錄與分析 Dashboard。

使用者透過網頁介面填寫家事紀錄：

```text
使用者
  │
  ▼
Streamlit / app.py
  │
  ▼
sheets_db.py
  │
  ▼
Google Sheets API
  │
  ▼
Google Spreadsheet
````

部署環境：

```text
本機開發
  │
  ▼
Git
  │
  ▼
GitHub
  │
  ▼
Render
  │
  ▼
Docker
  │
  ▼
Streamlit
```

---

# 二、專案資料流程

## 1. 使用者輸入

使用者在 Streamlit 的「線上填寫」頁面輸入：

* 日期
* 孩子
* 家事類別
* 任務
* 次數
* 完成狀態
* 點數
* 心情
* 紀錄者
* 備註

系統另外產生：

```text
created_at
```

作為實際寫入時間。

---

## 2. Streamlit 建立資料

`app.py` 將表單資料整理成一個 record：

```text
使用者輸入
    ↓
record
    ↓
append_record()
```

---

## 3. 寫入 Google Sheets

`app.py` 呼叫：

```python
append_record(record)
```

再由：

```text
sheets_db.py
```

負責呼叫 Google Sheets API。

資料會 append 到：

```text
records
```

工作表。

---

## 4. Google Sheets 欄位

目前 V1 使用以下欄位：

```text
date
child
category
task
times
completed
points
mood
recorder
note
created_at
```

資料結構：

```text
A           date
B           child
C           category
D           task
E           times
F           completed
G           points
H           mood
I           recorder
J           note
K           created_at
```

---

# 三、資料讀取流程

Dashboard 需要資料時：

```text
Google Sheets
      ↓
read_records()
      ↓
pandas DataFrame
      ↓
clean_data()
      ↓
資料清理 / 型別轉換
      ↓
統計欄位計算
      ↓
Dashboard
```

`clean_data()` 主要負責：

* 日期轉換
* 孩子名稱清理
* 類別清理
* 任務清理
* 次數轉數字
* 點數轉數字
* 完成狀態標準化
* 完成點數計算
* 完成次數計算
* 月份欄位
* 日期顯示欄位

---

# 四、Google Service Account

本機與 Render 使用不同的 credential 來源。

## 本機

使用：

```text
google-service-account.json
```

架構：

```text
app.py
  ↓
sheets_db.py
  ↓
google-service-account.json
  ↓
Google Sheets API
```

---

## Render

Render 不使用本機 JSON 檔案。

改使用 Environment Variable：

```text
GOOGLE_SERVICE_ACCOUNT_JSON
```

架構：

```text
Render
  ↓
Environment Variables
  ↓
GOOGLE_SERVICE_ACCOUNT_JSON
  ↓
sheets_db.py
  ↓
Google Sheets API
```

---

# 五、Render Environment Variables

目前需要設定：

| Environment Variable          | 用途                      |
| ----------------------------- | ----------------------- |
| `GOOGLE_SPREADSHEET_ID`       | Google Spreadsheet ID   |
| `GOOGLE_SHEET_NAME`           | Google Sheet 工作表名稱      |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Service Account 完整 JSON |

目前工作表名稱：

```text
records
```

---

# 六、Credential 安全原則

以下檔案不能提交到 Git：

```text
google-service-account.json
.env
.streamlit/secrets.toml
```

`.gitignore` 應包含：

```gitignore
google-service-account.json
*-service-account.json
.env
.streamlit/secrets.toml
```

---

## 絕對不要

不要：

```text
google-service-account.json
        ↓
git add .
        ↓
git push
        ↓
GitHub
```

因為 Service Account credential 一旦公開，就可能造成 Google API 資源被未授權使用。

---

# 七、Git → GitHub 流程

修改程式後：

```powershell
git status
```

確認修改內容。

---

## 加入 Git

```powershell
git add .
```

再次確認：

```powershell
git status
```

確認沒有：

```text
google-service-account.json
```

---

## Commit

```powershell
git commit -m "Update project"
```

---

## Push

```powershell
git push
```

流程：

```text
修改程式
   ↓
git status
   ↓
git add .
   ↓
git commit
   ↓
git push
   ↓
GitHub
```

---

# 八、Render 部署流程

Render 連接 GitHub repository。

流程：

```text
GitHub
  ↓
Render Web Service
  ↓
讀取 repository
  ↓
讀取 Dockerfile
  ↓
Docker Build
  ↓
安裝 requirements.txt
  ↓
啟動 Streamlit
```

---

# 九、Docker

專案使用：

```text
Dockerfile
```

建立部署環境。

Docker 啟動 Streamlit 時不能把 Render port 寫死。

使用：

```dockerfile
CMD streamlit run app.py --server.address=0.0.0.0 --server.port=$PORT
```

其中：

```text
$PORT
```

由 Render 提供。

---

# 十、本機 Docker 測試

如果需要在部署前測試：

```powershell
docker build -t family-housework-dashboard .
```

啟動：

```powershell
docker run --rm -p 8501:8501 -e PORT=8501 family-housework-dashboard
```

然後開啟：

```text
http://localhost:8501
```

---

# 十一、Render 部署後驗證

每次 Render 部署完成後，建議依序確認：

### 1. 網頁是否正常開啟

```text
Render URL
    ↓
Streamlit Dashboard
```

---

### 2. 測試新增資料

進入：

```text
線上填寫
```

新增一筆測試資料。

---

### 3. 確認 Google Sheets

確認：

```text
Google Sheets
    ↓
records
```

是否出現剛才新增的資料。

---

### 4. 確認 Dashboard

回到 Dashboard：

```text
Google Sheets
    ↓
read_records()
    ↓
Dashboard
```

確認資料有正確讀回。

---

### 5. 確認最近紀錄

確認最新資料：

* 有出現
* `created_at` 正確
* 排序正常

---

# 十二、遇到 Render 問題的排查順序

如果：

```text
本機正常
Render 異常
```

不要先修改資料邏輯。

建議依序檢查：

```text
① Render Logs
      ↓
② Environment Variables
      ↓
③ Docker Build
      ↓
④ requirements.txt
      ↓
⑤ Google Service Account
      ↓
⑥ Google Sheet 權限
      ↓
⑦ Google Sheets API
```

---

# 十三、Google Sheets 權限

Service Account 必須具有目標 Spreadsheet 的適當權限。

如果出現：

```text
Permission denied
```

優先檢查：

```text
Google Sheet
    ↓
Share
    ↓
Service Account Email
    ↓
是否具有編輯權限
```

---

# 十四、完整系統流程

目前 V1 的完整流程：

```text
                    ┌──────────────────┐
                    │      使用者      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Streamlit     │
                    │      app.py      │
                    └────────┬─────────┘
                             │
                    建立 / 清理資料
                             │
                             ▼
                    ┌──────────────────┐
                    │   sheets_db.py   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Google Sheets API│
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Google Sheets   │
                    │     records      │
                    └────────┬─────────┘
                             │
                         read_records()
                             │
                             ▼
                    ┌──────────────────┐
                    │   clean_data()   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Dashboard     │
                    │ 統計 / 圖表 / 報告 │
                    └──────────────────┘
```

---

# 十五、部署架構

```text
                    GitHub
                       │
                       │ git push
                       ▼
                  ┌──────────┐
                  │  Render  │
                  └────┬─────┘
                       │
                   Docker Build
                       │
                       ▼
                ┌──────────────┐
                │   Streamlit  │
                │    app.py    │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │  sheets_db   │
                └──────┬───────┘
                       │
                       ▼
              Google Sheets API
                       │
                       ▼
                Google Sheets
```

---

# 十六、V1 完成狀態

目前已完成：

* [x] Streamlit Dashboard
* [x] 線上填寫
* [x] Google Sheets API
* [x] Service Account
* [x] Google Sheets 讀取
* [x] Google Sheets 寫入
* [x] 資料清理
* [x] 統計與圖表
* [x] Docker
* [x] requirements.txt
* [x] Git
* [x] GitHub
* [x] Render
* [x] Render Environment Variables
* [x] 線上部署

---

# 十七、後續開發原則

後續新增功能時：

```text
新增功能
   ↓
本機測試
   ↓
Git commit
   ↓
Git push
   ↓
Render 自動部署
   ↓
線上測試
   ↓
Google Sheets 驗證
```

建議每完成一個具有意義的功能就建立一個 Git commit。

例如：

```powershell
git commit -m "Add Excel report export"
```

或：

```powershell
git commit -m "Fix recent records sorting"
```

---

# 十八、版本升級原則

目前 V1 使用：

```text
Streamlit
+
Google Sheets
+
Docker
+
Render
```

不要因為未來功能增加就立即更換架構。

當出現以下情況時，再考慮升級資料庫：

* 資料量明顯增加
* 多人同時寫入
* 查詢變複雜
* Google Sheets API 成為效能瓶頸
* 需要交易／一致性控制
* 需要正式使用者權限
* 需要更複雜的後端 API

可能的下一階段：

```text
Google Sheets
      ↓
SQLite
      ↓
PostgreSQL
```

---

# 十九、目前 V1 的核心概念

這個專案目前最重要的架構決策是：

> **Render 負責執行程式，Google Sheets 負責保存資料。**

因此即使 Render：

```text
Restart
Redeploy
Container Rebuild
```

資料仍然保存在：

```text
Google Sheets
```

而不是 Render container 的本地檔案。

這也是從原本 CSV 儲存架構升級到目前 V1 的核心原因。

````

你可以直接把這個檔案放到專案根目錄，檔名建議：

```text
專案流程_家庭家事Dashboard.md
````

PDF 就可以不放進 Git 了。

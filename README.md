# 家事紀錄儀表板 V3

這是一個給兩位孩子使用的家事與生活紀錄 Dashboard。

## 功能

- 線上填表單，送出後自動寫入 `data/housework_records.csv`
- 可上傳 CSV / Excel 分析
- 卡片式 KPI Dashboard
- 每日完成趨勢、類別分布、Top 任務、個人比較
- 資料清理報告與清理後 CSV 下載
- 內建一個月範例資料：`sample_data/housework_month_sample.csv`

## 欄位格式

| 欄位 | 說明 |
|---|---|
| date | 日期 |
| child | 孩子，例如哥哥、弟弟 |
| category | 類別，例如個人清潔、居家整理 |
| task | 具體項目 |
| times | 次數 |
| completed | 是否完成，是 / 否 |
| points | 每次點數 |
| mood | 完成狀態 |
| recorder | 填寫者 |
| note | 備註 |
| created_at | 建立時間 |

## 執行方式

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

如果公司電腦封鎖 `streamlit.exe`，請不要用 `streamlit run app.py`，改用：

```powershell
python -m streamlit run app.py
```

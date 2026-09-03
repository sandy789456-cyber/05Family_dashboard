# 踩過的坑與解決方案

## 1. Render 本地 CSV 不適合持久化
**問題：** 容器重新部署／重啟後，本地資料不可靠。  
**解決：** 改用 Google Sheets API 作為雲端資料來源。

## 2. Service Account 不能進 GitHub
**問題：** `google-service-account.json` 包含 credential。  
**解決：** `.gitignore` 忽略 credential；Render 使用 `GOOGLE_SERVICE_ACCOUNT_JSON`。

## 3. 本機與 Render credential 來源不同
**解決：** 程式優先讀環境變數；沒有時才讀本機 JSON。

## 4. 最近填寫紀錄排序異常
**問題：** `created_at` 若維持字串，排序可能不符合預期。  
**解決：**
```python
df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
df.sort_values("created_at", ascending=False, na_position="last")
```

## 5. API append 成功仍需驗證
**解決：** 測試階段採 append → read_records() → 比對測試資料，確認寫入與讀取都成功。

## 6. requirements.txt 版本格式
錯誤：
```text
charset_normalizer=3.4.9
```
正確：
```text
charset_normalizer==3.4.9
```

## 7. Render Docker port
不要寫死 8501。使用：
```dockerfile
CMD streamlit run app.py --server.address=0.0.0.0 --server.port=$PORT
```

## 8. Google Sheet 欄位變更
新增欄位時同步檢查：
- FORM_COLUMNS
- append_record()
- read_records()
- clean_data()
- Google Sheet header
- Dashboard 顯示

## 9. Python 3.10 提醒
目前可運作；未來可考慮 Python 3.11+。升級前需重新測試 dependencies、Google Sheets API、Streamlit、Plotly、Excel、Docker 與 Render。

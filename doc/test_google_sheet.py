from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


# ============================================================
# Google Sheets 設定
# ============================================================

# 你的 Service Account JSON
SERVICE_ACCOUNT_FILE = "google-service-account.json"

# 把這裡換成你的 Google Sheet ID
SPREADSHEET_ID = "16jmElmRZBpysqyCIoN2-_LBE8a-676pwZiVq9_W_SbE"


# Google Sheet 工作表名稱
SHEET_NAME = "records"

# Google Sheets API 權限
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]


# ============================================================
# 建立 Google Sheets API 連線
# ============================================================

def get_sheets_service():
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES,
    )

    service = build(
        "sheets",
        "v4",
        credentials=credentials,
    )

    return service


# ============================================================
# 讀取資料
# ============================================================

def read_records(service):
    range_name = f"{SHEET_NAME}!A:K"

    result = (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
        )
        .execute()
    )

    values = result.get("values", [])

    return values


# ============================================================
# 新增測試資料
# ============================================================

def append_test_record(service):

    test_row = [
        "2026-09-01",
        "哥哥",
        "API測試",
        "Google Sheets API 測試",
        1,
        "是",
        5,
        "測試",
        "Python API",
        "這是一筆 Google Sheets API 測試資料",
        "2026-09-01 17:00:00",
    ]

    body = {
        "values": [test_row]
    }

    result = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A:K",
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body=body,
        )
        .execute()
    )

    return result


# ============================================================
# 主程式
# ============================================================

def main():

    print("=" * 60)
    print("Google Sheets API 測試")
    print("=" * 60)

    try:

        # 1. 建立連線
        print("\n[1/3] 建立 Google Sheets API 連線...")

        service = get_sheets_service()

        print("✅ Google Sheets API 連線成功")

        # 2. 讀取資料
        print("\n[2/3] 讀取 Google Sheet...")

        values = read_records(service)

        print(f"✅ 讀取成功，共 {len(values)} 列")

        if values:
            print("\n目前資料：")

            for row in values[:5]:
                print(row)

        # 3. 新增測試資料
        print("\n[3/3] 寫入測試資料...")

        result = append_test_record(service)

        print("✅ 測試資料寫入成功")
        print(f"更新範圍：{result.get('updates', {}).get('updatedRange')}")

        print("\n" + "=" * 60)
        print("🎉 Google Sheets API 測試成功！")
        print("=" * 60)

    except Exception as e:

        print("\n❌ Google Sheets API 測試失敗")

        print("\n錯誤內容：")
        print(e)

        print("\n請檢查：")
        print("1. Service Account JSON 是否正確")
        print("2. SPREADSHEET_ID 是否正確")
        print("3. Google Sheet 是否分享給 Service Account")
        print("4. Service Account 是否有 Editor 權限")
        print("5. Google Sheets API 是否已啟用")


if __name__ == "__main__":
    main()
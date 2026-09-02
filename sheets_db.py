from __future__ import annotations

import json
import os
from pathlib import Path

import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


# ============================================================
# 基本設定
# ============================================================

APP_DIR = Path(__file__).parent

# 本機測試用 Service Account JSON
LOCAL_SERVICE_ACCOUNT_FILE = (
    APP_DIR / "google-service-account.json"
)

# Google Sheet ID
#
# 優先使用 Render Environment Variable：
# GOOGLE_SPREADSHEET_ID
#
# 如果沒有設定，才使用下面的本機設定。
SPREADSHEET_ID = os.getenv(
    "GOOGLE_SPREADSHEET_ID",
    "16jmElmRZBpysqyCIoN2-_LBE8a-676pwZiVq9_W_SbE",
)

# Google Sheet 工作表名稱
SHEET_NAME = os.getenv(
    "GOOGLE_SHEET_NAME",
    "records",
)

# Google Sheets API 權限
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]


# ============================================================
# 取得 Google Service Account Credentials
# ============================================================

def get_credentials() -> Credentials:
    """
    本機：
        使用 google-service-account.json

    Render：
        使用 GOOGLE_SERVICE_ACCOUNT_JSON Environment Variable
    """

    # --------------------------------------------------------
    # 優先使用 Environment Variable
    # --------------------------------------------------------

    service_account_json = os.getenv(
        "GOOGLE_SERVICE_ACCOUNT_JSON"
    )

    if service_account_json:

        try:
            info = json.loads(service_account_json)

            return Credentials.from_service_account_info(
                info,
                scopes=SCOPES,
            )

        except json.JSONDecodeError as exc:
            raise ValueError(
                "GOOGLE_SERVICE_ACCOUNT_JSON "
                "不是有效的 JSON 格式。"
            ) from exc

    # --------------------------------------------------------
    # 本機使用 JSON 檔案
    # --------------------------------------------------------

    if LOCAL_SERVICE_ACCOUNT_FILE.exists():

        return Credentials.from_service_account_file(
            LOCAL_SERVICE_ACCOUNT_FILE,
            scopes=SCOPES,
        )

    # --------------------------------------------------------
    # 找不到 credentials
    # --------------------------------------------------------

    raise FileNotFoundError(
        "找不到 Google Service Account 憑證。\n\n"
        "本機請確認：\n"
        f"{LOCAL_SERVICE_ACCOUNT_FILE}\n\n"
        "Render 請設定：\n"
        "GOOGLE_SERVICE_ACCOUNT_JSON"
    )


# ============================================================
# 建立 Google Sheets API Service
# ============================================================

def get_sheets_service():

    if not SPREADSHEET_ID or SPREADSHEET_ID.startswith("請換成"):

        raise ValueError(
            "尚未設定 GOOGLE_SPREADSHEET_ID。"
        )

    credentials = get_credentials()

    service = build(
        "sheets",
        "v4",
        credentials=credentials,
    )

    return service


# ============================================================
# 讀取 Google Sheet
# ============================================================

def read_records() -> pd.DataFrame:

    service = get_sheets_service()

    result = (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A:K",
        )
        .execute()
    )

    values = result.get("values", [])

    # 沒有任何資料
    if not values:
        return pd.DataFrame()

    # --------------------------------------------------------
    # 第一列是欄位名稱
    # --------------------------------------------------------

    headers = values[0]

    rows = values[1:]

    # 只有標題，沒有資料
    if not rows:
        return pd.DataFrame(columns=headers)

    # --------------------------------------------------------
    # 確保每一列都有 11 個欄位
    # Google Sheet 空白欄位可能造成 row 長度不足
    # --------------------------------------------------------

    normalized_rows = []

    for row in rows:

        row = list(row)

        if len(row) < len(headers):
            row.extend(
                [""] * (len(headers) - len(row))
            )

        normalized_rows.append(
            row[:len(headers)]
        )

    return pd.DataFrame(
        normalized_rows,
        columns=headers,
    )


# ============================================================
# 新增一筆紀錄
# ============================================================

def append_record(
    record: dict[str, object]
) -> None:

    service = get_sheets_service()

    row = [
        record.get("date", ""),
        record.get("child", ""),
        record.get("category", ""),
        record.get("task", ""),
        record.get("times", ""),
        record.get("completed", ""),
        record.get("points", ""),
        record.get("mood", ""),
        record.get("recorder", ""),
        record.get("note", ""),
        record.get("created_at", ""),
    ]

    body = {
        "values": [row]
    }

    (
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
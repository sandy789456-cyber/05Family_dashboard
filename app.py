
# Run:
# python -m streamlit run app.py


####################################################
# 0. 完整流程
# CSS 美化
# 資料載入與清理
# 表單填寫
# 統計總覽
# 孩子比較
# 資料清理報告
# 項目管理
# 主程式流程
####################################################



####################################################
# 1. 基本設定與匯入套件
# __future__ import annotations：讓 Python 在型別註解時更靈活，避免循環引用問題。
# Pathlib.Path：用來處理檔案路徑，比 os.path 更直覺。
# pandas：處理資料表格。
# plotly.express / plotly.graph_objects：畫圖表。
# streamlit：建立互動式網頁介面。
# 這裡就是整個應用的基礎工具箱。
####################################################

from __future__ import annotations
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


####################################################
# 2. 檔案路徑與基本資料
# APP_DIR：程式所在的資料夾。
# SAMPLE_PATH：範例資料 CSV。
# RECORD_PATH：使用者的紀錄檔案。
# 這些路徑讓程式知道要去哪裡讀取或儲存資料。
####################################################

APP_DIR = Path(__file__).parent
SAMPLE_PATH = APP_DIR /  "sample_data" / "housework_month_sampele.csv"
DATA_DIR = APP_DIR / "data"
RECORD_PATH = DATA_DIR  / "housework_records.csv"

####################################################
# 3. 家事分類與點數設定
# CHILDREN：兩位孩子的名字。
# CATEGORY_ORDER：家事類別的排序。
# TASK_OPTIONS：每個類別有哪些具體任務。
# DEFAULT_POINTS：每個任務的預設點數。
# 這些設定讓表單和統計有一致的規則。
####################################################

CHILDREN = ["哥哥", "弟弟"]
CATEGORY_ORDER = ["個人清潔", "居家整理", "學習相關", "餐飲協助", "信仰生活", "其他"]
TASK_OPTIONS = {
    "個人清潔": ["刷牙洗臉", "房間整理", "書包整理"],
    "居家整理": ["集中垃圾", "倒垃圾", "掃地", "拖地", "吸塵", "洗衣服", "晾衣服", "烘衣服", "收衣服", "分衣服"],
    "學習相關": ["補習", "作業", "複習", "預習"],
    "餐飲協助": ["餐前擺碗筷", "餐後收拾", "擦餐桌", "協助洗烘碗筷"],
    "信仰生活": ["聚會", "安息日", "讀經", "家庭祭壇", "筆記"],
    "其他": ["主動幫忙", "禮貌表現", "情緒管理", "其他"],
}
DEFAULT_POINTS = {
    "刷牙洗臉": 5, "房間整理": 3, "書包整理": 3,
    "集中垃圾": 5, "倒垃圾": 5, "掃地": 5, "拖地": 5, "吸塵": 5, "洗衣服": 5, "晾衣服": 5, "烘衣服": 5, "收衣服": 5, "分衣服": 5,
    "補習": 5, "作業": 5, "複習": 5, "預習": 5,
    "餐前擺碗筷": 3, "餐後收拾": 3, "擦餐桌": 3, "協助洗烘碗筷": 5,
    "聚會": 5, "安息日": 10, "讀經": 5, "家庭祭壇": 5, "筆記": 5,
    "主動幫忙": 5, "禮貌表現": 5, "情緒管理": 10, "其他": 5,
}
REQUIRED_COLUMNS = ["date", "child", "category", "task", "times", "completed", "points"]
FORM_COLUMNS = [
    "date", "child", "category", "task", "times", "completed", "points",
    "mood", "recorder", "note", "created_at",
]


####################################################
# 4. CSS 美化介面
# 這裡用 CSS 改造 Streamlit 預設樣式。
# :root{--purple:#7c3aed;} 定義顏色變數。
# .stApp{background:...} 設定整體背景漸層。
# .hero, .kpi-card, .child-card 等：自訂卡片樣式。
# CSS 的作用就是讓介面更漂亮、更有一致性。
# for details please refer to css_notes.md
####################################################


def css() -> None:
    st.markdown(
        """
        <style>
        :root{--purple:#7c3aed;--green:#10b981;--blue:#3b82f6;--pink:#ec4899;--ink:#111827;--muted:#64748b;}
        .stApp{background:linear-gradient(135deg,#fbfcff 0%,#f7f2ff 38%,#f0fff8 100%);}
        section[data-testid="stSidebar"]{background:linear-gradient(180deg,#fff 0%,#f7f1ff 100%);border-right:1px solid #eadcff;}
        section[data-testid="stSidebar"] .stRadio label{font-weight:750;}
        .main .block-container{padding-top:1.4rem;max-width:1500px;padding-left:2rem;padding-right:2rem;}
        .hero{display:flex;justify-content:space-between;align-items:center;gap:20px;padding:18px 22px;margin-bottom:18px;border:1px solid #e8e6f5;border-radius:28px;background:rgba(255,255,255,.82);box-shadow:0 14px 36px rgba(60,40,120,.08);}
        .hero h1{font-size:28px;margin:0;color:var(--ink);font-weight:900;}
        .hero p{margin:.35rem 0 0;color:#475569;font-weight:650;}
        .export-pill{padding:12px 18px;border-radius:16px;background:linear-gradient(135deg,#7c3aed,#a855f7);color:white;font-weight:900;white-space:nowrap;}
        .kpi-card{min-height:168px;padding:20px 22px;border-radius:24px;background:rgba(255,255,255,.94);border:1px solid #e8e8f3;box-shadow:0 12px 32px rgba(20,30,70,.08);}
        .kpi-icon{width:52px;height:52px;border-radius:17px;display:flex;align-items:center;justify-content:center;font-size:29px;margin-bottom:10px;background:linear-gradient(135deg,#ede9fe,#eff6ff);}
        .kpi-title{font-size:14px;font-weight:800;color:#64748b;}
        .kpi-value{font-size:36px;line-height:1.15;font-weight:950;color:#0f172a;margin-top:6px;white-space:nowrap;}
        .kpi-subtitle{font-size:13px;color:#64748b;margin-top:10px;font-weight:650;}
        .soft-card{padding:20px;border-radius:24px;background:rgba(255,255,255,.92);border:1px solid #e8e8f3;box-shadow:0 12px 30px rgba(20,30,70,.07);margin-bottom:18px;}
        .section-title{font-size:19px;font-weight:900;color:#172033;margin-bottom:10px;}
        .child-card{padding:22px;border-radius:24px;background:white;border:1px solid #e8e8f3;box-shadow:0 12px 30px rgba(20,30,70,.07);}
        .avatar{width:76px;height:76px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:42px;background:linear-gradient(135deg,#bfdbfe,#d1fae5);margin-bottom:8px;}
        .big-percent{font-size:36px;font-weight:950;margin:3px 0;color:#7c3aed;}
        .progress-bg{height:9px;border-radius:999px;background:#e9edf4;overflow:hidden;margin:7px 0 16px;}
        .progress-bar{height:100%;border-radius:999px;background:linear-gradient(90deg,#7c3aed,#a855f7);}
        .green-bar{background:linear-gradient(90deg,#10b981,#34d399);}
        .rank-row{display:grid;grid-template-columns:1.3fr 2fr .6fr;align-items:center;gap:12px;margin:12px 0;font-weight:750;color:#334155;}
        .mini-bar-bg{height:8px;border-radius:999px;background:#edf0f5;overflow:hidden;}.mini-bar{height:100%;border-radius:999px;background:linear-gradient(90deg,#7c3aed,#60a5fa);}.weak{background:linear-gradient(90deg,#fb7185,#fca5a5);}
        .cheer{margin-top:18px;padding:18px 22px;border-radius:22px;background:linear-gradient(90deg,#f3fff1,#fffbea);border:1px solid #d9f99d;color:#16a34a;font-size:18px;font-weight:900;}
        div[data-testid="stMetric"]{background:white;border:1px solid #e8e8f3;border-radius:18px;padding:12px;}
        .stTabs [data-baseweb="tab-list"]{gap:8px;}.stTabs [data-baseweb="tab"]{border-radius:999px;padding:10px 18px;background:white;border:1px solid #e8e8f3;font-weight:800;}
        </style>
        """,
        unsafe_allow_html=True,
    )

####################################################
# 5. 載入檔案 load_file
# 如果使用者有上傳檔案 → 判斷副檔名，支援 CSV 或 Excel。
# 如果沒有上傳 → 優先讀取 RECORD_PATH（之前的紀錄）。
# 如果紀錄檔不存在或是空的 → 使用範例檔 SAMPLE_PATH。
# 這樣設計的好處是：永遠有資料可用，不會因為沒有上傳就報錯。
####################################################


def load_file(uploaded_file) -> pd.DataFrame:
    if uploaded_file is not None:
        name = uploaded_file.name.lower()
        if name.endswith(".csv"):
            return pd.read_csv(uploaded_file)
        if name.endswith((".xlsx", ".xls")):
            return pd.read_excel(uploaded_file)
        raise ValueError("只支援 CSV 或 Excel。")
    if RECORD_PATH.exists() and RECORD_PATH.stat().st_size > 0:
        records = pd.read_csv(RECORD_PATH)
        if not records.empty:
            return records
    return pd.read_csv(SAMPLE_PATH)

####################################################
# 6. 清理資料 clean_data
# 清理後的資料就能直接用來做統計和圖表。
####################################################


def clean_data(df: pd.DataFrame) -> pd.DataFrame:

    # 先複製一份資料，避免修改原始檔。
    # 把欄位名稱去掉多餘空白。
    # 檢查是否缺少必要欄位（REQUIRED_COLUMNS），如果缺少就報錯。    
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError("資料缺少必要欄位：" + ", ".join(missing))


    # 確保所有表單欄位都存在。
    # 如果缺少 → 自動補上。
        # 文字型欄位（心情、備註、建立時間）補空字串。
        # 數值型欄位補 0。
    for col in FORM_COLUMNS:
        if col not in df.columns:
            df[col] = "" if col in ["mood", "recorder", "note", "created_at"] else 0



    # 把日期轉成 datetime 格式。
    # 把孩子、類別、項目欄位轉成字串並去掉空白。
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["child"] = df["child"].astype(str).str.strip()
    df["category"] = df["category"].astype(str).str.strip()
    df["task"] = df["task"].astype(str).str.strip()


    # 把「次數」和「點數」轉成數字。
    # 如果轉換失敗 → 補 0。
    df["times"] = pd.to_numeric(df["times"], errors="coerce").fillna(0).astype(int)
    df["points"] = pd.to_numeric(df["points"], errors="coerce").fillna(0).astype(int)

    # 標準化「完成」欄位，把不同寫法（true/yes/完成）都轉成「是」或「否」。
    # 新增一個布林欄位 is_completed，方便計算。
    df["completed"] = df["completed"].astype(str).str.strip().str.lower().replace(
        {"true":"是","1":"是","yes":"是","y":"是","完成":"是","false":"否","0":"否","no":"否","n":"否","未完成":"否"}
    )
    df["is_completed"] = df["completed"].eq("是")


    # earned_points：完成的次數 × 每次點數。
    # done_times：完成的次數（只算「是」）。
    # day / month：方便做每日或每月統計。
    # 最後刪掉日期為空的資料。
    df["earned_points"] = df["times"] * df["points"] * df["is_completed"].astype(int)
    df["done_times"] = df["times"] * df["is_completed"].astype(int)
    df["day"] = df["date"].dt.strftime("%m/%d")
    df["month"] = df["date"].dt.strftime("%Y-%m")
    return df.dropna(subset=["date"])



####################################################
# 7. 新增紀錄 append_record
# DATA_DIR.mkdir(exist_ok=True)：確保資料夾存在，沒有就建立。
# row = pd.DataFrame([record], columns=FORM_COLUMNS)：把單筆紀錄轉成 DataFrame。
# 如果紀錄檔存在 → 讀取舊資料，跟新紀錄合併。
# 如果不存在 → 直接用新紀錄。
# 最後存回 housework_records.csv。
# 這樣就能把表單送出的紀錄持續累積。
####################################################
 

def append_record(record: dict[str, object]) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    row = pd.DataFrame([record], columns=FORM_COLUMNS)
    if RECORD_PATH.exists() and RECORD_PATH.stat().st_size > 0:
        old = pd.read_csv(RECORD_PATH)
        out = pd.concat([old, row], ignore_index=True)
    else:
        out = row
    out.to_csv(RECORD_PATH, index=False, encoding="utf-8-sig")


####################################################
# 8. 統計摘要 summary
# total_days：有紀錄的天數。
# total_possible：所有應完成的次數（不管有沒有完成）。
# total_done：實際完成的次數。
# total_points：完成後得到的總點數。
# avg_daily：平均每天完成次數。
# rate：完成率（完成次數 ÷ 應完成次數）。
# child_points：依孩子分組，計算總點數。
# mvp：點數最高的孩子。
# 這個函式會回傳一個字典，後續用來顯示 KPI 卡片。
####################################################
 
def summary(df: pd.DataFrame) -> dict[str, object]:
    total_days = int(df["date"].dt.date.nunique())
    total_possible = int(df["times"].sum())
    total_done = int(df["done_times"].sum())
    total_points = int(df["earned_points"].sum())
    avg_daily = total_done / total_days if total_days else 0
    rate = total_done / total_possible if total_possible else 0
    child_points = df.groupby("child")["earned_points"].sum().sort_values(ascending=False)
    mvp = child_points.index[0] if not child_points.empty else "-"

    # 獲得最高點數的項目
    top_task = df.groupby("task")["earned_points"].sum().sort_values(ascending=False).index[0] if not df.empty else "-"
    return {"days": total_days, "done": total_done, "points": total_points, "avg": avg_daily, "rate": rate, "mvp": mvp, "top_task": top_task}


####################################################
# 9. KPI 卡片 kpi_card
# 用 HTML + CSS 顯示一張漂亮的 KPI 卡片。
# title：指標名稱。
# value：數值。
# subtitle：補充說明。
# icon：小圖示（emoji）。
# 這就是儀表板上看到的「總完成天數」「平均每日完成」等卡片。
####################################################

def kpi_card(title: str, value: str, subtitle: str, icon: str) -> None:
    st.markdown(
        f"""
        <div class="kpi-card">
          <div class="kpi-icon">{icon}</div>
          <div class="kpi-title">{title}</div>
          <div class="kpi-value">{value}</div>
          <div class="kpi-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


####################################################
# 10. Hero 區塊 hero
# 顯示一個「歡迎回來」的標題。
# selected_month：會顯示目前選擇的月份。
# 右邊有一個「匯出報告」按鈕樣式（目前只是裝飾，沒有功能）。
# 用 CSS class .hero 美化成一個橫幅區塊。
# 這是儀表板的開場白，讓使用者感覺更有互動性。
####################################################

def hero(selected_month: str) -> None:
    st.markdown(
        f"""
        <div class="hero">
          <div>
            <h1>歡迎回來！一起看看孩子們這個月的表現吧！ 🎉</h1>
            <p>{selected_month} 家事執行總覽｜可線上填寫、資料清理、圖表分析與統合報告</p>
          </div>
          <div class="export-pill">⬇ 匯出報告</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


####################################################
# 11. 表單設計 render_form
# 這是使用者每天填寫家事紀錄的入口。
####################################################



def render_form() -> None:
    st.markdown("<div class='section-title'>📝 今日填寫表單</div>", unsafe_allow_html=True)

    # 注意：
    # Streamlit 的 st.form 內部元件不會在選擇類別後立即重新整理，
    # 所以「類別 / 項目」連動要放在一般 widget 中，而不是放在 st.form 裡。
    # 這裡保留原本 4 欄 + 4 欄 + 備註 + 送出按鈕的版面配置，只修正連動邏輯。
    # 用 st.columns 把表單分成四欄。
    # date_input：選擇日期。
    # selectbox：選擇孩子、類別、項目。
    # task_options：根據類別動態顯示對應的任務。
    c1, c2, c3, c4 = st.columns([1, 1, 1.2, 1.2])

    # record_date改成可以用點選的日期選擇器，預設為今天的日期，並且可以選擇過去的日期。
    record_date = c1.date_input("日期", value=pd.Timestamp.now().date(), 
                                max_value=pd.Timestamp.now().date(), 
                                key="record_date",
    )

    # record_date = c1.date_input("日期", key="record_date") 

    child = c2.selectbox("孩子", CHILDREN, key="record_child")

    category = c3.selectbox(
        "類別",
        CATEGORY_ORDER,
        key="record_category",
    )

    task_options = TASK_OPTIONS.get(category, [])
    task = c4.selectbox(
        "項目",
        task_options,
        key=f"record_task_{category}",
    )

    c5, c6, c7, c8 = st.columns([1, 1, 1, 1.2])
    times = c5.number_input("次數", min_value=1, max_value=10, value=1, step=1, key="record_times")
    completed = c6.selectbox("完成", ["是", "否"], key="record_completed")


    # number_input：輸入次數與點數。
    # selectbox：選擇是否完成、孩子的狀態。
    # 點數會根據任務自動帶入預設值。
    # 用 task 當 key 的一部分，讓切換項目時預設點數可以跟著更新。
    points = c7.number_input(
        "每次點數",
        min_value=0,
        max_value=20,
        value=DEFAULT_POINTS.get(task, 1),
        step=1,
        key=f"record_points_{task}",
    )

    mood = c8.selectbox(
        "狀態",
        ["需要提醒", "普通", "主動完成", "表現很棒"],
        key="record_mood",
    )


    # text_input：輸入備註。
    # button：送出表單。
    # 當按下送出 → 呼叫 append_record() 把紀錄存到 CSV。
    # 顯示成功訊息。
    # st.balloons()：放氣球動畫，增加趣味性。
    note = st.text_input(
        "備註（可空白）",
        placeholder="例如：今天主動完成，值得鼓勵",
        key="record_note",
    )

    submitted = st.button("送出紀錄 ✅", use_container_width=True)

    if submitted:
        append_record({
            "date": record_date.isoformat(),
            "child": child,
            "category": category,
            "task": task,
            "times": int(times),
            "completed": completed,
            "points": int(points),
            "mood": mood,
            "recorder": "線上表單",
            "note": note.strip(),
            "created_at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        st.success("已儲存！重新整理或切到總覽即可看到最新統計。")
        st.balloons()


####################################################
# 12. 總覽儀表板 render_overview
# 先呼叫 summary(df)，取得統計摘要（天數、完成率、MVP 等）。
####################################################



def render_overview(df: pd.DataFrame) -> None:
    s = summary(df)

    # 第一排三張 KPI 卡片：完成天數、完成次數、平均每日完成。
    # 用 kpi_card() 顯示漂亮的卡片。    
    kpi_row_1 = st.columns(3, gap="large")
    with kpi_row_1[0]:
        kpi_card("總完成天數", f"{s['days']} 天", "本月有紀錄的天數", "📅")
    with kpi_row_1[1]:
        kpi_card("總完成次數", f"{s['done']} 次", f"達成率 {s['rate']:.1%}", "✅")
    with kpi_row_1[2]:
        kpi_card("平均每日完成", f"{s['avg']:.1f} 次", "依完成次數計算", "⭐")

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # 第二排三張 KPI 卡片：最高連續天數（目前未實作）、總獎勵點數、本月 MVP。
    kpi_row_2 = st.columns(3, gap="large")
    with kpi_row_2[0]:
        kpi_card("完成率", f"{s['rate']:.1%}", "完成次數 / 應完成次數", "🏅")
    with kpi_row_2[1]:
        kpi_card("總獎勵點數", f"{s['points']} 點", "完成項目才計分", "💖")
    with kpi_row_2[2]:
        kpi_card("最佳表現", str(s["top_task"]), "依點數排序", "👑")

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)


    # 第三排兩個圖表：每日完成趨勢（折線圖）、家事類別完成分布（圓餅圖）。
    # X 軸是日期，Y 軸是完成次數，顏色區分孩子。 
    # 右邊顯示「家事類別完成分布」圓餅圖。
    # 顯示各類別完成次數的比例。
    left, right = st.columns([1.15, 1], gap="large")
    with left:
        st.markdown("<div class='soft-card'><div class='section-title'>每日完成趨勢</div>", unsafe_allow_html=True)
        daily = df.groupby(["date", "day", "child"], as_index=False)["done_times"].sum().sort_values("date")
        fig = px.line(daily, x="day", y="done_times", color="child", markers=True, labels={"day":"日期","done_times":"次數","child":"孩子"})
        fig.update_layout(height=380, margin=dict(l=5, r=5, t=10, b=5), legend=dict(orientation="h", y=1.08))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='soft-card'><div class='section-title'>家事類別完成分布</div>", unsafe_allow_html=True)
        cat = df.groupby("category", as_index=False)["done_times"].sum().sort_values("done_times", ascending=False)
        fig = px.pie(cat, names="category", values="done_times", hole=.58)
        fig.update_traces(textposition="inside", textinfo="percent")
        fig.update_layout(height=380, margin=dict(l=5, r=5, t=10, b=5), legend=dict(orientation="v"))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


    # 排行榜 & 弱項
    # 左邊顯示「家事完成率 TOP 5」。
    # 用小橫條顯示完成率百分比。
    a, b, c = st.columns([1, 1, 1.85])
    with a:
        rank = df.groupby("task", as_index=False)["done_times"].sum().sort_values("done_times", ascending=False).head(5)
        st.markdown("<div class='soft-card'><div class='section-title'>家事完成率 TOP 5</div>", unsafe_allow_html=True)
        maxv = max(rank["done_times"].max(), 1) if not rank.empty else 1
        for _, r in rank.iterrows():
            pct = int(r["done_times"] / maxv * 100)
            st.markdown(f"<div class='rank-row'><div>🏆 {r['task']}</div><div class='mini-bar-bg'><div class='mini-bar' style='width:{pct}%'></div></div><div>{pct}%</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with b:
        # 中間顯示「需要加強的項目」。
        # 計算完成率最低的前5項。
        weak = df.groupby("task", as_index=False).agg(done=("done_times", "sum"), total=("times", "sum"))
        weak["rate"] = weak["done"] / weak["total"].replace(0, pd.NA)
        weak = weak.dropna().sort_values("rate").head(5)
        st.markdown("<div class='soft-card'><div class='section-title'>⚠️ 需要加強的項目</div>", unsafe_allow_html=True)
        for _, r in weak.iterrows():
            pct = int(r["rate"] * 100)
            st.markdown(f"<div class='rank-row'><div>♨ {r['task']}</div><div class='mini-bar-bg'><div class='mini-bar weak' style='width:{pct}%'></div></div><div>{pct}%</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c:
        # 右邊呼叫 render_child_compare()，顯示兩位孩子的完成率、次數、點數比較。
        render_child_compare(df)


    # 找出本月完成次數最多的任務。
    # 顯示鼓勵訊息，讓孩子更有成就感。
    best = df.groupby("task")["done_times"].sum().sort_values(ascending=False)
    best_task = best.index[0] if not best.empty else "-"
    st.markdown(f"<div class='cheer'>🏆 每一個小小的努力，都是成長的大步！本月最常完成的是「{best_task}」，繼續保持！ ⭐</div>", unsafe_allow_html=True)


####################################################
# 13. 個人表現比較 render_child_compare
# 建立一個「個人表現比較」區塊。
# 用 st.columns(2) 把畫面分成兩欄，分別顯示哥哥和弟弟。
# sub：篩選出某個孩子的紀錄。
# 計算：
    # total：應完成次數。
    # done：實際完成次數。
    # points：獎勵點數。
    # rate：完成率。
# color_class：不同孩子用不同顏色的進度條。

# 每個孩子顯示一張卡片：
# 👦 頭像。
# 完成率（百分比）。
# 進度條（不同顏色）。
# 完成次數、應完成次數、獎勵點數。
# 用 CSS class .child-card 美化。
# 這樣就能直觀比較兩位孩子的表現。
####################################################

def render_child_compare(df: pd.DataFrame) -> None:
    st.markdown("<div class='soft-card'><div class='section-title'>個人表現比較</div>", unsafe_allow_html=True)
    cols = st.columns(2)
    for i, child in enumerate(CHILDREN):
        sub = df[df["child"] == child]
        total = int(sub["times"].sum())
        done = int(sub["done_times"].sum())
        points = int(sub["earned_points"].sum())
        rate = done / total if total else 0
        color_class = "" if i == 0 else " green-bar"
        with cols[i]:
            st.markdown(
                f"""
                <div class="child-card">
                  <div class="avatar">👦</div>
                  <h3>{child}</h3>
                  <div>完成率</div>
                  <div class="big-percent" style="color:{'#7c3aed' if i == 0 else '#10b981'}">{rate:.1%}</div>
                  <div class="progress-bg"><div class="progress-bar{color_class}" style="width:{rate*100:.0f}%"></div></div>
                  <div>完成次數　<b>{done}</b> 次</div>
                  <div>總應完成　<b>{total}</b> 次</div>
                  <div>獎勵點數　<b>{points}</b> 點</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)



####################################################
# 14. 資料清理報告 render_cleaning
# 顯示清理後資料的基本統計：
    # 總筆數。
    # 欄位數。
    # 空值數量。
    # 重複列數。

# 提示清理規則。
# 顯示每個欄位的型態與空值數。
# 提供下載清理後 CSV 的按鈕。
# 這部分是給家長或老師檢查資料品質用的。
####################################################

def render_cleaning(df: pd.DataFrame) -> None:
    st.subheader("資料清理與統合報告")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("資料筆數", len(df))
    c2.metric("欄位數", len(df.columns))
    c3.metric("空值總數", int(df.isna().sum().sum()))
    c4.metric("重複列", int(df.duplicated().sum()))
    st.info("清理規則：日期轉換、次數與點數轉數值、完成欄位標準化、計算 earned_points 與 done_times。")
    dtype_df = pd.DataFrame({"欄位": df.columns, "型態": [str(t) for t in df.dtypes], "空值": [int(df[c].isna().sum()) for c in df.columns]})
    st.dataframe(dtype_df, use_container_width=True, hide_index=True)
    st.download_button("下載清理後資料 CSV", df.to_csv(index=False).encode("utf-8-sig"), "cleaned_housework_data.csv", "text/csv", use_container_width=True)


####################################################
# 15. 家事項目管理 render_task_schema
# 顯示一個表格，列出建議的欄位：
# date：日期。
# child：孩子。
# category：類別。
# task：項目。
# times：次數。
# completed：是否完成。
# points：每次點數。
# mood：完成狀態。
# note：備註。
# 每個欄位都有「說明」和「用途」。
# 這部分是給家長或老師參考，確保紀錄表格設計合理。

# 顯示另一個表格，列出所有建議的家事項目。
# 每個項目包含：
# 類別。
# 項目名稱。
# 建議點數（從 DEFAULT_POINTS 取值）。
# 用 st.dataframe 顯示成表格。
# 這樣就能一目了然知道有哪些家事任務，以及建議的獎勵點數。
####################################################

def render_task_schema() -> None:
    st.subheader("建議的家事紀錄表欄位")
    schema = pd.DataFrame([
        ["date", "日期", "每天紀錄與月報統計"], ["child", "孩子", "哥哥 / 弟弟"], ["category", "類別", "減少太零散的欄位"],
        ["task", "項目", "具體可觀察行為"], ["times", "次數", "一天多次完成可累計"], ["completed", "是否完成", "是 / 否"],
        ["points", "每次點數", "用來做獎勵與 MVP"], ["mood", "完成狀態", "區分主動與提醒"], ["note", "備註", "少量紀錄即可，不要過度紀錄"],
    ], columns=["欄位", "說明", "用途"])
    st.dataframe(schema, use_container_width=True, hide_index=True)
    st.subheader("建議項目")
    task_rows = []
    for cat, tasks in TASK_OPTIONS.items():
        for task in tasks:
            task_rows.append({"類別": cat, "項目": task, "建議點數": DEFAULT_POINTS.get(task, 1)})
    st.dataframe(pd.DataFrame(task_rows), use_container_width=True, hide_index=True)


####################################################
# 16. 主程式流程 main
# 設定網頁標題、icon、版面。
# 呼叫 css() 套用自訂樣式。
####################################################

def main() -> None:
    st.set_page_config(page_title="家事紀錄儀表板", page_icon="🏠", layout="wide")
    css()
    with st.sidebar:
        st.title("🏠 家事紀錄儀表板")
        st.caption("兩位小男生的成長日常")
        page = st.radio("功能選單", ["總覽儀表板", "線上填寫", "資料清理", "家事項目管理", "資料表"], label_visibility="collapsed")
        st.divider()
        uploaded = st.file_uploader("上傳 Excel / CSV 檔案", type=["csv", "xlsx", "xls"])
        st.caption("未上傳時：優先讀取線上表單紀錄；若沒有紀錄，使用範例資料。")
        if SAMPLE_PATH.exists():
            st.download_button("下載資料範本 CSV", SAMPLE_PATH.read_bytes(), "housework_month_sample.csv", "text/csv", use_container_width=True)


    # 嘗試載入並清理資料。
    # 如果失敗 → 顯示錯誤並停止。
    try:
        df = clean_data(load_file(uploaded))
    except Exception as exc:
        st.error(str(exc))
        st.stop()


    # 側邊欄提供篩選功能：
    # 月份。
    # 孩子。
    # 類別。
    months = sorted(df["month"].dropna().unique())
    selected_month = st.sidebar.selectbox("月份選擇", months, index=len(months)-1 if months else 0)
    selected_child = st.sidebar.selectbox("孩子選擇", ["全部"] + sorted(df["child"].dropna().unique()))
    selected_category = st.sidebar.selectbox("類別選擇", ["全部"] + sorted(df["category"].dropna().unique()))

    # 根據選擇的條件過濾資料。
    filtered = df[df["month"] == selected_month]
    if selected_child != "全部":
        filtered = filtered[filtered["child"] == selected_child]
    if selected_category != "全部":
        filtered = filtered[filtered["category"] == selected_category]


    # 根據選單顯示不同頁面：
    # 總覽 → render_overview
    # 線上填寫 → render_form
    # 資料清理 → render_cleaning
    # 項目管理 → render_task_schema
    # 資料表 → 顯示原始表格。
    hero(selected_month)
    if page == "總覽儀表板":
        render_overview(filtered)
    elif page == "線上填寫":
        render_form()
        st.divider()
        st.subheader("最近填寫紀錄")
        try:
            latest = clean_data(load_file(None)).sort_values("created_at", ascending=False).head(30)
            st.dataframe(latest[FORM_COLUMNS], use_container_width=True, hide_index=True)
        except Exception:
            st.info("目前尚無填寫紀錄。")
    elif page == "資料清理":
        render_cleaning(filtered)
    elif page == "家事項目管理":
        render_task_schema()
    else:
        st.dataframe(filtered, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()

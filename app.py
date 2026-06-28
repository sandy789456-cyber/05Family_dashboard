"""家事紀錄儀表板 V3

Run:
    python -m streamlit run app.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

APP_DIR = Path(__file__).parent
SAMPLE_PATH = APP_DIR / "sample_data" / "housework_month_sample.csv"
DATA_DIR = APP_DIR / "data"
RECORD_PATH = DATA_DIR / "housework_records.csv"

CHILDREN = ["哥哥", "弟弟"]
CATEGORY_ORDER = ["個人清潔", "居家整理", "學習相關", "餐飲協助", "生活自理", "其他"]
TASK_OPTIONS = {
    "個人清潔": ["刷牙洗臉", "洗澡", "換衣服", "整理個人物品"],
    "居家整理": ["整理房間", "收拾玩具", "整理書桌", "倒垃圾", "掃地", "擦桌子"],
    "學習相關": ["閱讀", "完成作業", "整理書包", "練習才藝"],
    "餐飲協助": ["餐前擺碗筷", "餐後收拾", "擦餐桌", "協助分類回收"],
    "生活自理": ["準時起床", "準備明日用品", "衣物放洗衣籃", "鞋子排好"],
    "其他": ["主動幫忙", "禮貌表現", "情緒管理", "其他"],
}
DEFAULT_POINTS = {
    "刷牙洗臉": 2, "洗澡": 2, "換衣服": 1, "整理個人物品": 2,
    "整理房間": 4, "收拾玩具": 3, "整理書桌": 3, "倒垃圾": 3, "掃地": 4, "擦桌子": 3,
    "閱讀": 4, "完成作業": 5, "整理書包": 3, "練習才藝": 4,
    "餐前擺碗筷": 2, "餐後收拾": 3, "擦餐桌": 3, "協助分類回收": 3,
    "準時起床": 2, "準備明日用品": 3, "衣物放洗衣籃": 2, "鞋子排好": 1,
    "主動幫忙": 3, "禮貌表現": 2, "情緒管理": 4, "其他": 1,
}
REQUIRED_COLUMNS = ["date", "child", "category", "task", "times", "completed", "points"]
FORM_COLUMNS = [
    "date", "child", "category", "task", "times", "completed", "points",
    "mood", "recorder", "note", "created_at",
]


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


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError("資料缺少必要欄位：" + ", ".join(missing))
    for col in FORM_COLUMNS:
        if col not in df.columns:
            df[col] = "" if col in ["mood", "recorder", "note", "created_at"] else 0
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["child"] = df["child"].astype(str).str.strip()
    df["category"] = df["category"].astype(str).str.strip()
    df["task"] = df["task"].astype(str).str.strip()
    df["times"] = pd.to_numeric(df["times"], errors="coerce").fillna(0).astype(int)
    df["points"] = pd.to_numeric(df["points"], errors="coerce").fillna(0).astype(int)
    df["completed"] = df["completed"].astype(str).str.strip().str.lower().replace(
        {"true":"是","1":"是","yes":"是","y":"是","完成":"是","false":"否","0":"否","no":"否","n":"否","未完成":"否"}
    )
    df["is_completed"] = df["completed"].eq("是")
    df["earned_points"] = df["times"] * df["points"] * df["is_completed"].astype(int)
    df["done_times"] = df["times"] * df["is_completed"].astype(int)
    df["day"] = df["date"].dt.strftime("%m/%d")
    df["month"] = df["date"].dt.strftime("%Y-%m")
    return df.dropna(subset=["date"])


def append_record(record: dict[str, object]) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    row = pd.DataFrame([record], columns=FORM_COLUMNS)
    if RECORD_PATH.exists() and RECORD_PATH.stat().st_size > 0:
        old = pd.read_csv(RECORD_PATH)
        out = pd.concat([old, row], ignore_index=True)
    else:
        out = row
    out.to_csv(RECORD_PATH, index=False, encoding="utf-8-sig")


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


def summary(df: pd.DataFrame) -> dict[str, object]:
    total_days = int(df["date"].dt.date.nunique())
    total_possible = int(df["times"].sum())
    total_done = int(df["done_times"].sum())
    total_points = int(df["earned_points"].sum())
    avg_daily = total_done / total_days if total_days else 0
    rate = total_done / total_possible if total_possible else 0
    child_points = df.groupby("child")["earned_points"].sum().sort_values(ascending=False)
    mvp = child_points.index[0] if not child_points.empty else "-"
    return {"days": total_days, "done": total_done, "points": total_points, "avg": avg_daily, "rate": rate, "mvp": mvp}


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


def render_form() -> None:
    st.markdown("<div class='section-title'>📝 今日填寫表單</div>", unsafe_allow_html=True)

    # 注意：
    # Streamlit 的 st.form 內部元件不會在選擇類別後立即重新整理，
    # 所以「類別 / 項目」連動要放在一般 widget 中，而不是放在 st.form 裡。
    # 這裡保留原本 4 欄 + 4 欄 + 備註 + 送出按鈕的版面配置，只修正連動邏輯。
    c1, c2, c3, c4 = st.columns([1, 1, 1.2, 1.2])

    record_date = c1.date_input("日期", key="record_date")
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


def render_overview(df: pd.DataFrame) -> None:
    s = summary(df)

    # 不要一次塞 6 張 KPI 卡。
    # 在 1366px 筆電寬度下，6 欄會很擠，所以改成 3 + 3。
    kpi_row_1 = st.columns(3, gap="large")
    with kpi_row_1[0]:
        kpi_card("總完成天數", f"{s['days']} 天", "本月有紀錄的天數", "📅")
    with kpi_row_1[1]:
        kpi_card("總完成次數", f"{s['done']} 次", f"達成率 {s['rate']:.1%}", "✅")
    with kpi_row_1[2]:
        kpi_card("平均每日完成", f"{s['avg']:.1f} 次", "依完成次數計算", "⭐")

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    kpi_row_2 = st.columns(3, gap="large")
    with kpi_row_2[0]:
        kpi_card("最高連續天數", "-", "下一版可加入 streak", "🏅")
    with kpi_row_2[1]:
        kpi_card("總獎勵點數", f"{s['points']} 點", "完成項目才計分", "💖")
    with kpi_row_2[2]:
        kpi_card("本月 MVP", str(s["mvp"]), "依點數排序", "👑")

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

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
        weak = df.groupby("task", as_index=False).agg(done=("done_times", "sum"), total=("times", "sum"))
        weak["rate"] = weak["done"] / weak["total"].replace(0, pd.NA)
        weak = weak.dropna().sort_values("rate").head(5)
        st.markdown("<div class='soft-card'><div class='section-title'>⚠️ 需要加強的項目</div>", unsafe_allow_html=True)
        for _, r in weak.iterrows():
            pct = int(r["rate"] * 100)
            st.markdown(f"<div class='rank-row'><div>♨ {r['task']}</div><div class='mini-bar-bg'><div class='mini-bar weak' style='width:{pct}%'></div></div><div>{pct}%</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c:
        render_child_compare(df)

    best = df.groupby("task")["done_times"].sum().sort_values(ascending=False)
    best_task = best.index[0] if not best.empty else "-"
    st.markdown(f"<div class='cheer'>🏆 每一個小小的努力，都是成長的大步！本月最常完成的是「{best_task}」，繼續保持！ ⭐</div>", unsafe_allow_html=True)


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

    try:
        df = clean_data(load_file(uploaded))
    except Exception as exc:
        st.error(str(exc))
        st.stop()

    months = sorted(df["month"].dropna().unique())
    selected_month = st.sidebar.selectbox("月份選擇", months, index=len(months)-1 if months else 0)
    selected_child = st.sidebar.selectbox("孩子選擇", ["全部"] + sorted(df["child"].dropna().unique()))
    selected_category = st.sidebar.selectbox("類別選擇", ["全部"] + sorted(df["category"].dropna().unique()))
    filtered = df[df["month"] == selected_month]
    if selected_child != "全部":
        filtered = filtered[filtered["child"] == selected_child]
    if selected_category != "全部":
        filtered = filtered[filtered["category"] == selected_category]

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

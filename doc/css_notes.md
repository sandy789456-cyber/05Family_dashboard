**CSS 程式碼 + 註解** 整理成一份好閱讀的 **Markdown 文件**，方便你快速瀏覽與分享：

---

# 🎨 CSS 樣式與註解整理

## 🌈 全域變數
```css
:root {
    --purple:#7c3aed;   /* 紫色 */
    --green:#10b981;    /* 綠色 */
    --blue:#3b82f6;     /* 藍色 */
    --pink:#ec4899;     /* 粉紅色 */
    --ink:#111827;      /* 深墨色 */
    --muted:#64748b;    /* 灰藍色 */
}
```

---

## 🖥️ App 與 Sidebar
```css
.stApp {
    background:linear-gradient(135deg,#fbfcff 0%,#f7f2ff 38%,#f0fff8 100%);
    /* App 背景：斜角漸層，淡藍白 → 淡紫 → 淡綠 */
}

section[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#fff 0%,#f7f1ff 100%);
    border-right:1px solid #eadcff;
    /* 側邊欄：垂直漸層，白 → 淡紫，右邊框淡紫 */
}

section[data-testid="stSidebar"] .stRadio label {
    font-weight:750; /* 側邊欄選項字體加粗 */
}
```

---

## 📦 主內容區塊
```css
.main .block-container {
    padding-top:1.4rem;
    max-width:1500px;
    padding-left:2rem;
    padding-right:2rem;
    /* 主內容：限制寬度，左右留白 */
}
```

---

## 🦸 Hero 區塊
```css
.hero {
    display:flex; justify-content:space-between; align-items:center;
    gap:20px; padding:18px 22px; margin-bottom:18px;
    border:1px solid #e8e6f5; border-radius:28px;
    background:rgba(255,255,255,.82);
    box-shadow:0 14px 36px rgba(60,40,120,.08);
    /* Hero 區塊：Flex 排版，半透明白底，圓角 + 陰影 */
}

.hero h1 {
    font-size:28px; margin:0; color:var(--ink); font-weight:900;
    /* Hero 標題：大字、深墨色、極粗 */
}

.hero p {
    margin:.35rem 0 0; color:#475569; font-weight:650;
    /* Hero 副標題：灰藍色、半粗 */
}
```

---

## 📊 KPI 卡片
```css
.kpi-card {
    min-height:168px; padding:20px 22px; border-radius:24px;
    background:rgba(255,255,255,.94);
    border:1px solid #e8e8f3;
    box-shadow:0 12px 32px rgba(20,30,70,.08);
    /* KPI 卡片：白底半透明，圓角，陰影 */
}

.kpi-icon {
    width:52px; height:52px; border-radius:17px;
    display:flex; align-items:center; justify-content:center;
    font-size:29px; margin-bottom:10px;
    background:linear-gradient(135deg,#ede9fe,#eff6ff);
    /* KPI 圖示：紫到藍漸層背景 */
}

.kpi-title { font-size:14px; font-weight:800; color:#64748b; }
.kpi-value { font-size:36px; font-weight:950; color:#0f172a; margin-top:6px; }
.kpi-subtitle { font-size:13px; color:#64748b; margin-top:10px; font-weight:650; }
```

---

## 🧩 卡片與區塊
```css
.soft-card {
    padding:20px; border-radius:24px;
    background:rgba(255,255,255,.92);
    border:1px solid #e8e8f3;
    box-shadow:0 12px 30px rgba(20,30,70,.07);
    margin-bottom:18px;
    /* 柔和卡片：白底半透明，圓角，陰影 */
}

.section-title {
    font-size:19px; font-weight:900; color:#172033; margin-bottom:10px;
    /* 區塊標題：大字、極粗、深色 */
}

.child-card {
    padding:22px; border-radius:24px; background:white;
    border:1px solid #e8e8f3;
    box-shadow:0 12px 30px rgba(20,30,70,.07);
    /* 子卡片：白底，圓角，陰影 */
}
```

---

## 👤 Avatar 與百分比
```css
.avatar {
    width:76px; height:76px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:42px; margin-bottom:8px;
    background:linear-gradient(135deg,#bfdbfe,#d1fae5);
    /* 頭像：圓形，藍綠漸層背景 */
}

.big-percent {
    font-size:36px; font-weight:950; margin:3px 0; color:#7c3aed;
    /* 大百分比數字：紫色，極粗 */
}
```

---

## 📈 進度條
```css
.progress-bg {
    height:9px; border-radius:999px; background:#e9edf4;
    overflow:hidden; margin:7px 0 16px;
    /* 進度條背景：灰色，圓角 */
}

.progress-bar {
    height:100%; border-radius:999px;
    background:linear-gradient(90deg,#7c3aed,#a855f7);
    /* 紫色漸層進度條 */
}

.green-bar {
    background:linear-gradient(90deg,#10b981,#34d399);
    /* 綠色漸層進度條 */
}
```

---

## 🏆 排名列與小進度條
```css
.rank-row {
    display:grid; grid-template-columns:1.3fr 2fr .6fr;
    align-items:center; gap:12px; margin:12px 0;
    font-weight:750; color:#334155;
    /* 排名列：三欄格局，粗字體，深灰藍色 */
}

.mini-bar-bg {
    height:8px; border-radius:999px; background:#edf0f5; overflow:hidden;
    /* 小進度條背景 */
}

.mini-bar {
    height:100%; border-radius:999px;
    background:linear-gradient(90deg,#7c3aed,#60a5fa);
    /* 小進度條：紫到藍漸層 */
}

.weak {
    background:linear-gradient(90deg,#fb7185,#fca5a5);
    /* 弱勢進度條：紅色漸層 */
}
```

---

## 🎉 Cheer 提示
```css
.cheer {
    margin-top:18px; padding:18px 22px; border-radius:22px;
    background:linear-gradient(90deg,#f3fff1,#fffbea);
    border:1px solid #d9f99d; color:#16a34a;
    font-size:18px; font-weight:900;
    /* 鼓勵提示：綠黃漸層背景，綠字，粗體 */
}
```

---

## 📑 Streamlit 元件
```css
div[data-testid="stMetric"] {
    background:white; border:1px solid #e8e8f3;
    border-radius:18px; padding:12px;
    /* Streamlit KPI 卡片：白底，圓角，邊框 */
}

.stTabs [data-baseweb="tab-list"] { gap:8px; }
.stTabs [data-baseweb="tab"] {
    border-radius:999px; padding:10px 18px;
    background:white; border:1px solid #e8e8f3;
    font-weight:800;
    /* Tabs：圓角膠囊，白底，粗字體 */
}
```

---


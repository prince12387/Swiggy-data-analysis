<div align="center">

<img src="assets/swiggy_logo.jpg" alt="Swiggy" width="140"/>

# Swiggy Restaurant Intelligence
### Power BI Analytics Dashboard + AI Q&A Chatbot (Streamlit · LangChain · Grok)

**Clean the data. Find the insights. Just ask.**

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Cleaning-150458?logo=pandas&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi&logoColor=black)
![LangChain](https://img.shields.io/badge/LangChain-xAI%20Grok-1C3C3C)

</div>

---

## 📑 Table of Contents

- [About](#-about)
- [Dashboard Preview](#️-dashboard-preview)
- [Highlights](#-highlights)
- [Dataset](#-dataset)
- [Project Structure](#-project-structure)
- [Installation](#️-installation)
- [Usage](#-usage)
- [How the Chatbot Works](#-how-the-chatbot-works)
- [Key Insights](#-key-insights)
- [Limitations](#️-limitations)
- [Roadmap](#-roadmap)
- [Troubleshooting](#-troubleshooting)
- [Disclaimer](#-disclaimer)

---

## 📌 About

An end-to-end analytics project on **118 Swiggy restaurants** across Bangalore (Koramangala, BTM, HSR and Jayanagar). It covers the full workflow:

1. 🧹 **Clean** raw data: broken ₹ symbols, missing ratings, messy locations, multi-valued cuisines
2. 📊 **Analyze** KPIs and visualize them in a **Power BI dashboard**
3. 🤖 **Chat** with the data using a Streamlit Q&A bot powered by **Grok (xAI)**

## 🖼️ Dashboard Preview

<div align="center">
<img src="assets/dashboard_preview.jpg" alt="Swiggy Restaurant Analytics Dashboard" width="800"/>
</div>

The dashboard includes 5 KPI cards, 4 slicers (Area, Rating, Cost, Cuisine) and visuals for restaurants by area, top cuisines, top-rated restaurants and cost vs rating.

## 📈 Highlights

| Restaurants | Avg Rating | Avg Cost for Two | Rated ≥ 4.0 |
|:-----------:|:----------:|:----------------:|:-----------:|
| **118** | **4.10 ⭐** | **₹321** | **78%** |

- 📍 Koramangala has the most restaurants (64), followed by BTM (35) and HSR (18)
- 💰 HSR is the priciest area (~₹389 for two); Koramangala is the most affordable (~₹298)
- 🏆 Top rated: Khichdi Experiment (4.8)

## 📊 Dataset

**Raw file:** `swiggy.xls` → **Cleaned file:** `swiggy_cleaned.csv` (118 rows × 7 columns)

| Column | Description |
|--------|-------------|
| `Shop_Name` | Restaurant name |
| `Cuisine` | Comma-separated cuisines |
| `Location` | Original locality string |
| `Area` | Standardized area (Koramangala, HSR, BTM, Jayanagar) |
| `Rating` | Customer rating (1 missing value) |
| `Cost_for_Two` | Approximate cost for two, in ₹ |
| `Cost_Bucket` | `≤200`, `201-300`, `301-400`, `401-500`, `>500` |

**Cleaning steps:** fixed garbled `â‚¹` symbols, converted `--` ratings to nulls, derived a standardized `Area`, normalized cuisine strings, removed duplicates and assigned proper data types.

**KPIs computed:** overall summary, area-wise performance, top 10 rated, best value (rating ≥ 4.2 and cost ≤ ₹300), top cuisines, rating distribution and cost bucket analysis.

## 📁 Project Structure

```
├── assets/
│   ├── swiggy_logo.jpg
│   └── dashboard_preview.jpg
├── swiggy.xls                       # Raw data
├── swiggy_cleaned.csv               # Cleaned data
├── Swiggy_Data_Cleaning_KPIs.ipynb  # Cleaning + KPI analysis
├── Swiggy.pbix                      # Power BI dashboard
├── swiggy_chatbot_app.py            # Streamlit chatbot
├── Swiggy_QA_Chatbot.ipynb          # Notebook chatbot
├── requirements.txt
└── README.md
```

## ⚙️ Installation

**Prerequisites:** Python 3.10+, an [xAI API key](https://console.x.ai/) (chatbot only) and Power BI Desktop (to open the `.pbix`).

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# 2. (Optional) create a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Extra packages for the cleaning notebook
pip install numpy matplotlib seaborn xlrd openpyxl jupyter
```

## 🚀 Usage

### 1. Data cleaning & KPI analysis

Open `Swiggy_Data_Cleaning_KPIs.ipynb` and run all cells.

> The notebook uses `/workspace/...` paths. Change the input to `swiggy.xls` and the output to `swiggy_cleaned.csv` before running locally.

### 2. Power BI dashboard

Open `Swiggy.pbix` in Power BI Desktop. If the data source breaks, go to **Home → Transform data → Data source settings**, point it to your local `swiggy_cleaned.csv` and click **Refresh**.

### 3. Streamlit chatbot

```bash
streamlit run swiggy_chatbot_app.py
```

Open `http://localhost:8501`, paste your **xAI API key** in the sidebar and start asking. You can also set the key as an environment variable:

```bash
export XAI_API_KEY="your-key-here"      # macOS / Linux
setx XAI_API_KEY "your-key-here"        # Windows (restart terminal)
```

### 💬 Try asking

- *Highest rated restaurants in Koramangala?*
- *Biryani places under Rs.400*
- *Which area has the most restaurants?*
- *Best value North Indian restaurants*
- *Ice cream shops with rating above 4.5*
- *Compare biryani options in Koramangala vs BTM*

## 🧠 How the Chatbot Works

```
Question → Keyword retrieval (top-k restaurants) → Prompt → Grok → Answer
```

1. Each CSV row becomes a text chunk (name, cuisines, location, area, rating, cost).
2. Query words are matched against chunks and the top 12 are retrieved.
3. `grok-4-latest` (temperature 0.1) answers using **only** the retrieved records and never invents data.

## 🔍 Key Insights

- Koramangala holds about **54%** of all listings (64 of 118).
- Ratings are consistently high: **78%** of restaurants are rated 4.0 or above.
- Average ratings are tightly clustered: Koramangala ≈ 4.13, HSR ≈ 4.07, BTM ≈ 4.05.
- The most common price band is **₹201–300** (37 restaurants), followed by ≤ ₹200 (30).
- About **24 restaurants** qualify as best value (rating ≥ 4.2 and cost ≤ ₹300).

## ⚠️ Limitations

- Keyword retrieval is not semantic, and only the top 12 matches reach the model, so "average" and "how many" questions may be approximate.
- Jayanagar has only 1 restaurant, so area comparisons for it are not meaningful.
- The data is a point-in-time snapshot and is not refreshed automatically.

## 🔮 Roadmap

- [ ] Pandas-based aggregation for exact counts and averages
- [ ] Embedding-based semantic search (FAISS / Chroma)
- [ ] Cuisine-level analysis in Power BI
- [ ] Docker + Streamlit Community Cloud deployment

## 🧰 Troubleshooting

| Problem | Fix |
|---------|-----|
| `Cleaned CSV not found` | Keep `swiggy_cleaned.csv` in the same folder as `swiggy_chatbot_app.py` and run from there |
| `Missing optional dependency 'xlrd'` | `pip install xlrd` (needed for `.xls`) |
| `FileNotFoundError: /workspace/...` | Change notebook paths to local relative paths |
| 401 / authentication error | Check your xAI API key and account credits |
| Images not showing on GitHub | Make sure the `assets/` folder is uploaded and names match exactly (case-sensitive) |

## 📜 Disclaimer

This is an educational / portfolio project and is **not affiliated with or endorsed by Swiggy**. The Swiggy name and logo belong to their respective owners. Restaurant data is a snapshot and may not reflect current ratings or prices.

---

<div align="center">

⭐ If you found this project useful, consider giving it a star!

</div>

# 🏘️ Intelligent Property Investment Dashboard (City-Level ROI Analysis)

This project is a real estate data analysis and dashboarding solution that aims to help investors, analysts, and businesses identify high-return property opportunities across major Indian cities like Mumbai, Hyderabad, Kolkata, and Gurgaon. The solution performs automated data ingestion, decoding, preprocessing, exploratory data analysis (EDA), price per square foot (₹/sqft) computation, and exports insights to Excel and Power BI.

---

## 📌 Objective

To build a data-driven system that:
- Ingests and cleans raw real estate listings using a SQLite pipeline.
- Decodes categorical IDs using reference tables (`facets/`).
- Derives key investment metrics like `PRICE_PER_SQFT`.
- Performs EDA to uncover ROI-friendly localities and property patterns.
- Presents findings via interactive Power BI dashboards.

---

## 🧱 Tech Stack

| Component        | Tools/Technologies                      |
|------------------|-----------------------------------------|
| Data Ingestion   | Python (`pandas`, `sqlite3`, `logging`) |
| Data Storage     | SQLite                                  |
| Data Cleaning    | SQL, Python                             |
| EDA & Analysis   | Python (`pandas`, `matplotlib`, `seaborn`) |
| Dashboarding     | Power BI                                |
| Exporting        | CSV, Excel                              |
| Version Control  | Git + GitHub                            |

---

## 🔄 Workflow

### **Data Ingestion & Decoding**
- Reads raw city-wise listing files from `/data/raw/`.
- Loads facet tables (e.g., `facing_direction`, `age`, etc.) for decoding encoded categorical variables.
- Stores cleaned data in SQLite for easy querying and reproducibility.

### **Feature Engineering**
- Computes `PRICE_PER_SQFT` using best available area column (e.g., `AREA`, `SUPERBUILTUP_SQFT`, etc.).
- Drops invalid rows (zero or missing price/area).
- Exports cleaned tables to `/data/processed/`.

### **Exploratory Data Analysis (EDA)**
- Analyze price trends, location-based pricing, area distribution.
- Identify overpriced or undervalued localities.
- Investigate the role of amenities, property age, facing, floor, etc.

### **Dashboarding (Planned)**
- Create Power BI dashboards comparing cities on:
  - Avg ₹/sqft by locality
  - Distribution of property types
  - Age vs. price correlation
  - Area-wise investment potential

---

## 📈 Future Enhancements

- [ ] Add Power BI dashboard
- [ ] Compare ROI across cities based on rental yield
- [ ] Property image scraping & tagging (for property type consistency)
- [ ] Streamlit app for interactive querying

---

## ✨ Why This Project?

- Inspired by real-world analytics at firms like JLL, Knight Frank, and 99acres.
- Focused on investment viability, not just listing aggregation.
- Demonstrates strong data cleaning, decoding, pipeline, and visualization skills.

---

## 📬 Contact

Made with 💻 by **[Your Name]**  
📫 [baliyans333@gmail.com]

# 📊 DataPolish — Smart CSV & Excel Data Cleaner SaaS Web Application

## 📌 Project Overview
**DataPolish** is a cloud-ready, automated data cleaning and transformation web application built using **Python, Streamlit, and Pandas**. It allows users, data analysts, and e-commerce business owners to upload unformatted, duplicate-ridden CSV and Excel exports, instantly detect data quality anomalies, apply automated normalization pipelines, visualize distribution insights, and export audit-ready Excel reports.

---

## 🎯 Business Problem Solved
Small business owners, digital marketing agencies, and operations teams spend an average of 4–6 hours weekly fixing broken spreadsheets:
1. **Duplicate Records:** Inflating sales counts and generating redundant outbound emails.
2. **Inconsistent Casing & Whitespace:** Corrupting database lookups (`VLOOKUP` / `XLOOKUP`).
3. **Mixed Currency & Number Formats:** Text strings like `$450` or `₹1,200` preventing mathematical analysis.
4. **Non-Standard Date Formats:** Mixed dates (`16/01/2024` vs `Jan 17 2024`) breaking timeline aggregations.

---

## 🛠️ Key Features
- **Multi-Format Ingestion:** Seamless support for `.csv` and `.xlsx` uploads, plus a one-click built-in test dataset.
- **Automated Quality Audit:** Real-time metrics showing total original rows, cleaned rows, detected duplicates, and cleaned columns.
- **Configurable Cleaning Pipeline:**
  - Automatic Deduplication (drop duplicate records)
  - String Trimming (eliminate leading/trailing whitespaces)
  - Text Normalization (convert to Proper Title Case)
  - Currency & Numeric Sanitization (strip non-numeric currency symbols)
  - Date Standardization (parse and format all dates to ISO `YYYY-MM-DD`)
- **Interactive Multi-Tab Dashboard:**
  - *Cleaned Dataset:* Full interactive dataframe viewer.
  - *Before vs After Diff:* Side-by-side comparison of raw input vs cleaned output.
  - *Analytics & Charts:* Instant categorical distribution bar charts.
- **Audit-Ready Exports:**
  - Download Cleaned `.xlsx` (Multi-sheet workbook preserving original and clean data).
  - Download Cleaned `.csv`.

---

## 📁 Repository Structure
```text
├── app.py                      # Main Streamlit web application
├── sample_messy_data.csv       # Sample uncleaned dataset for live testing
├── requirements.txt            # Cloud deployment dependencies
└── README.md                   # Technical documentation
```

---

## 🚀 How to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/Onkarhande96/datapolish-excel-cleaner-app.git
   cd datapolish-excel-cleaner-app
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch the Streamlit application:
   ```bash
   streamlit run app.py
   ```
4. Open `http://localhost:8501` in your browser.

---

## 👨‍💻 Author
**Onkar Hande**  
- Portfolio: [https://onkarhande96.github.io](https://onkarhande96.github.io)  
- GitHub: [https://github.com/Onkarhande96](https://github.com/Onkarhande96)  
- LinkedIn: [https://linkedin.com/in/onkarhande96](https://linkedin.com/in/onkarhande96)

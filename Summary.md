# 📈 Data Pipeline - Summary

## 🚀 Overview
This project automates the extraction, transformation, and loading (ETL) of financial data from a Simply API into a structured SQL database. It includes error handling, data validation,visualization and stock attribution analysis for quantitative investing insights.

---

## 🔹 Workflow Overview

### 1. Extract (API Data Retrieval)
- Connect to **Financial API** & fetch data.
- Handle & optimise **batch queries** for large datasets.
- Implement **error handling** (Exponential backoff, incremental batch retries) to streamline process.
- Convert **JSON → DataFrame → Flattened DataFrame → CSV **.

### 2. Transform (Data Processing & Cleaning)
- Merge and map API fields to SQL schema (**ETL Mapping**).
- Remove **nulls, duplicates, and invalid entries**.
- Flag **out-of-tolerance** data.
- Validate **expected vs actual** data and retry.

### 3. Load (SQL Database Storage)
- Insert data into **temporary tables**.
- Use **constraints & indexing**.
- Move data to **actual tables** after validation.

### 4. Financial Analysis & Insights
- Retrieve **cleaned** data for analysis.
- Apply **Attribution Analysis** for stock filtering.
- Export final selection to **Excel** for final watchlist.

### 5. Visualization
- **Power BI Insights**.
- Generate interactive **dashboards & reports**.

---

## 🌍 Visualizing the Process
To better understand the pipeline, here are visual representations:

### 📝 ETL Workflow
![ETL Workflow](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Test/Png1_Update.jpeg)
![ETL Workflow2](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Test/page-2.png)
![ETL Workflow3](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Test/page-3.png)
![ETL Workflow4](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Test/Filtered.jpeg)

---

## 🔗 Full Project Details
For a **detailed breakdown**, check the [Main README](./README.md).




# ETL Pipeline for SWS API

## Overview

This ETL (Extract, Transform, Load) pipeline automates the process of retrieving, transforming and loading financial data from the Simply Wall St (SWS) API into a PostgreSQL database.

## Tech Stack

- **Python**
- **PostgreSQL**
- **Libraries : Pandas,requests,sqlalchemy**
- **Simply Wall St API**

---

## ETL Process

### 1. Extract

- **Exchange Data**: Retrieves exchange data, including company counts, which are used as parameters for main API requests.[Exchanges&Counts](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/SWS-ETL-Pipeline_Modularized/1.Extract/1.1Get_Exchanges_Counts)
- **Financial Data**: Extracts financial data for companies across categories like Listings, Insider Transactions, Members, Owners and Statements. The extraction includes retry logic & error logging to handle failed batches.
  [Company Data](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/SWS-ETL-Pipeline_Modularized/1.Extract/1.2Get_All_Data_3x_Try)

### 2. Transform

- **Data Transformation**: Converts the extracted data into the appropriate format for loading into the PostgreSQL database.[Transform](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/SWS-ETL-Pipeline_Modularized/2.Transform/2.1Transform)

### 3. Pre-Load QA

- **Data Integrity**: Create summary of expected vs received data ++ log errors.      
- **Interim ETL**: Compare current data with new ones that do not haver unique identifiers to ensure only valid data is processed.
    [Pre-Load QA](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/SWS-ETL-Pipeline_Modularized/3.Pre%20Load%20QA/3.1Pre%20Load%20QA)
### 4. Load

- **DB Import**: Load all data in DB (Python/SQL Integration)[Load](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/SWS-ETL-Pipeline_Modularized/4.Load/4.1Load)
  
### 5. Post-Load QA

- **Post Data Integrity**: Ensure that data imported in DB are as expected vs Pre-Load QA summary.[Post-Load QA](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/SWS-ETL-Pipeline_Modularized/5.Post%20Load%20QA/5.1Post%20Load%20QA)
- **Data Locking**: A PL/pgSQL trigger blocks modification operations (INSERT, UPDATE, DELETE) for records with a date earlier than the current month.
- **Backup Automation**: Automates PostgreSQL backups using the `pg_dump` utility, with timestamped filenames and environment variable management for credentials.
- **Clean Directory**: Archives old data, deletes predefined folders, and resets the project directory structure for the next pipeline run.

---

### 🔜 Next Up

Planned enhancements to improve and expand the project:

- 📈 **Financial Attribution Analysis**  
  Use financial metrics to analyze performance, valuations, and relative comparisons across sectors or companies.

- 📊 **Interactive Dashboard**  
  Build a front-end (e.g., Streamlit, Dash, or Power BI) to visualize financial metrics.

- 🔎 **Data Extraction from Text **  
  Extract structured data from notes, disclosures, or embedded text fields using NLP / Regex

---

### 🆔 Project Info

**Author:** *Nicholas Papadimitris *  
**Created on:** *05/04/2025 6:58 PM* (UTC)   
**Project ID:** `SWS_ETL_05_Apr2025`
**GitHub**: [My GitHub](https://github.com/NPStraight2ThePoint)

📧 **Email:** nicholas.papadimitris@gmail.com  
💼 **LinkedIn:** [Nicholas Papadimitris](https://www.linkedin.com/in/nicholas-papadimitris/)

## Disclaimer
API is still in beta, which means things are subject to change. Specs could be updated, limits might be introduced, paywalls added, or even certain features removed .




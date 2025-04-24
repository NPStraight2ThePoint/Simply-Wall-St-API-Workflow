# ETL Pipeline for SWS API

## Overview

This ETL (Extract, Transform, Load) pipeline automates the process of retrieving, transforming, and loading financial data from the Simply Wall St (SWS) API into a PostgreSQL database.

## 🧰 Tech Stack

- **Language**: Python 🐍  
- **Database**: PostgreSQL 🐘  
- **API Source**: [Simply Wall St API](https://simplywall.st)  
- **Libraries Used**:
  - `pandas` — Data manipulation and Excel/csv operations
  - `requests` — API communication  
  - `sqlalchemy` — Database connection and ORM support  
  - `psycopg2` — PostgreSQL driver for Python  
  - `openpyxl` — Excel writing engine for `.xlsx` output  

<br />

<details>
<summary>🧱 Project Architecture Overview</summary>

```plaintext
📁 Project Root
│
├── 📂 config/
│   ├── api_queries.py           # Predefined API query templates
│   ├── env_utils.py             # Environment variable utilities
│   └── settings.py              # Centralized settings/configs
│
├── 📂 utils/
│   ├── api_utils.py             # API data fetching logic
│   ├── core_pipeline.py         # Main ETL process orchestration
│   ├── dir_utils.py             # Directory creation and file org
│   ├── flatten_utils.py         # Flattening nested API JSONs
│   ├── io_utils.py              # File input/output helpers
│   ├── load_utils.py            # PostgreSQL data loading
│   ├── sql_utils.py             # SQL query helpers
│   └── transform_utils.py       # Data transformation and standardization
│
├── 📂 sql/
│   └── *.sql                    # Raw SQL templates used in queries
│
├── 📂 ETL/
│   ├── ETL_1X/
│   │   ├── get_exchange_counts.py
│   │   ├── extract_companies.py
│   │   ├── extract_all_data.py
│   │   ├── transform_data.py
│   │   └── load_to_db.py
│   │
│   └── ETL_2X/
│       ├── retry_failed_batches.py
│       ├── transform_missing.py
│       └── load_missing.py
│
├── 📂 Data_QA/
│   ├── QA_1_counts_check.py     # Checks missing tickers & row diffs
│   ├── QA_2_deduplication.py    # Removes duplicates + company-wise QA
│   ├── move_temp_to_prod.py     # Migrate tables from temp → prod
│   ├── backup_database.py       # Create DB snapshot before critical ops
│   └── cleanup_archive.py       # Archive logs / intermediate files
│
├── 📂 orchestrators/
│   ├── get_exchange_counts.py
│   ├── ETL_orchestrator.py
│   └── data_qa_runner.py
│
├── README.md
└── thought_process.md

</details>

### 🆔 Project Info

**Author:** *Nicholas Papadimitris*  
**Created on:** *05/04/2025 6:58 PM* (UTC)  
**Project ID:** `SWS_ETL_05_Apr2025`  
**GitHub:** [My GitHub](https://github.com/NPStraight2ThePoint)

📧 **Email:** nicholas.papadimitris@gmail.com  
💼 **LinkedIn:** [Nicholas Papadimitris](https://www.linkedin.com/in/nicholas-papadimitris/)

> Note: The data shown above is publicly available, and the API is used solely to optimize the data retrieval and processing process.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## Attribution

The financial data is publicly available and retrieved using the Simply Wall St API. Ensure to comply with the API's terms of service when using it.

## Disclaimer

API is still in beta, which means things are subject to change. Specs could be updated, limits might be introduced, paywalls added, or even certain features removed.






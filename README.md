# ETL Pipeline 

## Overview
This ETL (Extract, Transform, Load) pipeline automates the process of retrieving, transforming, and loading financial data from API into a PostgreSQL database. The pipeline is designed to make financial data processing and analysis easier by automating data flow, allowing for efficient querying, manipulation, and further analysis.

- **Extract**: Retrieves raw financial data from API using via Python.
- **Transform**: Cleanses and transforms the data, including flattening nested JSON structures, handling missing data and aligning data formats to the database schema.
- **Load**: Loads the transformed data into a PostgreSQL database, making it ready for analysis, querying and reporting.

## 🧰 Tech Stack

- **Language**: Python 🐍  
- **Database**: PostgreSQL 🐘  
- **Libraries Used**:
  - `pandas` — Data manipulation and Excel/csv operations
  - `requests` — API communication  
  - `sqlalchemy` — Database connection and ORM support  
  - `psycopg2` — PostgreSQL driver for Python  
  - `openpyxl` — Excel writing engine for `.xlsx` output  


## 💻 Workflow
For detailed descriptions of each script and their purpose, refer to the [Script Descriptions](SCRIPT_DESCRIPTIONS.md) file.

### 🆔 Project Info

**Author:** *Nicholas Papadimitris*  
**Created on:** *05/04/2025 6:58 PM* (UTC)  
**Last modified:** *24/04/2025 9:20 PM* (UTC)   
**Project ID:** `SWS_ETL_05_Apr2025`  
**GitHub:** [My GitHub](https://github.com/NPStraight2ThePoint)

📧 **Email:** nicholas.papadimitris@gmail.com  
💼 **LinkedIn:** [Nicholas Papadimitris](https://www.linkedin.com/in/nicholas-papadimitris/)

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.







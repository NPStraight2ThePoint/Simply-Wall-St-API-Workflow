# 🧩 FinSuite Adapter — Simply Wall St (Legacy)

![Status: Archived](https://img.shields.io/badge/status-archived-lightgrey)
![Tech: Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Database: PostgreSQL](https://img.shields.io/badge/postgres-✓-green)
![License: MIT](https://img.shields.io/badge/license-MIT-yellow)

> ⚠️ **Legacy Adapter Notice**  
> The Simply Wall St API used in this pipeline is no longer active.  
> This repository is preserved as a **case study** in *FinSuite’s* ETL architecture evolution — showcasing resilient multi-stage orchestration, QA validation, and database promotion design patterns that inspired the [`finsuite-etl-engine`](https://github.com/NPStraight2ThePoint/finsuite-etl-engine).

---

## 📘 Overview
This adapter automates the retrieval, transformation, and loading of **financial statement and insider-activity data** from the *Simply Wall St* API into a **PostgreSQL** database.  

It represents the first generation of FinSuite’s financial ETL design — handling batch extraction, schema alignment, quality assurance, and production promotion.  
The approach emphasizes **transparency**, **reliability**, and **auditability** across every ETL stage.

### Process Flow


---

## 🧰 Tech Stack
| Area | Tools |
|------|-------|
| Language | Python 🐍 |
| Database | PostgreSQL 🐘 |
| Core Libraries | `pandas`, `requests`, `sqlalchemy`, `psycopg2`, `openpyxl` |
| Architecture | Multi-step modular ETL with QA checkpoints |
| Data Model | Normalized relational schema for company fundamentals and insider transactions |

---

## 🧱 Repository Structure
| Folder | Purpose |
|---------|----------|
| **`etl/`** | Core extraction, transformation, and loading scripts |
| **`config/`** | Environment and connection settings (`.env`, `settings.py`) |
| **`SQL Queries/`** | Helper and validation queries |
| **`utils/`** | Common utility functions (directory, logging, retry helpers) |
| **`Architecture/`** | Diagrams and technical design notes |
| **`Process Visuals/`** | ETL flowcharts and data-transformation visuals |

---

## 🧮 Key Scripts
| Script | Purpose |
|---------|----------|
| `etl_1x_1_get_exchanges_counts.py` | Retrieve exchanges and company counts (used for workload estimation). |
| `etl_1x_2_get_companies.py` | Collect base metadata (ticker, exchange, ID, market cap). |
| `etl_1x_3_get_all_data_3x.py` | Perform bulk API extraction with batch/retry logic. |
| `etl_1x_4_transform.py` | Clean, flatten, and transpose data for DB compatibility. |
| `etl_1x_5_load.py` | Load to temporary SQL tables for validation. |
| `etl_2x_*` | Re-query and patch failed tickers by unique ID. |
| `data_qa_1_qa_1.py` | Duplicate detection and row-count reconciliation. |
| `data_qa_2_qa_2.py` | Track insider transaction activity per ticker. |
| `data_qa_3_move_to_prod.py` | Promote validated data from temp → prod tables. |
| `data_qa_4_db_backup.py` | Backup production DB and reset temp environment. |

---

## 🧠 Design Highlights
- **Two-pass extraction strategy** to recover failed batches.  
- **QA-gated promotion**: only validated data enters production schema.  
- **Temp-to-prod isolation** for safe validation and rollback.  
- **Automated DB backup** ensures recoverability and traceability.  
- **Modular script orchestration**, precursor to FinSuite’s central ETL Engine.

---

## 🧩 Relation to FinSuite Ecosystem
| Evolution Path | Description |
|----------------|-------------|
| 🔹 **`finsuite-etl-engine`** | Modern orchestration framework that generalizes this adapter’s workflow model. |
| 🔹 **`finsuite-core`** | Provides shared utilities for logging, configuration, and I/O used across adapters. |
| 🔹 **`testops-engine`** | Integrates standardized data-QA checks derived from this project’s validation layer. |

---

## 🖼️ Architecture Visual
![ETL Workflow](Process%20Visuals/Data%20Transformation.png)  
*Multi-stage ETL flow from API ingestion to PostgreSQL loading.*

---

## 🧪 Data & Security
- No proprietary or confidential data included.  
- `.env` file excluded from version control; replace with your own credentials.  
- Synthetic examples and schemas used for demonstration.

---

## 🧾 Project Info
| Field | Detail |
|-------|--------|
| Author | **Nicholas Papadimitris** |
| Created | 05 Apr 2025 |
| Last Modified | 24 Apr 2025 |
| License | MIT License |
| Contact | [LinkedIn](https://www.linkedin.com/in/nicholas-papadimitris) • [GitHub](https://github.com/NPStraight2ThePoint) |

---

## 🗺️ FinSuite Portfolio Reference
Part of the **FinSuite** ecosystem — a modular suite for financial ETL, analytics, and ML pipelines.  
See the [**Portfolio Hub → FinSuite Overview**](https://github.com/NPStraight2ThePoint/portfolio-hub) for end-to-end architecture and live demos.

---








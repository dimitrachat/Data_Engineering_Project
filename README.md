# Sales Data Engineering Pipeline

## Overview

This project implements a data pipeline for a retail company to process monthly sales data from raw CSV files and produce a cleansed, analytics ready dataset suitable for reporting and BI use cases.

The pipeline is implemented using **Apache Spark (PySpark)** and follows a **Medallion Architecture (Bronze → Silver → Gold)** to ensure scalability, maintainability, and data quality as data volume and ingestion frequency increase.

The current implementation runs locally using **VS Code and Spark**, but the design aligns with production data lake architectures.

##  Dataset Description

- Source: Monthly sales data in CSV format
- Files: 12 CSV files (1 year of data)
- Rows: 186,850
- Size: 15.4 MB (raw CSV)

Although the dataset size is moderate, the pipeline is designed with scalability in mind to support larger volumes and more frequent ingestion in the future.


## Architecture Overview

The pipeline follows a Medallion Architecture:

### Bronze Layer (Raw)

- Preserves the original data structure with minimal transformations
- Enforces schema to prevent incorrect type inference
- Removes fully null rows and repeated CSV headers ingested as data
- Renames columns to follow consistent naming conventions
- Outputs data in Parquet format with no partitioning

### Silver Layer (Cleansed)

- Applies core business and data quality logic
- Validates null patterns and critical fields
- Converts Order_Date to timestamp format
- Derives Order_Year and Order_Month for partitioning
- Removes duplicate records using a composite business key (Order_ID, Product)
- Outputs partitioned Parquet files by year and month

### Gold Layer (Aggregated)

- Produces aggregated, business-level metrics
- Monthly sales KPIs (revenue, units sold, total orders)
- Designed for direct consumption by BI and reporting tools

## Pipeline Structure

notebooks/
 ├── 01_sales_ingestion.ipynb        # Bronze ingestion
 ├── 02_sales_ETL.ipynb              # Silver transformations
 └── 03_sales_aggregated.ipynb       # Gold aggregations

src/
 ├── enforced_schemas.py             # CSV schema definitions
 ├── sqlqueries.py                   # SQL-based validations & transformations
 └── spark_session.py                # Spark session initialization

utils/
 └── logger.py                       # Custom logging utility

data/
 ├── raw/                            # Raw CSV files
 ├── bronze/                         # Bronze Parquet output
 ├── cleansed/                       # Silver Parquet output (partitioned)
 └── gold/                           # Gold aggregated output

Logs/
 └── <job_name>/
     └── YYYY-MM-logs.txt            # Monthly execution logs

## Data Quality & Validation

The pipeline includes explicit data quality checks to ensure reliability:

- Fully null rows are identified and removed during Bronze ingestion
- Null patterns are logged for visibility and debugging
- A threshold based validation fails the pipeline only when fully null rows exceed 50% of the dataset
- The Order_Date column is strictly validated, as it is required for partitioning and downstream aggregations
- Missing or invalid Order_Date values trigger an immediate pipeline failure (fail-fast approach)
- This strategy prevents silent data corruption while avoiding unnecessary failures due to minor anomalies.

## Deduplication Strategy

Duplicates are identified using the composite business key: (Order_ID, Product)

Assumption:
- A single product should not appear more than once per order

Deduplication logic:
- The most recent record is retained based on Order_Date
- Implemented using a window function

## Partitioning Strategy

Partitioning is applied at the Silver layer using:

**Order_Year / Order_Month**

Reasoning:

- Aligns with common analytical access patterns (monthly reporting, trends)
- Avoids excessive small files caused by daily partitioning
- Ensures partitioning is based on validated and standardized timestamps


## File Format Choice: Parquet

**Parquet** was chosen as the output format due to:

- Columnar storage optimized for analytical workloads
- Efficient column pruning and reduced capacity
- Built-in compression and encoding
- Schema enforcement to prevent silent data inconsistencies
- Native compatibility with Spark and modern analytics engines

Storage impact:

Approximately **85% size reduction**
(15.4 MB CSV → ~2.5 MB Parquet)


## Logging Strategy

Each pipeline stage writes execution logs as monthly text files under a dedicated Logs/ directory.

Logs provide:

- Operational traceability
- Debugging support
- Visibility into data quality checks and pipeline behavior

In a production environment, logs would be centralized in a cloud logging solution (e.g. Kibana) rather than stored locally or in Git.

# How to Run the Project

**Prerequisites**
- Python 3.x
- Apache Spark (local mode)
- PySpark installed
- VS Code or any IDE with notebook support

##**Execution Order**

**Run the notebooks in sequence:**

1. 01_sales_ingestion.ipynb
2. 02_sales_ETL.ipynb
3. 03_sales_aggregated.ipynb

Each step depends on the output of the previous layer.

## Future Improvements

- Implement an incremental refresh strategy to process only newly ingested or updated data
- Improve scalability, performance, and cost efficiency as data volume increases

---

## Setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
 
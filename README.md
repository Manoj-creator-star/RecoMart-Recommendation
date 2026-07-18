# 🛒 RecoMart - End-to-End Recommendation System Data Pipeline

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Prefect](https://img.shields.io/badge/Orchestration-Prefect-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange)
![Pandas](https://img.shields.io/badge/Data-Pandas-yellow)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## 📖 Project Summary

RecoMart is a modular data management pipeline that ingests clickstream, purchase history, and product catalog data to build a client-facing recommendation model. The repository includes:

- data ingestion from CSV sources and external REST API
- data validation and quality reporting
- preprocessing and feature engineering
- SQLite-based feature store registration
- training dataset preparation
- KNN recommendation model training and evaluation
- workflow orchestration using Python scripts and Prefect

---

## 🎯 Business Problem

RecoMart is an e-commerce startup aiming to boost customer engagement by recommending relevant products to shoppers based on their browsing and purchase behavior.

The platform processes several data sources to support recommendations:

- user clickstream events
- historical purchase transactions
- product metadata from an external API

The expected pipeline output is a validated training dataset, feature store artifacts, a trained recommendation model, and model evaluation metrics.

---

## 🚀 Objectives

- Automate ingestion of source and API product data
- Validate dataset quality before transformation
- Prepare a cleaned analytical dataset
- Engineer user, product, and interaction features
- Store features in a SQLite feature store
- Prepare a training dataset for recommendation modeling
- Train and serialize a collaborative recommendation model
- Evaluate model predictions and ranking performance
- Orchestrate end-to-end execution using scripted workflow

---

## 📁 Repository Structure

```text
RecoMart-Recommendation/
├── config/
│   └── config.py
├── data/
│   ├── model/
│   ├── processed/
│   ├── raw/
│   │   ├── clickstream/
│   │   ├── purchase/
│   │   └── products/
│   └── source/
├── docs/
├── feature_store/
├── ingestion/
├── models/
├── orchestration/
├── preprocessing/
├── transformation/
├── validation/
├── database/
├── logs/
├── requirements.txt
└── README.md
```

---

## 🧩 Data Sources

### 1. Clickstream Data

- Stored in `data/raw/clickstream/`
- Source file: `data/source/clickstream.csv`
- Events include `view`, `click`, `wishlist`, `add_to_cart`, and `purchase`
- Used to create interaction-level event scores

### 2. Purchase History

- Stored in `data/raw/purchase/`
- Source file: `data/source/purchase_history.csv`
- Includes `order_id`, `user_id`, `product_id`, `quantity`, `price`, and `purchase_time`
- Used to calculate purchase statistics and prepare features

### 3. Product Metadata

- Downloaded from `https://fakestoreapi.com/products`
- Stored in `data/raw/products/`
- Includes `product_id`, `title`, `category`, `price`, `rating_rate`, and `rating_count`

---

## 🔧 Core Pipeline Modules

### Ingestion

- `ingestion/run_ingestion.py` orchestrates ingestion of clickstream, purchase, and product data.
- `ingestion/ingest_clickstream.py` copies clickstream CSV from `data/source/` to `data/raw/clickstream/`.
- `ingestion/ingest_purchase.py` copies purchase CSV from `data/source/` to `data/raw/purchase/`.
- `ingestion/ingest_products.py` downloads product metadata from the external API to `data/raw/products/`.

### Validation

- `validation/validate_clickstream.py` validates event types, missing values, and duplicates.
- `validation/validate_purchase.py` checks missing values, duplicates, negative prices, and invalid quantities.
- `validation/validate_products.py` inspects product catalog completeness and price validity.
- `validation/utils.py` provides summary metrics for each dataset.

### Data Preparation

- `preprocessing/prepare_data.py` loads the latest raw clickstream, purchase, and product files.
- It merges purchase records with product metadata, then joins clickstream events on `user_id` and `product_id`.
- Cleaning steps include duplicate removal, missing value imputation, datetime conversion, text normalization, derived feature generation, and column pruning.
- Output saved to `data/processed/prepared_dataset.csv`.

### Feature Engineering

- `transformation/feature_engineering.py` generates the feature tables using:
  - `transformation/user_features.py`
  - `transformation/product_features.py`
  - `transformation/interaction_features.py`
- Feature tables are loaded into `database/feature_store.db` via `transformation/load_to_sqlite.py`.

### Feature Store

- `database/feature_store.db` contains:
  - `user_features`
  - `product_features`
  - `interaction_features`
- `feature_store/register_features.py` records feature metadata in `feature_metadata`.

### Training Data

- `models/prepare_training_data.py` builds `data/model/training_data.csv` from the `interaction_features` table.
- It maps interaction scores to a rating-style training dataset for collaborative modeling.

### Modeling

- `models/train_model.py` trains a KNN model using a user-item interaction matrix.
- The serialized model artifact is saved to `models/saved_models/knn_model.pkl`.
- `models/recommend.py` loads the saved model and returns JSON-formatted top-K recommendations for a user.
- `models/predict.py` provides a user-based recommendation helper for inference.

### Evaluation

- `models/evaluate.py` runs a holdout-style ranking evaluation with Precision@K, Recall@K, and NDCG metrics.
- `models/evaluate_metrics.py` computes proxy recommendation metrics and similarity statistics.

---

## 🔄 Workflow Orchestration

### Scripted Pipeline

- `orchestration/pipeline.py` executes the following sequence:
  1. Generate source data
  2. Ingestion
  3. Clickstream validation
  4. Purchase validation
  5. Product validation
  6. Data preparation
  7. Feature engineering
  8. Feature store registration
  9. Training data preparation
  10. Model training
  11. Model evaluation

### Prefect-compatible Pipeline

- `orchestration/prefect_pipeline.py` implements the same step sequence and adds evaluation metrics and recommendation generation.

---

## 🚀 Setup and Execution

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the full pipeline

```bash
python -m orchestration.pipeline
```

### Run the Prefect-based pipeline

```bash
python -m orchestration.prefect_pipeline
```

### Run individual stages

- Ingestion: `python -m ingestion.run_ingestion`
- Validation: `python -m validation.validate_clickstream` / `python -m validation.validate_purchase` / `python -m validation.validate_products`
- Preparation: `python -m preprocessing.prepare_data`
- Feature engineering: `python -m transformation.feature_engineering`
- Train model: `python -m models.train_model`
- Evaluate model: `python -m models.evaluate`
- Generate recommendations: `python -m models.recommend`

---

## 📊 Outputs and Artifacts

- `data/processed/prepared_dataset.csv` — cleaned analytical dataset
- `database/feature_store.db` — SQLite feature store
- `data/model/training_data.csv` — training dataset
- `models/saved_models/knn_model.pkl` — serialized user-item KNN model
- `logs/` — pipeline runtime logs and audit messages

---

## 📌 Notes

- `config/config.py` creates raw data folders and sets the external API endpoint.
- Feature metadata is registered in `database/feature_store.db` by `feature_store/register_features.py`.
- Interaction scores are derived from event types using a configurable mapping in `transformation/interaction_features.py`.

---

## 🔮 Future Scope

- Add real-time streaming ingestion with Kafka
- Implement Feast or a managed feature store
- Add Docker support for reproducible deployment
- Extend model selection to include matrix factorization and content-based algorithms
- Replace placeholder evaluation metrics with production ranking metrics
- Add test coverage and CI automation


---

# ▶️ Quick Start

## 1. Environment Setup

Create and activate a Python environment, then install dependencies:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Run the Pipeline

Run the full end-to-end workflow:

```bash
python -m orchestration.prefect_pipeline
```

Or run each stage step-by-step:

```bash
python -m ingestion.run_ingestion
python -m validation.validate_clickstream
python -m validation.validate_purchase
python -m validation.validate_products
python -m preprocessing.prepare_data
python -m transformation.feature_engineering
python -m feature_store.register_features
python -m models.prepare_training_data
python -m models.train_model
python -m models.evaluate
```

## 3. Expected Outputs

The pipeline generates:

- Raw data under the data/raw folders
- Prepared datasets in data/processed
- Feature tables in the SQLite database at database/feature_store.db
- Training data in data/model/training_data.csv
- A model artifact in models/saved_models/knn_model.pkl
- A validation summary in validation_reports/data_quality_report.csv

---

# 📝 Assignment Alignment

This repository already addresses the main deliverables required for the assignment:

- Problem formulation and business context are captured in this README and the project workflow.
- Ingestion scripts are implemented for clickstream, purchase, and product data.
- Validation logic is implemented for all data sources and a consolidated report is produced.
- Data preparation, feature engineering, and feature-store registration are implemented.
- A training dataset and recommendation model are produced.
- A Prefect-based orchestration pipeline is included for end-to-end execution.

For the submission PDF, the project can be presented using the structure below:

1. Project Title
2. Team Member Details
3. Problem Statement
4. Objectives
5. Methodology and Pipeline
6. Implementation Details
7. Results and Output Screenshots
8. Conclusion and Future Scope

A submission-ready summary document is available in docs/assignment_submission_guide.md.
- Kubernetes deployment
- Monitoring with Prometheus and Grafana
- Streamlit dashboard
- Real-time recommendation API

---

# 👥 Authors

This project was developed collaboratively as part of the **Data Management for Machine Learning** course.

Project Contributors:

- **Manoj Kumar N.**
- **Ayush Saxena**
- **Mageshwaran M.**
- **Pawar Heramb R.**
- **Srushti Sanjeev S.**

---

# ⭐ Acknowledgements

Developed as part of the **Data Management for Machine Learning (AIMLCZG529 / DSECLZG529)** course to demonstrate the implementation of an end-to-end data engineering pipeline for a recommendation system using modern data engineering and machine learning practices.
# 🛒 RecoMart - End-to-End Data Engineering Pipeline for a Recommendation System

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Prefect](https://img.shields.io/badge/Orchestration-Prefect-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange)
![Pandas](https://img.shields.io/badge/Data-Pandas-yellow)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## 📖 Overview

RecoMart is an end-to-end Data Engineering and Machine Learning pipeline that simulates how an e-commerce company processes customer activity to generate personalized product recommendations.

The project demonstrates the complete lifecycle of a modern data platform, including data generation, ingestion, validation, preprocessing, feature engineering, feature storage, model preparation, recommendation model training, evaluation, and workflow orchestration.

The pipeline follows industry-standard Data Engineering practices and is designed to be modular, scalable, and reproducible.

---

# 🎯 Business Problem

RecoMart is an e-commerce platform that wants to improve customer engagement by recommending relevant products based on customer browsing behavior and purchase history.

The platform receives data from multiple sources:

- Customer Purchase History
- Website Clickstream Events
- Product Metadata from an external REST API

The objective is to automatically ingest, validate, process, and transform this data into features that can be used to train a recommendation model.

---

# 🚀 Project Objectives

- Generate realistic e-commerce datasets
- Automate data ingestion
- Validate incoming datasets
- Produce dynamic data quality reports
- Prepare clean analytical datasets
- Engineer reusable machine learning features
- Store features in a centralized Feature Store
- Build reproducible training datasets
- Train recommendation models
- Evaluate model performance
- Orchestrate the complete pipeline using Prefect

---

# 🏗️ Solution Architecture

```text
                     Fake Store API
                            │
Purchase History CSV   Clickstream CSV
         │                    │
         └──────────┬─────────┘
                    │
                    ▼
             Data Ingestion
                    │
                    ▼
              Raw Data Layer
                    │
                    ▼
            Data Validation
                    │
                    ▼
        Data Quality Report
                    │
                    ▼
          Data Preparation
                    │
                    ▼
         Feature Engineering
                    │
                    ▼
         SQLite Feature Store
                    │
                    ▼
      Training Dataset Creation
                    │
                    ▼
      Recommendation Model
                    │
                    ▼
         Model Evaluation
```

---

# ⚙️ Technology Stack

| Category | Technology |
|-----------|------------|
| Programming Language | Python |
| Workflow Orchestration | Prefect |
| Data Processing | Pandas |
| API Integration | Requests |
| Feature Store | SQLite |
| Machine Learning | Scikit-learn |
| Model Serialization | Joblib |
| Data Versioning | DVC |
| Version Control | Git |
| Data Visualization | Matplotlib |

---

# 📂 Data Sources

## 1. Purchase History

Source: CSV

Contains:

- Order ID
- User ID
- Product ID
- Quantity
- Price
- Purchase Timestamp

---

## 2. Clickstream Data

Source: CSV

Contains:

- User ID
- Product ID
- Event Type
- Timestamp

Examples:

- View
- Click
- Wishlist
- Add to Cart

---

## 3. Product Metadata

Source:

https://fakestoreapi.com/products

Contains:

- Product Name
- Category
- Price
- Rating
- Rating Count
- Product Description

---

# 📁 Project Structure

```text
recomart-pipeline/

│
├── config/
├── data/
│   ├── source/
│   ├── raw/
│   ├── processed/
│   └── model/
│
├── ingestion/
├── validation/
├── preprocessing/
├── transformation/
├── feature_store/
├── models/
├── orchestration/
├── reports/
├── database/
├── sql/
├── logs/
│
├── requirements.txt
└── README.md
```

---

# 🔄 Pipeline Workflow

## Step 1 – Data Generation

Synthetic datasets are generated for:

- Purchase History
- Customer Clickstream

---

## Step 2 – Data Ingestion

The ingestion layer collects data from:

- Purchase CSV
- Clickstream CSV
- Fake Store REST API

The datasets are stored in the Raw Data Layer.

---

## Step 3 – Data Validation

Each dataset is validated independently.

Validation includes:

- Missing Values
- Duplicate Records
- Invalid Prices
- Invalid Quantities
- Invalid Event Types

A consolidated Data Quality Report is generated automatically.

---

## Step 4 – Data Preparation

The preprocessing layer:

- Loads validated datasets
- Merges purchase history with product metadata
- Merges clickstream data
- Cleans missing values
- Standardizes data types
- Creates derived attributes
- Produces a processed analytical dataset

---

## Step 5 – Feature Engineering

Three feature tables are created:

### User Features

Examples:

- Total Purchases
- Total Quantity
- Average Purchase Value
- Unique Products Purchased

---

### Product Features

Examples:

- Product Popularity
- Average Price
- Product Rating
- Rating Count

---

### Interaction Features

Examples:

- User ID
- Product ID
- Customer Event
- Interaction Score

---

## Step 6 – Feature Store

The engineered features are stored inside a SQLite Feature Store.

Feature tables:

- User Features
- Product Features
- Interaction Features

The Feature Store enables feature reuse without recomputing transformations.

---

## Step 7 – Training Dataset Preparation

Interaction features are converted into a training dataset consisting of:

- User ID
- Product ID
- Rating

---

## Step 8 – Recommendation Model

The recommendation model is trained using historical customer-product interactions.

The trained model is serialized and stored for future predictions.

---

## Step 9 – Model Evaluation

The trained model is evaluated to verify recommendation quality.

---

## Step 10 – Workflow Orchestration

The complete pipeline is orchestrated using Prefect.

Pipeline execution includes:

- Data Ingestion
- Validation
- Data Preparation
- Feature Engineering
- Feature Store Registration
- Training Dataset Preparation
- Model Training
- Model Evaluation

---

# 📊 Project Outputs

## Generated Datasets

- Raw Data
- Processed Dataset
- User Features
- Product Features
- Interaction Features
- Training Dataset

---

## Generated Database

SQLite Feature Store

Contains:

- user_features
- product_features
- interaction_features

---

## Generated Reports

- Data Quality Report
- Validation Summary
- Model Evaluation Report

---

## Generated Models

Serialized Recommendation Model

---

# ✨ Key Features

- Modular pipeline architecture
- Automated data ingestion
- REST API integration
- Dynamic data validation
- Automated validation reporting
- Data preprocessing
- Feature engineering
- SQLite Feature Store
- Data versioning using DVC
- Prefect workflow orchestration
- End-to-end reproducible pipeline

---

# 🔮 Future Enhancements

- Apache Kafka for real-time ingestion
- Snowflake Data Warehouse integration
- AWS S3 Data Lake
- Feast Feature Store
- GitHub Actions CI/CD
- Docker containerization

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
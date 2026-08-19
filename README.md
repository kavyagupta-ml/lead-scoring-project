# LeadIntel Pro: AI-Powered Lead Scoring Dashboard

An AI-powered lead scoring dashboard that uses a Random Forest machine learning model to evaluate customer engagement data and predict lead conversion probability.

## 🚀 Live Demo

👉 [Open LeadIntel Pro](https://lead-scoring-project-ejnuczyhngmq839y4bwwub.streamlit.app/)

Automatically scores leads on a 0-100 scale based on engagement metrics and helps prioritize leads according to their predicted conversion potential.

---

## 📌 Project Overview

LeadIntel Pro is a machine learning-based lead scoring application designed to help identify and prioritize potential customers based on their engagement behaviour.

The application analyzes customer engagement data and generates a lead score on a 0-100 scale along with a corresponding priority category.

The project demonstrates the application of Machine Learning and Python in a practical lead prioritization use case.

---

## ✨ Features

- **Batch Scoring** – Upload a CSV file containing multiple leads and score them at once
- **Single Lead Scoring** – Enter individual prospect information and receive an instant prediction
- **Analytics Dashboard** – View lead score distribution and feature importance
- **Multi-Client Support** – Apply different scoring thresholds for different clients
- **Priority Classification** – Classify leads into priority categories
- **Interactive Dashboard** – Use the Streamlit interface to interact with the model

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Scikit-learn
- Random Forest Classifier
- Pandas
- NumPy
- Git & GitHub

---

## ⚙️ How It Works

1. Customer engagement information is provided as input.
2. The application processes the required features.
3. The trained Random Forest model analyzes the lead.
4. A lead score is generated on a 0-100 scale.
5. The lead is assigned a priority category.
6. The results are displayed through the Streamlit dashboard.

---

## 🤖 Machine Learning Model

### Algorithm

**Random Forest Classifier**

### Model Details

- Algorithm: Random Forest
- Framework: Scikit-learn
- Input: Customer engagement features
- Output: Lead score and prediction
- Trained model: `lead_scorer.pkl`
- Feature configuration: `model_columns.json`

---

## 📊 Model Performance

| Metric | Score |
|--------|-------|
| Accuracy | 91.9% |
| Precision | 89.3% |
| Recall | 88.7% |
| F1-Score | 89.0% |

The model was trained using customer engagement data and multiple engagement-related features.

---

## 📸 Application Preview

A screenshot of the deployed application can be added here.

---

## 📁 Project Structure

```text
lead-scoring-project/
│
├── data/
│
├── leadintel_pro.py
├── lead_scorer.pkl
├── model_columns.json
├── config.toml
├── requirements.txt
├── README.md
└── .gitignore
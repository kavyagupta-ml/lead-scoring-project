# LeadIntel Pro: AI-Powered Lead Scoring Dashboard

Automatically scores leads on a 0-100 scale, predicting conversion probability based on engagement metrics.

## Features

- **Batch Scoring**: Upload CSV with 100+ leads, score all instantly
- **Single Lead Scoring**: Manually enter prospect info, get instant prediction
- **Analytics Dashboard**: View score distribution and feature importance
- **Multi-Client Support**: Different thresholds for different clients
- **Priority Classification**: URGENT, HOT, WARM, ENGAGING, MODERATE, NURTURE, COLD, MONITOR

## Model Performance

| Metric | Score |
|--------|-------|
| Accuracy | 91.9% |
| Precision | 89.3% |
| Recall | 88.7% |
| F1-Score | 89.0% |

Trained on 9,240 lead records with 45 engagement features.

## Installation

### Requirements
- Python 3.8+
- pip

### Setup

1. Clone repository:
```bash
git clone https://github.com/YOUR-USERNAME/lead-scoring-project.git
cd lead-scoring-project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run locally:
```bash
streamlit run leadintel_pro.py
```

4. Open browser to: `http://localhost:8501`

## How to Use

### Batch Scoring
1. Click "Batch Scoring" tab
2. Upload CSV file with lead data
3. Click "Score All Leads"
4. View results and download

### Single Lead
1. Click "Single Lead" tab
2. Enter: website visits, time on site, page views, company name
3. Click "Score This Lead"
4. See instant prediction and recommendation

### Analytics
1. View lead score distribution
2. Check top converting factors
3. Compare client performance

## Files

- `leadintel_pro.py` - Main Streamlit application
- `lead_scorer.pkl` - Trained RandomForest model
- `requirements.txt` - Python dependencies
- `sample_leads.csv` - Sample data for testing
- `model_columns.json` - Model column configuration

## Model Details

- **Algorithm**: RandomForest Classifier
- **Trees**: 100
- **Training Records**: 9,240
- **Features**: 45 engagement signals
- **Framework**: Scikit-learn

### Top 5 Features by Importance

1. Website Visits (25%)
2. Time on Site (22%)
3. Email Engagement (20%)
4. Page Views (18%)
5. Lead Source (15%)

## Author

Kavya Gupta (2024)

## License

MIT License - Open source project
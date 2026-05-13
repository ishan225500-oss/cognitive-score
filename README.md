```markdown
# Cognitive Score Assessment Tool

A machine learning-based application that predicts cognitive performance scores using sleep and health metrics.

## Overview

This tool analyzes sleep patterns and health indicators to generate a cognitive score, helping users understand the relationship between their lifestyle habits and cognitive function. The system includes a trained ML model and a user-friendly web interface.

## Features

- **Cognitive Score Prediction**: Generate a score based on sleep quality, duration, and health metrics
- **Data Collection**: Track sleep patterns and health indicators over time
- **User Management**: Individual user accounts to track personal progress
- **Visual Analytics**: View trends and correlations between sleep habits and cognitive performance

## Project Structure

```
cognitive-score/
├── app.py              # Main web application (Flask/Dash/Streamlit)
├── train.py            # ML model training script
├── sleep_health.csv    # Dataset with sleep and health metrics
├── users.db            # SQLite database for user data storage
└── README.md           # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/ishan225500-oss/cognitive-score.git
cd cognitive-score
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

*Note: If `requirements.txt` doesn't exist, common dependencies likely include:*
```bash
pip install pandas numpy scikit-learn flask sqlite3 matplotlib seaborn
```

## Usage

### Train the Model

Run the training script to build the cognitive score prediction model:

```bash
python train.py
```

This will:
- Load data from `sleep_health.csv`
- Preprocess the features
- Train a regression/classification model
- Save the trained model for use in the web app

### Run the Web Application

Start the main application:

```bash
python app.py
```

Then open your browser to `http://localhost:5000` (or the port specified in the console)

### Using the Application

1. **Create an account** or log in (users stored in `users.db`)
2. **Input your data**:
   - Sleep duration (hours)
   - Sleep quality (1-10 scale)
   - Physical activity level
   - Stress level
   - Other health metrics
3. **Get your cognitive score** (typically 0-100 or similar scale)
4. **Track changes** over time with historical data

## Dataset Format

The `sleep_health.csv` file likely contains columns such as:

| Column | Description |
|--------|-------------|
| `sleep_duration` | Hours of sleep per night |
| `sleep_quality` | Self-rated quality (1-10) |
| `physical_activity` | Minutes of exercise per day |
| `stress_level` | Perceived stress (1-10) |
| `cognitive_score` | Target variable (the score to predict) |
| `age` | User's age |
| `gender` | User's gender |

*Note: Run `python -c "import pandas as pd; print(pd.read_csv('sleep_health.csv').columns.tolist())"` to see actual columns*

## Cognitive Score Interpretation

| Score Range | Interpretation |
|-------------|----------------|
| 90-100 | Excellent cognitive function |
| 75-89 | Good cognitive function |
| 60-74 | Average cognitive function |
| 40-59 | Below average - consider lifestyle changes |
| Below 40 | Concerning - consult healthcare professional |

## Customization

### Retraining with Your Own Data

1. Prepare a CSV file with the same column structure
2. Replace `sleep_health.csv` with your file
3. Run `python train.py` to retrain the model

### Modifying the Web Interface

Edit `app.py` to change:
- UI layout and styling
- Input fields and validation rules
- Score calculation weights
- Data visualization options

## Technical Details

- **Database**: SQLite for user management
- **ML Library**: scikit-learn (Random Forest/Linear Regression)
- **Frontend**:  Streamlit

## Limitations

- The model's accuracy depends on the quality and quantity of training data
- Self-reported metrics may introduce bias
- Not intended for medical diagnosis
- Requires regular retraining for optimal performance

## Future Improvements

- [ ] Add API endpoint for programmatic access
- [ ] Implement detailed sleep stage analysis
- [ ] Add integration with wearable devices
- [ ] Include cognitive training recommendations
- [ ] Add export functionality for personal records

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with clear description of changes

## License

*No license specified - contact the author for usage terms*

## Contact

**Author**: ishan vashestha (ishan225500-oss)

For questions or support, please open an issue on GitHub.

## Acknowledgments

- Dataset sources -https://www.kaggle.com/datasets/mohankrishnathalla/sleep-health-and-daily-performance-dataset

---

**Disclaimer**: This tool is for educational and research purposes only. It should not replace professional medical advice, diagnosis, or treatment.
```

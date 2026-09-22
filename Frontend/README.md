# Brain Stroke Prediction Using Machine Learning

A web application that predicts a person's risk of having a brain stroke based on health and demographic data. The project combines a machine learning model (trained on the Kaggle stroke prediction dataset) with a Flask web app that lets users sign up, log in, and get predictions through a simple form.

## Features

- **User authentication** — sign up, log in, log out (session-based, backed by SQLite)
- **Stroke risk prediction** — enter gender, age, hypertension, heart disease, marital status, work type, residence type, average glucose level, BMI, and smoking status to get a prediction
- **Pre-trained model** — a Decision Tree classifier (`decision_tree_model.pkl`) trained on the stroke dataset
- **Model training notebook** — the full data exploration, preprocessing, and model training workflow in a Jupyter notebook

## Project Structure

```
Brain-Stroke-Prediction-Using-Machine-Learning/
├── Backend/
│   ├── stroke_prediction_ipynb.ipynb     # Data analysis & model training notebook
│   ├── healthcare-dataset-stroke-data.csv # Dataset
│   └── decision_tree_model.pkl           # Trained model
└── Frontend/
    ├── app.py                            # Flask application
    ├── decision_tree_model.pkl           # Trained model used by the app
    ├── requirements.txt                  # Python dependencies
    ├── users.db                          # SQLite database for user accounts
    └── templates/                        # HTML templates
        ├── home.html
        ├── signup.html
        ├── login.html
        ├── prediction.html
        ├── result.html
        └── about.html
```

## Tech Stack

- **Backend:** Python, Flask
- **Machine Learning:** scikit-learn (Decision Tree), pandas, numpy, imbalanced-learn (SMOTE), joblib
- **Data visualization:** matplotlib, seaborn
- **Database:** SQLite
- **Frontend:** HTML (Flask/Jinja templates)

## Dataset

The model is trained on the [Stroke Prediction Dataset](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset), which includes the following features:

- Gender, age, hypertension, heart disease, marital status
- Work type, residence type
- Average glucose level, BMI, smoking status
- Stroke occurrence (target variable)

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/VikramNolan/Brain-Stroke-Prediction-Using-Machine-Learning.git
   cd Brain-Stroke-Prediction-Using-Machine-Learning
   ```

2. (Recommended) Create and activate a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   cd Frontend
   pip install -r requirements.txt
   ```

   > **Note:** `requirements.txt` is a full environment dump and includes many packages beyond what this app strictly needs. At minimum you'll need `Flask`, `pandas`, `numpy`, `scikit-learn`, and `joblib`.

### Running the App

From the `Frontend` directory:

```bash
python app.py
```

The app will start in debug mode at `http://127.0.0.1:5000/`.

### Usage

1. Open the app in your browser and sign up for an account.
2. Log in with your credentials.
3. Go to the **Prediction** page and fill in the required health details.
4. Submit the form to view your predicted stroke risk on the **Result** page.

## Model Training

The `Backend/stroke_prediction_ipynb.ipynb` notebook walks through:

- Loading and exploring the dataset
- Encoding categorical variables
- Handling class imbalance with SMOTE
- Outlier removal
- Training and evaluating Decision Tree and Random Forest classifiers
- Exporting the final model with `joblib`

## Disclaimer

This project is intended for educational purposes only and is **not** a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for concerns about stroke risk.

## License

No license has been specified for this project.

import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import ExtraTreesRegressor, GradientBoostingRegressor, VotingRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score

# ---------------- LOAD DATA ----------------
df = pd.read_csv("sleep_health.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# ---------------- FEATURES ----------------
features = [
    'sleep_duration_hrs',
    'stress_score',
    'sleep_quality_score',
    'exercise_day',
    'screen_time_before_bed_mins',
    'work_hours_that_day',
    'heart_rate_resting_bpm',
    'caffeine_mg_before_bed'
]

X = df[features]
y = df['cognitive_performance_score']

# ---------------- SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------- MODELS ----------------
ridge = Ridge(alpha=0.5)

extra = ExtraTreesRegressor(
    n_estimators=400,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

gb = GradientBoostingRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=5,
    random_state=42
)

# ---------------- ENSEMBLE ----------------
ensemble = VotingRegressor([
    ('ridge', ridge),
    ('extra', extra),
    ('gb', gb)
])

# ---------------- PIPELINE ----------------
model = Pipeline([
    ('scaler', StandardScaler()),
    ('model', ensemble)
])

# ---------------- TRAIN ----------------
model.fit(X_train, y_train)

# ---------------- EVALUATE ----------------
y_pred = model.predict(X_test)

print("MAE:", mean_absolute_error(y_test, y_pred))
print("R2 Score:", r2_score(y_test, y_pred))

# ---------------- SAVE ----------------
pickle.dump(model, open("model.pkl", "wb"))

print("Model saved successfully!")

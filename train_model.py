import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib

# 1. Load Data
print("Loading data...")
df = pd.read_csv('traveler_data.csv')

# 2. Preprocess Data
print("Preprocessing data...")
# Encode categorical variables
le_loyalty = LabelEncoder()
df['loyalty_code'] = le_loyalty.fit_transform(df['loyalty_tier'])

le_purpose = LabelEncoder()
df['purpose_code'] = le_purpose.fit_transform(df['travel_purpose'])

# Features for Segmentation (Unsupervised)
X_seg = df[['age', 'avg_spend', 'last_stay_days_ago', 'loyalty_code', 'purpose_code']]
scaler = StandardScaler()
X_seg_scaled = scaler.fit_transform(X_seg)

# 3. Train Segmentation Model (K-Means)
print("Training Segmentation Model (K-Means)...")
kmeans = KMeans(n_clusters=3, random_state=42)
df['segment'] = kmeans.fit_predict(X_seg_scaled)

# Map clusters to meaningful names (Basic heuristic for demo)
# We analyze centroids or just map arbitrarily for MVP speed:
# 0 -> 'Budget/Infrequent', 1 -> 'High Value/Frequent', 2 -> 'Mid-Tier'
# Real implementation would analyze centroids.
segment_map = {0: 'Budget Explorer', 1: 'Luxury Elite', 2: 'Business Regular'}
# Note: In a real run, we'd check means max/min to assign labels correctly.
# For stability in this demo, we'll just use the cluster ID in the app or do a quick check:
cluster_means = df.groupby('segment')['avg_spend'].mean()
sorted_clusters = cluster_means.sort_values().index
segment_labels = {}
segment_labels[sorted_clusters[0]] = 'Budget Explorer'
segment_labels[sorted_clusters[1]] = 'Standard Business'
segment_labels[sorted_clusters[2]] = 'Luxury Elite'

df['segment_label'] = df['segment'].map(segment_labels)
print("Segments identified:", df['segment_label'].unique())

# 4. Train Prediction Model (Random Forest)
# Predict 'outcome_label' (Booking Conversion) based on profile
X_pred = df[['age', 'avg_spend', 'last_stay_days_ago', 'loyalty_code', 'purpose_code', 'segment']]
y_pred = df['outcome_label']

print("Training Prediction Model (Random Forest)...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_pred, y_pred)

# 5. Save Artifacts
print("Saving models...")
model_data = {
    'kmeans': kmeans,
    'scaler': scaler,
    'rf_model': rf_model,
    'le_loyalty': le_loyalty,
    'le_purpose': le_purpose,
    'segment_labels': segment_labels
}

joblib.dump(model_data, 'models.pkl')
print("Done! Models saved to models.pkl")

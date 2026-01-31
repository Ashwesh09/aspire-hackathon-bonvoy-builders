import joblib
import pandas as pd
import numpy as np

def load_models():
    """Load the trained models and encoders."""
    try:
        model_data = joblib.load('models.pkl')
        return model_data
    except FileNotFoundError:
        return None

def predict_traveler_segment(model_data, profile):
    """
    Predict the segment for a given traveler profile.
    profile: dict with keys ['age', 'avg_spend', 'last_stay_days_ago', 'loyalty_tier', 'travel_purpose']
    """
    # 1. Prepare input
    # Needs to match training columns: ['age', 'avg_spend', 'last_stay_days_ago', 'loyalty_code', 'purpose_code']
    
    # Handle unknown labels gracefully (fallback to 0)
    try:
        loyalty_code = model_data['le_loyalty'].transform([profile['loyalty_tier']])[0]
    except:
        loyalty_code = 0
        
    try:
        purpose_code = model_data['le_purpose'].transform([profile['travel_purpose']])[0]
    except:
        purpose_code = 0
        
    features = np.array([[
        profile['age'], 
        profile['avg_spend'], 
        profile['last_stay_days_ago'],
        loyalty_code, 
        purpose_code
    ]])
    
    # Scale numerical features? 
    # Wait, in training we scaled X_seg which had these 5 columns.
    # We need to use the SAME scaler.
    features_scaled = model_data['scaler'].transform(features)
    
    segment_id = model_data['kmeans'].predict(features_scaled)[0]
    segment_label = model_data['segment_labels'][segment_id]
    
    return segment_label, segment_id

def predict_booking_prob(model_data, profile, segment_id):
    """Predict probability of booking."""
    # Training X_pred columns: ['age', 'avg_spend', 'last_stay_days_ago', 'loyalty_code', 'purpose_code', 'segment']
    
    try:
        loyalty_code = model_data['le_loyalty'].transform([profile['loyalty_tier']])[0]
    except:
        loyalty_code = 0
    try:
        purpose_code = model_data['le_purpose'].transform([profile['travel_purpose']])[0]
    except:
        purpose_code = 0
        
    features = np.array([[
        profile['age'], 
        profile['avg_spend'], 
        profile['last_stay_days_ago'],
        loyalty_code, 
        purpose_code,
        segment_id
    ]])
    
    prob = model_data['rf_model'].predict_proba(features)[0][1] # Probability of class 1 (Booking)
    return prob

def generate_personalized_copy(segment, purpose):
    """
    Simulate GenAI creating personalized marketing copy.
    """
    # In a real app, this would call OpenAI/Gemini API.
    # Here uses templates based on segment logic.
    
    if "Luxury" in segment:
        tone = "exclusive, refined, and attentive"
        offer = "Private Villa Upgrade + Butler Service"
    elif "Budget" in segment:
        tone = "adventurous, value-focused, and energetic"
        offer = "Standard Room + City Tour Pass"
    else: # Business
        tone = "efficient, professional, and comforting"
        offer = "Executive Suite + Lounge Access"
        
    if purpose == "Business":
        copy = f"Experience seamless productivity. {offer}. Enjoy high-speed Wi-Fi and 24/7 lounge access to keep you connected."
    else:
        copy = f"Unwind in style. {offer}. Discover local hidden gems and relax with our premium amenities designed just for you."
        
    return copy, offer

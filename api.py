from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import utils
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from event_service import EventService, PricingAdjustment
from cdp_service import CDPService
from email_service import EmailService
from datetime import datetime, timedelta
from typing import Optional

app = FastAPI(title="Harriot Inc. Experience Engine API")

# Enable CORS for Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the Angular app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Models and Services on Startup
model_data = utils.load_models()
event_service = EventService()
cdp_service = CDPService()
email_service = EmailService()

class TravelerProfile(BaseModel):
    age: int
    loyalty_tier: str
    avg_spend: float
    last_stay_days_ago: int
    travel_purpose: str
    preferred_amenities: str

class PredictionResponse(BaseModel):
    segment_label: str
    segment_id: int
    booking_probability: float
    estimated_ltv: float

class OfferRequest(BaseModel):
    segment_label: str
    travel_purpose: str

class OfferResponse(BaseModel):
    offer_name: str
    copy: str

class EventPricingRequest(BaseModel):
    city: str
    check_in_date: str  # ISO format: YYYY-MM-DD
    check_out_date: str  # ISO format: YYYY-MM-DD
    base_room_rate: float

class EventPricingResponse(BaseModel):
    original_rate: float
    adjusted_rate: float
    multiplier: float
    reason: str
    events_count: int
    confidence_score: float
    peak_event_date: Optional[str]

@app.get("/")
def read_root():
    return {"status": "active", "system": "Harriot Inc. Intelligence Engine"}

@app.post("/predict", response_model=PredictionResponse)
def predict(profile: TravelerProfile):
    if not model_data:
        raise HTTPException(status_code=500, detail="Models not loaded")
    
    # Convert Pydantic model to dict for utils
    profile_dict = profile.model_dump()
    
    segment_label, segment_id = utils.predict_traveler_segment(model_data, profile_dict)
    prob = utils.predict_booking_prob(model_data, profile_dict, segment_id)
    
    # Simple LTV calc
    ltv = profile.avg_spend * 12 * (1.5 if 'Luxury' in segment_label else 1.0)
    
    return {
        "segment_label": segment_label,
        "segment_id": int(segment_id),
        "booking_probability": prob,
        "estimated_ltv": ltv
    }

@app.post("/generate-offer", response_model=OfferResponse)
def generate_offer(req: OfferRequest):
    copy, offer_name = utils.generate_personalized_copy(req.segment_label, req.travel_purpose)
    return {
        "offer_name": offer_name,
        "copy": copy
    }

@app.post("/event-pricing", response_model=EventPricingResponse)
def calculate_event_pricing(req: EventPricingRequest):
    """Calculate dynamic pricing based on local events and concerts."""
    try:
        # Parse dates
        check_in = datetime.fromisoformat(req.check_in_date)
        check_out = datetime.fromisoformat(req.check_out_date)
        
        # Validate date range
        if check_out <= check_in:
            raise HTTPException(status_code=400, detail="Check-out date must be after check-in date")
        
        if (check_out - check_in).days > 30:
            raise HTTPException(status_code=400, detail="Date range cannot exceed 30 days")
        
        # Get pricing adjustment from event service
        pricing_adjustment = event_service.calculate_pricing_adjustment(
            city=req.city,
            check_in_date=check_in,
            check_out_date=check_out
        )
        
        # Calculate adjusted rate
        adjusted_rate = req.base_room_rate * pricing_adjustment.base_multiplier
        
        return EventPricingResponse(
            original_rate=req.base_room_rate,
            adjusted_rate=round(adjusted_rate, 2),
            multiplier=round(pricing_adjustment.base_multiplier, 3),
            reason=pricing_adjustment.reason,
            events_count=pricing_adjustment.events_count,
            confidence_score=round(pricing_adjustment.confidence_score, 2),
            peak_event_date=pricing_adjustment.peak_event_date.isoformat() if pricing_adjustment.peak_event_date else None
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating event pricing: {e}")

@app.get("/events/{city}")
def get_city_events(city: str, date: Optional[str] = None):
    """Get events for a specific city and date (optional)."""
    try:
        if date:
            target_date = datetime.fromisoformat(date)
        else:
            target_date = datetime.now()
        
        # Get events for the next 7 days
        end_date = target_date + timedelta(days=7)
        events = event_service.get_events_for_date_range(city, target_date, end_date)
        
        # Convert to serializable format
        events_data = []
        for event in events:
            events_data.append({
                "id": event.id,
                "name": event.name,
                "date": event.date.isoformat(),
                "venue": event.venue,
                "category": event.category,
                "expected_attendance": event.expected_attendance,
                "impact_level": event.impact_level.value,
                "distance_km": event.distance_km
            })
        
        return {
            "city": city,
            "date_range": {
                "start": target_date.isoformat(),
                "end": end_date.isoformat()
            },
            "events": events_data,
            "total_events": len(events_data)
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching events: {e}")

class CampaignRequest(BaseModel):
    subject: str
    body: str
    recipients: list

@app.get("/campaigns/audiences/q2-business-local")
def get_q2_business_local_audience():
    """Get business travelers within 200 miles with no Q2 booking."""
    try:
        audience = cdp_service.get_at_risk_business_travelers()
        stats = cdp_service.get_audience_stats()
        return {
            "audience": audience,
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/campaigns/send")
def send_campaign(req: CampaignRequest):
    """Send email campaign to recipients."""
    try:
        result = email_service.send_campaign(req.recipients, req.subject, req.body)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

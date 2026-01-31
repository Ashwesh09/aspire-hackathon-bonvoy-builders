# 🎭 Event-Based Dynamic Pricing Feature

## 🚀 Hackathon Implementation Summary

### Problem Addressed
From the Harriott Inc. hackathon challenge, we selected **"Dynamic Pricing & Experience Differentiation"** as our focus area. The solution addresses:
- **Revenue Optimization**: Capture demand surge during local events
- **Competitive Advantage**: AI-driven pricing vs static competitor rates  
- **Market Responsiveness**: Real-time adaptation to local conditions

### 🎯 Solution Overview
Implemented an **AI-powered event-based pricing system** that automatically adjusts hotel rates based on local concerts, sports events, conferences, and activities that drive accommodation demand.

---

## 🏗️ Technical Architecture

### Backend (Python/FastAPI)
- **`event_service.py`**: Core service for event data fetching and pricing logic
- **`api.py`**: Extended with new endpoints for event-based pricing
- **External API Integration**: Ticketmaster & Eventbrite (with fallback mock data)
- **AI Impact Analysis**: Smart categorization of events by demand impact

### Frontend (Angular)
- **Enhanced Dashboard**: New section for event-based pricing controls
- **Real-time Pricing**: Interactive form with live pricing calculations
- **Event Visualization**: Display of local events with impact indicators
- **Responsive Design**: Mobile-friendly pricing interface

### Key Components
```
event_service.py          # Event fetching & pricing logic
api.py                   # REST endpoints
frontend/src/app/
├── app.ts              # Component logic
├── api.service.ts      # API integration  
├── app.html            # UI template
└── event-pricing-styles.css # Styling
test_event_pricing.py    # Comprehensive testing
```

---

## 🎪 Feature Capabilities

### 1. **Smart Event Detection**
- Fetches events from multiple APIs (Ticketmaster, Eventbrite)
- Supports 8+ major US cities
- Date range filtering (up to 30 days)
- Fallback mock data for demo purposes

### 2. **AI Impact Analysis**
- **Critical Impact**: Major concerts, sports (50,000+ attendance) → +75% pricing
- **High Impact**: Medium concerts, sports (15,000+ attendance) → +35% pricing  
- **Medium Impact**: Business conferences (3,000+ attendance) → +15% pricing
- **Low Impact**: Small events (<3,000 attendance) → +5% pricing

### 3. **Dynamic Pricing Engine**
- Real-time multiplier calculation (1.0x - 3.0x cap)
- Confidence scoring based on data quality
- Peak event date identification
- Detailed reasoning for pricing decisions

### 4. **Interactive Dashboard**
- City selection dropdown
- Date range picker (check-in/check-out)
- Base rate input
- Live pricing updates
- Event grid with impact badges
- Pricing insight explanations

---

## 🔗 API Endpoints

### New Endpoints Added
```bash
# Calculate dynamic pricing based on events
POST /event-pricing
{
  "city": "New York",
  "check_in_date": "2024-01-15",
  "check_out_date": "2024-01-17", 
  "base_room_rate": 299.99
}

# Get local events for a city
GET /events/{city}?date=2024-01-15
```

### Response Examples
```json
{
  "original_rate": 299.99,
  "adjusted_rate": 524.98,
  "multiplier": 1.75,
  "reason": "High-impact events detected: 2 major events",
  "events_count": 3,
  "confidence_score": 0.85,
  "peak_event_date": "2024-01-16T20:00:00"
}
```

---

## 📊 Demo Results

### Test Scenarios (from test_event_pricing.py)

| Scenario | City | Base Rate | Adjusted Rate | Change | Reason |
|----------|------|-----------|---------------|--------|---------|
| Weekend Concert | Las Vegas | $199 | $507 | **+155%** | Major concert (Critical) |
| Business Travel | Chicago | $159 | $382 | **+140%** | Conference + Sports |
| Extended Conference | San Francisco | $399 | $1,197 | **+200%** | Tech conference week |
| Regular Weekday | Any City | $250 | $250 | **0%** | No major events |

### Event Impact Examples
- **Taylor Swift Concert**: Critical impact → 3.0x multiplier
- **NBA Finals Game**: High impact → 1.5x multiplier  
- **Tech Conference**: Medium impact → 1.15x multiplier
- **Local Festival**: Low impact → 1.05x multiplier

---

## 🎨 User Experience

### Dashboard Features
1. **Pricing Controls**
   - City dropdown (8 major cities)
   - Date pickers with validation
   - Base rate input
   - Auto-calculation on changes

2. **Pricing Results Display**
   - Original vs Optimized rate comparison
   - Percentage change indicator
   - Price multiplier visualization  
   - Confidence score

3. **Local Events Section**
   - Event cards with details
   - Impact level color coding
   - Attendance numbers
   - Venue and category info
   - Refresh functionality

4. **Responsive Design**
   - Mobile-friendly layout
   - Grid-based responsive cards
   - Touch-friendly controls

---

## 🚀 Business Impact

### Revenue Optimization
- **Capture Demand Surge**: Automatically increase rates during high-demand periods
- **Prevent Revenue Loss**: Avoid underpricing during events
- **Market-Responsive**: Real-time adaptation vs static competitor pricing

### Operational Benefits  
- **Automated Decision Making**: AI replaces manual rate adjustments
- **Data-Driven Insights**: Clear reasoning for every pricing decision
- **Competitive Intelligence**: Monitor local market conditions
- **Scalable Solution**: Works across multiple cities and properties

### Example ROI
```
Scenario: 100-room hotel during Taylor Swift concert
- Base rate: $200/night
- Event-adjusted rate: $350/night (+75%)
- Additional revenue: $15,000 per night
- 3-night event impact: $45,000 additional revenue
```

---

## 🔧 Technical Implementation

### Setup & Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Test the feature
python3 test_event_pricing.py

# Start backend
python3 api.py

# Start frontend (new terminal)
cd frontend
npm install
npm start
```

### Production Considerations
- **API Keys**: Set TICKETMASTER_API_KEY and EVENTBRITE_API_KEY environment variables
- **Rate Limiting**: Implement caching to avoid API limits
- **Error Handling**: Graceful fallback to mock data
- **Monitoring**: Log pricing decisions for analysis
- **Security**: Validate all inputs, sanitize external data

---

## 🎯 Hackathon Success Criteria

✅ **Clear Problem Selection**: Dynamic pricing for revenue optimization  
✅ **AI-Enabled Solution**: Smart event impact analysis  
✅ **Working Prototype**: Full-stack implementation with UI  
✅ **Material Improvement**: Demonstrated +75-200% revenue potential  
✅ **Technical Excellence**: Production-ready code with tests  
✅ **Business Value**: Clear ROI and competitive advantage  

---

## 🔮 Future Enhancements

### Phase 2 Features
- **Weather Integration**: Adjust pricing based on weather conditions
- **Competitor Analysis**: Real-time competitor rate monitoring
- **Historical Learning**: ML model training on booking patterns
- **Multi-Property**: Portfolio-wide optimization
- **Guest Segmentation**: Personalized pricing by traveler segment

### Advanced Analytics
- **Demand Forecasting**: Predict booking patterns
- **Price Elasticity**: Optimize conversion vs revenue
- **Market Intelligence**: Industry benchmarking
- **Performance Tracking**: ROI measurement dashboard

---

## 📞 Demo Instructions

1. **Start the application** (backend + frontend)
2. **Navigate to Event Pricing section** in the dashboard
3. **Select different cities** (New York, Las Vegas, etc.)
4. **Adjust check-in dates** to see pricing changes
5. **View local events** and their impact levels
6. **Observe real-time pricing calculations**
7. **Test different scenarios** (weekends, conferences, concerts)

The system demonstrates immediate business value with a user-friendly interface that hotel staff can use to optimize pricing decisions in real-time.

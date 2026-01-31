# Harriot Inc. - Intelligent Experience Engine 🏨✨

> **Hackathon Submission: AI/ML Track**
> **Focus:** Hyper-Personalized Experience Differentiation & Dynamic Upsell

## 1. Executive Summary
This project proposes an **AI-first "Experience Engine"** that solves two critical problems for Harriot Inc.:
1.  **Low Conversion**: Generic offers fail to capture indifferent travelers.
2.  **Operational Blind Spots**: Staff lack granular insights into traveler intent.

Our MVP uses **Unsupervised Learning (K-Means)** to discover hidden micro-segments and **Predictive Modeling (Random Forest)** to forecast booking probability. It acts as a "Copilot" for marketing and front-desk teams, suggesting the *perfect* offer with GenAI-crafted messaging to maximize emotional connection and revenue.

## 2. Business Problem & Solution
| Challenge | Our Solution |
| :--- | :--- |
| **Silent Churn** | Identify "at-risk" clusters (e.g., "Budget Explorers") and engage them early. |
| **Missed Revenue** | Dynamic upsells (e.g., bundling Spa with Business stays) based on predicted intent, not just status. |
| **Generic Service** | Personalized copy generation makes every guest feel like a VIP. |

## 3. Solution Architecture
Modern Dual-Stack Architecture:
1.  **Backend (Python/FastAPI)**:
    -   Serves ML Models (K-Means + Random Forest).
    -   Exposes REST endpoints for prediction and generation.
2.  **Frontend (Angular)**:
    -   Responsive Dashboard for Staff.
    -   Real-time "Traveler Simulator".
    -   Premium "Wow" UI with direct API integration.

## 4. How to Run
### Prerequisites
-   Python 3.8+
-   Node.js & npm

### Step 1: Backend Setup
1.  **Install Python Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Train Models** (required first time)
    ```bash
    python3 train_model.py
    ```
3.  **Test Event Pricing Feature** (optional)
    ```bash
    python3 test_event_pricing.py
    ```
4.  **Start API Server**
    ```bash
    python3 api.py
    ```
    *API will run at http://localhost:8000*
    
    **New API Endpoints:**
    - `POST /event-pricing` - Calculate dynamic pricing
    - `GET /events/{city}` - Get local events

### Step 2: Frontend Setup
1.  **Navigate to frontend**
    ```bash
    cd frontend
    ```
2.  **Install Dependencies**
    ```bash
    npm install
    ```
3.  **Start Application**
    ```bash
    npm start
    ```
    *Open http://localhost:4200 in your browser.*

## 5. File Structure
-   `api.py`: FastAPI Backend with Event-Based Pricing.
-   `event_service.py`: **NEW** - Event data fetching and pricing logic.
-   `train_model.py`: ML Training Pipeline.
-   `test_event_pricing.py`: **NEW** - Test suite for event pricing feature.
-   `frontend/`: Angular Source Code.
    -   `src/app/app.ts`: Main Component Logic with Event Pricing.
    -   `src/app/api.service.ts`: API Integration with Event Endpoints.
    -   `src/app/event-pricing-styles.css`: **NEW** - Styles for event pricing UI.
-   `traveler_data.csv`: Synthetic Dataset.

## 6. **NEW FEATURE: Event-Based Dynamic Pricing** 🎭

### Overview
This hackathon project now includes an **AI-powered event-based pricing system** that automatically adjusts hotel rates based on local concerts, sports events, conferences, and other activities that drive demand.

### Key Features
- **Real-time Event Detection**: Integrates with Ticketmaster and Eventbrite APIs
- **Smart Impact Analysis**: AI categorizes events by impact level (Low, Medium, High, Critical)
- **Dynamic Pricing**: Automatically calculates optimal rate multipliers
- **Interactive Dashboard**: Visual interface to explore events and pricing
- **Multi-city Support**: Works across major US cities

### API Endpoints
- `POST /event-pricing`: Calculate dynamic pricing based on events
- `GET /events/{city}`: Get local events for a specific city

### How It Works
1. **Event Discovery**: Fetches events from multiple APIs for selected dates
2. **Impact Assessment**: AI analyzes event type, attendance, and proximity
3. **Price Optimization**: Calculates multiplier based on demand impact
4. **Real-time Updates**: Provides live pricing recommendations

### Example Results
- **Taylor Swift Concert**: +75% rate increase (Critical impact)
- **Tech Conference**: +15% rate increase (Medium impact)  
- **Local Sports Game**: +35% rate increase (High impact)
- **No Events**: Base rate maintained

### Business Value
- **Revenue Optimization**: Capture demand surge during events
- **Competitive Advantage**: Dynamic pricing vs fixed competitor rates
- **Data-Driven Decisions**: AI-powered insights replace manual adjustments

## 7. Target Audience & User Personas 👥
This tool is designed to empower three distinct roles within the hotel ecosystem:

### 1. Revenue Manager (Primary User - Strategic)
-   **Goal**: Maximize RevPAR (Revenue Per Available Room) and optimize yield.
-   **Usage**: Uses the **Event Pricing Dashboard** to monitor upcoming demand surges (e.g., Taylor Swift concert) and approve dynamic rate adjustments.
-   **Benefit**: Replaces manual spreadsheet analysis with AI-driven confidence scores.

### 2. Front Desk Agent (Secondary User - Operational)
-   **Goal**: Increase guest satisfaction and ancillary revenue during check-in.
-   **Usage**: Uses the **Traveler Simulator/Copilot** to instantly identify a guest's micro-segment (e.g., "Luxury Elite") and confidently pitch the *right* paid upgrade (e.g., "Private Villa").
-   **Benefit**: Removes the awkwardness of upselling by providing a data-backed script.

### 3. Marketing Manager (Tertiary User - Tactical)
-   **Goal**: Drive engagement through personalized campaigns.
-   **Usage**: Uses the **GenAI Copy Generator** to craft hyper-personalized email offers for pre-arrival sequences.
-   **Benefit**: Scales "concierge-level" communication to thousands of guests.

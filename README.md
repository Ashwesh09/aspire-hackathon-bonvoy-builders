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
3.  **Start API Server**
    ```bash
    python3 api.py
    ```
    *API will run at http://localhost:8000*

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
-   `api.py`: FastAPI Backend.
-   `train_model.py`: ML Training Pipeline.
-   `frontend/`: Angular Source Code.
    -   `src/app/app.ts`: Main Component Logic.
    -   `src/app/api.service.ts`: API Integration.
-   `traveler_data.csv`: Synthetic Dataset.

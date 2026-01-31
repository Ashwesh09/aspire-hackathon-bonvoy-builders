import pandas as pd

class CDPService:
    def __init__(self, data_path='traveler_data.csv'):
        self.data_path = data_path
        self.df = pd.read_csv(data_path)

    def get_at_risk_business_travelers(self):
        """
        Identify 'Business' travelers within 200 miles who haven't booked Q2.
        Criteria:
        1. travel_purpose == 'Business'
        2. distance_miles < 200
        3. has_q2_booking == 0
        """
        # Reload data to ensure freshness if modified
        self.df = pd.read_csv(self.data_path)
        
        filtered_df = self.df[
            (self.df['travel_purpose'] == 'Business') &
            (self.df['distance_miles'] < 200) &
            (self.df['has_q2_booking'] == 0)
        ]
        
        results = []
        for _, row in filtered_df.iterrows():
            results.append({
                "email": row['email'],
                "loyalty_tier": row['loyalty_tier'],
                "home_city": row['home_city'],
                "distance_miles": row['distance_miles'],
                "last_stay_days_ago": row['last_stay_days_ago'],
                "avg_spend": row['avg_spend']
            })
            
        return results

    def get_audience_stats(self):
        at_risk = self.get_at_risk_business_travelers()
        total_potential_revenue = sum([p['avg_spend'] for p in at_risk])
        return {
            "audience_count": len(at_risk),
            "potential_revenue": total_potential_revenue,
            "segments": ["Business", "Local"],
            "criteria": "Business Travelers < 200 miles without Q2 Booking"
        }

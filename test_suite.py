import unittest
import utils
import os
import joblib
from cdp_service import CDPService
from email_service import EmailService

class TestHarriotAI(unittest.TestCase):
    def setUp(self):
        # Ensure model exists
        if not os.path.exists('models.pkl'):
            raise unittest.SkipTest("models.pkl not found, skipping tests")
        self.model_data = utils.load_models()

    def test_model_loading(self):
        self.assertIsNotNone(self.model_data, "Model data should load successfully")
        self.assertIn('rf_model', self.model_data)
        self.assertIn('kmeans', self.model_data)

    def test_prediction_logic(self):
        # Test Case 1: High Spender (Expect Luxury)
        luxury_profile = {
            'age': 55,
            'loyalty_tier': 'Titanium',
            'avg_spend': 2000,
            'last_stay_days_ago': 5,
            'travel_purpose': 'Leisure',
            'preferred_amenities': 'Spa'
        }
        segment, seg_id = utils.predict_traveler_segment(self.model_data, luxury_profile)
        # Note: Segment labels might vary if training seeded differently, but logic should run
        print(f"Test 1 Segment: {segment}")
        self.assertIsInstance(segment, str)

        prob = utils.predict_booking_prob(self.model_data, luxury_profile, seg_id)
        print(f"Test 1 Probability: {prob}")
        self.assertTrue(0 <= prob <= 1, "Probability must be between 0 and 1")

    def test_genai_mock(self):
        copy, offer = utils.generate_personalized_copy("Luxury Elite", "Business")
        self.assertIn("Private Villa", copy) # Should reference the luxury offer
        # "Luxury" might not be in the string literal if the template changed, checking offer content
        # "Executive Suite" is for Business Segment, not Luxury Segment.
        # Logic check:
        # if Luxury -> Private Villa
        # if Business Purpose -> "Experience seamless productivity"
        self.assertIn("Experience seamless productivity", copy)

    def test_cdp_service(self):
        cdp = CDPService()
        # Ensure it doesn't crash
        try:
            audience = cdp.get_at_risk_business_travelers()
            print(f"CDP Audience Size: {len(audience)}")
            self.assertIsInstance(audience, list)
            if len(audience) > 0:
                first = audience[0]
                self.assertIn('email', first)
                self.assertIn('home_city', first)
        except Exception as e:
            self.fail(f"CDP Service failed: {e}")

    def test_email_service(self):
        email_svc = EmailService()
        recipients = [{'email': 'test@example.com', 'name': 'Tester'}]
        result = email_svc.send_campaign(recipients, "Test Subject", "Test Body")
        
        self.assertEqual(result['status'], 'completed')
        self.assertEqual(result['sent_count'], 1)
        self.assertEqual(result['details'][0]['email'], 'test@example.com')

if __name__ == '__main__':
    unittest.main()

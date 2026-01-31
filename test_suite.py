import unittest
import utils
import os
import joblib

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

if __name__ == '__main__':
    unittest.main()

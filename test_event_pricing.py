#!/usr/bin/env python3
"""Test script for the event-based pricing feature.

This script demonstrates the new event-based pricing functionality
by testing various scenarios and API endpoints.
"""

import requests
import json
from datetime import datetime, timedelta
from event_service import EventService

def test_event_service():
    """Test the EventService functionality."""
    print("🧪 Testing EventService...")
    
    service = EventService()
    
    # Test 1: Get events for a date range
    print("\n📅 Test 1: Getting events for New York")
    start_date = datetime.now()
    end_date = start_date + timedelta(days=3)
    
    events = service.get_events_for_date_range("New York", start_date, end_date)
    print(f"Found {len(events)} events:")
    for event in events:
        print(f"  - {event.name} ({event.category}) - {event.impact_level.value}")
    
    # Test 2: Calculate pricing adjustment
    print("\n💰 Test 2: Calculating pricing adjustment")
    pricing = service.calculate_pricing_adjustment("New York", start_date, end_date)
    print(f"Base multiplier: {pricing.base_multiplier}x")
    print(f"Reason: {pricing.reason}")
    print(f"Events count: {pricing.events_count}")
    print(f"Confidence: {pricing.confidence_score:.2%}")
    
    return True

def test_api_endpoints():
    """Test the API endpoints."""
    print("\n🌐 Testing API endpoints...")
    
    base_url = "http://localhost:8000"
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Health check: {response.status_code}")
        print(f"   Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("❌ API server not running. Start with: python api.py")
        return False
    
    # Test 2: Event pricing calculation
    print("\n💰 Test 2: Event pricing calculation")
    pricing_request = {
        "city": "New York",
        "check_in_date": datetime.now().strftime("%Y-%m-%d"),
        "check_out_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
        "base_room_rate": 299.99
    }
    
    try:
        response = requests.post(f"{base_url}/event-pricing", json=pricing_request)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Original rate: ${data['original_rate']}")
            print(f"Adjusted rate: ${data['adjusted_rate']}")
            print(f"Multiplier: {data['multiplier']}x")
            print(f"Reason: {data['reason']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Error testing event pricing: {e}")
    
    # Test 3: Get city events
    print("\n🎭 Test 3: Get city events")
    try:
        response = requests.get(f"{base_url}/events/New York")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {data['total_events']} events in {data['city']}")
            for event in data['events'][:3]:  # Show first 3 events
                print(f"  - {event['name']} ({event['category']}) - {event['impact_level']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Error getting city events: {e}")
    
    return True

def test_pricing_scenarios():
    """Test different pricing scenarios."""
    print("\n🎯 Testing pricing scenarios...")
    
    service = EventService()
    
    scenarios = [
        {
            "name": "Weekend with major concert",
            "city": "Las Vegas",
            "days": 2,
            "base_rate": 199
        },
        {
            "name": "Weekday business travel",
            "city": "Chicago", 
            "days": 1,
            "base_rate": 159
        },
        {
            "name": "Extended stay during conference",
            "city": "San Francisco",
            "days": 5,
            "base_rate": 399
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📊 Scenario: {scenario['name']}")
        start_date = datetime.now() + timedelta(days=1)
        end_date = start_date + timedelta(days=scenario['days'])
        
        pricing = service.calculate_pricing_adjustment(
            scenario['city'], start_date, end_date
        )
        
        original_rate = scenario['base_rate']
        adjusted_rate = original_rate * pricing.base_multiplier
        change_pct = ((adjusted_rate - original_rate) / original_rate) * 100
        
        print(f"  City: {scenario['city']}")
        print(f"  Original rate: ${original_rate}")
        print(f"  Adjusted rate: ${adjusted_rate:.2f}")
        print(f"  Change: {change_pct:+.1f}%")
        print(f"  Reason: {pricing.reason}")
        print(f"  Confidence: {pricing.confidence_score:.1%}")

def main():
    """Run all tests."""
    print("🚀 Starting Event-Based Pricing Tests")
    print("=" * 50)
    
    # Test the event service
    test_event_service()
    
    # Test pricing scenarios
    test_pricing_scenarios()
    
    # Test API endpoints (requires server to be running)
    test_api_endpoints()
    
    print("\n✅ All tests completed!")
    print("\n📋 Next steps:")
    print("1. Start the API server: python api.py")
    print("2. Start the frontend: cd frontend && npm start")
    print("3. Test the new event pricing feature in the browser")
    print("4. Try different cities and date ranges")

if __name__ == "__main__":
    main()

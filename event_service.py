"""Event Service for fetching local events and concerts data.

This module provides functionality to fetch local events data from external APIs
and calculate dynamic pricing adjustments based on event impact.
"""

import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import os
from functools import lru_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EventImpact(Enum):
    """Event impact levels for pricing adjustments."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class Event:
    """Data class representing a local event."""
    id: str
    name: str
    date: datetime
    venue: str
    category: str
    expected_attendance: int
    impact_level: EventImpact
    distance_km: float

@dataclass
class PricingAdjustment:
    """Data class for pricing adjustment recommendations."""
    base_multiplier: float
    reason: str
    events_count: int
    peak_event_date: Optional[datetime]
    confidence_score: float

class EventService:
    """Service for fetching and analyzing local events data."""
    
    def __init__(self):
        """Initialize the Event Service with API configuration."""
        # In production, use environment variables for API keys
        self.ticketmaster_api_key = os.getenv('TICKETMASTER_API_KEY', 'demo_key')
        self.eventbrite_api_key = os.getenv('EVENTBRITE_API_KEY', 'demo_key')
        self.base_url_ticketmaster = "https://app.ticketmaster.com/discovery/v2/events"
        self.base_url_eventbrite = "https://www.eventbriteapi.com/v3/events/search/"
        
        # Cache for API responses to avoid rate limiting
        self._cache_duration = 3600  # 1 hour
        
    @lru_cache(maxsize=100)
    def _get_cached_events(self, city: str, date_str: str) -> List[Dict]:
        """Get cached events data to avoid excessive API calls."""
        return self._fetch_events_from_apis(city, date_str)
    
    def _fetch_events_from_apis(self, city: str, date_str: str) -> List[Dict]:
        """Fetch events from multiple APIs with error handling."""
        events = []
        
        try:
            # Fetch from Ticketmaster (concerts, sports, theater)
            ticketmaster_events = self._fetch_ticketmaster_events(city, date_str)
            events.extend(ticketmaster_events)
        except Exception as e:
            logger.warning(f"Failed to fetch Ticketmaster events: {e}")
            
        try:
            # Fetch from Eventbrite (local events, conferences)
            eventbrite_events = self._fetch_eventbrite_events(city, date_str)
            events.extend(eventbrite_events)
        except Exception as e:
            logger.warning(f"Failed to fetch Eventbrite events: {e}")
            
        # If APIs fail, return mock data for demo purposes
        if not events:
            events = self._get_mock_events(city, date_str)
            
        return events
    
    def _fetch_ticketmaster_events(self, city: str, date_str: str) -> List[Dict]:
        """Fetch events from Ticketmaster API."""
        if self.ticketmaster_api_key == 'demo_key':
            return []  # Skip API call in demo mode
            
        params = {
            'apikey': self.ticketmaster_api_key,
            'city': city,
            'startDateTime': f"{date_str}T00:00:00Z",
            'endDateTime': f"{date_str}T23:59:59Z",
            'size': 50,
            'sort': 'date,asc'
        }
        
        response = requests.get(self.base_url_ticketmaster, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        events = []
        
        if '_embedded' in data and 'events' in data['_embedded']:
            for event in data['_embedded']['events']:
                events.append({
                    'id': event['id'],
                    'name': event['name'],
                    'date': event['dates']['start']['dateTime'],
                    'venue': event['_embedded']['venues'][0]['name'] if event.get('_embedded', {}).get('venues') else 'Unknown',
                    'category': event['classifications'][0]['segment']['name'] if event.get('classifications') else 'General',
                    'source': 'ticketmaster'
                })
                
        return events
    
    def _fetch_eventbrite_events(self, city: str, date_str: str) -> List[Dict]:
        """Fetch events from Eventbrite API."""
        if self.eventbrite_api_key == 'demo_key':
            return []  # Skip API call in demo mode
            
        headers = {
            'Authorization': f'Bearer {self.eventbrite_api_key}'
        }
        
        params = {
            'location.address': city,
            'start_date.range_start': f"{date_str}T00:00:00",
            'start_date.range_end': f"{date_str}T23:59:59",
            'expand': 'venue'
        }
        
        response = requests.get(self.base_url_eventbrite, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        events = []
        
        if 'events' in data:
            for event in data['events']:
                events.append({
                    'id': event['id'],
                    'name': event['name']['text'],
                    'date': event['start']['utc'],
                    'venue': event.get('venue', {}).get('name', 'Unknown'),
                    'category': event.get('category', {}).get('name', 'General'),
                    'source': 'eventbrite'
                })
                
        return events
    
    def _get_mock_events(self, city: str, date_str: str) -> List[Dict]:
        """Generate mock events data for demo purposes."""
        mock_events = [
            {
                'id': 'mock_1',
                'name': 'Taylor Swift - Eras Tour',
                'date': f"{date_str}T20:00:00Z",
                'venue': f'{city} Stadium',
                'category': 'Music',
                'source': 'mock',
                'expected_attendance': 50000
            },
            {
                'id': 'mock_2',
                'name': 'Tech Conference 2024',
                'date': f"{date_str}T09:00:00Z",
                'venue': f'{city} Convention Center',
                'category': 'Business',
                'source': 'mock',
                'expected_attendance': 5000
            },
            {
                'id': 'mock_3',
                'name': 'NBA Finals Game',
                'date': f"{date_str}T19:30:00Z",
                'venue': f'{city} Arena',
                'category': 'Sports',
                'source': 'mock',
                'expected_attendance': 20000
            }
        ]
        
        # Return subset based on date to simulate real variation
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        if date_obj.weekday() < 5:  # Weekday
            return [mock_events[1]]  # Business event
        else:  # Weekend
            return mock_events  # All events
    
    def _calculate_event_impact(self, event_data: Dict) -> EventImpact:
        """Calculate the impact level of an event on hotel demand."""
        category = event_data.get('category', '').lower()
        attendance = event_data.get('expected_attendance', 1000)
        
        # High-impact categories
        if category in ['music', 'sports'] and attendance > 30000:
            return EventImpact.CRITICAL
        elif category in ['music', 'sports'] and attendance > 15000:
            return EventImpact.HIGH
        elif category in ['business', 'conference'] and attendance > 3000:
            return EventImpact.MEDIUM
        else:
            return EventImpact.LOW
    
    def get_events_for_date_range(self, city: str, start_date: datetime, 
                                  end_date: datetime) -> List[Event]:
        """Get all events for a specific date range."""
        events = []
        current_date = start_date
        
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            daily_events = self._get_cached_events(city, date_str)
            
            for event_data in daily_events:
                try:
                    event_date = datetime.fromisoformat(
                        event_data['date'].replace('Z', '+00:00')
                    )
                    
                    impact = self._calculate_event_impact(event_data)
                    
                    event = Event(
                        id=event_data['id'],
                        name=event_data['name'],
                        date=event_date,
                        venue=event_data['venue'],
                        category=event_data['category'],
                        expected_attendance=event_data.get('expected_attendance', 1000),
                        impact_level=impact,
                        distance_km=2.5  # Assume events are nearby for demo
                    )
                    events.append(event)
                    
                except Exception as e:
                    logger.warning(f"Failed to process event {event_data.get('name', 'Unknown')}: {e}")
                    
            current_date += timedelta(days=1)
            
        return events
    
    def calculate_pricing_adjustment(self, city: str, check_in_date: datetime, 
                                   check_out_date: datetime) -> PricingAdjustment:
        """Calculate pricing adjustment based on local events."""
        try:
            events = self.get_events_for_date_range(city, check_in_date, check_out_date)
            
            if not events:
                return PricingAdjustment(
                    base_multiplier=1.0,
                    reason="No significant events found",
                    events_count=0,
                    peak_event_date=None,
                    confidence_score=0.8
                )
            
            # Calculate impact score
            total_impact = 0
            high_impact_events = 0
            peak_event = None
            max_impact = 0
            
            impact_weights = {
                EventImpact.LOW: 0.05,
                EventImpact.MEDIUM: 0.15,
                EventImpact.HIGH: 0.35,
                EventImpact.CRITICAL: 0.75
            }
            
            for event in events:
                weight = impact_weights[event.impact_level]
                total_impact += weight
                
                if event.impact_level in [EventImpact.HIGH, EventImpact.CRITICAL]:
                    high_impact_events += 1
                    
                if weight > max_impact:
                    max_impact = weight
                    peak_event = event
            
            # Calculate multiplier (cap at 3.0x for extreme cases)
            base_multiplier = min(1.0 + total_impact, 3.0)
            
            # Generate reason
            if high_impact_events > 0:
                reason = f"High-impact events detected: {high_impact_events} major events"
            elif len(events) > 3:
                reason = f"Multiple events period: {len(events)} events"
            else:
                reason = f"Moderate event activity: {len(events)} events"
            
            # Confidence based on data quality and event proximity
            confidence = min(0.9, 0.6 + (len(events) * 0.1))
            
            return PricingAdjustment(
                base_multiplier=base_multiplier,
                reason=reason,
                events_count=len(events),
                peak_event_date=peak_event.date if peak_event else None,
                confidence_score=confidence
            )
            
        except Exception as e:
            logger.error(f"Failed to calculate pricing adjustment: {e}")
            return PricingAdjustment(
                base_multiplier=1.0,
                reason="Error calculating event impact",
                events_count=0,
                peak_event_date=None,
                confidence_score=0.3
            )

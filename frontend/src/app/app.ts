import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService, TravelerProfile, PredictionResponse, OfferResponse, EventPricingRequest, EventPricingResponse, EventsResponse } from './api.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  // Input State
  profile: TravelerProfile = {
    age: 35,
    loyalty_tier: 'Silver',
    avg_spend: 450,
    last_stay_days_ago: 45,
    travel_purpose: 'Leisure',
    preferred_amenities: 'Spa'
  };

  tiers = ['Member', 'Silver', 'Gold', 'Platinum', 'Titanium', 'Ambassador'];
  purposes = ['Leisure', 'Business'];
  amenitiesList = ['Spa', 'Golf', 'Dining', 'Lounge', 'Gym'];

  // Output State
  prediction: PredictionResponse | null = null;
  offer: OfferResponse | null = null;
  loadingPrediction = false;
  loadingOffer = false;

  // Event Pricing State
  eventPricing: EventPricingResponse | null = null;
  cityEvents: EventsResponse | null = null;
  loadingEventPricing = false;
  loadingEvents = false;
  
  // Event Pricing Form
  eventPricingForm = {
    city: 'New York',
    check_in_date: new Date().toISOString().split('T')[0],
    check_out_date: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    base_room_rate: 299
  };
  
  cities = ['New York', 'Los Angeles', 'Chicago', 'Miami', 'Las Vegas', 'San Francisco', 'Boston', 'Seattle'];

  constructor(private api: ApiService) { }

  // Triggered when sidebar inputs change
  onProfileChange() {
    this.updatePrediction();
  }

  updatePrediction() {
    this.loadingPrediction = true;
    this.api.predict(this.profile).subscribe({
      next: (res) => {
        this.prediction = res;
        this.loadingPrediction = false;
        // Reset offer when profile changes significantly? Maybe not, let user choose.
        this.offer = null;
      },
      error: (err) => {
        console.error("Prediction failed", err);
        this.loadingPrediction = false;
      }
    });
  }

  generateOffer() {
    if (!this.prediction) return;

    this.loadingOffer = true;
    this.api.generateOffer(this.prediction.segment_label, this.profile.travel_purpose).subscribe({
      next: (res) => {
        this.offer = res;
        this.loadingOffer = false;
      },
      error: (err) => {
        console.error("Offer generation failed", err);
        this.loadingOffer = false;
      }
    });
  }

  // Helper for amenities checkbox (simplified as single string in model for now)
  toggleAmenity(amenity: string, event: any) {
    const current = this.profile.preferred_amenities.split(',').filter(a => a);
    if (event.target.checked) {
      current.push(amenity);
    } else {
      const index = current.indexOf(amenity);
      if (index > -1) {
        current.splice(index, 1);
      }
    }
    this.profile.preferred_amenities = current.join(',');
    this.onProfileChange();
  }

  isAmenitySelected(amenity: string): boolean {
    return this.profile.preferred_amenities.includes(amenity);
  }

  getLtvMultiplier(): number {
    return (this.prediction?.estimated_ltv || 0) > 5000 ? 1.5 : 1;
  }

  // Event Pricing Methods
  calculateEventPricing() {
    this.loadingEventPricing = true;
    this.api.calculateEventPricing(this.eventPricingForm).subscribe({
      next: (res) => {
        this.eventPricing = res;
        this.loadingEventPricing = false;
      },
      error: (err) => {
        console.error('Event pricing calculation failed', err);
        this.loadingEventPricing = false;
      }
    });
  }

  loadCityEvents() {
    this.loadingEvents = true;
    this.api.getCityEvents(this.eventPricingForm.city, this.eventPricingForm.check_in_date).subscribe({
      next: (res) => {
        this.cityEvents = res;
        this.loadingEvents = false;
      },
      error: (err) => {
        console.error('Failed to load city events', err);
        this.loadingEvents = false;
      }
    });
  }

  onEventPricingFormChange() {
    // Auto-calculate when form changes
    this.calculateEventPricing();
  }

  getPriceChangePercentage(): number {
    if (!this.eventPricing) return 0;
    return ((this.eventPricing.adjusted_rate - this.eventPricing.original_rate) / this.eventPricing.original_rate) * 100;
  }

  getImpactLevelColor(level: string): string {
    switch (level) {
      case 'critical': return '#ff4757';
      case 'high': return '#ff6b35';
      case 'medium': return '#ffa502';
      case 'low': return '#2ed573';
      default: return '#747d8c';
    }
  }
}

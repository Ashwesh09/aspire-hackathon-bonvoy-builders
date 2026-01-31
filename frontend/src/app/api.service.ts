import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface TravelerProfile {
    age: number;
    loyalty_tier: string;
    avg_spend: number;
    last_stay_days_ago: number;
    travel_purpose: string;
    preferred_amenities: string;
}

export interface PredictionResponse {
    segment_label: string;
    segment_id: number;
    booking_probability: number;
    estimated_ltv: number;
}

export interface OfferResponse {
    offer_name: string;
    copy: string;
}

export interface EventPricingRequest {
    city: string;
    check_in_date: string;
    check_out_date: string;
    base_room_rate: number;
}

export interface EventPricingResponse {
    original_rate: number;
    adjusted_rate: number;
    multiplier: number;
    reason: string;
    events_count: number;
    confidence_score: number;
    peak_event_date: string | null;
}

export interface Event {
    id: string;
    name: string;
    date: string;
    venue: string;
    category: string;
    expected_attendance: number;
    impact_level: string;
    distance_km: number;
}

export interface EventsResponse {
    city: string;
    date_range: {
        start: string;
        end: string;
    };
    events: Event[];
    total_events: number;
}

@Injectable({
    providedIn: 'root'
})
export class ApiService {
    private apiUrl = 'http://localhost:8000';

    constructor(private http: HttpClient) { }

    predict(profile: TravelerProfile): Observable<PredictionResponse> {
        return this.http.post<PredictionResponse>(`${this.apiUrl}/predict`, profile);
    }

    generateOffer(segment_label: string, travel_purpose: string): Observable<OfferResponse> {
        return this.http.post<OfferResponse>(`${this.apiUrl}/generate-offer`, {
            segment_label,
            travel_purpose
        });
    }

    calculateEventPricing(request: EventPricingRequest): Observable<EventPricingResponse> {
        return this.http.post<EventPricingResponse>(`${this.apiUrl}/event-pricing`, request);
    }

    getCityEvents(city: string, date?: string): Observable<EventsResponse> {
        const params = date ? { date } : {};
        return this.http.get<EventsResponse>(`${this.apiUrl}/events/${city}`, { params });
    }
}

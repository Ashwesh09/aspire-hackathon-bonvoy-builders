import requests
import json
import time

BASE_URL = "http://localhost:8000"

def log(msg, type="INFO"):
    print(f"[{type}] {msg}")

def test_campaign_flow():
    log("Starting Campaign Flow Verification...")

    # 1. Get Audience
    log("Fetching Audience for Q2 Business Local...")
    try:
        res = requests.get(f"{BASE_URL}/campaigns/audiences/q2-business-local")
        if res.status_code == 200:
            data = res.json()
            audience = data.get("audience", [])
            stats = data.get("stats", {})
            log(f"Audience fetched. Count: {len(audience)}")
            log(f"Stats: {json.dumps(stats, indent=2)}")
            
            if len(audience) == 0:
                log("WARNING: Audience is empty. Check cdp_service logic or csv data.", "WARN")
                return
        else:
            log(f"Failed to fetch audience. Status: {res.status_code}", "ERROR")
            return
    except Exception as e:
        log(f"Exception fetching audience: {e}", "ERROR")
        return

    # 2. Generate Offer Copy (Simulated)
    log("Generating Offer Copy...")
    try:
        offer_req = {
            "segment_label": "Business Elite",
            "travel_purpose": "Business"
        }
        res = requests.post(f"{BASE_URL}/generate-offer", json=offer_req)
        if res.status_code == 200:
            offer_data = res.json()
            log(f"Offer Generated: {offer_data['offer_name']}")
        else:
            log(f"Failed to generate offer. Status: {res.status_code}", "ERROR")
            return
    except Exception as e:
        log(f"Exception generating offer: {e}", "ERROR")
        return

    # 3. Send Campaign
    log("Sending Campaign...")
    try:
        send_req = {
            "subject": f"Exclusive Offer: {offer_data['offer_name']}",
            "body": offer_data['copy'],
            "recipients": audience
        }
        res = requests.post(f"{BASE_URL}/campaigns/send", json=send_req)
        if res.status_code == 200:
            result = res.json()
            log("Campaign Sent Successfully!")
            log(f"Result: {json.dumps(result, indent=2)}")
        else:
            log(f"Failed to send campaign. Status: {res.status_code}. Response: {res.text}", "ERROR")
            return
    except Exception as e:
        log(f"Exception sending campaign: {e}", "ERROR")
        return

    log("Campaign Flow Verification Complete", "SUCCESS")

if __name__ == "__main__":
    time.sleep(1) # wait for server stable
    test_campaign_flow()

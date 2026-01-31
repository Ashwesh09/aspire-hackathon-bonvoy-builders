import time

class EmailService:
    def __init__(self):
        pass

    def send_campaign(self, recipients, subject, body):
        """
        Simulate sending emails to a list of recipients.
        In a real app, this would use SMTP or an API like SendGrid.
        """
        results = []
        print(f"📧 STARTING CAMPAIGN: {subject}")
        print(f"👥 Recipients: {len(recipients)}")
        
        for recipient in recipients:
            # Simulate network delay
            # time.sleep(0.1) 
            print(f"   -> Sending to {recipient['email']}...")
            results.append({
                "email": recipient['email'],
                "status": "sent",
                "timestamp": time.time()
            })
            
        print("✅ CAMPAIGN COMPLETE")
        return {
            "sent_count": len(results),
            "status": "completed",
            "details": results
        }

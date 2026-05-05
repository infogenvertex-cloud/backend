"""
Test script to verify the API returns proper subscription data with NULL handling.
"""
from app.database import SessionLocal
from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionResponse

def test_subscription_serialization():
    """Test that subscriptions with NULL values serialize correctly."""
    db = SessionLocal()
    try:
        # Get all subscriptions
        subs = db.query(Subscription).all()
        
        print(f"📊 Found {len(subs)} subscriptions in database\n")
        
        for sub in subs:
            print(f"Subscription ID {sub.id}:")
            print(f"  - amount: {sub.amount} (type: {type(sub.amount).__name__})")
            print(f"  - payment_date: {sub.payment_date} (type: {type(sub.payment_date).__name__})")
            
            # Try to serialize with Pydantic
            try:
                response = SubscriptionResponse.model_validate(sub, from_attributes=True)
                print(f"  ✅ Serialization successful")
                print(f"  - Response amount: {response.amount}")
                print(f"  - Response payment_date: {response.payment_date}")
                
                # Convert to dict to see JSON representation
                data = response.model_dump()
                print(f"  - JSON amount: {data.get('amount')}")
                print(f"  - JSON payment_date: {data.get('payment_date')}")
            except Exception as e:
                print(f"  ❌ Serialization failed: {e}")
            
            print()
    
    finally:
        db.close()

if __name__ == "__main__":
    test_subscription_serialization()

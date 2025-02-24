import os
from dotenv import load_dotenv
import requests
import asyncio

# Load environment variables from .env file
load_dotenv()

async def test_forward_to_nate():
    webhook_url = os.getenv('NATE_WEBHOOK_URL')
    if not webhook_url or webhook_url == 'your_webhook_url_here':
        print("Error: Please set NATE_WEBHOOK_URL in your .env file")
        return

    test_message = "This is a test message from the Splaa assistant"
    
    try:
        response = requests.post(webhook_url, json={"content": test_message})
        response.raise_for_status()
        print("✓ Message sent successfully!")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Error sending message: {str(e)}")

def main():
    print("Testing Nate's webhook integration...")
    print(f"Using webhook URL: {os.getenv('NATE_WEBHOOK_URL')}")
    
    # Run the async test function
    asyncio.run(test_forward_to_nate())

if __name__ == "__main__":
    main()
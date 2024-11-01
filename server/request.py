import requests
import json

def test_api():
    url = "http://localhost:8000/api/generate-package"
    
    payload = {
        "budget": 50000,
        "essential_items": [
            "Sofa",
            "Queen Bed Frame",
            "Office Desk",
            "Dining Table",
            "Washing Machine",
            "Microwave Oven",
            "Television",
            "Armchair",
            "Nightstand",
            "Refrigerator"
        ],
        "preferences": {
            "style": "Modern",
            "material": ["Wood", "Metal", "Fabric"],
            "color_palette": ["Neutral", "Dark"],
            "quality": "Premium"
        }
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Pretty print the response
        print(json.dumps(response.json(), indent=2))
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")

if __name__ == "__main__":
    test_api()
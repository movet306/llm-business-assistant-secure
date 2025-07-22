import requests
import json

# 1. Fetch data from the API
try:
    print("📡 Requesting data from API...")
    response = requests.get("https://fakestoreapi.com/products")
    print("✅ Status Code:", response.status_code)
except Exception as e:
    print("❌ Error while requesting:", str(e))
    exit()

# 2. Parse the response
try:
    data = response.json()
    print("📦 First product title:", data[0]["title"])
except Exception as e:
    print("❌ Error parsing JSON:", str(e))
    exit()

# 3. Save JSON to file
try:
    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("✅ JSON file has been saved to 'products.json'")
except Exception as e:
    print("❌ Error saving file:", str(e))








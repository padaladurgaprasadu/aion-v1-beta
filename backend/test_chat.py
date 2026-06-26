import requests
import json

def test_chat():
    print("Testing /api/chat endpoint...")
    
    # Test 1: General Question
    print("\n--- Test 1: General Chat ---")
    res1 = requests.post("http://localhost:8000/api/chat", json={"message": "What is Kedarnath?"})
    if res1.status_code == 200:
        print("Response:", json.dumps(res1.json(), indent=2))
    else:
        print(f"Failed with status: {res1.status_code}")
        print(res1.text)
        
    # Test 2: Build Request
    print("\n--- Test 2: Build Intent ---")
    res2 = requests.post("http://localhost:8000/api/chat", json={"message": "Build a python data visualization dashboard for sales."})
    if res2.status_code == 200:
        print("Response:", json.dumps(res2.json(), indent=2))
    else:
        print(f"Failed with status: {res2.status_code}")
        print(res2.text)

if __name__ == "__main__":
    try:
        test_chat()
    except Exception as e:
        print(f"Connection failed. Is the backend running on port 8000? Error: {e}")

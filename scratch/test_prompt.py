import requests
import json
import sseclient

def test_chat():
    url = "http://localhost:5000/api/chat"
    payload = {
        "message": "Explain Quantum Computing",
        "history": [],
        "memory": ""
    }
    
    print(f"Sending POST to {url}...")
    try:
        response = requests.post(url, json=payload, stream=True)
        print(f"Status Code: {response.status_code}")
        
        client = sseclient.SSEClient(response)
        full_text = ""
        for event in client.events():
            try:
                data = json.loads(event.data)
                if 'token' in data:
                    print(data['token'], end='', flush=True)
                    full_text += data['token']
            except Exception as e:
                pass
                
        print("\n\n--- RAW OUTPUT REVEAL ---")
        print(repr(full_text))
        
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_chat()

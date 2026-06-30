import requests
import json

def test_chat():
    url = "http://localhost:5000/api/chat"
    payload = {
        "message": "Explain Quantum Computing",
        "history": [],
        "memory": ""
    }
    
    print(f"Sending POST to {url}...")
    response = requests.post(url, json=payload, stream=True)
    print(f"Status Code: {response.status_code}")
    
    full_text = ""
    for line in response.iter_lines():
        if line:
            line_str = line.decode('utf-8')
            if line_str.startswith("data: "):
                try:
                    data = json.loads(line_str[6:])
                    if 'token' in data:
                        print(data['token'], end='', flush=True)
                        full_text += data['token']
                except Exception as e:
                    pass
            
    print("\n\n--- RAW OUTPUT REVEAL ---")
    print(repr(full_text))

if __name__ == "__main__":
    test_chat()

import urllib.request
import json

url = "http://127.0.0.1:8080/api/browse_folder"
try:
    print("Sending request to", url)
    # We can set a timeout of 10 seconds.
    response = urllib.request.urlopen(url, timeout=10)
    data = json.loads(response.read().decode('utf-8'))
    print("Response:")
    print(json.dumps(data, indent=2))
except Exception as e:
    print("Request failed!")
    print("Error:", e)
    if hasattr(e, 'read'):
        try:
            print("Response body:", e.read().decode('utf-8'))
        except Exception:
            pass

import requests

url = "http://localhost:9696/predict"

ride = {"PULocationID": 10, "DOLocationID": 130, "trip_distance": 50}


response = requests.post(url, json=ride)
# print(response)

# Check if the response is successful
if response.status_code == 200:
    try:
        result = response.json()
        print(result)
    except requests.exceptions.JSONDecodeError:
        print("Response is not in JSON format:", response.text)
else:
    print(f"Request failed with status code {response.status_code}: {response.text}")

import requests

ride = {"PULocationID": 10, "DOLocationID": 130, "trip_distance": 50}

url = "http://localhost:9696/predict"
response = requests.post(url, json=ride)
result = response.json()

print(result)

import requests

url = "https://app.terraform.io/api/v2/account/details"

headers = {
    "Authorization": "Bearer TOKEN",  # Replace YOUR_TOKEN_HERE with your actual token
    "Content-Type": "application/vnd.api+json"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")

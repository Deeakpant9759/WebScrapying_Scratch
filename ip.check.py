import requests

proxies = {
    "https": "http://207.254.38.169",  # use http:// here
}

try:
    response = requests.get("https://ipinfo.io/json", proxies=proxies, timeout=5)
    print(response.json())
except requests.exceptions.RequestException as e:
    print("Error:", e)

import socket
import requests

target = "example.com"

print(f"Target:{target}")

ip = socket.gethostbyname(target)
print(f"ResolvedIP:{ip}")

response = requests.get(f"https://{target}", timeout=10)

print(f"HTTP status:{response.status_code}")
print(f"Server header:{response.headers.get('server')}")
print(f"Content type:{response.headers.get('content-type')}")


import requests

url = "http://127.0.0.1:5000/products/16"
# new_product = {
#     "category":"abcd",
# }
data = requests.delete(url)
print(data.json())
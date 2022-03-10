import os
from pathlib import Path
import requests

PINATA_BASE_URL = "https://api.pinata.cloud/"
endpoint = "pinning/pinFileToIPFS"
filepath = "./img/pug.png" # If we wanted to pin other images, we'd change this or even set up some type fo for loop
filename = filepath.split("/")[-1:][0]
headers = { # We need some headers for our post request to the API (our API keys)
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
}

# Below we're saying, take the locally stored pug image, and send it to Pinata to store (pin it) on IPFS
def main():
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(
            PINATA_BASE_URL + endpoint,
            files={"file": (filename, image_binary)},
            headers=headers,
        )
        print(response.json())
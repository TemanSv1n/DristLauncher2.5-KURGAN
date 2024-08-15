import json
import os

import requests

import manifest_reader


# server_ip: str = "localhost"
# server_port: int = 8000

def getIpManifest():
    """Downloads a JSON file from a given URL and saves it to a specified path."""
    try:
        response = requests.get("https://raw.githubusercontent.com/TemanSv1n/Slons/main/launcher_ip.json")
        response.raise_for_status()  # Raise an exception for bad status codes

        os.makedirs(os.path.dirname("data/manifests/launcher_ip.json"), exist_ok=True)  # Create directory if it doesn't exist

        with open("data/manifests/launcher_ip.json", 'w') as f:
            f.write(response.text)
        print(f"Downloaded and saved: https://raw.githubusercontent.com/TemanSv1n/Slons/main/launcher_ip.json to data/manifests/launcher_ip.json")

    except requests.exceptions.RequestException as e:
        print(f"Error: Could not download file: {e}")


def splitIp(ip_string):
    parts = ip_string.split(':')
    if len(parts) == 2:
        return parts[0], parts[1]
    else:
        return None, None
def getServerIp():
    getIpManifest()
    data = manifest_reader.readMinecraftManifest("data/manifests/launcher_ip.json")
    mirror = manifest_reader.readMinecraftManifest("data/mirror.json")["mirror"]
    ipstring = data[mirror]
    if ipstring != "playit":
        ip, port = splitIp(ipstring)
    else:
        ip = ipstring

    return ip
def getServerPort():
    getIpManifest()
    data = manifest_reader.readMinecraftManifest("data/manifests/launcher_ip.json")
    mirror = manifest_reader.readMinecraftManifest("data/mirror.json")["mirror"]
    ipstring = data[mirror]
    if ipstring != "playit":
        ip, port = splitIp(ipstring)
    else:
        port = "playit"

    return port  # "localhost"

def constructServerAdress(ip: str, port) -> str:
    if port == "playit":
        return f"http://{ip}"
    return f"http://{ip}:{port}"
def getMinecraftManifest(url: str):
    try:
        response = requests.get(f"{url}/manifests/minecraft_manifest.json")
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse the JSON response
        manifest_data = response.json()
        with open("data/manifests/minecraft_manifest.json", 'w') as f:
            json.dump(manifest_data, f, indent=4)
        return manifest_data

    except requests.exceptions.RequestException as e:
        print(f"Error retrieving manifest: {e}")
        return None

def getModsManifest(url: str):
    try:
        response = requests.get(f"{url}/manifests/mods_manifest.json")
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse the JSON response
        manifest_data = response.json()
        with open("data/manifests/mods_manifest.json", 'w') as f:
            json.dump(manifest_data, f, indent=4)
        return manifest_data

    except requests.exceptions.RequestException as e:
        print(f"Error retrieving manifest: {e}")
        return None

def getFilesManifest(url: str):
    try:
        response = requests.get(f"{url}/manifests/files_manifest.json")
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse the JSON response
        manifest_data = response.json()
        with open("data/manifests/files_manifest.json", 'w') as f:
            json.dump(manifest_data, f, indent=4)
        return manifest_data

    except requests.exceptions.RequestException as e:
        print(f"Error retrieving manifest: {e}")
        return None


if __name__ == '__main__':
    print(getModsManifest(constructServerAdress(getServerIp(), getServerPort())))
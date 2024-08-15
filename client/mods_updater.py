import json
import os

import requests

import manifest_reader
import server_connector


def createClientModsManifest():
    version = 0
    modlist = []
    for filename in os.listdir("minecraft_event/mods"):
        if  filename.endswith(".disabled"):
            filename = filename[:-9]
        if not filename.startswith("IGNORE."):
            if filename.endswith(".jar"):
                modlist.append(filename)

    with open("data/manifests/client_mods_manifest.json", 'w') as f:
        json.dump({"version": version, "mods": modlist}, f, indent=4)
        print(f"Client manifest created!")

def compareManifests(client_path, server_path) -> dict:
    c_manifest = manifest_reader.readMinecraftManifest(client_path)
    s_manifest = manifest_reader.readMinecraftManifest(server_path)

    c_list: list = c_manifest["mods"]
    s_list: list = s_manifest["mods"]

    delete_list = []
    download_list = []

    for m in s_list:
        if not m in c_list:
            download_list.append(m)
        else:
            c_list.pop(c_list.index(m))

    for n in c_list:
        if not n in s_list: #на всякий случай
            delete_list.append(n)

    return {"delete": delete_list, "download": download_list}

def updateMods(upd_dict: dict):
    #delete mods at first
    mods_dir = "minecraft_event/mods"
    for d in upd_dict["delete"]:
        filepath = os.path.join(mods_dir, d)
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Deleted: {filepath}")
        elif os.path.exists(filepath + ".disabled"):
            os.remove(filepath+".disabled")
            print(f"Deleted: {filepath}.disabled")
        else:
            print(f"File not found: {filepath}")

    #now download mods
    for i in upd_dict["download"]:
        filepath = os.path.join(mods_dir, i)
        url = server_connector.constructServerAdress(server_connector.getServerIp(), server_connector.getServerPort())

        try:
            response = requests.get(f"{url}/mods/{i}", stream=True)
            response.raise_for_status()  # Raise an exception for bad status codes

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            print(f"Downloaded: {i} to {filepath}")

        except requests.exceptions.RequestException as e:
            print(f"Error downloading {i}: {e}")



def automaticUpdateMods():
    server_connector.getModsManifest(
        server_connector.constructServerAdress(server_connector.getServerIp(), server_connector.getServerPort()))
    createClientModsManifest()
    updateMods(compareManifests("data/manifests/client_mods_manifest.json", "data/manifests/mods_manifest.json"))

if __name__ == '__main__':
    automaticUpdateMods()
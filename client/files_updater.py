import json
import os
import shutil
import zipfile

import requests

import main
import manifest_reader
import server_connector


def createZeroClientFilesManifest(client_path):
    with open(client_path, 'w') as f:
        json.dump({"version": 0, "files": {}}, f, indent=4)
    print(f"Created {client_path}")

def getFileVersion(c_list: dict, file: str):
    if file in c_list:
        return c_list[file]
    return 0
def compareManifests(client_path, server_path) -> dict:
    c_manifest = manifest_reader.readMinecraftManifest(client_path)
    s_manifest = manifest_reader.readMinecraftManifest(server_path)

    if c_manifest == None:
        createZeroClientFilesManifest(client_path)
        c_manifest = manifest_reader.readMinecraftManifest(client_path)

    c_vers: int = c_manifest["version"]
    s_vers: int = s_manifest["version"]
    c_list: dict = c_manifest["files"]
    s_list: dict = s_manifest["files"]

    delete_list = []
    download_list = []

    if c_vers < s_vers:
        for i in s_list:
            if s_list[i] == -1:
                delete_list.append(i)
                print(f"Adding {i} to delete list")
            else:
                if getFileVersion(c_list, i) < s_list[i]:
                    download_list.append(i)
                    print(f"Adding {i} to update list")

    elif c_vers == s_vers:
        print("Manifest versions are equal, skipping checks")
    else:
        print("F#cking how?")



    return {"delete": delete_list, "download": download_list}

def updateFiles(upd_dict: dict):
    #delete files at first
    files_dir = "minecraft_event"
    for d in upd_dict["delete"]:
        full_path = os.path.join(files_dir, d)

        if os.path.exists(full_path):
            if os.path.isdir(full_path):
                shutil.rmtree(full_path)
                print(f"Deleted directory: {full_path}")
            else:
                os.remove(full_path)
                print(f"Deleted file: {full_path}")
        else:
            print(f"File or directory not found: {full_path}")

    #now upd mods
    succ_updated_list = []
    for i in upd_dict["download"]:

        url = server_connector.constructServerAdress(server_connector.getServerIp(), server_connector.getServerPort())
        if '.' not in i:
            i = i + ".zip"
        filepath = os.path.join(files_dir, i)

        try:
            response = requests.get(f"{url}/files/{i}", stream=True)
            response.raise_for_status()  # Raise an exception for bad status codes
            if exists(i):
                if i.endswith(".zip"):
                    g = i[:-4]
                full_path = os.path.join("minecraft_event", g)

                if os.path.exists(full_path):
                    if os.path.isdir(full_path):
                        shutil.rmtree(full_path)
                        print(f"Deleted directory: {full_path}")
                    else:
                        os.remove(full_path)
                        print(f"Deleted file: {full_path}")
                else:
                    print(f"File or directory not found: {full_path}, nothing to delete")

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(i)
            if i.endswith(".zip"):
                extract_dir = os.path.join("minecraft_event", i[:-4])  # Create extraction path
                print(extract_dir)
                os.makedirs(extract_dir, exist_ok=True)  # Create directory if it doesn't exist
                try:
                    with zipfile.ZipFile(os.path.join("minecraft_event", i), 'r') as zip_ref:
  # Extract to the same directory
                        zip_ref.extractall(extract_dir)
                        os.remove(os.path.join("minecraft_event", i))
                    print(f"Unzipped '{i}' to '{extract_dir}'")
                except Exception as e:
                    print(f"Error: Could not unzip file: {e}")

            print(f"Downloaded: {i} to {filepath}")
            if i.endswith(".zip"):
                i = i[:-4]
            succ_updated_list.append(i)

        except requests.exceptions.RequestException as e:
            print(f"Error downloading {i}: {e}")
    if not upd_dict["download"] == succ_updated_list:
        inputed = main.checkNumeric(input("Какие-то файлы не докачались!!! Повторим? Манифест будет обновлен лишь при полной загрузке файлов!\n1 - Да; 2- Нет"))
        if inputed == 1:
            updateFiles({"delete":[], "download": upd_dict["download"]})
        else:
            pass
    else:
        equalizeClientManifest("data/manifests/old_files_manifest.json", "data/manifests/files_manifest.json")

def equalizeClientManifest(client_path, server_path):
    with open(server_path, 'r') as f_in:
        data = json.load(f_in)

    with open(client_path, 'w') as f_out:
        json.dump(data, f_out, indent=4)

def exists(filename:str):
    if filename.endswith(".zip"):
        filename = filename[:-4]
    return os.path.exists(filename)


def automaticUpdateFiles():
    server_connector.getFilesManifest(
        server_connector.constructServerAdress(server_connector.getServerIp(), server_connector.getServerPort()))

    updateFiles(compareManifests("data/manifests/old_files_manifest.json", "data/manifests/files_manifest.json"))

if __name__ == '__main__':
    automaticUpdateFiles()
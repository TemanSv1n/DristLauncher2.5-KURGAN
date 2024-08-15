import json
import os
import shutil
import sys
import zipfile
from colorama import init
from colorama import Fore, Back, Style

import requests

init()
def start():
    # _______________________________________________________________
    # Создание папок

    folder_path_event_create = "minecraft_event"

    if not os.path.exists(folder_path_event_create):
        os.makedirs(folder_path_event_create)
        print(Back.GREEN + "Path \"minecraft_event\" Create", Style.RESET_ALL)
    if not os.path.exists(folder_path_event_create + "/mods"):
        os.makedirs(folder_path_event_create + "/mods")
        print(Back.GREEN + "Path \"minecraft_event/mods\" Create", Style.RESET_ALL)

    folder_path_data_create = "data"

    if not os.path.exists(folder_path_data_create):
        os.makedirs(folder_path_data_create)
        print(Back.GREEN + "Path \"Data\" Create", Style.RESET_ALL)

    #manifests folder creation
    folder_path_manifests_create = "data/manifests"
    if not os.path.exists(folder_path_manifests_create):
        os.makedirs(folder_path_manifests_create)
        print(Back.GREEN + "Path \"Manifests\" Create", Style.RESET_ALL)
    # _______________________________________________________________
    # Создание .json Файлов

    folder_path_event = 'minecraft_event/'
    folder_path_data = 'data/'
    folder_path_manifests = 'data/manifests/'

    #minecraft manifest creation
    # json_file_path_event = os.path.join(folder_path_manifests, 'minecraft_manifest.json')
    # if not os.path.exists(json_file_path_event):
    #     with open(json_file_path_event, 'w') as f:
    #         json.dump({}, f, indent=4)
    #     print(Back.GREEN + "Event file create: info.json", Style.RESET_ALL)

    # Event info.json create
    json_file_path_event = os.path.join(folder_path_event, 'info.json')
    if not os.path.exists(json_file_path_event):
        with open(json_file_path_event, 'w') as f:
            json.dump({"version": 0}, f, indent=4)
        print(Back.GREEN + "Event file create: info.json", Style.RESET_ALL)

    # nickname.json create
    json_file_path_nickname = os.path.join(folder_path_data, 'nickname.json')
    if not os.path.exists(json_file_path_nickname):
        with open(json_file_path_nickname, 'w') as f:
            json.dump({
                "accessToken": None,
                "clientToken": None,
                "User-info": [{
                    "username": "None",
                    "AUTH_TYPE": "Offline Login",
                    "UUID": "None"
                }]
            }, f, indent=4)
        print(Back.GREEN + "Data file create: nickname.json", Style.RESET_ALL)

    # config.json create
    json_file_path_nickname = os.path.join(folder_path_data, 'config.json')
    if not os.path.exists(json_file_path_nickname):
        with open(json_file_path_nickname, 'w') as f:
            json.dump({"ram": 2048}, f, indent=4)
        print(Back.GREEN + "Data file create: config.json")

    json_file_path_mirror = os.path.join(folder_path_data, 'mirror.json')
    if not os.path.exists(json_file_path_mirror):
        with open(json_file_path_mirror, 'w') as f:
            json.dump({"mirror": "default"}, f, indent=4)
        print(Back.GREEN + "Data file create: mirror.json")

    json_file_path_nickname = os.path.join(folder_path_data, 'options.json')
    if not os.path.exists(json_file_path_nickname):
        with open(json_file_path_nickname, 'w') as f:
            json.dump({
                "username": "None",
                "uuid": "None"
            }, f, indent=4)
        print(Back.GREEN + "Data file create: options.json", Style.RESET_ALL)

    # _______________________________________________________________
    print("Start DristLauncher", Style.RESET_ALL)

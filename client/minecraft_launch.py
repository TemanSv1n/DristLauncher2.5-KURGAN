import os
import subprocess
import json
import minecraft_launcher_lib
import random

import files_updater
import manifest_reader
import mods_updater
import server_connector
import jdkDownloader


def get_script_dir(file_path=__file__):
    return os.path.dirname(os.path.abspath(file_path))



def start_minecraft_event():
    server_connector.getMinecraftManifest(
        server_connector.constructServerAdress(server_connector.getServerIp(), server_connector.getServerPort()))
    print("\n Start Launch Minecraft")
    minecraft_directory = 'minecraft_event/'


    version_minecraft = manifest_reader.readMinecraftManifest("data/manifests/minecraft_manifest.json")["minecraft-version"]
    loader = manifest_reader.readMinecraftManifest("data/manifests/minecraft_manifest.json")["modloader"]
    loader_version = manifest_reader.readMinecraftManifest("data/manifests/minecraft_manifest.json")["modloader-version"]
    jdk_version = manifest_reader.readMinecraftManifest("data/manifests/minecraft_manifest.json")["jdk-version"]


    print(version_minecraft)
    print(loader)
    print(loader_version)

    jdkDownloader.download_jdk(jdk_version, "minecraft_event")


    print('\n\nCheck Errors\n')

    print('\nFix Minecraft\n')
    print("Download forge")

    current_max = 0

    def set_status(status: str):
        print(status)

    def set_progress(progress: int):
        if current_max != 0:
            print(f"{progress}/{current_max}")

    def set_max(new_max: int):
        global current_max
        current_max = new_max

    minecraft_directory = 'minecraft_event/'

    callback = {
        "setStatus": set_status,
        "setProgress": set_progress,
        "setMax": set_max
    }

    destination_folder = 'minecraft_event/'
    forge_version = loader_version
    print(forge_version)
    minecraft_launcher_lib.forge.install_forge_version(f"{version_minecraft}-{forge_version}", destination_folder, callback=callback)
    # __________________________________

    print(f"Fix {random.randrange(1, 1488)} Errors")
    print(f"Fucking beaver, what did you fucking build?")
    print(f"DristPunk3, son!")
    launchClient(jdk_version, version_minecraft, loader, loader_version)



def pure_launchClient(jdk_version, version_minecraft, loader, loader_version):
    file_path = 'data/nickname.json'
    minecraft_directory = 'minecraft_event/'

    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data1 = json.load(f)
        print("Nickname.json найден")

        print("Options 1")
        options = {
            "username": data1["User-info"][0]["username"],
            "uuid": data1["User-info"][0]["UUID"],
            "token": "",
            "jvmArguments": [],
            #"executablePath": os.path.realpath(shutil.which("java")),  # The path to the java executable
            "executablePath": f"{get_script_dir()}/minecraft_event/jdk-{jdk_version}/bin/java",
            "gameDirectory": ""
            # "executablePath" : executablePath
        }
        print("Options 2")
    else:
        print("Файл 'data/nickname.json' не найден.")
        return  # Выйти из функции, так как нет необходимых данных для запуска Minecraft

    file_path2 = 'data/config.json'
    print('Minecraft data path')
    destination_folder = 'minecraft_event/'
    if os.path.exists(file_path2):
        with open(file_path2, 'r') as config:
            ram_config = json.load(config)
        max_ram = ram_config["ram"]
        print('Minecraft pick ram')
    else:
        print("Файл 'data/config.json' не найден.")
        return

    options["jvmArguments"] = [f"-Xmx{max_ram}m", f"-Xms256m"]
    options["gameDirectory"] = "minecraft_event/"
    print('Minecraft jvmArgs applyed')

    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(
        f"{version_minecraft}-{loader}-{loader_version}", #1.18.2-forge-40.2.21
        minecraft_directory, options)
    print(f'Minecraft command OK: {minecraft_command}')

    try:
        # if os.name == "nt":
        # Запуск Minecraft
        subprocess.Popen(minecraft_command)
        print("РАКЕТА ЗАПУЩЕНА!!! Ждите, товарищ")
        input("0_0\n 0 ")
    except Exception as e:
        print(f"Ошибка при запуске Minecraft: {e}")


def launchClient(jdk_version, version_minecraft, loader, loader_version): #Launches minecraft with all mods & files checks
    mods_updater.automaticUpdateMods()
    files_updater.automaticUpdateFiles()
    pure_launchClient(jdk_version, version_minecraft, loader, loader_version)

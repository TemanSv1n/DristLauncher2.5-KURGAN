import json

import files_updater
import launch
import manifest_reader
import minecraft_launch
import sys, os

import mods_updater
import server_connector

sys.path.insert(0, os.path.abspath('./funcs'))



def welcomeScript() -> None:
    print("Добро пожаловать в ДристЛаунчер ёпта")
    launch.start()

state: str = "main_screen"
PHRASE_DICT: dict = {"main_screen": "1 - Чтобы ПОЛНОСТЬЮ установить МАЙНКРАФТ\n2 - Чтобы изменить RAM-оперативку / Никнейм\n3 - Чтобы запустить МАЙНКРАФТ\n4 - Чтобы войти в ДЕБАГ ЗОНУ",
                     "config_screen": "1 - Чтобы изменить количество выделенной Оперативной памяти\n2 - Чтобы изменить Никнейм\n3 - Чтобы вернуться на главный экран",
                     "debug_auth_screen": "Пройдите очень сложную авторизацию, чтобы отличить вас от ПРИЦЕЛА...\nВведите БОБРОВОЕ СЛОВО",
                     "debug_screen": "1 - Чтобы запустить МАЙНКРАФТ без проверок\n2 - Чтобы обновить манифест модов\n3 - Чтобы обновить манифест файлов\n4 - Чтобы сменить зеркало\n5 - Чтобы вернуться на главный экран"
                     }
def setState(newState: str) -> str:
    global state
    state = newState
    return state

def checkNumeric(string: str) -> int:
    if not string.isnumeric():
        print("ТЫ ДУРАК!!!")
        return 0
    return int(string)

def setRam(file_path, key, new_value):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            data[key] = new_value

            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)

            print(f"Modified JSON file: {file_path}")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {file_path}")
    else:
        print(f"Error: File not found: {file_path}")

def setName(file_path, new_username):

  if os.path.exists(file_path):
    try:
      with open(file_path, 'r') as f:
        data = json.load(f)

      # Find the user-info array
      user_info = data.get("User-info", [])
      if user_info:
        # Modify the username in the first user object
        user_info[0]["username"] = new_username

      with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

      print(f"Modified username in JSON file: {file_path}")
    except json.JSONDecodeError:
      print(f"Error: Invalid JSON format in {file_path}")
  else:
    print(f"Error: File not found: {file_path}")

def inputHandler(string: str) -> None:
    global state
    if state == "main_screen":
        num: int = checkNumeric(string)
        match num:
            case 1:
                minecraft_launch.start_minecraft_event()
            case 2:
                setState("config_screen")
            case 3:
                mc_manifest = manifest_reader.readMinecraftManifest("data/manifests/minecraft_manifest.json")
                minecraft_launch.launchClient(
                    mc_manifest["jdk-version"],
                    mc_manifest["minecraft-version"],
                    mc_manifest["modloader"],
                    mc_manifest["modloader-version"]
                )
            case 4:
                setState("debug_auth_screen")


    elif state == "config_screen":
        num: int = checkNumeric(string)
        match num:
            case 1:
                setRam("data/config.json", "ram", checkNumeric(input("Введите количество выделенной оперативы для майна. Главное больше чем у вас есть не выделяйте)\n")))
            case 2:
                setName("data/nickname.json", input("Введите ваш новый никнейм. Только латиница и без тупых символов\n"))
            case 3:
                setState("main_screen")
    elif state == "debug_auth_screen":
        if string == "Graph_Bober_IV":
            setState("debug_screen")
        else:
            print("Скилл дрищью")
            setState("main_screen")
    elif state == "debug_screen":
        num: int = checkNumeric(string)
        match num:
            case 1:
                mc_manifest = manifest_reader.readMinecraftManifest("data/manifests/minecraft_manifest.json")
                minecraft_launch.pure_launchClient(
                    mc_manifest["jdk-version"],
                    mc_manifest["minecraft-version"],
                    mc_manifest["modloader"],
                    mc_manifest["modloader-version"]
                )
            case 2:
                mods_updater.automaticUpdateMods()
            case 3:
                files_updater.automaticUpdateFiles()
            case 4:
                server_connector.getIpManifest()
                print("Думайте с умом над сменой зеркала... Ничего не делайте, если не знаете, зачем оно надо...")
                ip_mani = manifest_reader.readMinecraftManifest("data/manifests/launcher_ip.json")
                mirror = manifest_reader.readMinecraftManifest("data/mirror.json")["mirror"]
                print(f"Ваше зеркало - {mirror}, адрес - {ip_mani[mirror]}")
                for i in ip_mani:
                    print (f"Зеркало {i} -> {ip_mani[i]}")
                mir = input("Введите текстовое обозначение зеркала\n")
                with open("data/mirror.json", "w") as f:
                    json.dump({"mirror": mir}, f, indent=4)
                ip_mani = manifest_reader.readMinecraftManifest("data/manifests/launcher_ip.json")
                mirror = manifest_reader.readMinecraftManifest("data/mirror.json")["mirror"]
                print(f"Ваше зеркало - {mirror}, адрес - {ip_mani[mirror]}")
                setState("debug_screen")
            case 5:
                setState("main_screen")







if __name__ == '__main__':
    welcomeScript()
    while True:
        if inputHandler(input(PHRASE_DICT.get(state)+ "\n")) == -1:
            break


import json
import os
import shutil
import zipfile


def checkNumeric(string: str) -> int:
    if not string.isnumeric():
        print("ТЫ ДУРАК!!!")
        return 0
    return int(string)
def inputHandler(string: str) -> None:
        num: int = checkNumeric(string)
        match num:
            case 1:
                modsManifestBuild("manifests/mods_manifest.json")
            case 2:
                filesManifestBuild("manifests/files_manifest.json")


def modsManifestBuild(old_manifest_path):
    manifest = getManifest(old_manifest_path)
    version = manifest["version"]
    modlist = []
    for filename in os.listdir("mods"):
        modlist.append(filename)
    if modlist != manifest["mods"]:
        with open(old_manifest_path, 'w') as f:
            json.dump({"version": version+1, "mods": modlist}, f, indent=4)
            print(f"Manifest updated, new version is {version+1}")
    else:
        print("Nothing changed! If changes actually are, try renaming changed mod files")

def getManifest(filepath):
    json_file_path_event = filepath
    if not os.path.exists(json_file_path_event):
        with open(json_file_path_event, 'w') as f:
            json.dump({"version": 0, "mods": []}, f, indent=4)
        print(f"Created {filepath}")
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {filepath}")
        return None

def getFilesManifest(filepath):
    json_file_path_event = filepath
    if not os.path.exists(json_file_path_event):
        with open(json_file_path_event, 'w') as f:
            json.dump({"version": 0, "files":{}}, f, indent=4)
        print(f"Created {filepath}")
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {filepath}")
        return None

def filesManifestBuild(old_manifest_path):
    manifest = getFilesManifest(old_manifest_path)
    version = manifest["version"]
    mani_files = manifest["files"]
    changes = 0;
    files = mani_files
    for filename in os.listdir("files"):
        if not filename.endswith(".zip"):

            print(f"Update {filename} ? 1 - yes, 2 NO!!! GOD NO!!! PLEASE NO!!!, 3 - DELETE file")

            inputed = checkNumeric(input())
            if inputed == 1:
                changes += 1
                f_version = 0
                if (filename in mani_files):
                    f_version = mani_files[filename]
                    if f_version == -1:
                        f_version = version
                files[filename] = f_version + 1
                print(filename + " - updating...")
                if os.path.isdir(os.path.join("files", filename)):
                    if os.path.exists(filename + ".zip"):
                        os.remove(filename + ".zip")
                        print(f"Deleted: {filename}.zip")

                    zip_path = os.path.join("files", filename + ".zip")
                    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for root, _, filez in os.walk(os.path.join("files", filename)):
                            for file in filez:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, os.path.join("files", filename))
                                zipf.write(file_path, arcname)
                        print(f"ZIPPED {filename} into {filename}.zip")
            elif inputed == 2:
                "SKIPPING file..."
            elif inputed == 3:
                changes += 1
                files[filename] = -1
                print(filename + " - deleting...")
                full_path = os.path.join("files", filename)
                zip_path = os.path.join("files", filename + ".zip")

                if os.path.exists(full_path):
                    if os.path.isdir(full_path):
                        shutil.rmtree(full_path)
                        print(f"Deleted directory: {full_path}")
                    else:
                        os.remove(full_path)
                        print(f"Deleted file: {full_path}")

                if os.path.exists(zip_path):
                    os.remove(zip_path)
                    print(f"Deleted ZIP file: {zip_path}")



    if changes > 0:
        with open(old_manifest_path, 'w') as f:
            json.dump({"version": version+1, "files": files}, f, indent=4)
            print(f"Manifest updated, new version is {version+1}")
    else:
        print("You did not change anything >-^. Grandfuhrer is very ANGRY!!!")

if __name__ == '__main__':
    while True:
        if inputHandler(input("1 - Build mods_manifest.json\n2 - Build files_manifest.json\n")) == -1:
            break

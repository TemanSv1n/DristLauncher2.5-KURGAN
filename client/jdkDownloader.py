import os
import requests
import zipfile
import shutil
import tarfile

def download_jdk(jdk_version, download_folder):
    """Downloads the JDK of the specified version into the given folder.

    Args:
        jdk_version: The Java JDK version to download (e.g., "17").
        download_folder: The folder where the JDK should be downloaded.
    """
    print("CHECKING YOUR JDK's BALLS")
    if os.path.isdir(f"{download_folder}/jdk-{jdk_version}"):
        print(f"Your java is here, {download_folder}/jdk-{jdk_version}. If problem appears - try to delete this folder, launcher reinstalls java")
        return
    print("No jdk folder, checking for file")
    ext: str = ".tar.gz"
    if os.name == 'nt':
        ext = ".zip"
    if os.path.isfile(f"{download_folder}/jdk-{jdk_version}{ext}"):
        print(f"File located, extracting {download_folder}/jdk-{jdk_version}{ext}")
        extract(os.path.join(download_folder, f"jdk-{jdk_version}{ext}"), download_folder, f"jdk-{jdk_version}", os.name)
        return

    # Define the download URL (adapt based on your preferred source)
    download_url = f"https://download.oracle.com/java/17/latest/jdk-{jdk_version}_linux-x64_bin.tar.gz"  # Example for Linux (x64)
    if os.name == 'nt':
        download_url = f"https://download.oracle.com/java/17/latest/jdk-{jdk_version}_windows-x64_bin.zip" # Example for Windows (x64)

    # Create the download folder if it doesn't exist
    os.makedirs(download_folder, exist_ok=True)

    # Download the file
    response = requests.get(download_url, stream=True)
    response.raise_for_status()  # Raise an exception for bad status codes

    # Save the file to the download folder
    file_path = os.path.join(download_folder, f"jdk-{jdk_version}{ext}")
    with open(file_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    # Extract the archive (adjust based on archive type)
    # For .tar.gz archives:
    extract(os.path.join(download_folder, f"jdk-{jdk_version}{ext}"), download_folder, f"jdk-{jdk_version}", os.name)

    # (For other archive formats, use appropriate extraction methods)

    # Remove the downloaded archive file
    os.remove(file_path)

    print(f"JDK {jdk_version} downloaded and extracted to {download_folder}")

def extract(file_path, download_path , new_dir_name, os):
    if os == "nt":
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(download_path)
            print(f"Zip file '{file_path}' extracted to '{download_path}'")
    else:
        with tarfile.open(file_path, "r:gz") as tar_ref:
            tar_ref.extractall(download_path)
            print(f"Tar.gz file '{file_path}' extracted to '{download_path}'")

    rename_dir("jdk", new_dir_name)

def rename_dir(old_prefix, new_name):
  """
  Renames all directories starting with 'old_prefix' to 'new_name'.

  Args:
      old_prefix (str): The prefix of the directories to rename.
      new_name (str): The new name for the directories.
  """
  for dirpath, dirnames, filenames in os.walk("funcs"):
    for dirname in dirnames:
      if dirname.startswith(old_prefix):
        old_path = os.path.join(dirpath, dirname)
        new_path = os.path.join(dirpath, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed '{old_path}' to '{new_path}'")
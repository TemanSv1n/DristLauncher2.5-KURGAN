import json
import os
import random
import string
import uuid


def generate_cracked_uid():
    # Read data from the JSON file
    file_path = 'data/nickname.json'
    with open(file_path) as f:
        data1 = json.load(f)

    # Check if UUID is None
    if data1["User-info"][0]["UUID"] == "None" or data1["User-info"][0]["UUID"] == data1["User-info"][0]["UUID"]:
        # Generate a new UUID
        uid = uuid.uuid4().hex
        data1["User-info"][0]["UUID"] = str(uid)
        # Write the updated data back to the JSON file
        with open(file_path, 'w') as js_set:
            json.dump(data1, js_set, indent=4)

        print(uid)

        file_path1 = 'data/options.json'

        with open(file_path1) as f2:
            data2 = json.load(f2)

        data2["uuid"] = f"{uid}"

        with open(file_path1, 'w') as js_set:
            json.dump(data2, js_set, indent=4)

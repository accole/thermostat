import time
import json
import requests

def now():
    return round(time.time())

def save(filename, data):
    print(f"Saving JSON to {filename} ...")
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    return

def get(url, params={}, headers={}, timeout=15):
    """
    Makes a GET API request

    Args:
        url (str): API request URL
        params (dict, optional): API query string parameters
        headers (dict, optional): API request headers
        timeout (int, optional): API request timeout

    Returns:
        obj: A dictionary containing status code, error message, or data
    """
    try:
        headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "application/json",
            }
        )
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        output = {"status": response.status_code}
        if response.ok:
            output["data"] = response.json()
        else:
            output["error"] = response.reason

        return output

    except Exception as e:
        return {"status": 999, "error": f"An unexpected error occurred: {e}"}

def filter_object_keys(list_of_objects, keys_to_keep):
    """
    Filters the keys of objects in a list, keeping only the specified keys.

    Args:
      list_of_objects: A list of dictionaries (objects).
      keys_to_keep: A list of keys to retain in each object.

    Returns:
      A new list containing objects with only the specified keys.
    """
    return [{k: obj[k] for k in keys_to_keep if k in obj} for obj in list_of_objects]

def alphabetize(dict):
    keys = list(dict.keys())
    keys.sort()
    return {i: dict[i] for i in keys}

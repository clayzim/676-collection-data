import requests
import json
import csv

csv_filename = "./ftu-libraries-set-list.csv"
fieldnames = ["image", "link", "title"]
parameters = {"fo": "json"}

def get_collection_list(url):
    response = requests.get(url, params=parameters)
    if response.status_code == 200:
        return response.text
    else:
        raise ValueError("Didn't get an HTTP OK")

def download_collection_json(url, outfile):
    items_json = get_collection_list(url)
    items = json.loads(items_json)
    with open(outfile, mode='w', encoding="utf-8") as file:
        output = json.dumps(items["content"], sort_keys = True, indent = 4)
        file.write(output)

def create_csv_list_from_json(infile, outfile):
    with open(infile, mode='r', encoding="utf-8") as response:
        content = json.load(response)

    items = content["set"]["items"]

    with open(outfile, mode='w', encoding="utf-8") as csv_file:
        output = csv.writer(csv_file)

        output.writerow(fieldnames)
        for item in items:
            image = item["image"] if "image" in item else "NO_IMAGE"
            link = item["link"] if "link" in item else "NO_LINK"
            title = item["title"] if "title" in item else "NO_TITLE"
            output.writerow([image, link, title])

def extract_libraries_list():
    libraries_url = "https://www.loc.gov/free-to-use/libraries/"
    json_filename = "./ftu-libraries-set-info.json"
    download_collection_json(libraries_url, json_filename)
    create_csv_list_from_json(json_filename, csv_filename)

def retrieve_item_metadata(infile):
    base_url = "https://www.loc.gov"
    base_json_path = "./item-metadata/"
    error_filename = "errors.txt"
    with open(infile, mode='r', encoding="utf-8") as csv_file:
        items = csv.DictReader(csv_file)
        with open(error_filename, mode='w', encoding="utf-8") as errors:
            for index, item in enumerate(items):
                url = base_url + item["link"]
                identifier = item["link"].split('/')[2]
                response = requests.get(url, params=parameters)
                if response.status_code != 200:
                    errors.write(f"Index {index}: No HTTP OK\n")
                content_type = response.headers["Content-Type"].split('/')[-1]
                if content_type == "json":
                    data = response.json()
                    outfile = base_json_path + identifier + ".json"
                    with open(outfile, mode='w', encoding="utf-8") as item_file:
                        output = json.dumps(data, sort_keys = True, indent = 4)
                        item_file.write(output)
                else:
                    errors.write(f"Index {index}: No JSON\n")


def retrieve_item_files(infile):
    base_url = "https://www.loc.gov"
    base_image_path = "./item-files/"
    error_filename = "image-errors.txt"
    with open(infile, mode='r', encoding="utf-8") as csv_file:
        items = csv.DictReader(csv_file)
        with open(error_filename, mode='w', encoding="utf-8") as errors:
            for index, item in enumerate(items):
                url = base_url + item["image"]
                identifier = item["link"].split('/')[2]
                response = requests.get(url)
                if response.status_code != 200:
                    errors.write(f"Index {index}: No HTTP OK\n")
                outfile = base_image_path + identifier + ".jpg"
                with open(outfile, mode="wb") as item_file:
                    for chunk in response:
                        item_file.write(chunk)

extract_libraries_list()
retrieve_item_metadata(csv_filename)
retrieve_item_files(csv_filename)
import requests
import csv

import json

def ssn_data():
    url='https://services.swpc.noaa.gov/json/solar-cycle/sunspots.json'


    proxies={}
    response=requests.get(url=url,proxies=proxies)
    df= (response.content)
    decode_data=df.decode('utf-8')
    json_data = json.loads(decode_data)


    data = json_data

    csv_file_path = 'data.csv'

    # Extracting the keys from the first dictionary in the list
    fieldnames = data[0].keys()

    # Open the CSV file in write mode
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write each dictionary as a row in the CSV file
        writer.writerows(data)

    print(f"CSV file '{csv_file_path}' created successfully.")




    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    # Specify the condition for row deletion
    condition_column_index = data[0].index('time-tag')
    condition_value = "1958"

    # Filter the rows based on the condition
    filtered_data = [row for row in data if row[condition_column_index] >= condition_value]

    # Write the remaining rows back to the CSV file
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(filtered_data)

    print(f"CSV file '{csv_file_path}' has been updated with the rows removed.")

    
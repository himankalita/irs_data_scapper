import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options


def irs_data():
        
    os.environ['PATH'] += r"/"
    options = webdriver.ChromeOptions()
    # Enable headless mode
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')




    driver = webdriver.Chrome(options=options)
    driver.get("https://ccmc.gsfc.nasa.gov/modelweb/models/iri2016_vitmo.php")
    year=1958
    month_names = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }
    #latitute and longitude of guwahati
    latitude=26.1158
    longitude=91.7086
    height=100
    TEC= 10000
    stepsize=500
    start=500
    row_number = 1
    #inserting row number
    column_names = ['ne_500', 'Te_500', 'ne_1000', 'Te_1000', 'ne_1500', 'Te1500', 'ne_2000' ,'Te_2000','TEC']

    filename = 'data.csv'
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        existing_data = list(reader)
        

        # Append the new data horizontally to the existing data
    if 1 <= row_number <= len(existing_data):
        existing_data[row_number - 1].extend(column_names)

        

        # Write the modified data back to the CSV file
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(existing_data)

    row_number=row_number+1



    while(year<2024):


        if(year==2023):
            n=7

        else:
            n=13
        for month in range(1,13):
            month_name = month_names[month]
            driver = webdriver.Chrome()
            driver.get("https://ccmc.gsfc.nasa.gov/modelweb/models/iri2016_vitmo.php")




            year_input = driver.find_element(By.NAME,'year')


            # Clear the input field before entering a new value
            year_input.clear()
            year_input.send_keys(year)

            #month_input
            month_dropdown = driver.find_element(By.NAME, 'month')
            month_select = Select(month_dropdown)
            month_select.select_by_visible_text(month_name)

            #latitue_input
            latitude_input = driver.find_element(By.NAME,'latitude')
            latitude_input.clear()
            latitude_input.send_keys(latitude)

            #longitude_input
            longitude_input = driver.find_element(By.NAME,'longitude')
            longitude_input.clear()
            longitude_input.send_keys(longitude)

            #height_input
            height_input = driver.find_element(By.NAME,'height')
            height_input.clear()
            height_input.send_keys(height)

            #start_input
            start_input = driver.find_element(By.NAME,'start')
            start_input.clear()
            start_input.send_keys(start)

            #stepsize_input
            stepsize_input = driver.find_element(By.NAME,'step')
            stepsize_input.clear()
            stepsize_input.send_keys(stepsize)

            #TEC_input
            TEC_input = driver.find_element(By.NAME,'htec_max')
            TEC_input.clear()
            TEC_input.send_keys(TEC)


            #click checkbox_electron temperature
            checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox' and @value='21']")


            if not checkbox.is_selected():
                checkbox.click()

            #click checkbox_TEC
            checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox' and @value='29']")


            if not checkbox.is_selected():
                checkbox.click()

            #click checkbox_Ratio of Ne and F2 peak density(Ne/NmF2)>
            checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox' and @value='18']")


            if checkbox.is_selected():
                checkbox.click()

            # Submit the form
            submit_button = driver.find_element(By.XPATH, "//input[@value='Submit']")
            submit_button.click()

            # Wait for the page to load or perform further actions as needed
            wait = WebDriverWait(driver, 0)  # 3 seconds
            wait.until(EC.url_to_be("https://ccmc.gsfc.nasa.gov/cgi-bin/modelweb/models/vitmo_model.cgi"))

            text_content = driver.find_element(By.TAG_NAME,'html').text
            target_word="     1            2      3     4"
            index = text_content.find(target_word)

            # Remove everything before the word (including the word itself)
            result = text_content[index + len(target_word):]


            target_word="ModelWeb Curator: CCMC Instant-Run Team (CCMC Support)"
            split_parts = result.split(target_word)
            result = split_parts[0]


            rows = result.strip().split('\n')

            # Split each row into elements
            nested_list = [row.split() for row in rows]
            # split_list = [sublist[0].split() for sublist in nested_list]

            # # Flatten the nested list structure
            # flattened_list = [item for sublist in split_list for item in sublist]
            # print(flattened_list)
            updated_nested_list = [sublist[1:] for sublist in nested_list]
            # print(updated_nested_list)
            # Print the extracted text content

            single_list = [item for sublist in updated_nested_list for item in sublist]
            indices_to_remove = [2, 5, 8]  # Indices of elements to remove

            modified_list = [item for index, item in enumerate(single_list) if index not in indices_to_remove]


            filename = 'data.csv'  # Specify the filename for the CSV file


            # Insert the list items into the CSV file with column names
            existing_data = []
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                existing_data = list(reader)


                # Append the new data horizontally to the existing data
            if 1 <= row_number <= len(existing_data):
                existing_data[row_number - 1].extend(modified_list)



                # Write the modified data back to the CSV file
                with open(filename, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(existing_data)

            row_number=row_number+1
            driver.back()

        year=year+1




    driver.quit()

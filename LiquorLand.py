from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import math
import csv
from datetime import datetime

webdriver_service = Service('/usr/local/bin/chromedriver')
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
driver = webdriver.Chrome(service=webdriver_service, options=options)

productsPerPage = 60
driver.get('https://www.liquorland.com.au/specials/spirit-specials')

driver.implicitly_wait(20)

productCountElement = driver.find_element(By.XPATH, '//*[@id="main-container"]/div[2]/div[2]/div/div[2]/div[4]/div/div[1]/div/div[1]/b')
productCount = productCountElement.text
print(f"{productCount} products on special at Liquor Land!")
numberOfPages = math.ceil(int(productCount) / productsPerPage)
print(f'There are {numberOfPages} pages of products')

# Generate the timestamp for the CSV filename
current_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
filename = f"liquorLandSpiritPrices {current_time}.csv"

# Open the CSV file in write mode
with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["storeName", "brand", "name", "salePrice", "originalPrice", "percentageDiscount"])  # Write column headers

    for page in range(1, numberOfPages + 1):
        driver.get(f'https://www.liquorland.com.au/specials/spirit-specials?page={page}')
        driver.implicitly_wait(20)

        if page == numberOfPages:
            numProductsToScan = int(productCount) - (productsPerPage * (page - 1)) + 1
        else:
            numProductsToScan = productsPerPage

        print(numProductsToScan)
        productsRemaining = int(productCount) - 1

        for num in range(1, numProductsToScan):
            brandElement = driver.find_element(By.XPATH, f'//*[@id="main-container"]/div[2]/div[2]/div/div[2]/div[4]/div/div[2]/div[{num}]/div/div[2]/h3[1]/a/div')
            nameElement = driver.find_element(By.XPATH, f'//*[@id="main-container"]/div[2]/div[2]/div/div[2]/div[4]/div/div[2]/div[{num}]/div/div[2]/h3[2]/a/div')
            dollarElement = driver.find_element(By.XPATH, f'//*[@id="main-container"]/div[2]/div[2]/div/div[2]/div[4]/div/div[2]/div[{num}]/div/div[4]/div[2]/span[2]/div/span[2]')
            centsElement = driver.find_element(By.XPATH, f'//*[@id="main-container"]/div[2]/div[2]/div/div[2]/div[4]/div/div[2]/div[{num}]/div/div[4]/div[2]/span[2]/div/span[4]')
            originalDollarElement = driver.find_element(By.XPATH, f'//*[@id="main-container"]/div[2]/div[2]/div/div[2]/div[4]/div/div[2]/div[{num}]/div/div[4]/div[2]/span[1]/div/span[2]')

            brand = brandElement.text
            name = nameElement.text
            dollarValue = dollarElement.text
            centValue = centsElement.text
            salePrice = float(f"{dollarValue}.{centValue}")
            originalDollarValue = originalDollarElement.text

            print(f"{brand} - {name} - ${salePrice} was ${originalDollarValue}")

            # Calculate percentage discount
            percentageDiscount = 1 - (salePrice / float(originalDollarValue))

            # Write the data to the CSV file
            writer.writerow(["Liquor Land", brand, name, salePrice, originalDollarValue, percentageDiscount])

        print(f"Page {page} complete!")

print("All pages complete!")

driver.quit()


def sortCsvByPercentageDiscount(input_filename, output_filename):
    # Read the CSV file
    data = []
    with open(input_filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip the header row
        data = sorted(reader, key=lambda row: float(row[5]), reverse=True)  # Sort by percentage discount column

    # Write the sorted data to a new CSV file
    with open(output_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)  # Write the header row
        writer.writerows(data)


# Sort the CSV file by percentage discount in descending order
input_filename = filename
output_filename = f"sorted_liquorLandSpiritPrices {current_time}.csv"
sortCsvByPercentageDiscount(input_filename, output_filename)
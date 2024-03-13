from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import math

webdriver_service = Service('/usr/local/bin/chromedriver')
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
driver = webdriver.Chrome(service=webdriver_service, options=options)

productsPerPage = 40
driver.get('https://bws.com.au/productgroup/spirit-specials')

# driver.implicitly_wait(20)

productCountElement = driver.find_element(By.XPATH, '//*[@id="center-panel"]/div[1]/div[3]/bws-product-group/div/bws-filters/div/wow-quick-filters/div/div[1]/span')
productCount = productCountElement.text
productCountNum = productCount.split(" ", 1)[0]
print(f"{productCountNum} products on special at BWS!")
numberOfPages = math.ceil(int(productCountNum) / productsPerPage)
print(f'There are {numberOfPages} pages of products')

for page in range(1, numberOfPages + 1):

    driver.get(f'https://bws.com.au/productgroup/spirit-specials?pageNumber={page}')
    # driver.implicitly_wait(20)
    try:
        button = driver.find_element(By.XPATH, '//*[@id="body-container"]/div[1]/wow-store-picker-panel/div/div[2]/button')
        button.click()
        print("Store select exit button clicked!")
    except NoSuchElementException:
        print("XPath not found. Button not clicked.")

    if page == numberOfPages:
        numProductsToScan = int(productCountNum) - (productsPerPage * (page - 1)) + 1
    else:
        numProductsToScan = productsPerPage

    print(numProductsToScan)
    productsRemaining = int(productCountNum) - 1

    for num in range(1, numProductsToScan * 2, 2):
        if num == 11:
            print("Catalogue Banner Skipped")
            continue

        try:
            brandElement = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, f'//*[@id="br-special-items-container"]/div[{num}]/wow-card/span/bws-product/div/div[2]/a/h2'))
            )
            nameElement = driver.find_element(By.XPATH, f'//*[@id="br-special-items-container"]/div[{num}]/wow-card/span/bws-product/div/div[2]/div')
            dollarElement = driver.find_element(By.XPATH, f'//*[@id="br-special-items-container"]/div[{num}]/wow-card/span/bws-product/div/div[3]/span[2]')
            centsElement = driver.find_element(By.XPATH, f'//*[@id="br-special-items-container"]/div[{num}]/wow-card/span/bws-product/div/div[3]/span[3]')

            try:
                savingElement = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located(
                        (By.XPATH, f'//*[@id="br-special-items-container"]/div[{num}]/wow-card/span/bws-product/div/div[1]/savings-badge/span/span/span'))
                )
                savingValue = savingElement.text
            except NoSuchElementException:
                savingValue = "N/A"
                continue
            except TimeoutException:
                savingValue = "N/A"
                continue

            brand = brandElement.text
            name = nameElement.text
            dollarValue = dollarElement.text
            centValue = centsElement.text
            savingValue = savingElement.text
            
            
            salePrice = float(f"{dollarValue}.{centValue}")
            originalDollarValue = salePrice + float(savingValue[1:])
            print(salePrice)
            print(f"{brand} - {name} - ${salePrice} was {originalDollarValue}")
        #Timeout when finished because errors, i didnt get the product page counting formula right lol
        except TimeoutException:
            break

    print(f"Page {page} complete!")

print("All pages complete!")

driver.quit()
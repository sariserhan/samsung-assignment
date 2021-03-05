from selenium import webdriver
from bs4 import BeautifulSoup
import os
from selenium.webdriver.common.action_chains import ActionChains
    
def phonePriceCheck():
    DRIVER_PATH = os.path.dirname(__file__) + "/chromedriver"
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.get('https://www.samsung.com/us/mobile/phones/galaxy-z/?Flagship%20Series%20Name=Galaxy+Z&model_family=Galaxy+Z+Fold2+5G,Galaxy+Fold')

    soup = BeautifulSoup(driver.page_source, "html.parser")

    product = soup.find_all(class_='ProductName-common-518700986 ProductName-title-3949175622')
    price = soup.find_all(class_='Product-card__price-current')

    phoneName = [i.string for i in product]
    phonePrice = ['$'+str(i).split('-->$')[1].split('<!--')[0] for i in price]

    phonePriceDict = dict(zip(phoneName,phonePrice))
    phonePriceDictBuyNow = {}
    print(phonePriceDict)
    
    buttonProduct1 = "//div[@id='app']/div/div/div/div/div[4]/div/div/section/div[2]/section/div/div/a"
    buttonProduct2 = "//div[@id='app']/div/div/div/div/div[4]/div/div/section[2]/div[2]/section/div/div/a"

    driver.find_element_by_xpath(buttonProduct1).click()
    driver.implicitly_wait(1000)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    priceBuyNow = str(soup.find_all(class_='price-info'))
    productBuyNow = str(soup.select('h1.oos-title2')[0].text.strip())
    priceBuyNowProduct1 = '$' + priceBuyNow.split('<strong>$')[1].split('<strike>')[0]

    phonePriceDictBuyNow[productBuyNow] = priceBuyNowProduct1

    driver.get('https://www.samsung.com/us/mobile/phones/galaxy-z/?Flagship%20Series%20Name=Galaxy+Z&model_family=Galaxy+Z+Fold2+5G,Galaxy+Fold')
    driver.implicitly_wait(1000)

    driver.find_element_by_xpath(buttonProduct2).click()
    driver.implicitly_wait(1000)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    priceBuyNow = soup.find_all(class_='epp-price')
    productBuyNow = str(soup.select('h1.product-details__info-title')[0].text.strip())
    priceBuyNowProduct2 = '$' + [i.string for i in priceBuyNow][0]

    phonePriceDictBuyNow[productBuyNow] = priceBuyNowProduct2
    print(phonePriceDictBuyNow)

    driver.quit()
    
    return (phonePriceDict, phonePriceDictBuyNow)

def compare_dict(dict1, dict2):
    result = {}
    for x1 in dict1.keys():
        z = dict1.get(x1) == dict2.get(x1)
        if not z:
            print('key', x1)            
            print('value A', dict1.get(x1), '\nvalue B', dict2.get(x1))
            print('-----\n')
            if x1 not in result:
                if dict1.get(x1) != dict2.get(x1):
                    result[x1] = ['value A ' + str(dict1.get(x1)), 'value B ' + str(dict2.get(x1))], False
                else:
                    result[x1] = ['value A ' + str(dict1.get(x1)), 'value B ' + str(dict2.get(x1))], True
            
            
    for x1 in dict2.keys():
        z = dict1.get(x1) == dict2.get(x1)
        if not z:
            print('key', x1)
            print('value A', dict1.get(x1), '\nvalue B', dict2.get(x1))
            print('-----\n')
            if x1 not in result:
                if dict1.get(x1) != dict2.get(x1):
                    result[x1] = ['value A ' + str(dict1.get(x1)), 'value B ' + str(dict2.get(x1))], False
                else:
                    result[x1] = ['value A ' + str(dict1.get(x1)), 'value B ' + str(dict2.get(x1))], True
                
    return result


if __name__ == "__main__":
    a, b = phonePriceCheck()
    print(compare_dict(a, b))
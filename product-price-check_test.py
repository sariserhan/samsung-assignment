import unittest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

class SamsungProductPriceTest(unittest.TestCase):
    
    def setUp(self):
        DRIVER_PATH = os.path.dirname(__file__) + "/chromedriver"        
        pageUrl = "https://www.samsung.com/us/mobile/phones/galaxy-z/?Flagship%20Series%20Name=Galaxy+Z&model_family=Galaxy+Z+Fold2+5G,Galaxy+Fold"        
        self.driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
        self.driver.get(pageUrl)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        product = soup.find_all(class_='ProductName-common-518700986 ProductName-title-3949175622')
        price = soup.find_all(class_='Product-card__price-current')
        phoneName = [i.string for i in product]
        phonePrice = ['$'+str(i).split('-->$')[1].split('<!--')[0] for i in price]
        self.phonePriceDict = dict(zip(phoneName,phonePrice))
        
        self.mockData = {}

        self.mockData['Galaxy Z Fold2 5G'] = '$1,449.99'
        self.mockData['Galaxy Fold 512GB'] = '$1,980.00'
        self.mockData['Galaxy S20 FE 5G'] = '$100000000'
                
    def test_WebPage(self):                                
        self.assertEqual('Samsung Galaxy Z - Phones | Samsung US', self.driver.title)
        self.assertEqual(self.mockData['Galaxy Z Fold2 5G'], self.phonePriceDict['Galaxy Z Fold2 5G'])
        self.assertEqual(self.mockData['Galaxy Fold 512GB'], self.phonePriceDict['Galaxy Fold 512GB'])

 
    # Closing the driver.
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
from selenium import webdriver

class Helper():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def get_element_by_xpath(self, page, xpath):
        driver.get(page)
        element = driver.find_element_by_xpath(xpath)
        return element
    
    def get_elements_by_xpath(self, page, xpath):
        driver.get(page)
        elements = driver.find_elements_by_xpath(xpath)
        return elements
    

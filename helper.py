from selenium import webdriver

class Helper():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def get_element_by_xpath(self, page, xpath):
        self.driver.get(page)
        element = self.driver.find_element_by_xpath(xpath)
        return element
    
    def get_elements_by_xpath(self, page, xpath):
        self.driver.get(page)
        elements = self.driver.find_elements_by_xpath(xpath)
        return elements
    
    def quit(self):
        self.driver.quit()
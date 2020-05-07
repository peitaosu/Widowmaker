class Helper():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def get_element_by_xpath(page, xpath):
        driver.get(page)
        element = driver.find_element_by_xpath(xpath)
        return element

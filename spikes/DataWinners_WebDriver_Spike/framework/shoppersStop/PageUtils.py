from framework.shoppersStop.Page import Page

__author__ = 'anandb'

class PerspectivesUtilities(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def getAllValidationErrors(self):
        validationErrors = self.driver.find_element_by_class_name("validationError").find_elements_by_tag_name("span")
        print "Validation Errors:"
        for eachError in validationErrors:
            print eachError.get_text()
        return [ eachError.get_text() for eachError in validationErrors ]

    def getValidationError(self):
        validationError = self.driver.find_element_by_class_name("validationError").find_element_by_tag_name("span").get_text()
        return validationError

    def getStatusByID(self, id):
        objectStatus = self.driver.find_element_by_id(id).is_enabled()
        return objectStatus

    def waitForElement(self):
        self.driver.wait(3000)
        return self

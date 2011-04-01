

__author__ = 'ravi'

from framework.mangrovetests.page import Page
from selenium.webdriver.common.by import By
from selenium.webdriver.common.exceptions import NoSuchElementException


class CommonUtilities(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def getAllValidationErrors(self):
        validationErrors = self.driver.find_element_by_class_name("emailError").find_elements_by_tag_name("span")
        print "Validation Errors:"
        for eachError in validationErrors:
            print eachError.get_text()
        return [ eachError.get_text() for eachError in validationErrors ]

    def getValidationError(self):
        validationError = self.driver.find_element_by_class_name("validationError").find_element_by_tag_name("span").get_text()
        return validationError

    def getEmailValidationErrorMessage(self, id):
        actualEmailValidationErrorMessage = self.driver.find_element_by_id(id).text
        return actualEmailValidationErrorMessage

    def getStatusByID(self, id):
        objectStatus = self.driver.find_element_by_id(id).is_enabled()
        return objectStatus

    def waitForElement(self, timeOutInSeconds, objectIDToBeFound):
        """Finds elements by their id by waiting till timeout."""
        import datetime
        currentTime = datetime.datetime.now()
        endTime = currentTime + datetime.timedelta(0,timeOutInSeconds)

        while currentTime < endTime:
            try:
                self.driver.find_element_by_id(objectIDToBeFound)
                print "Object", objectIDToBeFound, "is present."
                break
            except NoSuchElementException:
                currentTime = datetime.datetime.now()
        return self


    '''def addSecs(self):
        import datetime
        currentTime = datetime.datetime.now()
        endTime = currentTime + datetime.timedelta(0,3)
        return endTimeoptionToBeSelected'''

    def validateErrorMessage(self, errorElementID, expectedEmailValidationErrorMessage):
        actualValidationErrorMessage = self.driver.find_element_by_id(errorElementID).text
        if expectedEmailValidationErrorMessage == actualValidationErrorMessage:
            return True
        return False

    def findTextBoxAndEnterText(self, textBoxID, textToBeEntered):
        self.driver.find_element_by_id(textBoxID).send_keys(textToBeEntered)
        return self

    def findDropDownAndSelectOption(self, dropDownID, optionToBeSelected):
        self.driver.find_drop_down(dropDownID).set_selected(optionToBeSelected)
        return self
    
    def findElementAndClick(self, elementId):
         self.driver.find_element_by_id(elementId).click()
         return self

    def isElementPresent(self, elementLocator, by=By.ID):
        try:
            locator = self.driver.find_element(by,elementLocator)
            return locator
        except NoSuchElementException:
            return False

from framework.shoppersStop.Page import Page

__author__ = 'anandb'

class RegistrationPage (Page):

    def __init__(self, driver):
        Page.__init__(self, driver)


    def NoPasswordEnteredAndRegister(self):
        #self.driver.find_element_by_name('createAccountEmail').send_keys('sudheerbhai@mail.com')
        #self.EnterTextInTextBox('createAccountEmail', 'sudheerbhai@mail.com')
        self.driver.find_text_box("createAccountEmail").is_enabled()
        self.driver.find_text_box("createAccountEmail").enter_text("sudheerbahi@mail.com")

        self.driver.find_drop_down("salutation").set_selected("Mr.")


        self.driver.find_element_by_name('createAccountFirstName').send_keys('Sudheer')
        self.driver.find_element_by_name('createAccountLastName').send_keys('Bhai')
        self.driver.find_radio_button('gender_male').radio_button_status()
        self.driver.find_element_by_id('gender_male').select()
        #self.assertEqual(self.driver.find_radio_Button('gender_male').is_disabled(), "False", "The Male Gender RadioButton is disabled")
        birthMonthDropDown = self.driver.find_drop_down("birthMonth")
        birthMonthDropDown.set_selected("August")
    
        birthDateDropDown = self.driver.find_drop_down("birthDate")
        birthDateDropDown.set_selected("15")
        birthYearDropDown = self.driver.find_drop_down("birthYear")
        birthYearDropDown.set_selected("1947")

        self.driver.find_element_by_name('acceptTerms').set_selected()
        self.driver.find_element_by_class_name('button_style_2').click()
        return self


    def NoEmailEnteredAndRegister(self):
        salutationDropDown = self.driver.find_drop_down("salutation")
        salutationDropDown.set_selected("Mr.")
        self.driver.find_element_by_name('createAccountFirstName').send_keys('Sudheer')
        self.driver.find_element_by_name('createAccountLastName').send_keys('Bhai')
        self.driver.find_element_by_id('gender_male').select()

        birthMonthDropDown = self.driver.find_drop_down("birthMonth")
        birthMonthDropDown.set_selected("August")
        birthDateDropDown = self.driver.find_drop_down("birthDate")
        birthDateDropDown.set_selected("15")
        birthYearDropDown = self.driver.find_drop_down("birthYear")
        birthYearDropDown.set_selected("1947")

        self.driver.find_element_by_name('createAccountPassword').send_keys('rock1234')
        self.driver.find_element_by_name('createAccountConfirmPassword').send_keys('rock1234')

        #print salutationDropDown.get_options()
        #print salutationDropDown.get_selected()
        #print salutationDropDown.is_selected("Mrs.")
        #print salutationDropDown.get_selected()
        self.driver.find_element_by_name('acceptTerms').select()
        self.driver.find_element_by_class_name('button_style_2').click()
        return self

    def validateErrorMessagesContains(self, expectedErrorMessage):
        from PageUtils import PerspectivesUtilities
        actualValidationErrors = PerspectivesUtilities(self.driver).getAllValidationErrors()
        for eachError in actualValidationErrors:
            if expectedErrorMessage == eachError:
                return True
        return False

    def validateErrorMessage(self, expectedErrorMessage):
        from PageUtils import PerspectivesUtilities
        actualValidationError = PerspectivesUtilities(self.driver).getValidationError()
        if expectedErrorMessage == actualValidationError:
                return True
        return False

    def findRadioButtonAndValidateStatus(self, id, expectedRadioButtonStatus):
        from PageUtils import PerspectivesUtilities
        actualRadioButtonStatus = PerspectivesUtilities(self.driver).getStatusByID(id)
        print actualRadioButtonStatus
        if expectedRadioButtonStatus ==  actualRadioButtonStatus:
                return True
        return False



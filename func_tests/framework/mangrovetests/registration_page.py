from framework.mangrovetests.page import Page
from framework.utils.common_utils import CommonUtilities

__author__ = 'kumarr'


class RegistrationPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def get_title(self):
        """Fetch the title of the web page

        Return title of the web page
        """
        page_title = self.driver.title
        return page_title

    def enter_data_in_all_fields_and_click_register(self, organization_name,
                                                    organization_sector,
                                                    organization_addressline1,
                                                    organization_addressline2,
                                                    organization_city,
                                                    organization_state,
                                                    organization_country,
                                                    organization_zipcode,
                                                    organization_office_phone,
                                                    organization_website,
                                                    title,
                                                    first_name,
                                                    last_name,
                                                    email,
                                                    password,
                                                    confirm_password):
        self.driver.find_text_box_by_name_and_enter_text("organization_name", organization_name)
        self.driver.find_drop_down_by_name_and_select_option("organization_sector", organization_sector)
        self.driver.find_text_box_by_name_and_enter_text("id_organization_addressline1", organization_addressline1)
        self.driver.find_text_box_by_name_and_enter_text("id_organization_addressline1", organization_addressline2)
        self.driver.find_text_box_by_name_and_enter_text("organization_city", organization_city)
        self.driver.find_text_box_by_name_and_enter_text("organization_state", organization_state)
        self.driver.find_text_box_by_name_and_enter_text("organization_country", organization_country)
        self.driver.find_text_box_by_name_and_enter_text("organization_zipcode", organization_zipcode)
        self.driver.find_text_box_by_name_and_enter_text("organization_office_phone", organization_office_phone)
        self.driver.find_text_box_by_name_and_enter_text("organization_website", organization_website)
        self.driver.find_text_box_by_name_and_enter_text("title", title)
        self.driver.find_text_box_by_name_and_enter_text("first_name", first_name)
        self.driver.find_text_box_by_name_and_enter_text("last_name", last_name)
        self.driver.find_text_box_by_name_and_enter_text("password", password)
        self.driver.find_text_box_by_name_and_enter_text("email", email)
        self.driver.find_text_box_by_name_and_enter_text("confirm_password", confirm_password)
        self.driver.find_element_by_css_selector("input[value='Register']").click()
        return self
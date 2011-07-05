# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from pages.createprojectpage.create_project_page import CreateProjectPage
from pages.projectoverviewpage.project_overview_page import ProjectOverviewPage
from pages.projectspage.projects_locator import *
from pages.page import Page


class ProjectsPage(Page):

    def __init__(self, driver):
        Page.__init__(self, driver)

    def navigate_to_create_project_page(self):
        """
        Function to navigate to create project page of the website.

        Return create project page
         """
        self.driver.find(CREATE_A_NEW_PROJECT_LINK).click()
        return CreateProjectPage(self.driver)

    def navigate_to_project_page(self, project_name):
        """
        Function to navigate to specific project overview page

        Return project overview page
         """
        project_link = by_xpath(PROJECT_LINK_XPATH % project_name.lower())
        self.driver.find(project_link).click()
        return ProjectOverviewPage(self.driver)

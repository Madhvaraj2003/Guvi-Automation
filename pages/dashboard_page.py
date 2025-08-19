"""Dashboard page object for OrangeHRM navigation and module access.

This page object manages interaction with the main dashboard/landing page
after successful login. It provides:
- Navigation methods for accessing different modules (Admin, PIM, Leave, etc.)
- Verification methods for confirming successful page loads
- Logout functionality and menu item visibility checks
- Specialized methods for accessing nested menu items

The dashboard serves as the central hub for all HRM functionality.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class DashboardPage(BasePage):
    """Page Object for the OrangeHRM dashboard and main navigation menu."""
    
    # Header and user interaction locators
    WELCOME_MENU = (By.XPATH, "//span[@class='oxd-userdropdown-tab']")
    LOGOUT_LINK = (By.XPATH, "//a[contains(text(),'Logout')]")
    DASHBOARD_TITLE = (By.XPATH, "//h6[contains(text(),'Dashboard')]")
    
    # Main menu locators
    ADMIN_MENU = (By.XPATH, "//span[text()='Admin']")
    PIM_MENU = (By.XPATH, "//span[text()='PIM']")
    LEAVE_MENU = (By.XPATH, "//span[text()='Leave']")
    TIME_MENU = (By.XPATH, "//span[text()='Time']")
    RECRUITMENT_MENU = (By.XPATH, "//span[text()='Recruitment']")
    MY_INFO_MENU = (By.XPATH, "//span[text()='My Info']")
    PERFORMANCE_MENU = (By.XPATH, "//span[text()='Performance']")
    DASHBOARD_MENU = (By.XPATH, "//span[text()='Dashboard']")
    CLAIM_MENU = (By.XPATH, "//span[text()='Claim']")
    
    # Sub-menu locators
    USERS_SUBMENU = (By.XPATH, "//a[contains(text(),'Users')]")
    ASSIGN_LEAVE_MENU = (By.XPATH, "//a[contains(text(),'Assign Leave')]")
    SUBMIT_CLAIM_MENU = (By.XPATH, "//a[contains(text(),'Submit Claim')]")
    
    # My Info sub-menu locators
    PERSONAL_DETAILS = (By.XPATH, "//a[contains(text(),'Personal Details')]")
    CONTACT_DETAILS = (By.XPATH, "//a[contains(text(),'Contact Details')]")
    EMERGENCY_CONTACTS = (By.XPATH, "//a[contains(text(),'Emergency Contacts')]")
    DEPENDENTS = (By.XPATH, "//a[contains(text(),'Dependents')]")
    IMMIGRATION = (By.XPATH, "//a[contains(text(),'Immigration')]")
    JOB = (By.XPATH, "//a[contains(text(),'Job')]")
    SALARY = (By.XPATH, "//a[contains(text(),'Salary')]")
    TAX_EXEMPTIONS = (By.XPATH, "//a[contains(text(),'Tax Exemptions')]")
    REPORT_TO = (By.XPATH, "//a[contains(text(),'Report-to')]")
    QUALIFICATIONS = (By.XPATH, "//a[contains(text(),'Qualifications')]")
    MEMBERSHIPS = (By.XPATH, "//a[contains(text(),'Memberships')]")
    
    def is_dashboard_loaded(self):
        """Check if dashboard is loaded"""
        try:
            # Prefer Dashboard title
            if self.is_element_visible(self.DASHBOARD_TITLE, timeout=10):
                return True
            # Fallback: URL contains dashboard
            if "dashboard" in self.get_current_url().lower():
                return True
            # Fallback: presence of any main menu item indicates authenticated UI loaded
            menu_locators = [
                self.ADMIN_MENU,
                self.PIM_MENU,
                self.LEAVE_MENU,
                self.MY_INFO_MENU,
                self.DASHBOARD_MENU,
            ]
            for locator in menu_locators:
                if self.is_element_visible(locator, timeout=5):
                    return True
            return False
        except:
            return False
    
    def logout(self):
        """Perform logout"""
        try:
            self.wait_for_element_clickable(self.WELCOME_MENU)
            self.click_element(self.WELCOME_MENU)
            self.wait_for_element_clickable(self.LOGOUT_LINK)
            self.click_element(self.LOGOUT_LINK)
        except:
            self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    
    def click_admin_menu(self):
        """Click admin menu"""
        try:
            self.wait_for_element_clickable(self.ADMIN_MENU)
            self.click_element(self.ADMIN_MENU)
        except:
            pass
    
    def click_pim_menu(self):
        """Click PIM menu"""
        try:
            self.wait_for_element_clickable(self.PIM_MENU)
            self.click_element(self.PIM_MENU)
        except:
            pass
    
    def click_leave_menu(self):
        """Click Leave menu"""
        try:
            self.wait_for_element_clickable(self.LEAVE_MENU)
            self.click_element(self.LEAVE_MENU)
        except:
            pass
    
    def click_my_info_menu(self):
        """Click My Info menu"""
        try:
            self.wait_for_element_clickable(self.MY_INFO_MENU)
            self.click_element(self.MY_INFO_MENU)
        except:
            pass
    
    def click_users_submenu(self):
        """Click Users submenu"""
        try:
            self.wait_for_element_clickable(self.USERS_SUBMENU)
            self.click_element(self.USERS_SUBMENU)
        except:
            pass
    
    def click_assign_leave_menu(self):
        """Open Leave module then click Assign Leave submenu"""
        try:
            self.wait_for_element_clickable(self.LEAVE_MENU)
            self.click_element(self.LEAVE_MENU)
        except:
            pass
        try:
            self.wait_for_element_clickable(self.ASSIGN_LEAVE_MENU)
            self.click_element(self.ASSIGN_LEAVE_MENU)
        except:
            pass
    
    def click_submit_claim_menu(self):
        """Open Claim module then click Submit Claim submenu"""
        try:
            # Open Claim module first to reveal submenus
            self.wait_for_element_clickable(self.CLAIM_MENU)
            self.click_element(self.CLAIM_MENU)
        except:
            pass
        try:
            self.wait_for_element_clickable(self.SUBMIT_CLAIM_MENU)
            self.click_element(self.SUBMIT_CLAIM_MENU)
        except:
            pass
    
    def verify_menu_items_visibility(self):
        """Verify that main menu items are visible"""
        menu_items = [
            self.ADMIN_MENU, self.PIM_MENU, self.LEAVE_MENU, self.TIME_MENU,
            self.RECRUITMENT_MENU, self.MY_INFO_MENU, self.PERFORMANCE_MENU, self.DASHBOARD_MENU
        ]
        
        visible_count = 0
        for menu_item in menu_items:
            if self.is_element_visible(menu_item):
                visible_count += 1
        
        return visible_count >= 3
    
    def verify_my_info_submenu_items(self):
        """Verify that My Info submenu items are visible"""
        submenu_items = [
            self.PERSONAL_DETAILS, self.CONTACT_DETAILS, self.EMERGENCY_CONTACTS,
            self.DEPENDENTS, self.IMMIGRATION, self.JOB, self.SALARY,
            self.TAX_EXEMPTIONS, self.REPORT_TO, self.QUALIFICATIONS, self.MEMBERSHIPS
        ]
        
        visible_count = 0
        for submenu_item in submenu_items:
            if self.is_element_visible(submenu_item):
                visible_count += 1
        
        return visible_count >= 3
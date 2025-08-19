from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class LeavePage:
    """Minimal POM for Assign Leave + Leave List with popup handling and verification."""
    def __init__(self, driver, timeout: int = 15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ===== Core locators (kept to your style) =====
    _menu_leave = (By.XPATH, "//span[normalize-space()='Leave']/ancestor::a")
    _lnk_assign_leave = (By.XPATH, "//a[contains(. , 'Assign Leave')]")
    _lnk_leave_list  = (By.XPATH, "//a[contains(@href,'viewLeaveList')]")

    # Assign Leave form
    _inp_employee = (By.XPATH, "//input[@placeholder='Type for hints...']")
    _opt_autocomplete = (By.XPATH, "//div[contains(@class,'oxd-autocomplete-option')]//span")
    _dd_leave_type = (By.XPATH, "(//div[contains(@class,'oxd-select-text-input')])[1]")
    _opt_leave_type_items = (By.XPATH, "//div[@role='option']//span")
    _inp_from_date = (By.XPATH, "(//input[@placeholder='yyyy-dd-mm'])[1]")
    _inp_to_date   = (By.XPATH, "(//input[@placeholder='yyyy-dd-mm'])[1]")
    _txt_comment   = (By.XPATH, "//textarea")
    _btn_submit    = (By.XPATH, "//button[@type='submit']")
    _btn_ok        = (By.XPATH, "//button[normalize-space()='Ok']")
    _toast_success = (By.XPATH, "//div[contains(@class,'oxd-toast--success') or contains(@class,'oxd-toast-content--success')]")

    # Leave List (filters)
    _flt_employee = (By.XPATH, "//input[@placeholder='Type for hints...']")
    _flt_from     = (By.XPATH, "//input[@placeholder= 'yyyy-dd-mm' ][1]")
    _flt_to       = (By.XPATH, "//input[@placeholder= 'yyyy-dd-mm' ][1]")
    _flt_status  = (By.XPATH, "//div[@class = 'oxd-select-text-input']")
    _btn_search   = (By.XPATH, "//button[@type='submit']")
    _tbl_rows     = (By.XPATH, "//div[@role='table']//div[@role='row']")

    # ===== Navigation =====
    def open_leave_module(self):
        self.wait.until(EC.element_to_be_clickable(self._menu_leave)).click()
        # land usually on Leave List; just wait for either tab link to exist
        try:
            self.wait.until(EC.presence_of_element_located(self._lnk_leave_list))
        except TimeoutException:
            pass

    def go_to_assign_leave(self):
        self.open_leave_module()
        # try tab/link; if not found fast, direct URL fallback
        try:
            self.wait.until(EC.element_to_be_clickable(self._lnk_assign_leave)).click()
        except TimeoutException:
            self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/leave/assignLeave")
        # form guard
        self.wait.until(EC.presence_of_element_located(self._inp_employee))

    def go_to_leave_list(self):
        self.open_leave_module()
        try:
            self.wait.until(EC.element_to_be_clickable(self._lnk_leave_list)).click()
        except TimeoutException:
            self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/leave/viewLeaveList")
        # filter guard
        self.wait.until(EC.presence_of_element_located(self._flt_employee))

    # ===== Helpers =====
    def _type_and_select_autocomplete(self, locator, value):
        el = self.wait.until(EC.element_to_be_clickable(locator))
        el.click()
        el.send_keys(Keys.CONTROL, "a")
        el.send_keys(value)
        # pick first matching suggestion (or first available)
        try:
            options = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located(self._opt_autocomplete)
            )
            # prefer contains match
            target = None
            low = value.strip().lower()
            for op in options:
                try:
                    if low in op.text.strip().lower():
                        target = op; break
                except Exception:
                    continue
            (target or options[0]).click()
        except TimeoutException:
            # if no suggestions, assume exact text is acceptable
            pass

    def _select_from_dropdown(self, trigger_locator, expected_text: str):
        self.wait.until(EC.element_to_be_clickable(trigger_locator)).click()
        items = self.wait.until(EC.presence_of_all_elements_located(self._opt_leave_type_items))
        # prefer exact case-insensitive, then contains
        low = expected_text.strip().lower()
        pick = None
        for it in items:
            if it.text.strip().lower() == low:
                pick = it; break
        if pick is None:
            for it in items:
                if low in it.text.strip().lower():
                    pick = it; break
        (pick or items[0]).click()

    def _set_date(self, locator, value):
        box = self.wait.until(EC.element_to_be_clickable(locator))
        box.click()
        box.send_keys(Keys.CONTROL, "a")
        box.send_keys(value)
        box.send_keys(Keys.ENTER)

    # ===== Main flows =====
    def fill_and_submit_assign_leave(self, employee_name: str, leave_type: str,
                                     from_date: str, to_date: str, comment: str = "Automated"):
        # Employee
        self._type_and_select_autocomplete(self._inp_employee, employee_name)
        # Leave Type
        self._select_from_dropdown(self._dd_leave_type, leave_type)
        # Dates (yyyy-mm-dd)
        self._set_date(self._inp_from_date, from_date)
        self._set_date(self._inp_to_date, to_date)
        # Comment
        self.wait.until(EC.element_to_be_clickable(self._txt_comment)).clear()
        self.driver.find_element(*self._txt_comment).send_keys(comment)
        # Submit
        self.wait.until(EC.element_to_be_clickable(self._btn_submit)).click()
        # Optional confirmation
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self._btn_ok)).click()
        except TimeoutException:
            pass
        # Success toast
        toast = self.wait.until(EC.visibility_of_element_located(self._toast_success))
        return toast.text.strip()

    def search_in_leave_list(self, employee_name, from_date, to_date, leave_status="Scheduled"):
        self.go_to_leave_list()
        # Employee filter
        self._type_and_select_autocomplete(self._flt_employee, employee_name,)
        # Date range
        self._set_date(self._flt_from, from_date)
        self._set_date(self._flt_to, to_date)
        self._select_from_dropdown(self._flt_status, leave_status)
        
        # Search
        self.wait.until(EC.element_to_be_clickable(self._btn_search)).click()
        # Results
        self.wait.until(EC.presence_of_element_located(self._tbl_rows))
        rows = self.driver.find_elements(*self._tbl_rows)
        # first row is header usually
        body_rows = rows[1:] if len(rows) > 1 else []
        body_texts = [r.text.lower() for r in body_rows]
        return {
            "rows_count": len(body_rows),
            "has_employee": any(employee_name.lower() in t for t in body_texts)
        }

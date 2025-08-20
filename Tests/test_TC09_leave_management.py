import pytest
from pages.leave_page import LeavePage
import time

@pytest.mark.usefixtures("logged_in_session")
class TestAssignLeave:
    def test_assign_leave_and_verify(self, logged_in_session):
        """
        TC09: Assign leave to an employee and verify in Leave List.
        - Navigate to Leave -> Assign Leave
        - Fill Employee, Leave Type, From/To Dates, Comment
        - Submit, handle popup (Ok)
        - Verify success toast
        - Go to Leave List, filter and verify record appears
        """
        driver, _, _ = logged_in_session
        leave = LeavePage(driver)

        # --- Data (use valid employee + yyyy-dd-mm dates) ---
        employee_name = "sww test"          # use a real, suggestible name from your instance
        leave_type     = "CAN - Bereavement"      
        from_date      = "2025-25-09"
        to_date        = "2025-26-09"
        comment        = "Test comment for automation"

        # 1) Navigate & assign
        leave.go_to_assign_leave()
        toast_text = leave.fill_and_submit_assign_leave(
            employee_name, leave_type, from_date, to_date, comment
        )

        # 2) Validate success message
        assert "success" in toast_text.lower() or "assigned" in toast_text.lower(), \
            f"Expected success toast, got: {toast_text}"

        # 3) Verify in Leave List
        Results = leave.search_in_leave_list(employee_name, from_date, to_date, leave_status="Scheduled")
        assert len(Results) == 2, f"Expected two result, found {len(Results)}"
        print("Test passed")
        time.sleep(8)

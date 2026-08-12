"""
class Branch:
    def __init__(self, branch_code, location, manager_id):
        self.branch_code = branch_code
        self.location = location
        self.manager_id = manager_id
        self.staff = []

    def add_staff(self, staff_member):
        self.staff.append(staff_member)

    def __str__(self):
        return f"Branch {self.branch_code} ({self.location}), staff: {len(self.staff)}"

        """
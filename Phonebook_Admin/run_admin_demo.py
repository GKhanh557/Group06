import tkinter as tk
from admin_view import AdminScreen
from contact_service import ContactService
from group_service import GroupService
from user_service import UserService


class DummyUser:

    def __init__(self):
        self.username = "Thien (Admin)"
        self.role = "admin"


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Phone Book Management System - Admin Test")
    root.geometry("900x550")

    user_service = UserService()
    contact_service = ContactService()
    group_service = GroupService()

    app = AdminScreen(
        parent=root,
        controller=None,
        admin_user=DummyUser(),
        user_service=user_service,
        contact_service=contact_service,
        group_service=group_service,
    )
    app.pack(fill="both", expand=True)

    root.mainloop()
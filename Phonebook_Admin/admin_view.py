from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk


class AdminScreen(tk.Frame):

    def __init__(
        self,
        parent,
        controller,
        admin_user,
        user_service,
        contact_service,
        group_service,
    ):
        super().__init__(parent)
        self.controller = controller
        self.admin_user = admin_user
        self.user_service = user_service
        self.contact_service = contact_service
        self.group_service = group_service

        self.configure(bg="#F5F5F5")
        self.create_header()

        main_container = tk.Frame(self, bg="#F5F5F5")
        main_container.pack(fill="both", expand=True, padx=20, pady=15)

        self.create_stats_panel(main_container)
        self.create_user_management_panel(main_container)

    def create_header(self):
        header_frame = tk.Frame(self, bg="#1E1E1E", height=50)
        header_frame.pack(fill="x", side="top")

        title_label = tk.Label(
            header_frame,
            text="PHONE BOOK - ADMIN DASHBOARD",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#1E1E1E",
        )
        title_label.pack(side="left", padx=15, pady=10)

        signout_btn = tk.Button(
            header_frame,
            text="SIGN OUT",
            command=self.logout,
            bg="#333333",
            fg="white",
            relief="flat",
        )
        signout_btn.pack(side="right", padx=15, pady=8)

        badge_label = tk.Label(
            header_frame,
            text="ADMIN",
            font=("Arial", 9, "bold"),
            bg="#D9534F",
            fg="white",
            padx=6,
            pady=2,
        )
        badge_label.pack(side="right", padx=5, pady=10)

        admin_username = (
            getattr(self.admin_user, "username", str(self.admin_user))
            if self.admin_user
            else "Admin"
        )
        admin_info = tk.Label(
            header_frame,
            text=f"A  {admin_username}",
            font=("Arial", 10),
            fg="white",
            bg="#1E1E1E",
        )
        admin_info.pack(side="right", padx=10, pady=10)

    def get_users_list(self):
        """Lấy dữ liệu linh hoạt từ database hỗ trợ Object, Dict và Tuple"""
        if self.user_service and hasattr(self.user_service, "get_all_users"):
            try:
                users = self.user_service.get_all_users()
                formatted_users = []
                for u in users:
                    if isinstance(u, dict):
                        formatted_users.append(u)
                    elif isinstance(u, (list, tuple)):
                        # Trường hợp lấy dữ liệu dạng Tuple từ cursor.fetchall()
                        formatted_users.append({
                            "user_id": u[0],
                            "username": u[1],
                            "email": u[2] if len(u) > 2 else "",
                            "role": u[3] if len(u) > 3 else "user",
                            "is_locked": (
                                bool(u[4])
                                if len(u) > 4
                                else (bool(u[5]) if len(u) > 5 else False)
                            ),
                        })
                    else:
                        formatted_users.append({
                            "user_id": getattr(
                                u, "user_id", getattr(u, "id", None)
                            ),
                            "username": getattr(u, "username", ""),
                            "email": getattr(u, "email", ""),
                            "role": getattr(u, "role", "user"),
                            "is_locked": getattr(u, "is_locked", False),
                        })
                return formatted_users
            except Exception as e:
                messagebox.showerror("Error", f"Failed to fetch users: {e}")
                return []
        return []

    def create_stats_panel(self, parent):
        stats_frame = tk.LabelFrame(
            parent,
            text=" System Statistics ",
            font=("Arial", 11, "bold"),
            bg="white",
            padx=15,
            pady=15,
        )
        stats_frame.pack(side="left", fill="y", padx=(0, 10))

        users = self.get_users_list()
        total_users = len(users)
        locked_users = sum(1 for u in users if u.get("is_locked", False))

        total_contacts = 0
        if self.contact_service and hasattr(
            self.contact_service, "get_total_contacts"
        ):
            total_contacts = self.contact_service.get_total_contacts()

        total_groups = 0
        if self.group_service and hasattr(
            self.group_service, "get_total_groups"
        ):
            total_groups = self.group_service.get_total_groups()

        recent_contacts = 0
        if self.contact_service and hasattr(
            self.contact_service, "get_recent_contacts_count"
        ):
            recent_contacts = (
                self.contact_service.get_recent_contacts_count()
            )

        self.lbl_users = tk.Label(
            stats_frame,
            text=f"Total Users: {total_users}",
            font=("Arial", 10),
            bg="white",
            anchor="w",
        )
        self.lbl_users.pack(fill="x", pady=5)

        self.lbl_locked = tk.Label(
            stats_frame,
            text=f"Locked Users: {locked_users}",
            font=("Arial", 10, "bold"),
            fg="#D9534F",
            bg="white",
            anchor="w",
        )
        self.lbl_locked.pack(fill="x", pady=5)

        self.lbl_contacts = tk.Label(
            stats_frame,
            text=f"Total Contacts: {total_contacts}",
            font=("Arial", 10),
            bg="white",
            anchor="w",
        )
        self.lbl_contacts.pack(fill="x", pady=5)

        self.lbl_groups = tk.Label(
            stats_frame,
            text=f"Total Groups: {total_groups}",
            font=("Arial", 10),
            bg="white",
            anchor="w",
        )
        self.lbl_groups.pack(fill="x", pady=5)

        self.lbl_recent = tk.Label(
            stats_frame,
            text=f"Recent Contacts (7d): {recent_contacts}",
            font=("Arial", 10),
            fg="#0275D8",
            bg="white",
            anchor="w",
        )
        self.lbl_recent.pack(fill="x", pady=5)

        btn_refresh = tk.Button(
            stats_frame,
            text="Refresh Stats",
            command=self.refresh_data,
            bg="#0275D8",
            fg="white",
            relief="flat",
        )
        btn_refresh.pack(fill="x", pady=(15, 0))

    def create_user_management_panel(self, parent):
        user_frame = tk.LabelFrame(
            parent,
            text=" User Account Management ",
            font=("Arial", 11, "bold"),
            bg="white",
            padx=15,
            pady=15,
        )
        user_frame.pack(side="right", fill="both", expand=True)

        top_bar = tk.Frame(user_frame, bg="white")
        top_bar.pack(fill="x", pady=(0, 10))

        tk.Label(
            top_bar, text="Search:", font=("Arial", 10, "bold"), bg="white"
        ).pack(side="left", padx=(0, 5))
        self.search_entry = tk.Entry(top_bar, width=20)
        self.search_entry.pack(side="left", padx=(0, 15))
        self.search_entry.bind(
            "<KeyRelease>", lambda e: self.load_users_to_tree()
        )

        tk.Label(
            top_bar, text="Filter:", font=("Arial", 10, "bold"), bg="white"
        ).pack(side="left", padx=(0, 5))
        self.filter_var = tk.StringVar(value="All")
        cmb_filter = ttk.Combobox(
            top_bar,
            textvariable=self.filter_var,
            values=["All", "Locked Only", "Active Only"],
            state="readonly",
            width=12,
        )
        cmb_filter.pack(side="left")
        cmb_filter.bind(
            "<<ComboboxSelected>>", lambda e: self.load_users_to_tree()
        )

        columns = ("user_id", "username", "email", "role", "is_locked")
        self.tree = ttk.Treeview(
            user_frame, columns=columns, show="headings", height=10
        )

        self.tree.heading("user_id", text="User ID")
        self.tree.heading("username", text="Username")
        self.tree.heading("email", text="Email")
        self.tree.heading("role", text="Role")
        self.tree.heading("is_locked", text="Is Locked")

        self.tree.column("user_id", width=60, anchor="center")
        self.tree.column("username", width=120)
        self.tree.column("email", width=180)
        self.tree.column("role", width=80, anchor="center")
        self.tree.column("is_locked", width=80, anchor="center")

        self.tree.pack(fill="both", expand=True, pady=(0, 10))

        btn_action_frame = tk.Frame(user_frame, bg="white")
        btn_action_frame.pack(fill="x")

        add_btn = tk.Button(
            btn_action_frame,
            text="Add User",
            command=self.add_user,
            bg="#0275D8",
            fg="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            padx=8,
        )
        add_btn.pack(side="left", padx=(0, 5))

        edit_btn = tk.Button(
            btn_action_frame,
            text="Edit User",
            command=self.edit_user,
            bg="#F0AD4E",
            fg="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            padx=8,
        )
        edit_btn.pack(side="left", padx=(0, 5))

        del_btn = tk.Button(
            btn_action_frame,
            text="Delete User",
            command=self.delete_user,
            bg="#D9534F",
            fg="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            padx=8,
        )
        del_btn.pack(side="left", padx=(0, 15))

        lock_btn = tk.Button(
            btn_action_frame,
            text="Lock Account",
            command=self.lock_selected_user,
            bg="#D9534F",
            fg="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            padx=8,
        )
        lock_btn.pack(side="left", padx=(0, 5))

        unlock_btn = tk.Button(
            btn_action_frame,
            text="Unlock Account",
            command=self.unlock_selected_user,
            bg="#5CB85C",
            fg="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            padx=8,
        )
        unlock_btn.pack(side="left")

        self.load_users_to_tree()

    def load_users_to_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        users = self.get_users_list()
        filter_mode = self.filter_var.get()
        search_query = self.search_entry.get().strip().lower()

        for u in users:
            is_locked = u.get("is_locked", False)
            username = str(u.get("username", "")).lower()
            email = str(u.get("email", "")).lower()

            if search_query and (
                search_query not in username and search_query not in email
            ):
                continue

            if filter_mode == "Locked Only" and not is_locked:
                continue
            if filter_mode == "Active Only" and is_locked:
                continue

            self.tree.insert(
                "",
                "end",
                values=(
                    u["user_id"],
                    u["username"],
                    u["email"],
                    u["role"],
                    is_locked,
                ),
            )

    def add_user(self):
        dialog = tk.Toplevel(self)
        dialog.title("Add New User")
        dialog.geometry("300x250")

        tk.Label(dialog, text="Username:").pack(pady=(10, 2))
        ent_username = tk.Entry(dialog)
        ent_username.pack()

        tk.Label(dialog, text="Email:").pack(pady=(5, 2))
        ent_email = tk.Entry(dialog)
        ent_email.pack()

        tk.Label(dialog, text="Password:").pack(pady=(5, 2))
        ent_password = tk.Entry(dialog, show="*")
        ent_password.pack()

        def save():
            uname = ent_username.get().strip()
            email = ent_email.get().strip()
            pwd = ent_password.get().strip()

            if not uname or not email or not pwd:
                messagebox.showwarning(
                    "Warning", "Please enter all fields!", parent=dialog
                )
                return

            if self.user_service:
                # Thử gọi hàm register / create_user / add_user tùy theo cấu trúc của user_service
                success = False
                if hasattr(self.user_service, "register_user"):
                    success = self.user_service.register_user(uname, email, pwd)
                elif hasattr(self.user_service, "add_user"):
                    try:
                        success = self.user_service.add_user(
                            username=uname, email=email, password=pwd
                        )
                    except TypeError:
                        success = self.user_service.add_user(
                            uname, email, pwd
                        )

                if success:
                    messagebox.showinfo(
                        "Success",
                        f"User '{uname}' added successfully!",
                        parent=dialog,
                    )
                    dialog.destroy()
                    self.refresh_data()
                else:
                    messagebox.showerror(
                        "Error", "Failed to add user to database!", parent=dialog
                    )
            else:
                messagebox.showerror(
                    "Error", "User service is not available!", parent=dialog
                )

        tk.Button(
            dialog,
            text="Save",
            command=save,
            bg="#5CB85C",
            fg="white",
            relief="flat",
        ).pack(pady=15)

    def edit_user(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a user to edit!")
            return

        user_values = self.tree.item(selected_item[0], "values")
        user_id = int(user_values[0])

        dialog = tk.Toplevel(self)
        dialog.title("Edit User")
        dialog.geometry("300x200")

        tk.Label(dialog, text="Username:").pack(pady=(10, 2))
        ent_username = tk.Entry(dialog)
        ent_username.insert(0, user_values[1])
        ent_username.pack()

        tk.Label(dialog, text="Email:").pack(pady=(5, 2))
        ent_email = tk.Entry(dialog)
        ent_email.insert(0, user_values[2])
        ent_email.pack()

        def save_changes():
            new_uname = ent_username.get().strip()
            new_email = ent_email.get().strip()

            if self.user_service and hasattr(self.user_service, "update_user"):
                success = self.user_service.update_user(
                    user_id=user_id, username=new_uname, email=new_email
                )
                if success:
                    messagebox.showinfo(
                        "Success", "User details updated!", parent=dialog
                    )
                    dialog.destroy()
                    self.refresh_data()
                else:
                    messagebox.showerror(
                        "Error", "Failed to update user in database!", parent=dialog
                    )
            else:
                messagebox.showerror(
                    "Error", "User service is not available!", parent=dialog
                )

        tk.Button(
            dialog,
            text="Update",
            command=save_changes,
            bg="#0275D8",
            fg="white",
            relief="flat",
        ).pack(pady=15)

    def delete_user(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a user to delete!")
            return

        user_values = self.tree.item(selected_item[0], "values")
        user_id, username = int(user_values[0]), user_values[1]

        if messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete user '{username}'?",
        ):
            if self.user_service and hasattr(self.user_service, "delete_user"):
                success = self.user_service.delete_user(user_id)
                if success:
                    messagebox.showinfo(
                        "Success", f"User '{username}' has been deleted."
                    )
                    self.refresh_data()
                else:
                    messagebox.showerror(
                        "Error", "Failed to delete user from database!"
                    )
            else:
                messagebox.showerror("Error", "User service is not available!")

    def lock_selected_user(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a user to lock!")
            return

        user_values = self.tree.item(selected_item[0], "values")
        user_id, username, is_locked_str = (
            int(user_values[0]),
            user_values[1],
            str(user_values[4]),
        )

        if is_locked_str == "True":
            messagebox.showinfo(
                "Notice", f"Account '{username}' is ALREADY locked!"
            )
            return

        if messagebox.askyesno(
            "Confirm Lock",
            f"Are you sure you want to lock account '{username}'?",
        ):
            if self.user_service and hasattr(self.user_service, "lock_user"):
                success = self.user_service.lock_user(user_id)
                if success:
                    messagebox.showinfo(
                        "Success",
                        f"Account '{username}' has been locked successfully.",
                    )
                    self.refresh_data()
                else:
                    messagebox.showerror(
                        "Error", "Failed to lock account in database!"
                    )
            else:
                messagebox.showerror("Error", "User service is not available!")

    def unlock_selected_user(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a user to unlock!")
            return

        user_values = self.tree.item(selected_item[0], "values")
        user_id, username, is_locked_str = (
            int(user_values[0]),
            user_values[1],
            str(user_values[4]),
        )

        if is_locked_str == "False":
            messagebox.showinfo(
                "Notice", f"Account '{username}' is NOT locked yet!"
            )
            return

        if messagebox.askyesno(
            "Confirm Unlock",
            f"Are you sure you want to unlock account '{username}'?",
        ):
            if self.user_service and hasattr(self.user_service, "unlock_user"):
                success = self.user_service.unlock_user(user_id)
                if success:
                    messagebox.showinfo(
                        "Success",
                        f"Account '{username}' has been unlocked successfully.",
                    )
                    self.refresh_data()
                else:
                    messagebox.showerror(
                        "Error", "Failed to unlock account in database!"
                    )
            else:
                messagebox.showerror("Error", "User service is not available!")

    def refresh_data(self):
        users = self.get_users_list()
        total_users = len(users)
        locked_users = sum(1 for u in users if u.get("is_locked", False))

        total_contacts = 0
        if self.contact_service and hasattr(
            self.contact_service, "get_total_contacts"
        ):
            total_contacts = self.contact_service.get_total_contacts()

        total_groups = 0
        if self.group_service and hasattr(
            self.group_service, "get_total_groups"
        ):
            total_groups = self.group_service.get_total_groups()

        recent_contacts = 0
        if self.contact_service and hasattr(
            self.contact_service, "get_recent_contacts_count"
        ):
            recent_contacts = (
                self.contact_service.get_recent_contacts_count()
            )

        self.lbl_users.config(text=f"Total Users: {total_users}")
        self.lbl_locked.config(text=f"Locked Users: {locked_users}")
        self.lbl_contacts.config(text=f"Total Contacts: {total_contacts}")
        self.lbl_groups.config(text=f"Total Groups: {total_groups}")
        self.lbl_recent.config(text=f"Recent Contacts (7d): {recent_contacts}")

        self.load_users_to_tree()

    def logout(self):
        if hasattr(self.controller, "show_frame"):
            self.controller.show_frame("LoginScreen")
        else:
            self.destroy()
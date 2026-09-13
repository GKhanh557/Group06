"""
contact.py

The Contact class handles everything related to one contact:
add, edit, delete, and search.
"""

import re
from models.database import get_connection

# A valid phone number must be 9 to 11 digits, nothing else.
PHONE_PATTERN = re.compile(r"^\d{9,11}$")


class Contact:

    @staticmethod
    def is_valid_phone(phone_number):
        """Check the phone number format (used before saving)."""
        return bool(PHONE_PATTERN.match(phone_number))

    @staticmethod
    def add_contact(full_name, phone_number, user_id, email="", address="", note="", group_id=None):
        """FR4: add a new contact for the given user."""
        full_name = full_name.strip()
        phone_number = phone_number.strip()

        if full_name == "":
            return False, "Full name cannot be empty."
        if not Contact.is_valid_phone(phone_number):
            return False, "Phone number must be 9-11 digits."

        conn = get_connection()
        cursor = conn.cursor()

        # Check for a duplicate phone number for this same user
        cursor.execute(
            "SELECT * FROM Contact WHERE phone_number = ? AND user_id = ?",
            (phone_number, user_id),
        )
        if cursor.fetchone() is not None:
            conn.close()
            return False, "This phone number already exists in your contact list."

        cursor.execute(
            """INSERT INTO Contact (full_name, phone_number, email, address, note, group_id, user_id)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (full_name, phone_number, email, address, note, group_id, user_id),
        )
        conn.commit()
        conn.close()
        return True, "Contact added successfully."

    @staticmethod
    def edit_contact(contact_id, user_id, full_name, phone_number, email, address, note, group_id):
        """FR7: edit an existing contact."""
        if not Contact.is_valid_phone(phone_number):
            return False, "Phone number must be 9-11 digits."

        conn = get_connection()
        cursor = conn.cursor()

        # Make sure the new phone number is not used by ANOTHER contact of this user
        cursor.execute(
            "SELECT * FROM Contact WHERE phone_number = ? AND user_id = ? AND contact_id != ?",
            (phone_number, user_id, contact_id),
        )
        if cursor.fetchone() is not None:
            conn.close()
            return False, "This phone number already exists in your contact list."

        cursor.execute(
            """UPDATE Contact SET full_name = ?, phone_number = ?, email = ?,
               address = ?, note = ?, group_id = ?
               WHERE contact_id = ? AND user_id = ?""",
            (full_name, phone_number, email, address, note, group_id, contact_id, user_id),
        )
        conn.commit()
        updated = cursor.rowcount > 0
        conn.close()

        if not updated:
            return False, "Contact not found."
        return True, "Contact updated successfully."

    @staticmethod
    def delete_contact(contact_id, user_id):
        """FR8: delete a contact."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Contact WHERE contact_id = ? AND user_id = ?", (contact_id, user_id))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted

    @staticmethod
    def toggle_favorite(contact_id, user_id):
        """FR10: mark/unmark a contact as favorite."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Contact SET is_favorite = 1 - is_favorite WHERE contact_id = ? AND user_id = ?",
            (contact_id, user_id),
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_contacts(user_id):
        """FR5: list all contacts belonging to this user."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT c.*, g.group_name FROM Contact c
               LEFT JOIN Groups g ON c.group_id = g.group_id
               WHERE c.user_id = ? ORDER BY c.full_name""",
            (user_id,),
        )
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def search_contact(user_id, keyword):
        """FR6: search contacts by name or phone number."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT c.*, g.group_name FROM Contact c
               LEFT JOIN Groups g ON c.group_id = g.group_id
               WHERE c.user_id = ? AND (c.full_name LIKE ? OR c.phone_number LIKE ?)
               ORDER BY c.full_name""",
            (user_id, "%" + keyword + "%", "%" + keyword + "%"),
        )
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def export_to_csv(user_id, filepath):
        """FR16: save all contacts of this user into a CSV file."""
        import csv
        contacts = Contact.get_all_contacts(user_id)
        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["full_name", "phone_number", "email", "address", "note"])
            for c in contacts:
                writer.writerow([c["full_name"], c["phone_number"], c["email"], c["address"], c["note"]])
        return len(contacts)

    @staticmethod
    def import_from_csv(user_id, filepath):
        """FR15: read contacts from a CSV file and add them."""
        import csv
        imported = 0
        skipped = 0
        with open(filepath, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                success, _ = Contact.add_contact(
                    full_name=row.get("full_name", ""),
                    phone_number=row.get("phone_number", ""),
                    user_id=user_id,
                    email=row.get("email", ""),
                    address=row.get("address", ""),
                    note=row.get("note", ""),
                )
                if success:
                    imported += 1
                else:
                    skipped += 1
        return imported, skipped

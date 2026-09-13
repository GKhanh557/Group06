"""
group.py

The Group class handles creating, editing, deleting and viewing contact groups
(for example: "Family", "Work", "Friends"...).
"""

from models.database import get_connection


class Group:

    @staticmethod
    def add_group(group_name, user_id):
        """FR12: create a new group."""
        group_name = group_name.strip()
        if group_name == "":
            return False, "Group name cannot be empty."

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM Groups WHERE group_name = ? AND user_id = ?",
            (group_name, user_id),
        )
        if cursor.fetchone() is not None:
            conn.close()
            return False, "A group with this name already exists."

        cursor.execute("INSERT INTO Groups (group_name, user_id) VALUES (?, ?)", (group_name, user_id))
        conn.commit()
        conn.close()
        return True, "Group created successfully."

    @staticmethod
    def edit_group(group_id, user_id, new_name):
        """FR14: rename a group."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Groups SET group_name = ? WHERE group_id = ? AND user_id = ?",
            (new_name.strip(), group_id, user_id),
        )
        conn.commit()
        updated = cursor.rowcount > 0
        conn.close()
        return updated

    @staticmethod
    def delete_group(group_id, user_id):
        """
        FR11: delete a group.
        The contacts inside the group are NOT deleted - they just become "no group".
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Contact SET group_id = NULL WHERE group_id = ? AND user_id = ?",
            (group_id, user_id),
        )
        cursor.execute("DELETE FROM Groups WHERE group_id = ? AND user_id = ?", (group_id, user_id))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted

    @staticmethod
    def get_all_groups(user_id):
        """FR13: list all groups belonging to this user."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Groups WHERE user_id = ? ORDER BY group_name", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows

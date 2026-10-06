import json
from pathlib import Path


class LocalEmailService:
    def __init__(self, file_path="emails.json"):
        self.file_path = Path(file_path)
        self.emails = self._load_emails()

    def _load_emails(self):
        if not self.file_path.exists():
            return []

        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _save_emails(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(self.emails, file, indent=2)

    def get_all_emails(self):
        return self.emails

    def search_emails(self, query):
        query = query.lower()

        return [
            email
            for email in self.emails
            if query in email["subject"].lower()
            or query in email["body"].lower()
            or query in email["sender"].lower()
            or query in email["category"].lower()
        ]

    def get_by_category(self, category):
        return [
            email
            for email in self.emails
            if email["category"].lower() == category.lower()
        ]

    def archive_email(self, email_id):
        for email in self.emails:
            if email["id"] == email_id:
                email["archived"] = True
                self._save_emails()
                return True

        return False

    def delete_email(self, email_id):
        for email in self.emails:
            if email["id"] == email_id:
                email["deleted"] = True
                self._save_emails()
                return True

        return False
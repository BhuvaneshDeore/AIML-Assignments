from pathlib import Path
from collections import Counter

from mcp.server import MCPServer

from local_email_service import LocalEmailService


# ---------------------------------------------------------
# MCP SERVER
# ---------------------------------------------------------

mcp = MCPServer("Smart Email Organizer MCP")


# ---------------------------------------------------------
# EMAIL SERVICE
# ---------------------------------------------------------

BASE_DIR = Path(__file__).parent
EMAIL_FILE = BASE_DIR / "emails.json"

email_service = LocalEmailService(str(EMAIL_FILE))


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def active_emails():
    """Return emails that have not been deleted."""
    return [
        email
        for email in email_service.get_all_emails()
        if not email.get("deleted", False)
    ]


def format_email(email):
    """Format an email for readable MCP output."""
    return (
        f"ID: {email['id']}\n"
        f"From: {email['sender']}\n"
        f"Subject: {email['subject']}\n"
        f"Date: {email['date']}\n"
        f"Category: {email['category']}\n"
        f"Read: {email['read']}\n"
        f"Important: {email['important']}"
    )


# =========================================================
# 1. MCP TOOL
# =========================================================

@mcp.tool()
def manage_emails(
    operation: str,
    query: str = "",
    email_id: str = "",
    confirm: bool = False
) -> str:
    """
    Manage local emails.

    Supported operations:
    - search
    - analyze
    - preview_promotions
    - archive
    - delete_promotions

    Delete operations require explicit confirmation.
    """

    operation = operation.lower().strip()

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    if operation == "search":

        if not query:
            return "Please provide a search query."

        results = [
            email
            for email in email_service.search_emails(query)
            if not email.get("deleted", False)
        ]

        if not results:
            return f"No emails found for: {query}"

        output = [
            f"Found {len(results)} email(s) for '{query}':\n"
        ]

        for email in results:
            output.append(format_email(email))
            output.append("-" * 50)

        return "\n".join(output)

    # -----------------------------------------------------
    # ANALYZE
    # -----------------------------------------------------

    elif operation == "analyze":

        emails = active_emails()

        if not emails:
            return "No active emails found."

        category_counts = Counter(
            email.get("category", "other")
            for email in emails
        )

        unread_count = sum(
            not email.get("read", False)
            for email in emails
        )

        important_count = sum(
            email.get("important", False)
            for email in emails
        )

        output = [
            "EMAIL ANALYSIS",
            "=" * 40,
            f"Total emails: {len(emails)}",
            f"Unread emails: {unread_count}",
            f"Important emails: {important_count}",
            "",
            "CATEGORY BREAKDOWN",
            "-" * 40,
        ]

        for category, count in sorted(category_counts.items()):
            output.append(f"{category.title()}: {count}")

        return "\n".join(output)

    # -----------------------------------------------------
    # PREVIEW PROMOTIONS
    # -----------------------------------------------------

    elif operation == "preview_promotions":

        promotions = [
            email
            for email in active_emails()
            if email.get("category") == "promotion"
        ]

        if not promotions:
            return "No active promotional emails found."

        output = [
            f"Found {len(promotions)} promotional email(s).",
            "",
            "PREVIEW ONLY - NOTHING HAS BEEN DELETED.",
            "=" * 50,
        ]

        for email in promotions:
            output.append(format_email(email))
            output.append("-" * 50)

        output.append(
            "\nTo delete these emails, call "
            "delete_promotions with confirm=True."
        )

        return "\n".join(output)

    # -----------------------------------------------------
    # ARCHIVE
    # -----------------------------------------------------

    elif operation == "archive":

        if not email_id:
            return "Please provide an email_id."

        email = next(
            (
                email
                for email in active_emails()
                if email["id"] == email_id
            ),
            None
        )

        if not email:
            return f"Email '{email_id}' was not found."

        success = email_service.archive_email(email_id)

        if success:
            return (
                f"Email '{email_id}' has been archived successfully.\n"
                f"Subject: {email['subject']}"
            )

        return f"Unable to archive email '{email_id}'."

    # -----------------------------------------------------
    # DELETE PROMOTIONS
    # -----------------------------------------------------

    elif operation == "delete_promotions":

        promotions = [
            email
            for email in active_emails()
            if email.get("category") == "promotion"
        ]

        if not promotions:
            return "No active promotional emails found."

        # SAFETY CHECK
        if not confirm:

            output = [
                f"Found {len(promotions)} promotional email(s).",
                "",
                "⚠️ CONFIRMATION REQUIRED",
                "",
                "The following emails are ready to be moved "
                "to the simulated trash:",
                "=" * 50,
            ]

            for email in promotions:
                output.append(
                    f"{email['id']} | "
                    f"{email['sender']} | "
                    f"{email['subject']}"
                )

            output.append(
                "\nNo emails have been deleted."
            )

            output.append(
                "\nCall delete_promotions with confirm=True "
                "to continue."
            )

            return "\n".join(output)

        # -------------------------------------------------
        # EXECUTE DELETE
        # -------------------------------------------------

        deleted_count = 0

        for email in promotions:
            if email_service.delete_email(email["id"]):
                deleted_count += 1

        return (
            f"Successfully moved {deleted_count} promotional "
            f"email(s) to the simulated trash."
        )

    # -----------------------------------------------------
    # INVALID OPERATION
    # -----------------------------------------------------

    else:

        return (
            f"Unknown operation: '{operation}'.\n\n"
            "Supported operations:\n"
            "- search\n"
            "- analyze\n"
            "- preview_promotions\n"
            "- archive\n"
            "- delete_promotions"
        )


# =========================================================
# 2. MCP RESOURCE
# =========================================================

@mcp.resource("emails://summary")
def email_summary() -> str:
    """
    Provides a read-only summary of the current email collection.
    """

    emails = active_emails()

    category_counts = Counter(
        email.get("category", "other")
        for email in emails
    )

    unread_count = sum(
        not email.get("read", False)
        for email in emails
    )

    important_count = sum(
        email.get("important", False)
        for email in emails
    )

    output = [
        "SMART EMAIL ORGANIZER SUMMARY",
        "=" * 40,
        f"Total emails: {len(emails)}",
        f"Unread emails: {unread_count}",
        f"Important emails: {important_count}",
        "",
        "Categories:",
    ]

    for category, count in sorted(category_counts.items()):
        output.append(f"- {category.title()}: {count}")

    return "\n".join(output)


# =========================================================
# 3. MCP PROMPT
# =========================================================

@mcp.prompt()
def email_cleanup() -> str:
    """
    Provides a safe workflow for organizing and cleaning emails.
    """

    return """
You are an email organization assistant.

Follow this safe workflow:

1. Analyze the user's email collection.
2. Identify important, job, internship, college,
   newsletter, promotion, personal, and other emails.
3. Never delete emails automatically.
4. Before deleting promotional emails, show the user
   a complete preview.
5. Ask the user for explicit confirmation.
6. Only perform deletion when the user explicitly
   confirms the action.
7. Search for relevant emails when requested.
8. Archive emails only when specifically requested.
9. Prefer reversible actions over destructive actions.
10. Clearly report what was changed after every operation.

Important safety rule:

Never treat a request such as "clean my inbox",
"remove promotions", or "delete unwanted emails"
as automatic permission to delete emails.

Always preview first and require explicit confirmation.
"""


# =========================================================
# START MCP SERVER
# =========================================================

if __name__ == "__main__":
    mcp.run()
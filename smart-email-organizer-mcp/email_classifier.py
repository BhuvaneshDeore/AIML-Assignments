"""
Email Classifier Module
Provides rule-based classification for emails based on metadata (sender, subject, snippet, labels).

Supported Categories:
- important
- job
- internship
- college
- newsletter
- promotion
- personal
- other
"""

import re
from typing import Dict, List, Any


def classify_email(email: Dict[str, Any]) -> str:
    """
    Classifies a single email dictionary into one of the designated categories
    using available Gmail metadata (labels, sender, subject, snippet).

    Args:
        email (Dict[str, Any]): Dictionary containing email metadata fields:
                                - 'sender': From address/name
                                - 'subject': Subject text
                                - 'snippet': Email snippet / preview
                                - 'labels': List of Gmail label strings

    Returns:
        str: The assigned category name.
    """
    sender = (email.get("sender") or "").lower()
    subject = (email.get("subject") or "").lower()
    snippet = (email.get("snippet") or "").lower()
    labels = [lbl.upper() for lbl in email.get("labels", [])]
    full_text = f"{sender} {subject} {snippet}"

    # 1. Internship Emails
    internship_keywords = [
        "internship", "intern ", "interns", "co-op", "summer analyst",
        "software engineering intern", "swe intern", "summer intern", "intern application"
    ]
    if any(kw in full_text for kw in internship_keywords):
        return "internship"

    # 2. Job Emails
    job_keywords = [
        "job application", "interview request", "offer letter", "recruiter",
        "hiring manager", "application status", "greenhouse.io", "lever.co",
        "workday", "career opportunity", "job opening", "employment offer",
        "position update", "talent acquisition"
    ]
    if any(kw in full_text for kw in job_keywords):
        return "job"

    # 3. College / Academic Emails
    college_keywords = [
        "university", "college", "tuition", "registrar", "degree program",
        "campus", "course assignment", "professor", "gpa", "financial aid",
        "syllabus", "semester", "academic advisor", "department of"
    ]
    if ".edu" in sender or any(kw in full_text for kw in college_keywords):
        return "college"

    # 4. Important Emails (Gmail label or critical keywords)
    important_keywords = [
        "urgent", "security alert", "action required", "billing statement",
        "invoice", "bank alert", "tax document", "flight confirmation",
        "booking confirmation", "password reset", "verification code", "two-factor"
    ]
    if "IMPORTANT" in labels or any(kw in full_text for kw in important_keywords):
        return "important"

    # 5. Newsletter Emails
    newsletter_keywords = [
        "newsletter", "weekly digest", "daily briefing", "substack",
        "medium.com", "issue #", "edition #", "tech roundup", "weekly update",
        "changelog", "digest"
    ]
    if any(kw in full_text for kw in newsletter_keywords):
        return "newsletter"

    # 6. Promotional Emails (Gmail category label or discount/marketing keywords)
    promo_keywords = [
        "% off", "discount", "black friday", "cyber monday", "exclusive offer",
        "sale ends", "promo code", "shop now", "free shipping", "clearance",
        "buy now", "limited time", "special deal", "save up to", "don't miss out"
    ]
    if "CATEGORY_PROMOTIONS" in labels or any(kw in full_text for kw in promo_keywords):
        return "promotion"

    # 7. General Newsletter / Marketing indicator (Unsubscribe)
    if "unsubscribe" in full_text:
        return "newsletter"

    # 8. Personal Email (Gmail Personal label or fallback)
    if "CATEGORY_PERSONAL" in labels:
        return "personal"

    return "other"


def categorize_emails(emails: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Groups a list of emails by their classified categories.

    Args:
        emails (List[Dict[str, Any]]): List of email metadata dictionaries.

    Returns:
        Dict[str, List[Dict[str, Any]]]: Dictionary mapping category names to list of email dicts.
    """
    categories: Dict[str, List[Dict[str, Any]]] = {
        "important": [],
        "job": [],
        "internship": [],
        "college": [],
        "newsletter": [],
        "promotion": [],
        "personal": [],
        "other": []
    }

    for email in emails:
        cat = classify_email(email)
        # Ensure email dict records its assigned category
        email_copy = dict(email)
        email_copy["category"] = cat
        categories[cat].append(email_copy)

    return categories


def summarize_categories(emails: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Computes summary counts for each category from a list of emails.

    Args:
        emails (List[Dict[str, Any]]): List of email metadata dictionaries.

    Returns:
        Dict[str, int]: Count of emails per category.
    """
    categorized = categorize_emails(emails)
    return {cat: len(items) for cat, items in categorized.items()}

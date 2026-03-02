import imaplib
import email
import email.header
import re
from html import unescape


def connect(address, app_password):
    """Connect and authenticate to Gmail IMAP."""
    imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    imap.login(address, app_password)
    return imap


def decode_header_value(raw):
    """Decode an email header value into a plain string."""
    parts = email.header.decode_header(raw)
    decoded = []
    for data, charset in parts:
        if isinstance(data, bytes):
            decoded.append(data.decode(charset or "utf-8", errors="replace"))
        else:
            decoded.append(data)
    return "".join(decoded)


def strip_html(html_text):
    """Crude HTML-to-text: remove tags, decode entities."""
    text = re.sub(r"<a\b[^>]*>.*?</a>", "", html_text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<img\b[^>]*>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", " ", text)
    return text.strip()


def strip_text(text_body):
    """Clean plain text: remove URLs and normalize line endings."""
    text = text_body.replace("\r\n", "\n")
    text = re.sub(r"https?://\S+", "", text)
    text = text.replace("( )", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", " ", text)
    return text.strip()


def parse_email(raw_bytes):
    """Parse a raw email into a structured dict."""
    msg = email.message_from_bytes(raw_bytes)

    subject = decode_header_value(msg.get("Subject", "(no subject)"))
    date = msg.get("Date", "")

    text_body = ""
    html_body = ""

    for part in msg.walk():
        content_type = part.get_content_type()

        if content_type == "text/plain":
            charset = part.get_content_charset() or "utf-8"
            payload = part.get_payload(decode=True)
            if payload:
                text_body += payload.decode(charset, errors="replace")

        elif content_type == "text/html":
            charset = part.get_content_charset() or "utf-8"
            payload = part.get_payload(decode=True)
            if payload:
                html_body += payload.decode(charset, errors="replace")

    # Prefer plain text; fall back to stripped HTML
    if text_body.strip():
        body = strip_text(text_body)
    elif html_body.strip():
        body = strip_html(html_body)
    else:
        body = ""

    return {
        "subject": subject,
        "date": date,
        "body": body,
    }


def fetch_emails(imap, folder, limit=None):
    """Fetch unread emails from a folder, sorted newest-first. Returns a list of (uid, parsed_email) tuples."""
    status, _ = imap.select(f'"{folder}"', readonly=True)
    if status != "OK":
        raise RuntimeError(f"Could not select folder: {folder}")

    status, data = imap.search(None, "UNSEEN")
    if status != "OK":
        raise RuntimeError("Failed to search emails")

    uids = data[0].split()
    if not uids:
        return []

    # Fetch INTERNALDATE for sorting, then sort newest-first
    uid_dates = []
    for uid in uids:
        status, date_data = imap.fetch(uid, "(INTERNALDATE)")
        if status != "OK":
            continue
        internal_date = imaplib.Internaldate2tuple(date_data[0])
        uid_dates.append((uid, internal_date))

    uid_dates.sort(key=lambda x: x[1])

    if limit:
        uid_dates = uid_dates[:limit]

    emails = []
    for uid, _ in uid_dates:
        status, msg_data = imap.fetch(uid, "(RFC822)")
        if status != "OK":
            continue
        raw = msg_data[0][1]
        emails.append((uid, parse_email(raw)))

    return emails


def mark_as_read(imap, folder, uids):
    """Mark the given email UIDs as read (Seen) in the specified folder."""
    status, _ = imap.select(f'"{folder}"', readonly=False)
    if status != "OK":
        raise RuntimeError(f"Could not select folder: {folder}")

    for uid in uids:
        imap.store(uid, "+FLAGS", "\\Seen")

import os
from datetime import datetime, timezone
import dlai_config
from dlai_scanner import connect, fetch_emails, mark_as_read
from dlai_summarizer import summarize_email


def dlai_scan(model=dlai_config.OLLAMA_MODEL, limit=1):
    # Connect to GMAIL and get the e-mails
    print(f"Connecting to Gmail as {dlai_config.GMAIL_ADDRESS}...")
    imap = connect(dlai_config.GMAIL_ADDRESS, dlai_config.GMAIL_APP_PASSWORD)

    print(f"Fetching emails from '{dlai_config.GMAIL_FOLDER}'...")
    fetched = fetch_emails(imap, dlai_config.GMAIL_FOLDER, limit=limit)

    if not fetched:
        imap.logout()
        print("No emails found in this folder.")
        return

    uids, emails = zip(*fetched)

    print(f"Found {len(emails)} email(s). Generating summaries...\n")

    # Produce e-mails summaries
    results = []
    for i, email_data in enumerate(emails, 1):
        print(f" E-mail [{i}/{len(emails)}] : {email_data['subject']}")
        summary = summarize_email(email_data, model)

        result = {
            "model": model,
            "subject": email_data["subject"],
            "date": email_data["date"],
            "summary": summary,
        }
        results.append(result)

        print(f"  Date: {email_data['date']}")
        print(f"  Summary: {summary}")
        print()

    # Save to Markdown
    os.makedirs(dlai_config.OUTPUT_FOLDER, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(dlai_config.OUTPUT_FOLDER, f"summaries_{timestamp}.md")

    lines = [
        f"**Scanned at:** {datetime.now(timezone.utc).isoformat()}  ",
        f"**Email count:** {len(results)}",
        f"",
    ]

    for result in results:
        lines.append(f"## {result['subject']}")
        lines.append(f"**Date:** {result['date']}")
        lines.append(f"**Model:** {result['model']}")
        lines.append(f"")
        lines.append(result["summary"])
        lines.append(f"")
        lines.append(f"---")
        lines.append(f"")

    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    print(f"Summaries saved to {output_path}")

    mark_as_read(imap, dlai_config.GMAIL_FOLDER, uids)
    print(f"Marked {len(uids)} email(s) as read.")
    imap.logout()


if __name__ == "__main__":
    dlai_scan(model='ministral-3:14b', limit=5)

import os
from datetime import datetime, timezone
import dlai_config
from dlai_scanner import connect, fetch_emails, mark_as_read
from dlai_summarizer import summarize_email


def dlai_scan(model='ollama', limit=5):
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

    if model == 'openai':
        url = None
        api_key = dlai_config.openai_api_key
        model = dlai_config.OPENAI_MODEL
    if model == 'claude':
        url = dlai_config.ANTHROPIC_BASE_URL
        api_key = dlai_config.anthropic_api_key
        model = dlai_config.ANTHROPIC_MODEL
    if model == 'gemini':
        url = dlai_config.GEMINI_BASE_URL
        api_key = dlai_config.gemini_api_key
        model = dlai_config.GEMINI_MODEL
    if model == 'grok':
        url = dlai_config.GROK_BASE_URL
        api_key = dlai_config.grok_api_key
        model = dlai_config.GROK_MODEL
    if model == 'groq':
        url = dlai_config.GROQ_BASE_URL
        api_key = dlai_config.groq_api_key
        model = dlai_config.GROQ_MODEL
    if model == 'ollama':
        url = dlai_config.OLLAMA_BASE_URL
        api_key = "ollama"
        model = dlai_config.OLLAMA_MODEL

    # Produce e-mails summaries
    results = []
    for i, email_data in enumerate(emails, 1):
        summary = summarize_email(email_data, model, url, api_key)

        result = {
            "subject": email_data["subject"],
            "date": email_data["date"],
            "model": model,
            "scan_date": datetime.now().isoformat(),
            "summary": summary,
        }
        results.append(result)

    # Save to Markdown
    os.makedirs(dlai_config.OUTPUT_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(dlai_config.OUTPUT_FOLDER, f"dlai_summaries_{timestamp}.md")

    lines = [
        f"**Email count:** {len(results)}",
        f"",
    ]

    for result in results:
        lines.append(f"## {result['subject']}")
        lines.append(f"**Scanned at:** {result['scan_date']}")
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
    dlai_scan(model='claude', limit=10)
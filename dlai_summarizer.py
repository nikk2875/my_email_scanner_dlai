import anthropic
from openai import OpenAI
import dlai_config


def get_prompt(body):
    """Define prompt to use for the summarization."""
    prompt = f"""
Summarize the following email. Remove any part regarding feedback, job opening and course
announcements.
---
{body}
---"""
    return prompt


def summarize_email_claude(body):
    """Use Claude to summarize an email."""
    prompt = get_prompt(body)

    client = anthropic.Anthropic(api_key=dlai_config.ANTHROPIC_API_KEY)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text


def summarize_email_ollama(body, model):
    """Use Ollama to summarize an email."""
    prompt = get_prompt(body)

    client = OpenAI(base_url=dlai_config.OLLAMA_BASE_URL, api_key="ollama")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content


def summarize_email(email_data, model):
    """Wrapper for summarizing an email."""
    body = email_data["body"]
    if not body:
        return "Empty email — no text content found."

    print(f"Using {model}...")

    if model=='claude':
        return summarize_email_claude(body)
    else:
        return summarize_email_ollama(body, model)

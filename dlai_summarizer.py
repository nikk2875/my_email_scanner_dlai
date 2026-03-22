import dlai_config
import ollama
from openai import OpenAI


def get_complete_prompt(user_prompt, body):
    """Define prompt to use for the summarization."""
    prompt = f"""{user_prompt}
---
{body}
---
"""
    return prompt


def get_response(prompt, model, url, api_key):
    """Use given model to summarize."""
    client = OpenAI(base_url=url, api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def get_ollama_response(prompt, model):
    """Special version for getting response from Ollama. Finally I don't use it, but may be usefull for "overthinking" models like Qwen3.5."""
    response = ollama.chat(
        model=model,
        think=False,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.message.content


def summarize_email(email_data, model, url, api_key):
    """Wrapper for summarizing an email."""

    input_prompt_for_key_message = """The following text is a newsletter. It contains 2 major parts. The first part is a 
    key message by the author and the second part has news articles. Please find the key message part and summarize it. Return 
    only the summary. This is the text:
    """
    input_prompt_for_news = """The following text is a newsletter. It contains 2 major parts. The first part is a key message 
    by the author and the second part has news articles. Please find the news articles part and summarize it. Return only 
    the summaries. This is the text:
    """

    body = email_data["body"]
    if not body:
        return "Empty email — no text content found."

    print(f"Using {model}...")

    """
    During development, I found that if you summarize the key message of Andrew Ng and news as separate sections,
    you get much better results. For this reason, I make 2 requests instead of 1 and combine the results.
    """

    # Produce summary for key message
    prompt = get_complete_prompt(input_prompt_for_key_message, body)
    summary = get_response(prompt, model, url, api_key)

    # Produce summary for news and add to the previous
    prompt = get_complete_prompt(input_prompt_for_news, body)
    summary = summary + "\n\n---\n**NEWS:**\n\n" + get_response(prompt, model, url, api_key)

    return summary
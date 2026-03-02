# my_email_scanner
This is a collection of tools to get insights on specific mail groups of my Gmail account. There are many informative e-mails I get in mu account, but I don't have the time to go through all of them. So, I am building a couple of tools that will help get a summary of them, so that I can focus only on those that I find really important. The first group of mails I wanted to analyze, is those that I get from Deeplearning.AI.

### About Deeplearning.AI code (DLAI)
Their newsletter typically has a message from Andrew Ng, then news articles on various ML & AI topics. For them I have created `dlai_scan.py`, wchih performs the following actions:
1. Logins to my e-mail.
2. Fetches all my mails. Please note that:
    - I have created a specific folder in my inbox to store these mails, so there is no filtering logic. I just fetch all mails from the DLAI folder.
    - I set a limit on the number of e-mails that I will fetch. Default is 1.
    - I get only unread e-mails in reverse chronological order.
3. Goes though each e-mail and produces a summary. There are 2 options:
    - **A frontier model**. I use Claude Sonnet.
    - **Ollama**. I have tested a few models, my preference is `ministral-3:14b`. I have an NVIDIA GPU with 12GB VRAM, so I can afford a 14b model. But I also suggest `granite4:3b` for a small setup.
4. Summary output goes to an output folder and all fetched e-mails are marked as read.

### NOTE
I have my own `.env` file, but to define your own settings I also include a `.env.sample` to use as template.

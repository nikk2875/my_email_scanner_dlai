# my_email_scanner_dlai
There are many informative e-mails I get in my Gmail account, but I don't have the time to go through all of them. So, I am building a couple of tools that will help me to produce summaries and let me focus only on those that really matter to me. The first group of mails I wanted to analyze, is those that I get from *Deeplearning.AI*.

### About Deeplearning.AI code (DLAI)
Deeplearning.AI newsletter typically has a message from Andrew Ng, then news articles on various ML & AI topics. For this case, I have created `dlai_scan.py`, which performs the following actions:
1. It logins to my e-mail account.
2. It fetches all e-mails in a given folder. Please note that:
    - I have created a specific folder in my inbox to store these mails, so there is no filtering logic. I just fetch all mails from DLAI folder.
    - I set a maximum limit on the number of e-mails that I will fetch. Default is 5.
    - I get only unread e-mails in reverse chronological order. Therefore, I start from older e-mails and gradually come to the fresh ones.
3. It goes though each e-mail and produces a summary. There are 2 options:
    - **A frontier model**. I have set options for all major providers (OpenAI, Anthropic, Google, Grok, Groq).
    - **Ollama**. I have tested a few models, my preference for this particular is `phi4:14b`. I have an NVIDIA GPU with 12GB VRAM, so I can afford a 14b model.
4. It produces a summary output that goes to an output folder (that I define) and all fetched e-mails are marked as read.

## What you need to do
Once you clone the repository, you need to:
1. define the folder that the code will be deployed by setting the `BASE_SCRIPT_DIR` variable. You need to alter both `install_dlai.sh` and `run_dlai.sh`.
2. run the commands `chmod +x install_dlai.sh` then `./install_dlai.sh`.
3. go to the directory that you have deployed the code.
4. run `./run_dlai.sh` (if you want to use the default settings) or go to `My_Email_Scanner_DLAI` folder and modify `dlai_scan.py` first.

## Configurations
You can set 2 parameters: `model` and `limit`. With `limit` you define the maximum number of e-mails to fetch (default is 5). Defining the model is a bit more complicated. The `model` parameter defines the providee that you will use. There are technically 5 choices: *openai*, *claude*, *gemini*, *grok*, *groq*, *ollama*. In reality you will be able to use only those that have a key defined in `.env`. For the specific models you would like to use, you need to make a separate configuration in `dlai_config.py`. I have defined the best of my tests for each provider.

## Note for the .env file
I have my own `.env` file, but to define your own settings I have also included a `.env.sample`. You can use it as a template.

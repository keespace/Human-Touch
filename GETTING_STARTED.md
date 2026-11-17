# Running Human Touch on your computer

Human Touch runs entirely on your own computer. You need about 10 minutes the first time.

## 1. Install Python (one time)

Download it from https://www.python.org/downloads/ and run the installer.

- **Windows:** on the first installer screen, tick **"Add python.exe to PATH"**.
- **Mac:** the standard installer is fine.

## 2. Get your own Anthropic API key (one time)

The detailed analysis, web search and assistant use Claude, Anthropic's AI. Each person needs their own key:

1. Sign up at https://platform.claude.com.
2. Add a few dollars of credit under **Settings → Billing**. $5 covers roughly 50–100 checks.
3. Create a key under **Settings → API keys** and copy it.

Without a key, the app still runs the free quick pattern check.

## 3. Start the app

Unzip the folder anywhere, for example on your Desktop. Then:

- **Windows:** double-click **`Start Human Touch.bat`**.
- **Mac:** open the Terminal app, type `bash ` (with a space), drag the **`start-mac.sh`** file into the window, and press Enter.

The first time, the app installs what it needs. It then creates a file called `.env` and opens it so you can paste your API key after `ANTHROPIC_API_KEY=`. Save the file and continue.

Your browser then opens at **http://localhost:8765**. Keep the black or Terminal window open while you use the app, and close it to stop.

## Good to know

- Your API key stays in the `.env` file on your computer. **Never share that file** or put it online.
- **Even safer:** store the key as a Windows user environment variable named `ANTHROPIC_API_KEY` (Start → "Edit environment variables for your account" → New) and delete `.env`. The app picks it up automatically.
- Text is only sent to Anthropic for analysis. Nothing is stored.
- **If Windows shows "Windows protected your PC"** when you double-click the start file, click **More info → Run anyway**. This appears for any script downloaded from someone else. Only do it if you trust the person who sent you the app.
- **If you see "address already in use"**, the app is already running. Open http://localhost:8765 in your browser.
- **Results describe patterns in the text, not facts about a person.** Never use them as the only basis for a decision about anyone, or to make public claims about someone's work.

# Security

## Your API key
- Human Touch reads your Anthropic API key from a local `.env` file. That file is listed in `.gitignore` and is never committed, served or zipped.
- Never paste your key into an issue, a pull request, a screenshot or a chat.
- If you think a key has leaked, delete it at https://platform.claude.com (Settings → API keys) and create a new one. Setting a monthly spend limit on your account caps any damage.

- **Safest option:** instead of a `.env` file, store the key as a user environment variable called `ANTHROPIC_API_KEY`. On Windows: Start → "Edit environment variables for your account" → New. The app uses it automatically, and no file containing the key exists in any folder. Restart the app after setting it.

## How the app protects you
- The server only listens on your own computer (`127.0.0.1`). Other devices on your network can't reach it.
- It serves exactly one page (`index.html`) and nothing else, so `.env`, source files and data can't be downloaded through the browser.
- Pasted text and web pages are passed to Claude as *data*, with instructions to ignore any commands inside them.
- Web search matches are only shown if their link really came back from a search, so the app never shows invented sources.

## Reporting a problem
If you find a security issue, please open a GitHub issue that describes the problem without including any secrets, or contact the maintainer privately through their GitHub profile.

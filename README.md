# Human Touch

### What are our children reading?

More and more of the stories, books and articles our kids read are written by machines. **Human Touch helps parents, teachers and readers look closer at the words in front of them.** It shows the writing patterns that point to a real person, with real emotions, empathy and judgement, or to a machine, and where matching wording appears online.

> Human Touch describes patterns in a text. It does not determine who wrote it or how, and it makes no claims about any person. Results are signals for a human to review, never conclusions.

![Human Touch home page](docs/screenshots/home.png)

## Why it's different

- **Made for what kids read.** It handles picture books, school reading, stories and articles carefully, because simple writing is not a sign of AI.
- **Human, AI, or in between.** It doesn't give a single score. The verdict is one of four kinds of authorship, with percentages and a paragraph-by-paragraph breakdown:

  | Verdict | What it means |
  |---|---|
  | 🟢 **Reads as human-written** | The text shows the patterns typical of human writing. |
  | 🟡 **Signs of AI-assisted editing** | Specific, personal substance with an unusually smooth, polished surface. |
  | 🟠 **Signs of an edited AI draft** | A template-like structure with personal touches layered on. |
  | 🔴 **Strong AI-like patterns** | Generic content and surface typical of unedited AI output. |

  Many people use AI tools legitimately, for spelling, translation or editing, so AI-like patterns are not evidence of wrongdoing.

- **Shows its evidence.** Every verdict explains why, and every web source is a link you can open and read yourself.
- **Honest by design.** It describes the text, never the person. When the signals are close, it says "inconclusive" instead of guessing.
- **An assistant you can ask.** It answers questions about the result, such as "Is this from a published book?" or "Which paragraph looks most AI-written?", and runs refined web searches with cited sources.

![Example result: a children's story analysed by Human Touch](docs/screenshots/results.png)

## Quick start

You need **Python 3.10+** ([download](https://www.python.org/downloads/)). On Windows, tick *"Add python.exe to PATH"* during setup.

You also need **your own Anthropic API key** ([get one](https://platform.claude.com)). Without a key, only the free quick check works.

```bash
git clone https://github.com/keespace/Human-Touch.git
```

```bash
cd Human-Touch
```

Then start it:
- **Windows:** double-click `Start Human Touch.bat`.
- **Mac or Linux:** run `bash start-mac.sh`.

On first run, the script installs the one dependency and creates a `.env` file for your key. It then opens http://localhost:8765. See [GETTING_STARTED.md](GETTING_STARTED.md) for a non-technical walkthrough.

To try it instantly with an example, open http://localhost:8765/?example=kids. You can also use `article` or `essay` in place of `kids`.

## How it works

| Layer | What it does | Runs | Cost |
|---|---|---|---|
| **Quick pattern check** | Measures sentence rhythm, stock AI vocabulary, personal voice, concrete detail, formulaic structure and tidy endings | In your browser | Free |
| **Detailed analysis** | Claude reads the text paragraph by paragraph, with objective measurements as evidence, and gives probabilities for the four categories | Anthropic API | ~$0.03–0.08 per check |
| **Find matching text online** | Planned exact-phrase web searches, verified overlap, and every source listed as a clickable link. Matching text can have innocent explanations, such as quotation, licensing or reuse by others. | Anthropic API + web search | ~$0.05–0.15 per search |
| **Assistant** | Answers questions about the result and runs refined searches with citations | Anthropic API + web search | ~$0.02–0.10 per question |

**How the verdict is decided:** the human share is compared with all AI shares combined.
- 60% or more human: the result is **reads as human-written**.
- 40% or less human: the result is the strongest of the three AI-like patterns.
- Anything in between: **inconclusive**, with the direction it leans.

The quick pattern check is shown alongside the main verdict, but it's easy to fool. For example, AI that imitates a personal voice can pass it. The detailed analysis is the better guide.

## Measuring accuracy

A detector is only as trustworthy as its measured error rate. [`eval/`](eval/README.md) contains a test set and a script that report a confusion matrix and, most importantly, how often real human writing is wrongly flagged.

```bash
python eval/evaluate.py
```

The current test set is small: 1 known-human text and 10 AI-written or AI-assisted texts. **Contributions of known-human texts, especially children's writing, are very welcome.** That's what makes the numbers meaningful.

## Privacy

- The quick check runs entirely in your browser.
- The detailed analysis, web search and assistant send the text to Anthropic's API. Nothing is stored by this app.
- Your API key stays in `.env` on your computer. See [SECURITY.md](SECURITY.md).

## Project layout

```
index.html            the whole user interface (quick check, results, assistant)
server.py             local server and the Claude-powered checks
eval/                 accuracy test set and evaluation scripts
Start Human Touch.bat / start-mac.sh   one-click start with first-run setup
make_share_zip.py     builds a shareable zip without your API key
```

## Important

**Results describe patterns, not people.** No tool can determine for certain how a text was produced, and formal, simple or non-native writing can show AI-like patterns. Never use a result as the sole basis for any decision about a person, such as grading, discipline, hiring or publishing decisions. Never use it to make public claims about a person or their work.

Human Touch uses Claude by Anthropic. It is an independent project and is not affiliated with or endorsed by Anthropic.

## License

[MIT](LICENSE). Free to use, share and adapt.

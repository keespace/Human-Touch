# Testing how accurate Human Touch is

A detector is only as trustworthy as its measured error rate. This folder lets you measure it on texts whose real origin you know.

## Folders: one per true answer

```
eval/samples/
  human_written/            texts you KNOW a person wrote without AI
  ai_assisted/              a person's draft, polished by AI          (auto-made from human_written/)
  ai_written_human_edited/  an AI draft that a person then revised     (needs you - see below)
  ai_generated/             AI output used as-is                       (auto-made)
```

Each `.txt` file is one test text. 150–600 words works best.

## What to add (the most valuable part)

1. **`human_written/`**: 10 or more texts you're certain are human, and as close as possible to what you'll check in real life:
   - pages from children's books published **before 2022** (typed out or copied)
   - your own emails, posts or school essays from before 2022
   - simple, plain writing, since that's where false alarms happen
2. **`ai_written_human_edited/`**: ask ChatGPT or Claude for a short story or essay, then edit it yourself like a real person would: change some words, add a personal detail, cut a paragraph. Save your edited version.
3. Optionally, add AI texts from **other AI tools** (ChatGPT, Gemini and others) to `ai_generated/`, because each model writes a little differently.

## Run it

```bash
python eval/make_samples.py
```

This generates `ai_generated/` texts and an AI-polished copy of each human text. Run it again after adding human texts.

```bash
python eval/evaluate.py
```

This prints each verdict, a confusion matrix and the error rates. It costs about 3–8 cents per text.

The number to watch is **"Human texts wrongly flagged AI"**. For a tool used on children's books and students' work, a false accusation is worse than a miss.

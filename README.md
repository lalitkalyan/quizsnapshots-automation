# quizsnapshots‑automation

This repository contains a proof‑of‑concept automation pipeline for
producing short quiz videos for the **Quiz Snapshots** channel. The
system is designed to run end‑to‑end with minimal manual intervention
while giving you the ability to approve key stages via Telegram.

## Features

- **Shorts only**: Each video is rendered in vertical format (1080×1920)
  with a runtime between **45** and **59** seconds.
- **Buffer control**: Maintains a buffer of ready‑to‑publish videos. When
  the number of ready items falls below a low‑watermark, a cron job asks
  you whether to begin refilling the buffer.
- **Three approval gates**: You approve the topic, the question preview,
  and the final enqueue into the upload queue.
- **Multi‑platform support**: Placeholder logic exists for YouTube
  Shorts, TikTok, and Instagram Reels. The upload script currently
  simulates scheduling without hitting external APIs.

## Project structure

```
config/       # YAML configuration files
data/         # CSV and JSONL files storing topics, queues and question bank
scripts/      # Python scripts for each pipeline stage
workflows/    # Example n8n flows for buffer monitoring and production
README.md     # This file
```

### Config files

- **`config/ops.yml`** – Buffer thresholds, approval toggles and Telegram
  chat ID.
- **`config/brand.yml`** – Fonts, colours and timing settings for the
  renderer.
- **`config/status_keys.yml`** – List of pipeline states and which
  states count towards the buffer.
- **`config/seo.yml`** – Simple templates for titles, descriptions and
  hashtags.

### Data files

- **`data/backlog.csv`** – Your master list of potential quiz topics.
- **`data/publish_queue.csv`** – Topics scheduled for production. New
  entries are added here after you approve a topic.
- **`data/questions_bank.jsonl`** – A running bank of all previously
  published questions used for de‑duplication.

### Scripts

Each script corresponds to a stage in the pipeline. They are designed
to be chained together by an orchestrator (e.g. n8n). All scripts can
also be run manually for testing.

- `buffer_watcher.py` – Monitors the buffer of READY items and asks
  whether to refill when it drops below the low‑watermark.
- `propose_topic.py` – Proposes the next topic from the publish queue
  for your approval.
- `gen_questions.py` – Generates placeholder questions for a given
  topic.
- `preview_approval.py` – Sends a preview of generated questions and
  waits for your approval.
- `factcheck.py` – Stubbed fact‑checker that marks questions as
  verified.
- `dedupe.py` – Stubbed de‑duplicator to remove repeat questions.
- `render_native.py` – Renders the final video using MoviePy.
- `make_thumbnail.py` – Generates a simple thumbnail using Pillow.
- `queue_approval.py` – Asks for approval to move a READY item into
  the publish queue.
- `upload_schedule.py` – Simulates uploading and scheduling across
  platforms.
- `analytics.py` – Prints a summary of published videos.

### Workflows

The JSON files in `workflows/` illustrate how you might wire up the
scripts in **n8n**. The `n8n_buffer.json` flow runs the buffer watcher
every few hours, while `n8n_production.json` orchestrates the full
production loop: proposing a topic, generating questions, previewing,
fact‑checking, de‑duplicating, rendering, thumbnail creation, queue
approval and finally scheduling uploads.

## Installation

1. Clone this repository or download it as a zip:

   ```bash
   git clone https://github.com/lalitkalyan/quizsnapshots-automation.git
   cd quizsnapshots-automation
   ```

2. Install the dependencies (preferably in a virtualenv):

   ```bash
   pip install -r requirements.txt
   ```

   For this proof of concept the key packages are:

   - `moviepy`
   - `Pillow`
   - `python-telegram-bot` (only needed for a real Telegram integration)

3. Set up a Telegram bot and obtain your `TELEGRAM_BOT_TOKEN`. Place it in
   your environment (e.g. export it in your shell) and update
   `config/ops.yml` with your chat ID.

## Running a local test

The following steps simulate one cycle of the pipeline locally:

1. **Propose a topic** from the backlog (manually add an entry to
   `publish_queue.csv` with status `PLANNED` if none exist).
   
   ```bash
   python scripts/propose_topic.py
   ```

2. **Generate questions** for the approved topic:

   ```bash
   python scripts/gen_questions.py --topic "World Capitals" --out tmp/questions.jsonl
   ```

3. **Preview approval**:

   ```bash
   python scripts/preview_approval.py --questions tmp/questions.jsonl
   ```

4. **Fact‑check and deduplicate**:

   ```bash
   python scripts/factcheck.py --in tmp/questions.jsonl --out tmp/verified.jsonl
   python scripts/dedupe.py --in tmp/verified.jsonl --bank data/questions_bank.jsonl --out tmp/deduped.jsonl
   ```

5. **Render the video**:

   ```bash
   python scripts/render_native.py --in tmp/deduped.jsonl --out tmp/video.mp4
   ```

6. **Generate a thumbnail**:

   ```bash
   python scripts/make_thumbnail.py --topic "World Capitals" --hook "Can you guess them all?" --out tmp/thumb.png
   ```

7. **Queue approval**:

   ```bash
   python scripts/queue_approval.py
   ```

8. **Upload and schedule** (simulated):

   ```bash
   python scripts/upload_schedule.py
   ```

9. **Review analytics**:

   ```bash
   python scripts/analytics.py
   ```

## Buffer logic

The buffer keeps your pipeline from stalling. It counts the number of
``READY`` items (rendered videos that still require queue approval). A
cron job (see `buffer_watcher.py` and `workflows/n8n_buffer.json`) checks
the buffer every few hours. If the count is below the low‑watermark
specified in `ops.yml`, it sends you a Telegram message asking whether
to start generating more videos. If you respond positively, the
production flow runs until there are `target` READY items.

## License

This project is provided as a demonstration and does not include a
software license. Feel free to modify and adapt it for your own use.
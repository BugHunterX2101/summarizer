# Interview Transcript Summarizer

A command-line tool that takes an interview transcript and produces a structured summary: topics covered, candidate profile, and a written candidate summary — powered by Groq's LLM API.

---

## Setup

### 1. Clone / download the repo

```bash
git clone <your-repo-url>
cd <repo-folder>
```

### 2. Install dependencies

```bash
pip install groq python-dotenv
```

### 3. Add your API key

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

> ⚠️ Never commit this file. It is listed in `.gitignore`.

---

## How to Run

```bash
python summarizer.py sample_transcript_assignment_1.txt
```

To also save the raw JSON output alongside the formatted output:

```bash
python summarizer.py sample_transcript_assignment_2.txt --json
```

### Example output

```
============================================================
INTERVIEW SUMMARY
============================================================

📌 TOPICS COVERED
----------------------------------------
  1. AI-assisted development workflow with Cursor and GitHub Copilot
  2. Ionic v7 mobile dashboard with responsiveness and virtual scroll
  3. Capacitor image capture and file system sync workflow
  4. Tailwind CSS design system and utility-first approach
  5. Angular modular architecture and lazy loading
  6. React state management with Context API and React Query
  7. Redux slice and Zustand familiarity

👤 CANDIDATE PROFILE
----------------------------------------
  Role: Frontend/Mobile Engineer — mid-level
  Why: Prasanna has 9 years of experience focused on Angular, React,
       and Ionic with Capacitor. He showed hesitation writing Zustand
       and Redux slice code from scratch, suggesting mid-level depth.

📝 CANDIDATE SUMMARY
----------------------------------------
  Prasanna Kumar is a software developer with nine years of experience
  specializing in Angular, React, and Ionic/Capacitor...

============================================================
```

---

## LLM Provider and Model

- **Provider:** [Groq](https://console.groq.com)
- **Model:** `llama-3.1-8b-instant`

Groq was chosen for its fast inference and generous free tier (500,000 tokens/day on this model). The model is sufficient for structured summarization tasks on transcripts of this length.

---

## Reflection

### What surprised me

The biggest surprise was how much prompt structure mattered for cross-transcript generalization. A prompt tuned for a technical engineering interview (Transcript 1) produced shallow, buzzword-heavy output on the PM interview (Transcript 2) until I added explicit field definitions and the evidence-grounding rule. The instruction *"base everything strictly on what is said in the transcript"* alone eliminated most hallucination — the model had been silently filling in assumed seniority years and inferred skills without it.

I also didn't expect the model to consistently wrap JSON in markdown fences (` ```json `) despite being told not to — a small but real reliability issue that required a defensive strip step in the parsing code.

### What I'd improve with another day

1. **Multi-turn refinement:** Ask the model a follow-up question like "What is the single biggest risk in hiring this candidate?" to surface sharper concerns than a single-pass prompt can produce.
2. **Confidence signaling:** Add a `"confidence"` field (low/medium/high) that the model sets based on transcript length and answer quality — useful for flagging summaries that are based on thin evidence.
3. **Speaker role detection:** Currently the prompt assumes a standard interviewer/candidate structure. A preprocessing step to reliably identify which speaker is the candidate (using heuristics on turn length and question phrasing) would make the tool more robust to unusual transcript formats.
4. **Streaming output:** For very long transcripts, streaming the response would improve perceived latency significantly.

### Limitations of the final prompt

- **Short or fragmented transcripts:** If a transcript has fewer than ~10 substantial exchanges, topics become generic and the candidate summary will be underdetermined. The prompt handles this gracefully (it asks the model to note uncertainty) but cannot conjure signal that isn't there.
- **Multi-candidate transcripts:** The prompt assumes one candidate. Panel interviews or transcripts with multiple candidates are not handled.
- **Non-English transcripts:** The prompt works in English only. Transcripts with significant code-switching (e.g., Hindi phrases mid-sentence, as noted in Transcript 2) are handled because the model understands context, but a non-English transcript would produce degraded output.
- **Hallucination risk on vague transcripts:** Despite the grounding instruction, the model may occasionally infer seniority or experience years not explicitly stated. Users should treat the profile as a starting point, not a definitive assessment.

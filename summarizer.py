import os
import sys
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def build_prompt(transcript: str) -> str:
    return f"""You are an expert technical recruiter and interview analyst. You will be given a raw interview transcript and must produce a structured summary.

Your output must be a valid JSON object with exactly these three keys:

1. "topics_covered": A list of 3–7 strings, each naming a main theme discussed (e.g., "Angular state management", "vendor onboarding process"). Be specific to what was actually discussed.

2. "profile": An object with:
   - "role": The role/profile this candidate fits (e.g., "Frontend/Mobile Engineer — mid-level")
   - "justification": 1–2 sentences explaining why, based on evidence from the transcript.

3. "candidate_summary": A single paragraph of 3–6 sentences covering:
   - Their background and years of experience
   - Core technical or domain strengths
   - Any notable weaknesses or concerns raised
   - Overall impression of suitability

Rules:
- Base everything strictly on what is said in the transcript. Do not invent or assume.
- If the transcript is short or vague, still produce the best summary you can and note uncertainty in the justification.
- Output ONLY the JSON object. No preamble, no markdown, no explanation outside the JSON.

TRANSCRIPT:
\"\"\"
{transcript}
\"\"\"
"""

def summarize_transcript(transcript: str, model: str = "llama-3.1-8b-instant") -> dict:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found. Set it in your .env file or environment.")

    client = Groq(api_key=api_key)

    prompt = build_prompt(transcript)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a precise interview analyst. Always respond with valid JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=1000,
    )

    raw = response.choices[0].message.content.strip()

    # Strip markdown fences if model wraps output in ```json ... ```
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    result = json.loads(raw)
    return result

def format_output(summary: dict) -> str:
    lines = []
    lines.append("=" * 60)
    lines.append("INTERVIEW SUMMARY")
    lines.append("=" * 60)

    lines.append("\n📌 TOPICS COVERED")
    lines.append("-" * 40)
    for i, topic in enumerate(summary.get("topics_covered", []), 1):
        lines.append(f"  {i}. {topic}")

    profile = summary.get("profile", {})
    lines.append("\n👤 CANDIDATE PROFILE")
    lines.append("-" * 40)
    lines.append(f"  Role: {profile.get('role', 'N/A')}")
    lines.append(f"  Why: {profile.get('justification', 'N/A')}")

    lines.append("\n📝 CANDIDATE SUMMARY")
    lines.append("-" * 40)
    lines.append(f"  {summary.get('candidate_summary', 'N/A')}")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)

def main():
    if len(sys.argv) < 2:
        print("Usage: python summarizer.py <path_to_transcript.txt> [--json]")
        print("  --json   Optional: also save raw JSON to <transcript>_summary.json")
        sys.exit(1)

    transcript_path = sys.argv[1]
    save_json = "--json" in sys.argv

    if not os.path.exists(transcript_path):
        print(f"Error: File '{transcript_path}' not found.")
        sys.exit(1)

    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript = f.read()

    if len(transcript.strip()) < 50:
        print("Warning: Transcript appears very short. Results may be limited.")

    print(f"Processing transcript: {transcript_path}")
    print("Calling Groq API (llama-3.1-8b-instant)...\n")

    summary = summarize_transcript(transcript)
    formatted = format_output(summary)
    print(formatted)

    if save_json:
        json_path = transcript_path.replace(".txt", "_summary.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        print(f"\nJSON saved to: {json_path}")

if __name__ == "__main__":
    main()

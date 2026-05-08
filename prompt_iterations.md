# Prompt Iterations Log

Tested against both sample transcripts:
- **Transcript 1**: Prasanna Kumar — Frontend/Mobile Engineer (Angular, Ionic, React)
- **Transcript 2**: Krishna — Program/Project Manager (Ed-tech, fraud detection, BPO ops)

---

## Iteration 1 — Baseline Prose Prompt

### Prompt

```
You are a recruiter assistant. Read the following interview transcript and provide:
1. A list of topics discussed
2. The candidate's profile and role fit
3. A short summary of the candidate

Transcript:
"""
{transcript}
"""
```

### Input (excerpt — Transcript 1)
```
Candidate: Hi sir. My name is Prasanna Kumar. I have around nine plus years of experience in software development. My core technical expertise is on Angular, React and Ionic framework. I'm working with the backend by using Node.js, Express and .NET Core.
```

### Output
```
Topics discussed: Angular, React, mobile development, Capacitor, CSS, state management.

Profile: Prasanna Kumar seems to be a mid to senior level frontend developer with mobile experience.

Summary: Prasanna Kumar has nine years of experience in software development. He is skilled in Angular and React. He discussed various topics during the interview including Ionic and Tailwind CSS. He seems to be a solid candidate for frontend roles.
```

### What worked / what didn't
- **Worked:** Got the basic structure out. Topics and role were roughly correct.
- **Didn't work:** Output was unstructured prose — hard to parse programmatically. "Topics" were just buzzword keywords, not meaningful themes (e.g., "state management" instead of "React state management strategy with Context API and React Query"). The candidate summary was vague and generic ("solid candidate"). No mention of weaknesses. Transcript 2 (PM role) produced similarly shallow output — no mention of fraud detection initiative or vendor management depth.
- **Change for next version:** Force JSON output and give explicit field definitions so both transcripts produce consistent, parseable structure.

---

## Iteration 2 — JSON Output + Field Definitions

### Prompt

```
You are an expert recruiter. Analyze the interview transcript below and return a JSON object with three keys:

- "topics_covered": list of strings (main themes discussed)
- "profile": string (role and seniority with one sentence justification)
- "candidate_summary": string (3–5 sentences on background, strengths, weaknesses, impression)

Return ONLY the JSON. No explanation.

Transcript:
"""
{transcript}
"""
```

### Input (excerpt — Transcript 2)
```
Candidate: From scratch to ISO certification. Building a CRM, drafting KRAs and KPIs, building dashboard for fraud detection. Sales team did fraudulent activities like punching fake documents. We built FTP risk score, implemented in CRM. Drafted BRD requirements to product team. Enrolled 22 vendors at pan India level.
```

### Output
```json
{
  "topics_covered": ["CRM implementation", "fraud detection", "vendor management", "KPIs", "stakeholder communication"],
  "profile": "Program Manager — mid-level. Has handled end-to-end project delivery including CRM rollouts and fraud detection systems.",
  "candidate_summary": "Krishna has around 5–7 years of operations and program management experience in ed-tech. He demonstrated strong initiative in building fraud detection systems and enrolling vendors. He appears confident in stakeholder communication and data-driven decision making. Some concerns around communication style and use of jargon in English were flagged by the interviewer."
}
```

### What worked / what didn't
- **Worked:** JSON output was clean and parseable. Topics were now meaningful themes, not just keywords. The summary for Transcript 2 was much richer — it captured the fraud detection initiative and the interviewer's communication feedback.
- **Didn't work:** `profile` was a single string mixing role + justification — harder to display or filter programmatically. For Transcript 1, topics were still a bit surface-level (e.g., "Capacitor" as a topic rather than "Capacitor image capture and file system plugin workflow"). Candidate summary occasionally drifted to assumptions ("5–7 years") rather than strictly using transcript evidence.
- **Change for next version:** Split `profile` into `role` and `justification` sub-fields. Add an explicit instruction to ground all claims in transcript evidence only. Tighten topic specificity with an example.

---

## Iteration 3 — Structured Profile Object + Evidence Grounding (Final)

### Prompt

```
You are an expert technical recruiter and interview analyst. You will be given a raw interview transcript and must produce a structured summary.

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
"""
{transcript}
"""
```

### Input — Transcript 1 (Prasanna Kumar, full transcript)

*(Full transcript used — see `sample_transcript_assignment_1.txt`)*

### Output — Transcript 1
```json
{
  "topics_covered": [
    "AI-assisted development workflow with Cursor and GitHub Copilot",
    "Ionic v7 mobile dashboard with responsiveness and virtual scroll",
    "Capacitor image capture and file system sync workflow",
    "Tailwind CSS design system and utility-first approach",
    "Angular modular architecture and lazy loading",
    "React state management with Context API and React Query",
    "Redux slice and Zustand familiarity"
  ],
  "profile": {
    "role": "Frontend/Mobile Engineer — mid-level",
    "justification": "Prasanna has 9 years of experience focused on Angular, React, and Ionic with Capacitor, with solid command of component architecture and state management. He is hands-on with AI coding assistants but showed hesitation when asked to write Zustand and Redux slice code from scratch, suggesting mid-level depth rather than senior."
  },
  "candidate_summary": "Prasanna Kumar is a software developer with nine years of experience specializing in Angular, React, and Ionic/Capacitor for cross-platform mobile applications. He demonstrated strong conceptual knowledge of component architecture, lazy loading, state management with RxJS and React Query, and AI-assisted development using Cursor and GitHub Copilot. His answers were generally structured but often high-level — when asked to write live code for Capacitor file system operations or a Redux slice, he struggled to produce clean, complete snippets under pressure. A notable gap is limited hands-on experience with Zustand, which he explicitly acknowledged. Overall, he appears a capable mid-level engineer for Ionic/Angular-heavy projects but may need support in code-level depth for senior React roles."
}
```

### Output — Transcript 2
```json
{
  "topics_covered": [
    "End-to-end fraud detection system design and implementation",
    "Vendor sourcing, onboarding, and underperformance management",
    "Cross-functional stakeholder alignment and conflict resolution",
    "BPO and calling operations optimization with predictive dialing",
    "KPI definition and executive dashboard reporting",
    "Prioritization under conflicting stakeholder demands",
    "CRM implementation and operational process improvement"
  ],
  "profile": {
    "role": "Program/Operations Manager — mid-level",
    "justification": "Krishna has approximately 5–6 years of experience spanning ed-tech operations, fraud detection unit leadership, and CRM rollouts. He demonstrates broad ownership across vendor management, analytics, and cross-team coordination, consistent with a mid-level program manager growing into senior responsibilities."
  },
  "candidate_summary": "Krishna is an operations and program management professional with a background in ed-tech, having progressed from associate operations roles to leading a fraud detection and prevention unit from scratch. His most notable achievement was designing a proprietary risk scoring system integrating CIBIL, Experian, telecom APIs, and Truecaller, which reduced manual audits significantly. He also demonstrated strong vendor management instincts — enrolling 22 vendors, handling underperformance diplomatically, and navigating a major fraud case against pushback from leadership. A concern flagged by the interviewer is his tendency to use Hindi jargon during explanations, which could hinder communication in senior stakeholder or leadership settings. Overall, he is a resourceful and data-driven operator with strong delivery credentials, but will need to polish executive communication to succeed in higher-level program management roles."
}
```

### What worked / what didn't
- **Worked:** Both transcripts now produce specific, evidence-grounded output. Topics are precise and role-specific. The `profile` split makes the output easy to display. The candidate summary reliably covers all four required dimensions (background, strengths, concerns, impression) for both transcripts. The evidence-grounding rule prevented hallucinated years-of-experience on Transcript 2.
- **Didn't work (minor):** For very short or fragmented transcripts (e.g., if only 5 exchanges exist), topics may still be slightly generic. The model occasionally adds markdown fences around JSON despite instructions — handled in code with a strip step.
- **This is the final version** used in `summarizer.py`.

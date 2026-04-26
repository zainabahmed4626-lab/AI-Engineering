from pathlib import Path

base = Path(
    r"C:/Users/zaine/OneDrive/Documents/AI_Engineering_Super1/ai_env/Ai_Engineering_Part1/hf_spaces"
)
base.mkdir(exist_ok=True)

spaces = {
    "ai-textbook-rag-studio-demo": {
        "title": "AI Textbook RAG Studio Demo",
        "emoji": "📚",
        "colorFrom": "indigo",
        "colorTo": "blue",
        "sdk": "gradio",
        "app_file": "app.py",
        "pinned": True,
        "app": """import gradio as gr

KNOWLEDGE = [
    {"source": "RAG Basics", "text": "Retrieval-Augmented Generation combines vector search with LLM prompting to ground answers in external context."},
    {"source": "Chunking", "text": "Chunking strategy affects retrieval quality. Overlap helps preserve context between segments."},
    {"source": "Evaluation", "text": "RAG systems should be evaluated for groundedness, relevance, latency, and hallucination rate."},
    {"source": "Vector DB", "text": "Chroma, FAISS, and Pinecone are common vector stores used in production RAG pipelines."},
]


def retrieve(query: str):
    q = (query or "").lower().strip()
    if not q:
        return "Enter a question to run retrieval."

    scored = []
    for item in KNOWLEDGE:
        score = sum(1 for token in q.split() if token in item["text"].lower())
        scored.append((score, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = [x[1] for x in scored[:3]]

    lines = ["### Retrieved Context\\n"]
    for i, t in enumerate(top, start=1):
        lines.append(f"**{i}. {t['source']}**\\n{t['text']}\\n")

    answer = (
        "### Grounded Answer (Demo)\\n"
        + "This demo shows a recruiter-friendly RAG pattern: retrieve top context first, then answer using only that context."
    )
    return "\\n".join(lines + [answer])


with gr.Blocks(title="AI Textbook RAG Studio Demo") as demo:
    gr.Markdown("# 📚 AI Textbook RAG Studio Demo\\nAsk a question and inspect retrieved context.")
    q = gr.Textbox(label="Question", placeholder="How should I evaluate a RAG system?")
    out = gr.Markdown()
    gr.Button("Run Retrieval").click(retrieve, inputs=q, outputs=out)

if __name__ == "__main__":
    demo.launch()
""",
    },
    "contract-analysis-ai-demo": {
        "title": "Contract Analysis AI Demo",
        "emoji": "📄",
        "colorFrom": "gray",
        "colorTo": "indigo",
        "sdk": "gradio",
        "app_file": "app.py",
        "pinned": True,
        "app": """import gradio as gr

RISK_RULES = [
    ("auto-renew", "Medium", "Auto-renewal detected. Add explicit termination notice window."),
    ("unlimited liability", "High", "Unlimited liability detected. Cap liability to reduce risk."),
    ("indemnify", "Medium", "Indemnification clause detected. Verify scope and carve-outs."),
    ("exclusive jurisdiction", "Low", "Jurisdiction clause found. Confirm venue is acceptable."),
]


def analyze(contract_text: str):
    text = (contract_text or "").lower()
    findings = []
    for needle, severity, recommendation in RISK_RULES:
        if needle in text:
            findings.append((severity, needle, recommendation))

    if not findings:
        return "No rule-based risk flags found in this demo pass."

    lines = ["### Risk Findings"]
    for sev, needle, rec in findings:
        lines.append(f"- **{sev}**: `{needle}` -> {rec}")
    lines.append("\\n_This is a lightweight demo of clause detection logic used in contract AI workflows._")
    return "\\n".join(lines)


with gr.Blocks(title="Contract Analysis AI Demo") as demo:
    gr.Markdown("# 📄 Contract Analysis AI Demo\\nPaste contract text to flag high-risk clauses.")
    txt = gr.Textbox(lines=10, label="Contract Text")
    out = gr.Markdown()
    gr.Button("Analyze").click(analyze, inputs=txt, outputs=out)

if __name__ == "__main__":
    demo.launch()
""",
    },
    "habitflow-ai-coach-demo": {
        "title": "HabitFlow AI Coach Demo",
        "emoji": "🧠",
        "colorFrom": "pink",
        "colorTo": "purple",
        "sdk": "gradio",
        "app_file": "app.py",
        "pinned": True,
        "app": """import gradio as gr


def coach(goal: str, days_per_week: int, blockers: str):
    goal = (goal or "Build consistency").strip()
    blockers = (blockers or "time and energy dips").strip()
    days = max(1, min(7, int(days_per_week)))

    plan = f\"\"\"### Personalized Habit Plan (Demo)
**Goal:** {goal}
**Cadence:** {days} days/week

1. Start with a 10-minute version of your habit.
2. Anchor it to an existing routine (same time/place).
3. Track completion daily with a simple yes/no check.
4. Pre-plan a fallback action for: {blockers}.
5. Review progress weekly and increase difficulty by 5-10%.

**Coach Note:** Consistency beats intensity. Build streak confidence first.
\"\"\"
    return plan


with gr.Blocks(title="HabitFlow AI Coach Demo") as demo:
    gr.Markdown("# 🧠 HabitFlow AI Coach Demo\\nGenerate a behavior-focused habit plan in seconds.")
    goal = gr.Textbox(label="Primary Goal", placeholder="Study AI engineering for job interviews")
    days = gr.Slider(1, 7, value=5, step=1, label="Days per week")
    blockers = gr.Textbox(label="Main blockers", placeholder="Low energy after work")
    out = gr.Markdown()
    gr.Button("Generate Plan").click(coach, inputs=[goal, days, blockers], outputs=out)

if __name__ == "__main__":
    demo.launch()
""",
    },
    "zainab-ai-portfolio": {
        "title": "Zainab AI Portfolio",
        "emoji": "🚀",
        "colorFrom": "yellow",
        "colorTo": "red",
        "sdk": "gradio",
        "app_file": "app.py",
        "pinned": True,
        "app": """import gradio as gr

PORTFOLIO = [
    ("🧬 Digital Twin with RAG + Tools", "https://huggingface.co/spaces/Zainab4626/my-first-digital-twin", "Persona-grounded assistant with retrieval and tool-calling workflows."),
    ("📚 AI Textbook RAG Studio Demo", "https://huggingface.co/spaces/Zainab4626/ai-textbook-rag-studio-demo", "Retrieval-first QA demo with context inspection."),
    ("⚖️ Contract Analysis AI (Custom UI)", "https://huggingface.co/spaces/Zainab4626/auto-legal-analyst-custom-ui", "Full React/Vite UI for contract intelligence storytelling + interactive demo."),
    ("🌱 HabitBloom (Custom UI)", "https://huggingface.co/spaces/Zainab4626/habitbloom-custom-ui", "Full React/Vite UI + Supabase-backed habit tracking + AI coaching workflows."),
]


def render_portfolio():
    lines = [
        "# 🚀 Zainab Ahmed Safeer — AI Engineer Portfolio",
        "I build **production-minded AI systems**: grounded retrieval, tool calling, evaluation discipline, and full-stack delivery.\\n",
        "## Featured demos (click each)",
    ]
    for title, url, desc in PORTFOLIO:
        lines.append(f"- **{title}**\\n  - {desc}\\n  - {url}")
    lines.append(
        "\\n## What recruiters should look for (technical checklist)\\n"
        "- **Grounding**: retrieval-first prompting and explicit context stitching\\n"
        "- **Tooling**: function calling for real workflows (notifications, automation)\\n"
        "- **Data contracts**: schema validation + defensive parsing for LLM outputs\\n"
        "- **Security**: least privilege, secrets in Space settings, multi-tenant isolation patterns\\n"
        "- **Shipping**: Docker Spaces for full-fidelity UIs + reproducible builds\\n"
    )
    lines.append(
        "\\n## Repo mirrors (HF Datasets)\\n"
        "- https://huggingface.co/datasets/Zainab4626/AI-Engineering\\n"
        "- https://huggingface.co/datasets/Zainab4626/auto-legal-analyst\\n"
        "- https://huggingface.co/datasets/Zainab4626/habit-bloom-464\\n"
    )
    lines.append(
        "\\n## Notes\\n"
        "- The lightweight Gradio demos are intentionally small and fast to run.\\n"
        "- The **custom UI** Spaces are Dockerized Vite apps for full product fidelity.\\n"
    )
    return "\\n".join(lines)


with gr.Blocks(title="Zainab AI Portfolio") as demo:
    gr.Markdown(render_portfolio())

if __name__ == "__main__":
    demo.launch()
""",
    },
}

README_APPEND = {
    "ai-textbook-rag-studio-demo": """

## At a glance (what this Space is)

- **Goal**: show a recruiter-friendly “RAG loop” without hiding the mechanics.
- **Runtime**: pure Python + Gradio (fast cold start, easy to read).
- **Retrieval model**: intentionally **not** embeddings/ANN — lexical overlap is a stand-in for vector search.

## System anatomy (map this to production RAG)

1. **Corpus**: a tiny in-memory knowledge base (`KNOWLEDGE` list) with `source` + `text`.
2. **Candidate generation**: score chunks by token overlap with the user query (proxy for similarity search).
3. **Context packaging**: render the top-k chunks as explicit “retrieved context”.
4. **Answer policy (demo)**: the UI explains the *engineering constraint* — answers should be grounded in retrieved text.

## What I would change for production

- **Embeddings + ANN**: replace overlap scoring with `text-embedding-*` + FAISS/Chroma/Pinecone (metadata filters, hybrid BM25+dense).
- **Chunking policy**: document-type aware chunk sizes, overlap tuned to semantics, stable IDs, deduping.
- **Reranking**: cross-encoder rerank on top-k to reduce “almost relevant” false positives.
- **Observability**: log retrieval IDs, scores, prompt versions, model params, latency, token usage.
- **Evaluation**: groundedness checks, citation correctness, refusal behavior, regression suites on fixed queries.

## Interview talking points (recruiter-ready)

- “I can explain the difference between **retrieval quality** problems vs **generation** problems.”
- “I design UX that forces **inspectable context** before the model answers.”

""",
    "contract-analysis-ai-demo": """

## At a glance (what this Space is)

- **Goal**: demonstrate **risk triage UX** + **explainability** for contract workflows.
- **Engine**: deterministic **keyword/rule triggers** (fast, transparent, debuggable).
- **Not a claim**: this is not a full legal reasoning engine — it’s a recruiter-friendly slice of the *product problem*.

## Why deterministic scanning still matters in LLM systems

- **Latency + cost**: cheap pre-filters and structured checks before expensive model calls.
- **Auditability**: triggers are inspectable (“why did we flag this?”).
- **Safety**: reduces “model invents a clause” failure modes when paired with extraction/grounding.

## How this maps to a production contract AI stack

1. **Ingestion**: PDF text extraction + layout-aware parsing (tables/headers) + OCR fallback when needed.
2. **Normalization**: de-hyphenation, whitespace cleanup, section detection.
3. **Clause typing**: classify spans (termination, liability, indemnity, jurisdiction, payment…).
4. **Risk scoring**: combine rules + model uncertainty + business policy thresholds.
5. **Human-in-the-loop**: reviewer UI, comments, approvals, export trails.

## Full-fidelity UI (Docker Space)

For the full React/Vite product storytelling + interactive demo:

- https://huggingface.co/spaces/Zainab4626/auto-legal-analyst-custom-ui

## Source of truth (repo mirror)

- https://huggingface.co/datasets/Zainab4626/auto-legal-analyst

""",
    "habitflow-ai-coach-demo": """

## At a glance (what this Space is)

- **Goal**: show how “AI coach” outputs should be **structured**, **actionable**, and **reviewable**.
- **Engine**: template-based plan generator (no external model call) — emphasizes UX + habit science framing.

## Product engineering signals (even without an LLM call)

- **Constraints in the UI**: cadence slider, blockers field → forces specificity.
- **Action design**: tiny habits, anchoring, fallback plans, weekly review loops.
- **Safety**: avoids medical claims; keeps guidance general and user-directed.

## How this maps to a production coaching product

1. **Personalization inputs**: goals, schedule, energy patterns, constraints, preferences.
2. **Grounding**: pull recent adherence logs + streak context from storage (not generic advice).
3. **Structured generation**: JSON schema outputs validated on the client/server (Zod / pydantic).
4. **Tooling**: calendar holds, reminders, integrations (email/push), analytics exports.
5. **Evaluation**: user satisfaction, adherence lift, churn, harmful advice monitoring.

## Full-fidelity UI (Docker Space)

For the full React/Vite UI + Supabase-backed workflows:

- https://huggingface.co/spaces/Zainab4626/habitbloom-custom-ui

## Source of truth (repo mirror)

- https://huggingface.co/datasets/Zainab4626/habit-bloom-464

""",
    "zainab-ai-portfolio": """

## How to use this hub (2 minutes)

1. Open **custom UI** Spaces first — they best represent full-stack product engineering on Hugging Face.
2. Open the **digital twin** Space for **RAG + tool calling** patterns grounded in a persona document.
3. Skim **dataset mirrors** if you want repo-level browsing without leaving Hugging Face.

## Featured Spaces (what to evaluate technically)

### Digital twin — RAG + tools

- **Space**: https://huggingface.co/spaces/Zainab4626/my-first-digital-twin
- **Stack**: Gradio UI, OpenAI client, optional Chroma vector store, `text-embedding-3-small`, PDF ingestion via `pypdf`, tool calling (Pushover notification + dice roll demo tool).
- **Engineering highlights**: explicit system grounding text, chunking with overlap, retrieval stitching in the response path, graceful degradation if keys/db are unavailable.

### AI Textbook RAG Studio (toy retrieval loop)

- **Space**: https://huggingface.co/spaces/Zainab4626/ai-textbook-rag-studio-demo
- **Purpose**: teach the RAG loop with inspectable retrieved context (overlap scoring stands in for embeddings).

### Contract Analysis — full UI

- **Space (Docker/Vite)**: https://huggingface.co/spaces/Zainab4626/auto-legal-analyst-custom-ui
- **Dataset mirror**: https://huggingface.co/datasets/Zainab4626/auto-legal-analyst

### HabitBloom — full UI

- **Space (Docker/Vite + Supabase)**: https://huggingface.co/spaces/Zainab4626/habitbloom-custom-ui
- **Dataset mirror**: https://huggingface.co/datasets/Zainab4626/habit-bloom-464

## Repo mirrors (HF Datasets)

- https://huggingface.co/datasets/Zainab4626/AI-Engineering
- https://huggingface.co/datasets/Zainab4626/auto-legal-analyst
- https://huggingface.co/datasets/Zainab4626/habit-bloom-464

## “Production mindset” checklist (what I optimize for)

- Grounding + citations, eval harnesses, latency/cost, observability, schema validation, least-privilege secrets, and deployable UX.

""",
}

for slug, meta in spaces.items():
    d = base / slug
    d.mkdir(parents=True, exist_ok=True)
    readme = f"""---
title: {meta["title"]}
emoji: {meta["emoji"]}
colorFrom: {meta["colorFrom"]}
colorTo: {meta["colorTo"]}
sdk: {meta["sdk"]}
app_file: {meta["app_file"]}
pinned: {str(meta["pinned"]).lower()}
---

# {meta["title"]}

Recruiter-facing showcase by **Zainab Ahmed Safeer** — each Space is designed to make the engineering decisions visible (not just the UI).
"""
    readme += README_APPEND.get(slug, "")
    (d / "README.md").write_text(readme, encoding="utf-8")
    (d / "app.py").write_text(meta["app"], encoding="utf-8")
    (d / "requirements.txt").write_text("gradio\n", encoding="utf-8")

print(f"created {len(spaces)} space folders at {base}")

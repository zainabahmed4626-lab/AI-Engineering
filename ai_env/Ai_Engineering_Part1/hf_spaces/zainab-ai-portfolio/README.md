---
title: Zainab AI Portfolio
emoji: 🚀
colorFrom: yellow
colorTo: red
sdk: gradio
app_file: app.py
pinned: true
---

# Zainab AI Portfolio

Recruiter-facing showcase by **Zainab Ahmed Safeer** — each Space is designed to make the engineering decisions visible (not just the UI).


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


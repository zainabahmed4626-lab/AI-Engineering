---
title: My Digital Twin
emoji: 🧬
colorFrom: yellow
colorTo: red
sdk: gradio
app_file: app.py
pinned: true
short_description: Persona twin — Gradio, optional Chroma RAG, OpenAI tools
---

# Digital Twin — RAG + Tool Calling (Gradio Space)

Live Space: https://huggingface.co/spaces/Zainab4626/my-digital-twin

This Space is a **small but complete LLM application** that demonstrates how I think about **grounding**, **retrieval**, and **tool execution** in a user-facing chat product.

## What a recruiter can verify in 5 minutes

- **Grounded persona**: a fixed profile document is injected as system context (first-person “digital twin” behavior).
- **Dynamic context**: lightweight keyword routing adds extra topic snippets when user messages match curated keys.
- **Optional RAG**: Chroma stores embedded chunks from the system prompt (and optional PDFs when present) and retrieves top passages into the system message before generation.
- **Tool calling**: OpenAI tool calls are executed in a loop until the model returns a normal assistant message (Pushover notification tool + a simple dice tool).

## Stack (libraries + responsibilities)

- **Gradio `ChatInterface`**: fastest path to a credible demo UX on Hugging Face.
- **`openai` Python SDK**: chat completions + embeddings + tool calling loop.
- **`chromadb`**: ephemeral vector index for demo retrieval (rebuilt on cold start when keys are available).
- **`pypdf`**: optional PDF text extraction when resume/profile PDFs exist in the Space file root.
- **`requests`**: server-side HTTP call for optional Pushover notifications.

## Runtime flow (high level)

1. **System prompt assembly**: persona document + safety instructions (“don’t invent facts”).
2. **Topic augmentation**: substring match against `Topic_Context` adds short grounded snippets.
3. **Retrieval (optional)**:
   - Chunk `system_message` with overlap (`max_chars`, `overlap`).
   - Embed chunks with `text-embedding-3-small`, store in Chroma, query with the user message embedding.
   - Stitch retrieved chunk text into the system message with explicit instructions to use it only when supportive.
4. **Generation + tools**:
   - Call `gpt-4.1-mini` with `tools=[...]`.
   - While the assistant message contains `tool_calls`, execute tools, append tool results, and continue until a final natural-language answer.

## Hugging Face configuration (secrets)

Configure these in **Space Settings → Variables and secrets**:

- **`OPENAI_API_KEY`**: required for chat + embeddings + tool calling.
- **`PUSHOVER_USER` / `PUSHOVER_TOKEN`**: optional; enables the `send_notification` tool end-to-end.

If `OPENAI_API_KEY` is missing, the app returns a clear setup message (cold start should not look “broken”).

## Engineering notes / limitations (intentionally honest)

- **Ephemeral vector store**: Chroma is recreated on startup for demo simplicity (not a durable multi-tenant production database).
- **Keyword topic routing**: intentionally simple; production would use classification, memory, or structured user profile fields.
- **Model choice**: pinned to `gpt-4.1-mini` for responsiveness; production would add routing, caching, eval gates, and cost controls.

## Optional documents

If you upload either of these filenames to the Space root, they will be chunked + embedded alongside the persona context:

- `linkedinPDFprofile.pdf`
- `Zainab_Ahmed_Safeer_AI_Engineer_ResumeV2.pdf`

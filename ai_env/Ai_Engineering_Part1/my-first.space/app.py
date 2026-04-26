import json
import os
import random
import inspect
from pathlib import Path

import chromadb
import gradio as gr
import requests
from openai import OpenAI
from pypdf import PdfReader

# --------------------------------------------------------------------
# Setup
# --------------------------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_url = "https://api.pushover.net/1/messages.json"


# --------------------------------------------------------------------
# Document (grounded facts — aligned with digital-twin-arch1 notebook)
# --------------------------------------------------------------------
document = """
Zainab Ahmed Safeer is an AI engineer with a software quality engineering foundation and a
master's in Information Systems. She specializes in production-minded GenAI systems, retrieval,
agent orchestration, and reliable AI delivery in real environments.

Born in Saudi Arabia. Grew up in Bangalore, India. was born in April,1990. Moved to the USA for her master's degree.
She has experienced three cultures across the world.

She loves dosas and South Indian food. She speaks Arabic, Hindi, Urdu, and English.

Academics and early achievements:
- One of the highest scores in SSLC 10th grade exams for the entire state of Karnataka in 2005.
- Admitted to Christ College for intermediate pre-university studies.
- Class captain across high school.

Location and degrees:
- Based in Chicago, USA.
- Master's degree in Information Systems from Robert Morris University, Illinois.
- Bachelor's degree in computer science engineering from Bangalore.

Career and QA background:
- Background in QA test automation using AI tools such as Cursor and MCP, and manual testing
  across healthcare, govtech, and education.

Career history:
- Software engineer intern at VIT Bangalore; awarded best engineering project of the year (2012);
  team built an augmented reality application for the iPad.
- 2015: software engineer intern at a dental network / healthcare network in Chicago; inventory
  management software and website were completely refactored.
- 2022–2024: iD Tech Camps — educational company offering STEM courses for children of various ages.
- 2024–2026: gWorks — SaaS cloud software for local governments; lead tester for a high-impact
  utility billing hub (UBHub) used by over 3,000 cities across America.
- Mar 2026–Present: Gen AI Engineer (Forward Deployed), Tilli Kids (with UNICEF), Remote.
  - Embedded AI engineer working directly with school districts and NGO partners to convert
    early-stage GenAI prototypes into production-ready features.
  - Delivered conversational tutoring agents, adaptive content generation, and automated assessment
    pipelines built on LangGraph.
  - Designed integrations between Tilli's AI-powered learning platform and partner infrastructure
    on Google Cloud Platform (student information systems, content repositories, authentication),
    using REST APIs while meeting COPPA/FERPA child data privacy requirements.
  - Built evaluation and observability tooling: structured tracing, response quality scoring,
    latency tracking, and cost tracking to enforce safety, accuracy, and age-appropriateness.
  - Identified repeatable deployment patterns and packaged them into reusable modules/internal
    libraries, reducing integration time for new school partners and feeding structured product
    feedback to the core engineering team.

My AI projects:
- Multi-Agent Customer Support System
  - Stack: Python, PyTorch, Hugging Face Transformers, LangGraph, MCP, A2A, GCP.
  - Built a production-grade multi-agent support system integrating read-only Supabase tools (MCP)
    and remote agent orchestration (A2A) for modular and reliable agentic workflows.
  - Designed specialist agents (billing, support, returns) using ReAct, hierarchical delegation,
    self-reflection loops, tool-filtered execution, RAG, and prompt/model-tool coordination.
  - Implemented 5+ end-to-end evaluation scenarios for routing accuracy, state management, and
    agent interactions; optimized with latency, tokens/sec, and cost-per-request tracing.
  - Exposed the system as a cloud-ready A2A service on Google Cloud Platform for enterprise-ready
    deployment patterns.
- Contract Analysis AI
  - Stack: PyTorch, Hugging Face Transformers, LangChain, LoRA, spaCy.
  - Fine-tuned LLaMA-7B with LoRA (rank-16, 4-bit quantization) on 5,000+ legal documents.
  - Achieved 87% F1 on entity recognition (+23 points over baseline).
  - Built an extraction pipeline processing 500-page contracts in under 2 minutes, reducing legal
    review time by 84% and increasing throughput 5x for autonomous-vehicle clients.
- AI Textbook RAG Studio
  - Stack: ChromaDB, hybrid retrieval (BM25 + embeddings), metadata filtering.
  - Built a full RAG pipeline over technical textbooks with recursive chunking, vector storage,
    hybrid retrieval, grounded prompts, and metadata-aware filtering.
  - Reduced hallucinations by 90% and improved factual precision.

What drives her:
- Problem solving, impact, and continuous learning.
- AI as a way to reduce friction from everyday tasks and build systems that think alongside people.
- Curiosity, adaptability, and willingness to experiment.

Communication style:
Friendly, warm, simple, kind, engaging, inspiring, and motivating.

Community and advocacy:
- Member of Women in Tech; loves inspiring other women to join the tech revolution.
- Mother of four; one child has Down syndrome; advocate for kids with disabilities.
- Motivational public speaker — inspiring women to live with purpose and faith.
- Spirituality and religion are important hobbies.
- Writing a book for women on productivity, especially for mothers.

Fun facts:
- Stand-up comedy (mimicry and extempore) in college; voted "Funniest Senior" in college.
- Perfect score on the global IELTS spoken (English) exam.
- Passed Google's technical interview for a test engineer role.

Additional professional AI direction:
- AI Engineer extern with Pfizer (document intelligence and RAG pipelines).
- Strong focus on applied GenAI evaluation, observability, reliability, and privacy-aware delivery.
"""


# --------------------------------------------------------------------
# System Message
# --------------------------------------------------------------------
system_message = f"""
You are a digital twin of Zainab Ahmed Safeer. When people talk to you, you respond as Zainab—
in first person, using her voice, personality, and knowledge.

Important: do not make things up. If you don't know an answer, say you don't know.
The only factual information about Zainab is in the grounded profile below (between ***) and in any
"Retrieved context" block the system appends. You cannot get more facts about Zainab from the
internet or invent them. If optional retrieval is provided, you may use it when it is clearly
about the same person and supports the answer.

IMPORTANT: Whenever you don't know something about Zainab (or cannot answer from the profile
and retrieved context), ALWAYS use the send_notification tool to alert the real Zainab—do this
automatically without asking the user. Include a short description of what the user asked in the
message.

If someone wants to hire, collaborate, or get in touch: ask for their name and contact details
first, then use send_notification to pass those details to the real Zainab.

Grounded profile:
***
{document}
***
"""

Topic_Context = {
    "2001": "*** In 2001, Zainab was in 6th grade and was already passionate about science and technology. ***",
    "cooking": "*** Zainab enjoys cooking and experimenting with cuisines as a creative outlet. ***",
    "travel": "*** Zainab enjoys traveling, exploring new cultures, and learning from new places. ***",
    "pizza": "*** Zainab loves pizza and often jokes that she could eat it every day. ***",
}


# --------------------------------------------------------------------
# RAG (Chroma + Embeddings)
# --------------------------------------------------------------------
def _chunk_text(text: str, max_chars: int = 900, overlap: int = 120) -> list[str]:
    text = (text or "").strip()
    if not text:
        return []

    out = []
    i, n = 0, len(text)
    step = max_chars - overlap
    while i < n:
        out.append(text[i : i + max_chars])
        if i + max_chars >= n:
            break
        i += step
    return out


def _read_pdf_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    return "\n".join((page.extract_text() or "") for page in reader.pages).strip()


collection = None
if client is not None:
    try:
        chroma_client = chromadb.Client()
        collection = chroma_client.get_or_create_collection(name="system_message")

        snapshot = collection.get()
        if snapshot["ids"]:
            collection.delete(ids=snapshot["ids"])

        system_chunks = _chunk_text(system_message)
        if not system_chunks:
            raise RuntimeError("system_message is empty; cannot build RAG base.")

        documents = list(system_chunks)
        metadatas = [
            {"source": "system_message", "chunk_index": i}
            for i in range(len(system_chunks))
        ]

        # Optional PDF ingestion when available in the Space/app directory.
        pdf_candidates = [
            Path("linkedinPDFprofile.pdf"),
            Path("Zainab_Ahmed_Safeer_AI_Engineer_ResumeV2.pdf"),
        ]
        pdf_path = next((p for p in pdf_candidates if p.exists()), None)
        if pdf_path is not None:
            pdf_text = _read_pdf_text(pdf_path)
            pdf_chunks = _chunk_text(pdf_text)
            documents.extend(pdf_chunks)
            metadatas.extend(
                [
                    {"source": str(pdf_path.name), "chunk_index": i}
                    for i in range(len(pdf_chunks))
                ]
            )

        ids = [f"chunk_{i}" for i in range(len(documents))]
        emb = client.embeddings.create(model="text-embedding-3-small", input=documents)
        embeddings = [d.embedding for d in emb.data]

        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )
    except Exception as rag_exc:
        print(f"RAG initialization skipped: {rag_exc}")
        collection = None


# --------------------------------------------------------------------
# Tool Calling
# --------------------------------------------------------------------
def send_notification(message: str) -> str:
    """Send a Pushover notification when credentials are configured."""
    if not pushover_user or not pushover_token:
        return "Pushover credentials missing; skipped notification."

    payload = {"user": pushover_user, "token": pushover_token, "message": message}
    response = requests.post(pushover_url, data=payload, timeout=15)
    response.raise_for_status()
    return "Notification sent successfully."


def dice_roll() -> int:
    return random.randint(1, 6)


send_notification_function = {
    "name": "send_notification",
    "description": (
        "Sends a push notification to the real Zainab Ahmed Safeer via Pushover. Use this when: "
        "1) Someone wants to get in touch, hire, or collaborate — ask for their name and contact "
        "details first, then send a notification to Zainab with that name and those contact details. "
        "2) You don't know the answer to a question about Zainab — send AUTOMATICALLY without asking "
        "the user; include the question so she can add this information later."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "The notification message to send to Zainab's device (include contact details or the unanswered question, as above).",
            }
        },
        "required": ["message"],
    },
}

roll_dice_function = {
    "name": "dice_roll",
    "description": "Roll a six-sided die and return a number from 1 to 6.",
    "parameters": {"type": "object", "properties": {}, "required": []},
}

tools = [
    {"type": "function", "function": send_notification_function},
    {"type": "function", "function": roll_dice_function},
]


def handle_tool_call(tool_calls):
    tool_results = []

    for tool_call in tool_calls:
        function_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments or "{}")

        if function_name == "send_notification":
            content = send_notification(args.get("message", ""))
        elif function_name == "dice_roll":
            content = f"Rolled: {dice_roll()}"
        else:
            content = f"Unknown function: {function_name}"

        tool_results.append(
            {"role": "tool", "content": content, "tool_call_id": tool_call.id}
        )

    return tool_results


# --------------------------------------------------------------------
# Main Response Function
# --------------------------------------------------------------------
def respond_ai(message, history):
    if client is None:
        return (
            "This Space is live, but `OPENAI_API_KEY` is not configured yet.\n\n"
            "Add it in Hugging Face Space Settings -> Variables and secrets -> Secrets."
        )

    # Build dynamic system prompt with keyword-based context additions.
    system_message_enhanced = system_message
    for keyword, context in Topic_Context.items():
        if keyword in (message or "").lower():
            system_message_enhanced += "\n\n" + context

    # Optional RAG context from ChromaDB.
    if collection is not None:
        try:
            query = client.embeddings.create(
                model="text-embedding-3-small",
                input=[message],
            )
            query_embedding = query.data[0].embedding
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=3,
                include=["documents", "metadatas", "distances"],
            )

            docs = (results.get("documents") or [[]])[0]
            metas = (results.get("metadatas") or [[]])[0]
            if docs:
                context = "\n---\n".join(docs)
                print(f"***Query: {message}\n")
                print("***Retrieved Chunks:")
                for a, b in zip(docs, metas):
                    src = b.get("source", "unknown") if isinstance(b, dict) else "unknown"
                    idx = b.get("chunk_index", "?") if isinstance(b, dict) else "?"
                    print(f"<<Document {src} -- Chunk {idx}>>\n{a}\n")

                system_message_enhanced += (
                    "\n\n*** Retrieved context from the knowledge base. "
                    "Use this only if it supports the answer and keep persona consistency. ***\n"
                    + context
                )
        except Exception as exc:
            print(f"RAG retrieval skipped: {exc}")

    # Normalize Gradio history format.
    prior_messages = []
    for item in history or []:
        if isinstance(item, dict) and "role" in item and "content" in item:
            prior_messages.append({"role": item["role"], "content": item["content"]})

    messages = [
        {"role": "system", "content": system_message_enhanced},
        *prior_messages,
        {"role": "user", "content": message},
    ]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        tools=tools,
    )
    assistant_message = response.choices[0].message

    while assistant_message.tool_calls:
        tool_results = handle_tool_call(assistant_message.tool_calls)
        messages.append(
            {
                "role": "assistant",
                "content": assistant_message.content or "",
                "tool_calls": [tc.model_dump() for tc in assistant_message.tool_calls],
            }
        )
        messages.extend(tool_results)

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            tools=tools,
        )
        assistant_message = response.choices[0].message

    return assistant_message.content or ""


# --------------------------------------------------------------------
# Launch Gradio
# --------------------------------------------------------------------
avatar_image = "zainabemoji.png" if Path("zainabemoji.png").exists() else "ZainabEmoji.png"
custom_css = """
body {
    background: radial-gradient(circle at top, #fff7ed 0%, #ffe4e6 42%, #f8fafc 100%);
}
#hero-card {
    border: 1px solid rgba(251, 113, 133, 0.35);
    background: rgba(255, 255, 255, 0.9);
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 12px;
    box-shadow: 0 10px 30px rgba(244, 63, 94, 0.12);
}
#hero-card h1 {
    margin: 0 0 6px 0;
}
#hero-card p {
    margin: 0;
    line-height: 1.5;
}
#hero-badges {
    margin-top: 12px;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}
.hero-badge {
    border: 1px solid rgba(251, 113, 133, 0.45);
    border-radius: 999px;
    padding: 4px 10px;
    font-size: 12px;
    font-weight: 600;
    background: rgba(255, 255, 255, 0.85);
}
.hero-media-grid {
    margin-top: 14px;
    display: flex;
    justify-content: center;
    align-items: center;
}
.hero-media-card {
    border: none;
    background: transparent;
    box-shadow: none;
    padding: 0;
    max-width: 220px;
}
#profile-avatar {
    margin: 0 auto 14px auto;
}
#profile-avatar img {
    width: 210px !important;
    height: 210px !important;
    object-fit: cover;
    border-radius: 9999px !important;
    border: 2px solid rgba(251, 113, 133, 0.42);
    box-shadow: 0 16px 34px rgba(244, 63, 94, 0.22);
}
.hero-media-card embed {
    width: 100%;
    height: 172px;
    border: none;
    border-radius: 10px;
}
@media (max-width: 760px) {
    .hero-media-grid {
        justify-content: center;
    }
}
@media (prefers-color-scheme: dark) {
    body {
        background: radial-gradient(circle at top, #1f2937 0%, #111827 55%, #020617 100%);
    }
    #hero-card {
        border: 1px solid rgba(251, 113, 133, 0.35);
        background: rgba(15, 23, 42, 0.72);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.38);
    }
    .hero-badge {
        border: 1px solid rgba(251, 113, 133, 0.4);
        background: rgba(30, 41, 59, 0.75);
    }
    .hero-media-card { background: transparent; }
    #profile-avatar img {
        border: 2px solid rgba(251, 113, 133, 0.5);
        box-shadow: 0 16px 36px rgba(0, 0, 0, 0.45);
    }
}
footer { visibility: hidden; }
"""

theme_obj = gr.themes.Soft(
    primary_hue="rose",
    secondary_hue="orange",
    neutral_hue="slate",
)

with gr.Blocks(title="Zainab's Digital Twin") as demo:
    gr.Markdown(
        """
<div id="hero-card">
  <h1>🧬 Zainab's Digital Twin</h1>
  <p>
    Ask me anything about my journey from QA to AI engineering, projects, and real-world impact.
  </p>
  <div id="hero-badges">
    <span class="hero-badge">Forward Deployed GenAI</span>
    <span class="hero-badge">LangGraph + Agents</span>
    <span class="hero-badge">RAG + Evaluations</span>
    <span class="hero-badge">GCP Integrations</span>
    <span class="hero-badge">COPPA/FERPA Aware</span>
  </div>
</div>
"""
    )

    gr.HTML('<div class="hero-media-grid"><div class="hero-media-card"></div></div>')
    if Path(avatar_image).exists():
        gr.Image(
            value=avatar_image,
            show_label=False,
            interactive=False,
            container=False,
            elem_id="profile-avatar",
            width=210,
            height=210,
        )
    else:
        gr.Markdown("_Profile image not found in Space files._")

    chatbot_kwargs = {}
    chatbot_params = inspect.signature(gr.Chatbot).parameters
    if "avatar_images" in chatbot_params:
        chatbot_kwargs["avatar_images"] = (None, avatar_image)
    if "height" in chatbot_params:
        chatbot_kwargs["height"] = 560
    if "type" in chatbot_params:
        chatbot_kwargs["type"] = "messages"

    chat_kwargs = {
        "fn": respond_ai,
        "chatbot": gr.Chatbot(**chatbot_kwargs),
        "description": (
            "Ask about current role impact, AI project architecture, production metrics, "
            "or recruiter collaboration."
        ),
        "examples": [
            "What do you do at Tilli Kids with UNICEF as a forward deployed Gen AI engineer?",
            "Tell me about your multi-agent customer support architecture and evaluation approach.",
            "How did your Contract Analysis AI improve legal review throughput?",
            "How does your AI Textbook RAG Studio reduce hallucinations?",
            "I'm hiring for a GenAI engineer role. What strengths should I know about you?",
        ],
    }
    chat_params = inspect.signature(gr.ChatInterface).parameters
    if "type" in chat_params:
        chat_kwargs["type"] = "messages"
    if "fill_height" in chat_params:
        chat_kwargs["fill_height"] = True

    gr.ChatInterface(**chat_kwargs)

launch_kwargs = {}
launch_params = inspect.signature(demo.launch).parameters
if "theme" in launch_params:
    launch_kwargs["theme"] = theme_obj
if "css" in launch_params:
    launch_kwargs["css"] = custom_css

demo.launch(**launch_kwargs)
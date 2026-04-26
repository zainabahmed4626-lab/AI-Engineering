import gradio as gr

PORTFOLIO = [
    ("🧬 Digital Twin with RAG + Tools", "https://huggingface.co/spaces/Zainab4626/my-first-digital-twin", "Persona-grounded assistant with retrieval and tool-calling workflows."),
    ("📚 AI Textbook RAG Studio Demo", "https://huggingface.co/spaces/Zainab4626/ai-textbook-rag-studio-demo", "Retrieval-first QA demo with context inspection."),
    ("⚖️ Contract Analysis AI (Custom UI)", "https://huggingface.co/spaces/Zainab4626/auto-legal-analyst-custom-ui", "Full React/Vite UI for contract intelligence storytelling + interactive demo."),
    ("🌱 HabitBloom (Custom UI)", "https://huggingface.co/spaces/Zainab4626/habitbloom-custom-ui", "Full React/Vite UI + Supabase-backed habit tracking + AI coaching workflows."),
]


def render_portfolio():
    lines = [
        "# 🚀 Zainab Ahmed Safeer — AI Engineer Portfolio",
        "I build **production-minded AI systems**: grounded retrieval, tool calling, evaluation discipline, and full-stack delivery.\n",
        "## Featured demos (click each)",
    ]
    for title, url, desc in PORTFOLIO:
        lines.append(f"- **{title}**\n  - {desc}\n  - {url}")
    lines.append(
        "\n## What recruiters should look for (technical checklist)\n"
        "- **Grounding**: retrieval-first prompting and explicit context stitching\n"
        "- **Tooling**: function calling for real workflows (notifications, automation)\n"
        "- **Data contracts**: schema validation + defensive parsing for LLM outputs\n"
        "- **Security**: least privilege, secrets in Space settings, multi-tenant isolation patterns\n"
        "- **Shipping**: Docker Spaces for full-fidelity UIs + reproducible builds\n"
    )
    lines.append(
        "\n## Repo mirrors (HF Datasets)\n"
        "- https://huggingface.co/datasets/Zainab4626/AI-Engineering\n"
        "- https://huggingface.co/datasets/Zainab4626/auto-legal-analyst\n"
        "- https://huggingface.co/datasets/Zainab4626/habit-bloom-464\n"
    )
    lines.append(
        "\n## Notes\n"
        "- The lightweight Gradio demos are intentionally small and fast to run.\n"
        "- The **custom UI** Spaces are Dockerized Vite apps for full product fidelity.\n"
    )
    return "\n".join(lines)


with gr.Blocks(title="Zainab AI Portfolio") as demo:
    gr.Markdown(render_portfolio())

if __name__ == "__main__":
    demo.launch()

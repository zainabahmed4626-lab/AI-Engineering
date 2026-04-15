# AI Engineering Portfolio

Applied AI and Generative AI project portfolio focused on practical implementation: retrieval-augmented generation (RAG), tool calling, prompt strategy, conversation memory, and interactive app workflows.

## About This Repository

This repository documents hands-on AI engineering work through executable notebooks and supporting scripts. The goal is to demonstrate practical system design and implementation skills for real-world GenAI applications.

## Core Skills Demonstrated

- LLM application development with OpenAI APIs
- Retrieval-Augmented Generation (RAG) pipelines
- Embeddings, chunking strategies, and semantic search setup
- Tool-calling and dynamic context orchestration patterns
- Prompt design and system-vs-user instruction control
- Conversational memory and context management
- Lightweight app prototyping with Gradio

## Featured Work

### RAG Implementation and Visualization
- `ai_env/Ai_Engineering_Part1/rag1.ipynb`
  - Implements text chunking with overlap and boundary-aware splitting
  - Generates embeddings (`text-embedding-3-small`)
  - Visualizes semantic structure with 2D/3D t-SNE clustering
  - Includes cluster-level interpretation output for explainability

### Dynamic Context + Tool Calling Architecture
- `ai_env/Ai_Engineering_Part1/digital-twin-arch1-dynamic-context-toolcallingZ1.ipynb`
- `ai_env/Ai_Engineering_Part1/digital-twin-arch2-basic-tool-calling.ipynb`
  - Explores architecture evolution from basic to dynamic tool-calling patterns
  - Demonstrates practical context assembly for agent-like behavior

### Prompting, Memory, and Agent Foundations
- `ai_env/Ai_Engineering_Part1/system-vs-user-prompt.ipynb`
- `ai_env/Ai_Engineering_Part1/conversation-history.ipynb`
- `ai_env/Ai_Engineering_Part1/tool_callling.ipynb`
  - Focus on instruction hierarchy, session memory, and safe tool invocation

### App and Workflow Prototypes
- `ai_env/Ai_Engineering_Part1/gradio.ipynb`
- `ai_env/Ai_Engineering_Part1/gradio_mcp_chat.py`
- `ai_env/Ai_Engineering_Part1/run_digital_twin_e2e.py`
  - Demonstrates prototyping and basic end-to-end execution workflows

## Tech Stack

- Python
- OpenAI API
- Jupyter Notebook
- NumPy, Matplotlib, scikit-learn
- Plotly
- Gradio
- python-dotenv

## Quick Start

1. Clone the repository
   ```bash
   git clone https://github.com/zainabahmed4626-lab/AI-Engineering.git
   cd AI-Engineering
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv .venv
   # Windows PowerShell
   .venv\Scripts\Activate.ps1
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   pip install numpy matplotlib scikit-learn plotly nbconvert ipykernel
   ```

4. Configure environment variables
   ```env
   OPENAI_API_KEY=your_key_here
   ```

5. Launch notebooks
   ```bash
   jupyter notebook
   ```

## Project Structure

- `ai_env/Ai_Engineering_Part1/` — main notebook experiments and prototypes
- `requirements.txt` — base dependencies
- `.env` — local environment variables (not for commit)

## Notes for Reviewers

- Notebooks are organized to show iterative engineering progress from fundamentals to architecture-level patterns.
- Several notebooks include execution-ready code and visualization output that can be run locally.
- This repo emphasizes implementation clarity and practical experimentation over framework-heavy abstractions.

## Contact

- GitHub: [zainabahmed4626-lab](https://github.com/zainabahmed4626-lab)
- Portfolio/Contact: [resume-zainab.lovable.app](https://resume-zainab.lovable.app/#contact)

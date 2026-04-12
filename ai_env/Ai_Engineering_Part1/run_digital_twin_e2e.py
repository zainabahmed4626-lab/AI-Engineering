"""
End-to-end run of digital-twin-arch1-dynamic-context-toolcallingZ1.ipynb logic.
Skips: empty cell, Pushover test ping, duplicate respond_ai cells, markdown.

  python run_digital_twin_e2e.py           -> automated smoke test (starts server, checks API/MCP, exits)
  python run_digital_twin_e2e.py --serve   -> start Gradio + MCP and keep running for manual testing
"""
import argparse
import json
import socket
import sys
import time
from pathlib import Path

import requests

NB = Path(__file__).with_name("digital-twin-arch1-dynamic-context-toolcallingZ1.ipynb")
ENV_ROOT = Path(__file__).resolve().parents[2] / ".env"

CELLS_TO_RUN = [1, 3, 5, 6, 9, 10, 12, 13, 16]


def _free_port() -> int:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def _port_open(port: int) -> bool:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", port))
        return True
    except OSError:
        return False
    finally:
        s.close()


def load_notebook_namespace() -> dict:
    from dotenv import load_dotenv

    load_dotenv(ENV_ROOT)
    load_dotenv()

    nb = json.loads(NB.read_text(encoding="utf-8"))
    ns: dict = {}

    for idx in CELLS_TO_RUN:
        cell = nb["cells"][idx]
        if cell["cell_type"] != "code":
            raise SystemExit(f"Expected code at cell {idx}")
        src = "".join(cell["source"]).strip()
        if not src:
            continue
        print(f"--- Executing cell {idx} ---", flush=True)
        exec(compile(src, f"notebook_cell_{idx}", "exec"), ns)

    return ns


def serve(port: int | None = None) -> None:
    """Block until Ctrl+C; Gradio + MCP on localhost."""
    ns = load_notebook_namespace()
    import gradio as gr  # noqa: PLC0415

    if port is None:
        port = 7866 if _port_open(7866) else _free_port()

    base = f"http://127.0.0.1:{port}"
    print(f"\n>>> Open in browser: {base}/", flush=True)
    print(f">>> MCP (streamable): {base}/gradio_api/mcp/\n", flush=True)

    demo = gr.ChatInterface(fn=ns["respond_ai"])
    demo.launch(
        inbrowser=True,
        server_name="127.0.0.1",
        server_port=port,
        mcp_server=True,
        show_error=True,
    )


def run_smoke_test() -> None:
    port = _free_port()
    base = f"http://127.0.0.1:{port}"
    ns = load_notebook_namespace()

    print("--- Launching Gradio (prevent_thread_lock=True) ---", flush=True)
    import gradio as gr  # noqa: PLC0415

    demo = gr.ChatInterface(fn=ns["respond_ai"])
    demo.launch(
        inbrowser=False,
        server_name="127.0.0.1",
        server_port=port,
        mcp_server=True,
        prevent_thread_lock=True,
        show_error=True,
    )

    for _ in range(30):
        try:
            r = requests.get(f"{base}/", timeout=1)
            if r.status_code == 200:
                break
        except OSError:
            time.sleep(0.5)
    else:
        raise SystemExit("Gradio did not become ready in time")

    print("--- API smoke test (gradio_client) ---", flush=True)
    from gradio_client import Client  # noqa: PLC0415

    client = Client(base)
    reply = client.predict(
        message="Hi — reply in one short sentence who you are.",
        api_name="/respond_ai",
    )
    print("Chat reply:", reply[:500] if reply else reply, flush=True)

    print("--- MCP endpoint (SSE Accept header) ---", flush=True)
    r = requests.get(
        f"{base}/gradio_api/mcp/",
        headers={"Accept": "text/event-stream"},
        stream=True,
        timeout=5,
    )
    print("MCP GET status:", r.status_code, "content-type:", r.headers.get("content-type"), flush=True)
    r.close()

    print("--- Done. Last URL:", base, "---", flush=True)
    time.sleep(2)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--serve",
        action="store_true",
        help="Start Gradio + MCP and keep running (manual testing in browser).",
    )
    p.add_argument(
        "--port",
        type=int,
        default=None,
        help="Port for --serve (default: 7866 if free, else random).",
    )
    args = p.parse_args()

    if args.serve:
        try:
            serve(port=args.port)
        except KeyboardInterrupt:
            print("\nStopped.", flush=True)
            sys.exit(0)
    else:
        run_smoke_test()


if __name__ == "__main__":
    main()

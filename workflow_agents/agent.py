# ------------------------------
# Add / merge these imports at top of agent.py (if not already present)
# ------------------------------
import os
import json
from datetime import datetime
from typing import List, Dict

# ADK imports (your ADK install may use these exact modules)
from google.adk.agents import LlmAgent, SequentialAgent, LoopAgent, Agent
from google.adk.apps import App
from google.adk.tools import ToolContext, exit_loop

# (keep load_dotenv and MODEL as you already have)
from dotenv import load_dotenv
load_dotenv()
MODEL = os.getenv("MODEL", "gemini-2.5-flash")


# ------------------------------
# Helper tools (append to state, wiki lookup, file writer)
# ------------------------------
def append_to_state(tool_context: ToolContext, key: str, value) -> Dict[str, str]:
    """Append `value` to list stored at session.state[key]."""
    lst = tool_context.state.get(key, [])
    lst.append(value)
    tool_context.state[key] = lst
    return {"status": "ok"}


def wiki_lookup(tool_context: ToolContext, query: str) -> Dict[str, str]:
    """Simple wikipedia lookup that stores a summary in state under 'research'."""
    import requests
    try:
        url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + requests.utils.requote_uri(query)
        resp = requests.get(url, timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            summary = data.get("extract", "")
        else:
            summary = f"(No summary found: HTTP {resp.status_code})"
    except Exception as e:
        summary = f"(Error: {e})"

    # Save research snippet (so loop can accumulate)
    append_to_state(tool_context, "research", {"query": query, "summary": summary})
    return {"status": "ok", "summary": summary}


def mock_screenwriter(tool_context: ToolContext, title_hint: str = None) -> Dict[str, str]:
    """Build a simple outline from saved research snippets (mock LLM behaviour)."""
    snippets = tool_context.state.get("research", [])
    title = title_hint or f"Untitled Film {datetime.now().strftime('%Y%m%d_%H%M%S')}"
    lines = [f"Title (draft): {title}", "Outline:"]
    for i, s in enumerate(snippets, start=1):
        q = s.get("query", "unknown")
        summary = s.get("summary", "")[:400]
        lines.append(f"- Research {i} ({q}): {summary}")
    outline = "\n".join(lines)
    append_to_state(tool_context, "drafts", outline)
    return {"status": "ok", "outline": outline}


def write_to_file(tool_context: ToolContext, filename_prefix: str = "movie_pitch") -> Dict[str, str]:
    """Write latest draft to disk and store file path in state."""
    drafts = tool_context.state.get("drafts", [])
    if not drafts:
        return {"status": "no_draft"}
    draft = drafts[-1]
    outdir = os.path.expanduser("~/adk_multiagent_systems/movie_pitches")
    os.makedirs(outdir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_prefix = filename_prefix.replace(" ", "_")
    filename = f"{safe_prefix}_{ts}.txt"
    path = os.path.join(outdir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(draft)
    append_to_state(tool_context, "written_files", path)
    return {"status": "written", "path": path}


# ------------------------------
# Coordinator tool (optionally used by Greeter to start the sequence)
# ------------------------------
def run_film_concept_sequence(tool_context: ToolContext) -> Dict[str, str]:
    """
    A coordinator that runs a simple sequence:
    - researcher (wiki lookups)
    - screenwriter (mock or LLM)
    - critic is handled by the LoopAgent below
    - after loop finishes, call write_to_file
    """
    subject = tool_context.state.get("subject")
    if not subject:
        return {"status": "no_subject"}

    # Perform initial research passes; loop agent will handle iterative passes later
    wiki_lookup(tool_context, subject)
    wiki_lookup(tool_context, f"{subject} biography")
    # produce an initial draft
    mock_screenwriter(tool_context, title_hint=f"{subject} — The Film")
    # write to file
    fw = write_to_file(tool_context, filename_prefix=subject)
    return {"status": fw.get("status"), "path": fw.get("path")}


# ------------------------------
# Agents: researcher, screenwriter, critic (critic can call exit_loop)
# ------------------------------
researcher = LlmAgent(
    name="researcher",
    model=MODEL,
    instruction=(
        "Research the subject by calling wiki_lookup as needed. Save findings via append_to_state(key='research', value=...)"
    ),
    tools=[wiki_lookup, append_to_state],
)

screenwriter = LlmAgent(
    name="screenwriter",
    model=MODEL,
    instruction=(
        "Read session.state['research'] and produce a concise plot outline. Save the outline to session.state['drafts'] "
        "using append_to_state."
    ),
    tools=[append_to_state],
)

critic = Agent(   # use Agent if your ADK exposes a neutral Agent; otherwise LlmAgent is fine
    name="critic",
    description="Review the current PLOT_OUTLINE and RESEARCH and decide whether to exit the writers loop or append critical feedback.",
    instruction="""
INSTRUCTIONS:
Consider these questions about the PLOT_OUTLINE:
- Does it meet a satisfying three-act structure?
- Are character motivations clear and engaging?
- Is it grounded in the provided RESEARCH?

If the outline is good, call the exit_loop tool to stop the writers loop.
If improvements are needed, use append_to_state to add feedback under 'critical_feedback', and explain briefly.
PLOT_OUTLINE:
{ draft = session.state['drafts'][-1] if session.state.get('drafts') else 'No draft yet' }
RESEARCH:
{ research? }
""",
    tools=[append_to_state, exit_loop],
)

# ------------------------------
# writers_room (LoopAgent): researcher -> screenwriter -> critic
# ------------------------------
writers_room = LoopAgent(
    name="writers_room",
    description="Iteratively research and refine a plot via (researcher -> screenwriter -> critic).",
    sub_agents=[researcher, screenwriter, critic],
    max_iterations=5,   # safety cap
)

# ------------------------------
# film_concept_team (SequentialAgent) : writers_room then file_writer
# ------------------------------
file_writer = LlmAgent(
    name="file_writer",
    model=MODEL,
    instruction="Create a movie title and finalize the output. Call write_to_file tool to persist.",
    tools=[write_to_file],
)

film_concept_team = SequentialAgent(
    name="film_concept_team",
    description="Run writers_room loop until exit, then file_writer to save draft to disk.",
    sub_agents=[writers_room, file_writer],
)

# ------------------------------
# Root greeter: asks for historical figure, sets session.state['subject'], and delegates to film_concept_team
# ------------------------------
greeter = LlmAgent(
    name="greeter",
    model=MODEL,
    description="Greets the user and asks for the historical figure (subject).",
    instruction=(
        "Greet the user and ask: 'Which historical figure or type of historical figure would you like to base the movie on?'\n\n"
        "When user replies, save the cleaned name in session.state['subject'] and transfer control to the sub-agent 'film_concept_team'."
    ),
    sub_agents=[film_concept_team],
)

# App registration (ADK Dev UI / adk CLI will load this app)
app = App(name="workflow_agents", root_agent=greeter)

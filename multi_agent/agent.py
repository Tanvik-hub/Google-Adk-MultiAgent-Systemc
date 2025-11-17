from google.adk.agents import LlmAgent
from google.adk.apps import App
import os
from dotenv import load_dotenv
from typing import List, Dict
from google.adk.tools import ToolContext

import os
from datetime import datetime
from google.adk.tools import ToolContext



load_dotenv()

MODEL = os.getenv("MODEL", "gemini-2.5-flash")

def save_attractions_to_state(
    tool_context: ToolContext,
    attractions: List[str]
) -> Dict[str, str]:
    """Add selected attractions into session.state['attractions']."""
    existing = tool_context.state.get("attractions", [])
    tool_context.state["attractions"] = existing + attractions
    return {"status": "saved"}


travel_brainstormer = LlmAgent(
    name="travel_brainstormer",
    model=MODEL,
    description="Suggests travel destinations when user has not decided a country.",
    instruction=(
        "Ask 2–3 quick questions (budget, interests). "
        "Then recommend 4–6 countries with short reasons."
    )
)

attractions_planner = LlmAgent(
    name="attractions_planner",
    model=MODEL,
    description="Suggests attractions for a known country or city.",
    instruction=(
        "When user gives a country/city, list 5–8 attractions with short notes.\n"
        "\n"
        "- When the user selects an attraction, CALL the tool `save_attractions_to_state` "
        "with that attraction.\n"
        "- After saving, acknowledge and suggest more attractions.\n"
        "\n"
        "- If user asks 'What is on my list?', return a bulleted list using { attractions? }."
    ),
    tools=[save_attractions_to_state]
)


steering = LlmAgent(
    name="steering",
    model=MODEL,
    description="Directs the user to the correct sub-agent.",
    instruction=(
        "Ask the user: 'Do you already have a country in mind or need help deciding?'\n\n"

        "If the user says things like 'I don't know', 'help me choose', "
        "transfer to travel_brainstormer.\n\n"

        "If the user says a country (e.g., Japan), transfer to attractions_planner.\n\n"

        "If user switches mode, allow transfer between the two sub-agents."
    ),
    sub_agents=[travel_brainstormer, attractions_planner]
)

app = App(
    name="multi_agent",
    root_agent=steering
)

# Google-Adk-MultiAgent-System

**A professional multi-agent AI system built with Google ADK, featuring LoopAgent for iterative research → draft → critique workflows, automated refinement, and content generation.**

**Built during the Google Cloud Technical Series: Multi-Agent AI Workshop**
---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
---

## Overview

This repository demonstrates a **multi-agent orchestration system** using Google ADK.  
The core component is the **`LoopAgent`**, which enables iterative workflows where agents:

1. **Research** – collect relevant information (e.g., Wikipedia summaries).  
2. **Draft** – produce an initial content outline based on research.  
3. **Critique** – evaluate drafts, provide feedback, and decide whether to continue or stop the loop.

<img width="1557" height="690" alt="image" src="https://github.com/user-attachments/assets/f5ab8e66-f497-4913-9f25-92cf9135d8ca" />

Once the iterative loop finishes, the system automatically **writes the final draft to disk**.  

This workflow models real-world content generation pipelines, autonomous agent orchestration, and iterative refinement systems.

---

## Features

- **Multi-Agent Workflow:** Researcher, Screenwriter, Critic, File Writer agents.  
- **LoopAgent:** Iterative research → draft → critique cycle.  
- **SequentialAgent:** Executes ordered steps after iterative loop.  
- **Automated File Output:** Drafts are saved in `movie_pitches/` folder.  
- **State Management:** Accumulates research, drafts, and feedback in `session.state`.  
- **Extensible:** Replace mock screenwriter with LLM-based models easily.  
- **Portfolio Ready:** Demonstrates agentic AI workflow, suitable for recruiter showcase.

---

## Project Structure

```text
~/Google-Adk-MultiAgent/
├─ workflow_agents/
│  ├─ agent.py           # Main file defining all agents and tools
│  ├─ __init__.py
├─ movie_pitches/        # Generated drafts are saved here
├─ README.md
├─ requirements.txt      # Python dependencies (e.g., google-adk, requests, dotenv)

## MODEL=gemini-2.5-flash


<img width="1832" height="939" alt="image" src="https://github.com/user-attachments/assets/df1247c2-61e2-4d8e-bff3-e7572a4adb33" />



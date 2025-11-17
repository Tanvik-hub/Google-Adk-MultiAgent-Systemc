# 🤖Google-Adk-MultiAgent-System-DAY 1 ,TASK 2

**A professional multi-agent AI system built with Google ADK, featuring LoopAgent for iterative research → draft → critique workflows, automated refinement, and content generation.**

**Built during the Google Cloud Technical Series: Multi-Agent AI Workshop**
<img width="1832" height="939" alt="image" src="https://github.com/user-attachments/assets/fc08b7e8-5675-4b1f-a2f8-d7814d9445d9" />

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
--[Event](#Event)

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
## Event

By building this system during the **Google Cloud Technical Series**, I gained hands-on experience in:

- Designing **multi-agent pipelines** for content generation  
- Implementing **LoopAgent and SequentialAgent** workflows  
- Managing agent **state, persistence, and feedback loops**  
- Integrating deterministic tools (APIs, file writing) with creative LLM outputs

  


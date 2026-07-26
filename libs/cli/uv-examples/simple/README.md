# Northstar Forge

Northstar Forge is a compact LangGraph project that turns a rough idea into a
practical project brief. Instead of returning one placeholder sentence, it now
builds a small execution packet with:

- a clarified objective
- a target audience
- staged milestones
- concrete deliverables
- risks to watch
- immediate first actions

## Why this project exists

This project is designed to feel like a real starter app, not just a smoke
test. It stays offline-first, so you can run it locally without wiring in model
providers or API keys.

## How to use it

Start the dev server:

```bash
./.venv314/bin/langgraph dev --host 127.0.0.1 --port 2024 --no-browser
```

Then open LangGraph Studio or the local API docs and send a goal such as:

- `Build a small internal dashboard for tracking sales outreach`
- `Create a content engine for a design newsletter`
- `Automate weekly reporting for our operations team`
- `Research the best launch plan for a new mobile habit app`

## What the graph does

The graph runs through four stages:

1. Intake the user goal and classify the project type.
2. Build milestones and deliverables for that type of work.
3. Surface common risks and fast wins.
4. Return a structured project brief.

## Files that matter

- `langgraph.json` points LangGraph at the compiled graph.
- `src/agent/graph.py` contains the full workflow.
- `pyproject.toml` defines the project metadata and dependencies.

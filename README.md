# Northstar Forge

Northstar Forge is a portfolio-ready LangGraph project that turns a rough idea
into a clear execution brief. It acts like a focused project architect:
classifying the work, shaping the objective, mapping milestones, surfacing
risks, and producing practical next steps.

This project is designed to showcase strong agent workflow thinking without
depending on an external model provider. It runs locally, responds instantly,
and demonstrates how a graph can transform unstructured input into structured,
useful output.

## What it does

Given a raw prompt such as:

```text
Build a small internal dashboard for tracking sales outreach
```

Northstar Forge returns a structured brief with:

- a refined objective
- a target audience
- milestone planning
- deliverables for the first release
- execution risks
- immediate first actions

## Workflow

The graph runs through four stages:

1. `intake_goal`
   It extracts the latest user request and classifies the project type.
2. `map_project`
   It chooses milestones and deliverables based on the kind of project.
3. `assess_risks`
   It adds execution risks and high-leverage quick wins.
4. `draft_response`
   It returns a polished planning brief as the final agent response.

## Showcase Scenarios

Northstar Forge is especially good for demos around:

- internal tools
- startup ideas
- AI products
- automation workflows
- research initiatives
- operations planning
- content systems

Example prompts:

- `Design a launch-ready habit tracking app for university students`
- `Automate weekly operations reporting for a remote team`
- `Create a content engine for a product design newsletter`
- `Research the strongest go-to-market path for an AI scheduling assistant`

## Run Locally

From this directory:

```bash
python3 -m venv .venv314
./.venv314/bin/pip install -U pip
./.venv314/bin/pip install "langgraph-cli[inmem]" "langgraph>=0.6.0,<2" "langchain-core>=1.3.3"
./.venv314/bin/langgraph dev --host 127.0.0.1 --port 2024 --no-browser
```

Then open:

- API Docs: `http://127.0.0.1:2024/docs`
- LangGraph Studio: `https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`

## Project Structure

- `src/agent/graph.py`
  The core LangGraph workflow and planning logic.
- `langgraph.json`
  The LangGraph entrypoint configuration.
- `pyproject.toml`
  Project metadata and Python dependencies.
- `.env.example`
  Placeholder env file for future provider integrations.

## Summary

Northstar Forge is no longer a generic sample. It is now a focused agent
project with a clear identity, practical output, and a polished story that is
easy to demo and easy to extend.

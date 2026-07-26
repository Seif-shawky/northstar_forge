from collections.abc import Sequence
from typing import Annotated, Literal, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages


ProjectType = Literal[
    "product",
    "content",
    "automation",
    "research",
    "operations",
    "general",
]


class State(TypedDict, total=False):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    goal: str
    project_type: ProjectType
    audience: str
    objective: str
    milestones: list[str]
    deliverables: list[str]
    risks: list[str]
    quick_wins: list[str]


def _latest_user_goal(messages: Sequence[BaseMessage]) -> str:
    for message in reversed(messages):
        if isinstance(message, HumanMessage):
            content = message.content
            if isinstance(content, str):
                cleaned = content.strip()
                if cleaned:
                    return cleaned
    return "Create a project that helps a team move from idea to execution."


def _detect_project_type(goal: str) -> ProjectType:
    lowered = goal.lower()
    keyword_map: list[tuple[ProjectType, tuple[str, ...]]] = [
        ("product", ("app", "product", "platform", "dashboard", "mobile", "website")),
        ("content", ("content", "course", "newsletter", "brand", "campaign", "media")),
        ("automation", ("automate", "workflow", "pipeline", "integration", "bot", "agent")),
        ("research", ("research", "analysis", "study", "report", "insight", "benchmark")),
        ("operations", ("process", "team", "ops", "operation", "rollout", "playbook")),
    ]
    for project_type, keywords in keyword_map:
        if any(keyword in lowered for keyword in keywords):
            return project_type
    return "general"


def _infer_audience(goal: str, project_type: ProjectType) -> str:
    lowered = goal.lower()
    if "customer" in lowered or "client" in lowered or "user" in lowered:
        return "External users who need a clear, low-friction experience."
    if "team" in lowered or "internal" in lowered or "company" in lowered:
        return "An internal team that needs faster coordination and clearer execution."
    default_map = {
        "product": "Users who want a focused product experience with fast feedback loops.",
        "content": "An audience that wants structured, useful, repeatable content.",
        "automation": "Operators who want less repetitive work and more reliable systems.",
        "research": "Decision-makers who need findings distilled into practical actions.",
        "operations": "A team that needs smoother handoffs, accountability, and visibility.",
        "general": "A small team moving an idea into a practical first release.",
    }
    return default_map[project_type]


def _infer_objective(goal: str, project_type: ProjectType) -> str:
    objective_map = {
        "product": "Ship a focused v1 that proves value quickly and reveals the next best features.",
        "content": "Create a repeatable content engine with a clear voice, cadence, and measurable output.",
        "automation": "Reduce manual work by designing a dependable workflow with clear guardrails.",
        "research": "Turn open questions into decisions through structured analysis and concise synthesis.",
        "operations": "Improve execution quality with a practical system that teams can adopt quickly.",
        "general": "Shape an ambitious idea into a small, testable project with momentum.",
    }
    return objective_map[project_type] + f" Current request: {goal}"


def intake_goal(state: State) -> State:
    goal = _latest_user_goal(state["messages"])
    project_type = _detect_project_type(goal)
    return {
        "goal": goal,
        "project_type": project_type,
        "audience": _infer_audience(goal, project_type),
        "objective": _infer_objective(goal, project_type),
    }


def map_project(state: State) -> State:
    project_type = state["project_type"]
    milestone_map: dict[ProjectType, list[str]] = {
        "product": [
            "Define the narrowest v1 promise and the primary user journey.",
            "Build the smallest usable experience with strong defaults.",
            "Run feedback sessions, trim scope, and harden the best path.",
        ],
        "content": [
            "Pick the core theme, tone, and audience promise.",
            "Create the first content batch and a reusable production workflow.",
            "Measure resonance and refine distribution around the strongest format.",
        ],
        "automation": [
            "Map the current workflow and identify the highest-friction handoff.",
            "Automate the most repetitive path with clear inputs and outputs.",
            "Add checks, alerts, and documentation so the workflow is trustworthy.",
        ],
        "research": [
            "Frame the questions, assumptions, and success criteria.",
            "Gather evidence from the highest-signal sources first.",
            "Package findings into recommendations, tradeoffs, and next moves.",
        ],
        "operations": [
            "Clarify ownership, bottlenecks, and the key operating rhythm.",
            "Design lightweight rituals, templates, and visibility points.",
            "Pilot the system with one team before wider rollout.",
        ],
        "general": [
            "Translate the idea into a clear value proposition and scope boundary.",
            "Build a first version that demonstrates the core outcome.",
            "Collect feedback and choose what to deepen, remove, or postpone.",
        ],
    }
    deliverable_map: dict[ProjectType, list[str]] = {
        "product": [
            "A one-page product brief",
            "A usable v1 flow",
            "A short learning backlog for iteration two",
        ],
        "content": [
            "A content strategy brief",
            "A starter content calendar",
            "Reusable templates for production and publishing",
        ],
        "automation": [
            "A workflow map",
            "An automated execution path",
            "An operating checklist for monitoring and recovery",
        ],
        "research": [
            "A research brief",
            "A findings summary",
            "A decision memo with recommended actions",
        ],
        "operations": [
            "An operating playbook",
            "A team cadence and ownership map",
            "A rollout checklist with feedback loops",
        ],
        "general": [
            "A project brief",
            "A roadmap for the first release",
            "A decision list for what stays out of scope",
        ],
    }
    return {
        "milestones": milestone_map[project_type],
        "deliverables": deliverable_map[project_type],
    }


def assess_risks(state: State) -> State:
    goal = state["goal"].lower()
    project_type = state["project_type"]
    common_risks = [
        "The scope may grow faster than the first version can support.",
        "Success might stay vague unless one concrete outcome is chosen early.",
        "The project can become impressive on paper but thin in real usage.",
    ]
    specialized_risks: dict[ProjectType, list[str]] = {
        "product": [
            "Too many features can dilute the value of the first user journey.",
            "UX polish may be prioritized before the core workflow is validated.",
        ],
        "content": [
            "Production cadence can collapse if the workflow depends on heroic effort.",
            "Brand tone may drift without a clear editorial standard.",
        ],
        "automation": [
            "Automation can encode a flawed process instead of improving it.",
            "Edge cases may quietly fail unless the system exposes its decisions.",
        ],
        "research": [
            "The team may gather more data than it can turn into decisions.",
            "Insights can feel interesting but still fail to change what happens next.",
        ],
        "operations": [
            "A new process can create overhead if it is not anchored to real pain points.",
            "Adoption may stall if owners are unclear or overloaded.",
        ],
        "general": [
            "The concept may stay broad unless a single audience is prioritized.",
            "Execution can slow down if every good idea is treated as essential.",
        ],
    }
    quick_wins = [
        "Write a one-sentence definition of success for the first release.",
        "Choose one audience to serve first and one thing you will deliberately ignore.",
        "Turn the next week of work into a visible checklist with owners.",
    ]
    if "ai" in goal or "agent" in goal:
        common_risks.append(
            "It may lean on AI novelty without a strong fallback path for reliability."
        )
        quick_wins.append(
            "Design the non-AI baseline first so the smarter path has something solid to improve."
        )
    return {
        "risks": common_risks + specialized_risks[project_type],
        "quick_wins": quick_wins,
    }


def draft_response(state: State) -> State:
    message = AIMessage(
        content=(
            "# Northstar Forge\n\n"
            f"## Project Goal\n{state['goal']}\n\n"
            f"## Audience\n{state['audience']}\n\n"
            f"## Objective\n{state['objective']}\n\n"
            "## Milestones\n"
            + "\n".join(f"- {item}" for item in state["milestones"])
            + "\n\n## Deliverables\n"
            + "\n".join(f"- {item}" for item in state["deliverables"])
            + "\n\n## Risks To Watch\n"
            + "\n".join(f"- {item}" for item in state["risks"])
            + "\n\n## First Actions\n"
            + "\n".join(f"- {item}" for item in state["quick_wins"])
        )
    )
    return {"messages": [message]}


workflow = StateGraph(State)
workflow.add_node("intake_goal", intake_goal)
workflow.add_node("map_project", map_project)
workflow.add_node("assess_risks", assess_risks)
workflow.add_node("draft_response", draft_response)
workflow.add_edge(START, "intake_goal")
workflow.add_edge("intake_goal", "map_project")
workflow.add_edge("map_project", "assess_risks")
workflow.add_edge("assess_risks", "draft_response")
workflow.add_edge("draft_response", END)

graph = workflow.compile()

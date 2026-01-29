# Whiteport Design Studio (WDS) Agents

This project uses the Whiteport Design Studio methodology with AI agents.
WDS files are installed in the `_wds/` directory.

## Available Agents

To activate a WDS agent, load and follow the instructions in the agent file:

- **Mimir** (Orchestrator & Guide): Read `_wds/agents/mimir-orchestrator.md` - Start here if you're new to WDS
- **Saga** (Analyst): Read `_wds/agents/saga-analyst.md` - Product Brief & Trigger Mapping (Phases 1-2)
- **Idunn** (Product Manager): Read `_wds/agents/idunn-pm.md` - Platform Requirements & Design Deliveries (Phases 3, 6)
- **Freya** (UX Designer): Read `_wds/agents/freya-ux.md` - UX Design, Design System & Testing (Phases 4-5, 7-8)

## How to Activate

Tell the AI: "Read and activate the agent in `_wds/agents/[agent-name].md`"

The agent will load its persona, read the project config, greet you, and show its menu.

## Project Configuration

Project settings are stored in `_wds/config.yaml`. Agents load this automatically on activation.

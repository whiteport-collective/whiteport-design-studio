# Whiteport Design Studio (WDS) - BMad Method Module

[![Fork of BMad Method](https://img.shields.io/badge/Fork%20of-BMad%20Method%20v6-blue)](https://github.com/bmad-code-org/BMAD-METHOD)
[![Module Status](https://img.shields.io/badge/Status-In%20Development-orange)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---
<<<<<<< HEAD

<div align="center">

## 🎉 NEW: BMAD V6 Installer - Create & Share Custom Content!

The completely revamped **BMAD V6 installer** now includes built-in support for creating, installing, and sharing custom modules, agents, workflows, templates, and tools! Build your own AI solutions or share them with your team - and real soon, with the whole BMad Community througha verified community sharing portal!

**✨ What's New:**

- 📦 **Streamlined Custom Module Installation** - Package your custom content as installable modules
- 🤖 **Agent & Workflow Sharing** - Distribute standalone agents and workflows
- 🔄 **Unitary Module Support** - Install individual components without full modules
- ⚙️ **Dependency Management** - Automatic handling of module dependencies
- 🛡️ **Update-Safe Customization** - Your custom content persists through updates

**📚 Learn More:**

- [**Custom Content Overview**](http://docs.bmad-method.org/explanation/bmad-builder/custom-content-types/) - Discover all supported content types
- [**Installation Guide**](http://docs.bmad-method.org/how-to/installation/install-custom-modules/) - Learn to create and install custom content
- [**2 Very simple Custom Modules of questionable quality**](./samples/sample-custom-modules/README.md) - if you want to download and try to install a custom shared module, get an idea of how to bundle and share your own, or create your own personal agents, workflows and modules.

</div>

---

## AI-Driven Agile Development That Scales From Bug Fixes to Enterprise

**Build More, Architect Dreams** (BMAD) with **21 specialized AI agents** across 4 official modules, and **50+ guided workflows** that adapt to your project's complexity—from quick bug fixes to enterprise platforms, and new step file workflows that allow for incredibly long workflows to stay on the rails longer than ever before!

Additionally - when we say 'Build More, Architect Dreams' - we mean it! The BMad Builder has landed, and now as of Alpha.15 is fully supported in the installation flow via NPX - custom stand along agents, workflows and the modules of your dreams! The community forge will soon open, endless possibility awaits!
=======

## 🎯 About This Fork
>>>>>>> 47ee5a45 (refactor: update README to reflect the new Whiteport Design Studio (WDS) module)

This repository is a **fork of [BMad-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)** with the purpose of contributing the **Whiteport Design Studio (WDS)** module to the BMad ecosystem.

### What is Whiteport Design Studio?

**WDS** is a design-focused methodology module that provides a complete **UX/UI design workflow** for product development—from initial product exploration through detailed component specifications. It complements the development-focused BMad Method (BMM) module by providing the **design artifacts** that feed into development.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         BMad Ecosystem                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────────────┐      ┌─────────────────┐                     │
│   │  Whiteport      │      │  BMad Method    │                     │
│   │  Design Studio  │ ───► │  (BMM)          │                     │
│   │  (WDS)          │      │                 │                     │
│   │                 │      │                 │                     │
│   │  • Product Brief│      │  • Architecture │                     │
│   │  • Trigger Map  │      │  • Epics/Stories│                     │
│   │  • Scenarios    │      │  • Development  │                     │
│   │  • PRD          │      │  • Testing      │                     │
│   │  • Design System│      │  • Deployment   │                     │
│   │  • UI Roadmap   │      │                 │                     │
│   │                 │      │                 │                     │
│   │  DESIGN ────────┼──────┼► DEVELOPMENT    │                     │
│   └─────────────────┘      └─────────────────┘                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ WDS Module Structure

The WDS module will be located at `src/modules/wds/` and follows BMad v6 module conventions:

```
src/modules/wds/
├── _module-installer/          # Installation configuration
│   └── install-config.yaml
├── agents/                     # WDS specialized agents
│   ├── analyst.agent.yaml      # Mary - Business & Product Analyst
│   ├── pm.agent.yaml           # Sarah - Product Manager
│   └── designer.agent.yaml     # Sally - UX/UI Designer
├── workflows/                  # Phase-selectable workflows
├── data/                       # Standards, frameworks, presentations
├── docs/                       # Module documentation (xxx-guide.md)
├── examples/                   # Real-world usage examples
├── reference/                  # Templates and checklists
├── teams/                      # Team configurations
└── README.md                   # Module entry point (only README)
```

---

## 📁 WDS Output Folder Structure

WDS creates a distinctive **alphabetized folder structure** in the user's project `docs/` folder:

<<<<<<< HEAD
<p align="center">
  <img src="./docs/tutorials/getting-started/images/workflow-method-greenfield.svg" alt="BMad Method Workflow" width="100%">
</p>
=======
```
docs/
├── A-Product-Brief/            # Phase 1: Strategic foundation & vision
├── B-Trigger-Map/              # Phase 2: Business goals, personas, drivers
├── C-Scenarios/                # Phase 4: Visual specifications & sketches
├── D-PRD/                      # Phase 3: Product requirements documentation
├── D-Design-System/            # Phase 5: Component library & design tokens
└── E-UI-Roadmap/               # Phase 6: Development integration bridge
```
>>>>>>> 47ee5a45 (refactor: update README to reflect the new Whiteport Design Studio (WDS) module)

**Why alphabetical?** The `A-B-C-D-E` prefix creates a clear visual namespace that:
- Groups WDS artifacts together in file explorers
- Distinguishes from other project documentation
- Provides natural sort order matching workflow progression
- Becomes a recognizable WDS brand signature

---

## 🔄 The WDS Phases

WDS provides **6 design phases** that can be selected based on project scale:

| Phase | Name | Output Folder | Description |
|-------|------|---------------|-------------|
| 1️⃣ | **Product Exploration** | `A-Product-Brief/` | Vision, positioning, ICP framework |
| 2️⃣ | **User Research** | `B-Trigger-Map/` | Personas, business goals, driving forces |
| 3️⃣ | **Requirements** | `D-PRD/` | Functional & technical requirements |
| 4️⃣ | **Conceptual Design** | `C-Scenarios/` | User scenarios, sketches, specifications |
| 5️⃣ | **Component Design** | `D-Design-System/` | Design tokens, component library |
| 6️⃣ | **Dev Integration** | `E-UI-Roadmap/` | Handoff artifacts for development |

### Phase-Selectable Workflow

Unlike rigid tracks, WDS allows users to **select individual phases** based on project needs:

- **Landing page?** → Phases 1, 4, 5
- **Full product?** → All 6 phases
- **Existing product enhancement?** → Phases 2, 4, 5, 6
- **Design system only?** → Phases 4, 5

---

## 🤖 WDS Agents - The Norse Pantheon 🏔️

WDS introduces **3 specialized design agents** named after Norse mythology:

| Agent | Role | Norse Meaning |
|-------|------|---------------|
| **Saga the Analyst** | Business & Product Analyst | Goddess of stories & wisdom - uncovers your business story |
| **Freyja the PM** | Product Manager | Goddess of love, war & strategy - leads with heart and mind |
| **Baldr the UX Expert** | UX/UI Designer | God of light & beauty - makes everything radiant |

---

## 🔗 Integration with BMad Method (BMM)

WDS is designed to **hand off to BMM** for development:

```
WDS Design Phases                    BMM Development Phases
─────────────────                    ─────────────────────
A-Product-Brief/    ──────────────►  Architecture Context
B-Trigger-Map/      ──────────────►  User Story Personas
D-PRD/              ──────────────►  Epic Breakdown Source
C-Scenarios/        ──────────────►  Story Specifications
D-Design-System/    ──────────────►  Component Implementation
E-UI-Roadmap/       ──────────────►  Development Roadmap
```

The `E-UI-Roadmap/` folder serves as the **integration bridge**, containing:
- Scenario-to-epic mapping
- Priority recommendations
- Technical constraints
- Component implementation notes
- Object ID inventory for testing

---

## 📋 Development Status

### Current Phase: Module Structure Setup

- [ ] Create `src/modules/wds/` folder structure
- [ ] Create `_module-installer/install-config.yaml`
- [ ] Convert agents to v6 YAML format (Mary, Sarah, Sally)
- [ ] Create phase-selectable workflow initialization
- [ ] Build core workflows for each phase
- [ ] Create documentation (xxx-guide.md format)
- [ ] Add example content (Dog Week patterns)
- [ ] Test integration with BMM

### Conventions

- **One README:** Only `README.md` at module root; all other docs use `xxx-guide.md` naming
- **Folder structure:** Alphabetized `A-B-C-D-E` prefix for user project output
- **Design focus:** No development/backlog artifacts (handled by BMM)
- **Phase-selectable:** Users choose phases based on project scale

---

## 🙏 Acknowledgments

### BMad Method

This module is built on the excellent **[BMad Method](https://github.com/bmad-code-org/BMAD-METHOD)** framework created by the BMad community. WDS leverages BMad Core's modular architecture to provide design-focused workflows.

### Whiteport Collective

WDS is contributed by **[Whiteport Collective](https://github.com/whiteport-collective)**, evolving from the earlier "Whiteport Sketch-to-Code" methodology into a proper BMad v6 module.

---

## 🔄 Keeping This Fork Updated

This fork is regularly synchronized with upstream BMad-METHOD:

```bash
<<<<<<< HEAD
# Install v6 RECOMMENDED
npx bmad-method@alpha install
```

```bash
# Install v4 Legacy (not recommended if starting fresh)
npx bmad-method install
# OR
npx bmad-method@latest install
```


### 2. Initialize Your Project
=======
# Sync with upstream
git fetch upstream
git merge upstream/main
git push origin main
```

---
>>>>>>> 47ee5a45 (refactor: update README to reflect the new Whiteport Design Studio (WDS) module)

## 📚 Original BMad Method Documentation

For complete BMad Method documentation, see:
- **[BMad Method README](https://github.com/bmad-code-org/BMAD-METHOD)** - Main documentation
- **[BMM Module Docs](./src/modules/bmm/docs/README.md)** - Development workflows
- **[Agent Customization](./docs/agent-customization-guide.md)** - Customize agents
- **[Quick Start Guide](./src/modules/bmm/docs/quick-start.md)** - Get started

<<<<<<< HEAD
This analyzes your project and recommends the right workflow track.

### 3. Choose Your Track

BMad Method adapts to your needs with three intelligent tracks:

| Track             | Use For                   | Planning                | Time to Start |
| ----------------- | ------------------------- | ----------------------- | ------------- |
| **⚡ Quick Flow**  | Bug fixes, small features | Tech spec only          | < 5 minutes   |
| **📋 BMad Method** | Products, platforms       | PRD + Architecture + UX | < 15 minutes  |
| **🏢 Enterprise**  | Compliance, scale         | Full governance suite   | < 30 minutes  |

> **Not sure?** Run `*workflow-init` and let BMad analyze your project goal.

## 🔄 How It Works: 4-Phase Methodology

BMad Method guides you through a proven development lifecycle:

1. **📊 Analysis** (Optional) - Brainstorm, research, and explore solutions
2. **📝 Planning** - Create PRDs, tech specs, or game design documents
3. **🏗️ Solutioning** - Design architecture, UX, and technical approach
4. **⚡ Implementation** - Story-driven development with continuous validation

Each phase has specialized workflows and agents working together to deliver exceptional results.

## 🤖 Meet Your Team

**12 Specialized Agents** working in concert:

| Development | Architecture   | Product     | Leadership   |
| ----------- | -------------- | ----------- | ------------ |
| Developer   | Architect      | PM          | Scrum Master |
| UX Designer | Test Architect | Analyst     | BMad Master  |
|             |                | Tech Writer |              |

**Test Architect** integrates with `@seontechnologies/playwright-utils` for production-ready web app fixture-based utilities.

Each agent brings deep expertise and can be customized to match your team's style.

## 📦 What's Included

### Official Modules

- **BMad Method (BMM)** - Complete agile development framework
  - 12 specialized agents
  - 34 workflows across 4 phases
  - Stand Along Quick Spec Flow for a streamlined simple implementation process
  - [→ Documentation Hub](http://docs.bmad-method.org/explanation/bmm/)

- **BMad Builder (BMB)** - Create custom agents and workflows
  - Build anything from simple agents to complex modules
  - Create domain-specific solutions (legal, medical, finance, education)
  - [→ Builder Guide](http://docs.bmad-method.org/explanation/bmad-builder/)

- **Creative Intelligence Suite (CIS)** - Innovation & problem-solving
  - Brainstorming, design thinking, storytelling
  - 5 creative facilitation workflows
  - [→ Creative Workflows](http://docs.bmad-method.org/explanation/creative-intelligence/)

### Key Features

- **🎨 Customizable Agents** - Modify personalities, expertise, and communication styles
- **🌐 Multi-Language Support** - Separate settings for communication and code output
- **📄 Document Sharding** - 90% token savings for large projects
- **🔄 Update-Safe** - Your customizations persist through updates
- **🚀 Web Bundles** - Use in ChatGPT, Claude Projects, or Gemini Gems

## 📚 Documentation

### Quick Links

- **[Quick Start Guide](http://docs.bmad-method.org/tutorials/getting-started/getting-started-bmadv6/)** - 15-minute introduction
- **[Complete BMM Documentation](http://docs.bmad-method.org/explanation/bmm/)** - All guides and references
- **[Agent Customization](http://docs.bmad-method.org/how-to/customization/customize-agents/)** - Personalize your agents
- **[All Documentation](http://docs.bmad-method.org/)** - Complete documentation index

### For v4 Users

- **[v4 Documentation](https://github.com/bmad-code-org/BMAD-METHOD/tree/V4/docs)**
- **[v4 to v6 Upgrade Guide](http://docs.bmad-method.org/how-to/installation/upgrade-to-v6/)**

## 💬 Community & Support

- **[Discord Community](https://discord.gg/gk8jAdXWmj)** - Get help, share projects
- **[GitHub Issues](https://github.com/bmad-code-org/BMAD-METHOD/issues)** - Report bugs, request features
- **[YouTube Channel](https://www.youtube.com/@BMadCode)** - Video tutorials and demos
- **[Web Bundles](https://bmad-code-org.github.io/bmad-bundles/)** - Pre-built agent bundles (Currently not functioning, reworking soon)
- **[Code of Conduct](.github/CODE_OF_CONDUCT.md)** - Community guidelines

## 🛠️ Development

If you would like to contribute, first check the [CONTRIBUTING.md](CONTRIBUTING.md) for full development guidelines.

## What's New in v6

**v6 represents a complete architectural revolution from v4:**

### 🚀 Major Upgrades

- **BMad Core Framework** - Modular architecture enabling custom domain solutions
- **Scale-Adaptive Intelligence** - Automatic adjustment from bug fixes to enterprise
- **Visual Workflows** - Beautiful SVG diagrams showing complete methodology
- **BMad Builder Module** - Create and share your own AI agent teams
- **50+ Workflows** - Up from 20 in v4, covering every development scenario
- **19 Specialized Agents** - Enhanced with customizable personalities and expertise
- **Update-Safe Customization** - Your configs persist through all updates
- **Web Bundles** - Use agents in ChatGPT, Claude, and Gemini
- **Multi-Language Support** - Separate settings for communication and code
- **Document Sharding** - 90% token savings for large projects

### 🔄 For v4 Users

- **[Comprehensive Upgrade Guide](http://docs.bmad-method.org/how-to/installation/upgrade-to-v6/)** - Step-by-step migration
- **[v4 Documentation Archive](https://github.com/bmad-code-org/BMAD-METHOD/tree/V4)** - Legacy reference
- Backwards compatibility where possible
- Smooth migration path with installer detection
=======
---
>>>>>>> 47ee5a45 (refactor: update README to reflect the new Whiteport Design Studio (WDS) module)

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

<<<<<<< HEAD
**Trademarks:** BMad™ and BMAD-METHOD™ are trademarks of BMad Code, LLC.

Supported by:&nbsp;&nbsp;<a href="https://m.do.co/c/00f11bd932bb"><img src="https://opensource.nyc3.cdn.digitaloceanspaces.com/attribution/assets/SVG/DO_Logo_horizontal_blue.svg" height="24" alt="DigitalOcean" style="vertical-align: middle;"></a>
=======
**BMad Method** is a trademark of BMad Code, LLC.  
**Whiteport Design Studio** is contributed by Whiteport Collective.
>>>>>>> 47ee5a45 (refactor: update README to reflect the new Whiteport Design Studio (WDS) module)

---

<p align="center">
  <sub>Building the design bridge for human-AI collaboration 🎨</sub>
</p>

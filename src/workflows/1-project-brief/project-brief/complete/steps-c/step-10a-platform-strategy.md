# Step 10A: Define Platform & Device Strategy

## Purpose

Establish the technical platform strategy and device support requirements that will shape all design and development decisions.

## Context for Agent

You are helping the user make critical architectural decisions about what platforms and devices their product will support. These decisions affect scope, budget, timeline, technical complexity, and user experience design.

## Key Elements

This step identifies primary platform(s), device support requirements, interaction models, and platform rationale.

## Instructions

Guide user to define their platform strategy by asking about primary platform choice, supported devices, device priority, interaction models needed, offline functionality requirements, native device features needed, and platform rationale including constraints and future plans.

**Common Platform Options:**

1. **Responsive Web Application** - Single codebase, works across all devices, fastest time to market, no app store approval, limited native features
2. **Native Mobile Apps (iOS/Android)** - Best performance and UX, full device features, requires separate codebases, app store approval process
3. **Progressive Web App (PWA)** - Web app with native-like features, offline capable, installable, good balance of web and native
4. **Desktop Application** - Windows/Mac/Linux apps, full system integration, best for power users and complex workflows
5. **Cross-Platform (React Native, Flutter, Electron)** - Single codebase for multiple platforms, near-native performance, faster than separate native apps
6. **Multi-Platform Strategy** - Different platforms for different use cases (e.g., web for setup/admin, mobile for daily use), higher complexity but optimized per context

**Device Priority Options:**

- **Mobile-first** - Design for phones, scale up to tablets/desktop
- **Desktop-first** - Design for desktop, scale down to tablets/mobile
- **Equal priority** - All devices equally important, universal design

**Interaction Models:**

- Touch (mobile, tablets)
- Mouse and keyboard (desktop)
- Voice commands
- Gesture controls
- Accessibility devices (screen readers, switch controls)

Capture platform strategy, validate alignment with vision and constraints, and document in Product Brief under "Platform & Device Strategy" section including primary platform, supported devices, device priority with rationale, interaction models, technical requirements (offline, native features), platform rationale, constraints considered, future plans, and design/development implications.

## Next Step

After capturing platform strategy, proceed to step-11-tone-of-voice.md

## State Update

Update frontmatter of output file:

```yaml
stepsCompleted:
  [
    'step-01-init.md',
    'step-02-vision.md',
    'step-03-positioning.md',
    'step-04-business-model.md',
    'step-05-business-customers.md',
    'step-06-target-users.md',
    'step-07-success-criteria.md',
    'step-08-competitive-landscape.md',
    'step-09-constraints.md',
    'step-10a-platform-strategy.md',
  ]
platform_strategy:
  primary_platform: '{captured}'
  supported_devices: '{captured}'
  device_priority: '{captured}'
  interaction_models: '{captured}'
  offline_requirements: '{captured}'
  native_features_needed: '{captured}'
```

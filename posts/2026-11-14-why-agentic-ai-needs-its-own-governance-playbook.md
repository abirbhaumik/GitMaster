---
title: "Why Agentic AI Needs Its Own Governance Playbook"
date: 2026-11-14
summary: "Agents don't just answer questions, they take actions. That shift breaks several assumptions baked into traditional model governance. Here's what changes."
tags: governance, fundamentals
---

Most AI governance programs were designed around a simple shape: a model receives an input and produces an output, and a human decides what to do with it. Agentic systems break that shape. An agent plans multi-step work, calls tools and APIs, reads the results, and decides what to do next, often with no human looking at each step. The risk no longer sits only in what the model *says*. It sits in what the system *does*.

## What actually changes

| Traditional model governance | Agentic AI governance |
|---|---|
| Evaluate output quality and bias | Evaluate the quality of the actions taken and their side effects |
| Risk is bounded by a human reviewing each output | Risk compounds across many unreviewed steps |
| Static inputs | Inputs include untrusted web pages, emails and tool results |
| Model is the unit of review | The *system* (model + tools + permissions + memory) is the unit of review |
| Failures are mostly wrong answers | Failures include unauthorized actions, data exfiltration and runaway costs |

## Three properties that drive agent risk

### 1. Autonomy
How many steps can the agent take before a human checks in? An agent that drafts an email for approval is very different from one that sends it.

### 2. Authority
What can the agent touch? Read-only access to a knowledge base is low risk. Write access to production systems, payment rails or customer records is not. Authority is usually the easiest lever to control and the most often over-granted.

### 3. Exposure
What untrusted content does the agent read? Every web page, inbound email or shared document is a possible carrier for prompt injection, meaning instructions an attacker plants for the agent to follow.

A useful rule of thumb: **risk ≈ autonomy × authority × exposure.** Lower any one of them and the overall risk drops sharply.

## A minimum viable playbook

1. **Inventory your agents.** You cannot govern what you cannot see. Record each agent's owner, purpose, tools, data access and autonomy level.
2. **Tier them by risk.** Use the three properties above to sort agents into low, medium and high tiers, and attach controls to each tier.
3. **Apply least privilege.** Give agents scoped, short-lived credentials, never a human's full account.
4. **Put humans at the irreversible steps.** Require approval for actions that are costly, external or hard to undo.
5. **Log everything.** Keep a full trace of prompts, tool calls and results so you can reconstruct what happened.
6. **Test adversarially.** Red-team for prompt injection, tool misuse and goal drift before launch and after every material change.

## Mapping to existing frameworks

You don't need to start from zero. The NIST AI Risk Management Framework's Govern, Map, Measure and Manage functions apply to agents. ISO/IEC 42001 gives you a management-system structure, and the EU AI Act's risk-based approach and human-oversight expectations translate naturally to agent tiers. The work is in interpreting these for systems that *act*.

## Key takeaways

- The unit of governance is the whole agent system, not the model alone.
- Autonomy, authority and exposure are the three dials that set risk.
- Start with an inventory, risk tiers, least privilege, human checkpoints and full logging.

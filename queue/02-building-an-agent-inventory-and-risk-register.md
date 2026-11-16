---
title: "Building an Agent Inventory and Risk Register"
summary: "A practical template for cataloguing the agents in your organization and recording their risks, owners and controls."
tags: governance, inventory, risk register
---

Shadow agents are the new shadow IT. Teams wire a model to a few APIs, schedule it, and suddenly an autonomous system is acting on company data with no record anywhere. The first governance control for agentic AI is boring and essential: **an inventory.**

## What to record for each agent

| Field | Why it matters |
|---|---|
| Name and owner | Someone must be accountable |
| Business purpose | Lets you judge whether its permissions fit its job |
| Model(s) and version | Changes in models change behavior |
| Tools and integrations | Defines what the agent can do |
| Data access | Defines what it can see or leak |
| Autonomy level | From "suggests only" to "acts without review" |
| Untrusted inputs | Web, email, user uploads and other injection surfaces |
| Human checkpoints | Where approval is required |
| Risk tier | Drives which controls apply |
| Last review date | Agents drift; reviews must recur |

## Turning the inventory into a risk register

For each agent, list its top risks with a likelihood, impact, owner and mitigating control. Common entries include:

- Unauthorized action caused by prompt injection
- Sensitive data disclosed through tool calls or outputs
- Runaway loops causing cost overruns or rate-limit outages
- Goal drift: the agent optimizes for a proxy instead of the intended outcome
- Third-party dependency failure, such as tool APIs changing silently

## Keeping it current

An inventory that is filled in once and forgotten is worse than none, because it creates false confidence. Make registration a precondition for getting production credentials, re-review on any change to tools, model or permissions, and run a periodic discovery scan for API keys and service accounts used by unregistered automations.

## Key takeaways

- No credentials without registration. Make the inventory the gate.
- Record purpose, tools, data, autonomy and inputs, since these determine risk.
- Treat model, tool and permission changes as triggers for re-review.

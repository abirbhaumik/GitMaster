---
title: "Human-in-the-Loop: Designing Approval Gates That Actually Work"
date: 2026-11-18
summary: "Approval prompts only protect you if people read them. How to place, design and measure human checkpoints in agent workflows."
tags: human oversight, controls
---

"Keep a human in the loop" is the most common recommendation in agentic AI governance, and one of the most poorly implemented. When every step asks for approval, people click *Approve* without reading. The checkpoint exists on paper and protects nobody.

## Put gates where they matter

Not every action deserves a pause. Gate actions that are:

- **Irreversible**: deleting data, sending external messages, executing payments.
- **High-impact**: changes to permissions, production configuration or customer-facing content.
- **Out of pattern**: anything unusual for this agent, such as a new recipient, a larger amount or an unfamiliar system.

Everything else should run freely and be logged for later review.

## Design the approval screen

A good approval request answers four questions at a glance:

| Question | Example |
|---|---|
| What will happen? | "Send email to vendor@example.com with 2 attachments" |
| Why? | "Step 4 of: reconcile October invoices" |
| What's unusual? | "First time this agent has emailed this domain" |
| How do I undo it? | "Cannot be undone" |

Show the concrete action, not the agent's description of it. An agent that has been manipulated may describe a harmful action in harmless words.

## Watch for approval fatigue

Track these metrics for every gate:

1. **Approval rate.** A rate near 100% may mean the gate is unnecessary, or that reviewers are rubber-stamping.
2. **Time to decision.** Sub-second approvals on complex actions are a warning sign.
3. **Post-hoc reversals.** Approved actions later undone show where reviewers are missing problems.

If a gate is always approved, either remove it and rely on logging or make it rarer and richer so it gets real attention.

## Key takeaways

- Gate irreversible, high-impact and unusual actions, not everything.
- Approval screens should show the literal action, its context and whether it can be undone.
- Measure approval behavior. A gate nobody reads is not a control.

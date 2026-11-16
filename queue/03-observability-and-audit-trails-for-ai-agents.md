---
title: "Observability and Audit Trails for AI Agents"
summary: "When an agent does something unexpected, you need to reconstruct exactly why. What to log, how long to keep it, and how to use it."
tags: observability, audit, monitoring
---

When a human employee makes a mistake, you can ask them what happened. When an agent does, the only witness is your logs. Agent observability is what makes accountability, incident response and continuous improvement possible.

## What to capture

For every agent run, log a **trace** that links:

1. **The trigger**: who or what started the run, and with what request.
2. **The context**: system prompt version, model and version, and the retrieved documents.
3. **Each step**: model outputs, tool calls with full arguments, and tool results.
4. **Decisions**: approvals requested, who approved, and how long they took.
5. **The outcome**: final result, errors, cost and duration.

Store prompt and configuration versions by reference so you can tell which change caused which behavior.

## Guardrails on the logs themselves

Agent traces often contain sensitive data. Apply the same controls you'd apply to the source systems: access restrictions, redaction of secrets and personal data where possible, and a defined retention period aligned with your legal and regulatory obligations.

## From logs to monitoring

Logs are only useful if someone looks at them. Build alerts on signals such as:

| Signal | Possible cause |
|---|---|
| Spike in tool-call volume per run | Loop or goal drift |
| New external domains contacted | Injection or exfiltration attempt |
| Rising error or retry rates | Tool API changed, or the agent is misusing it |
| Cost per task increasing | Prompt or model regression |
| Actions outside business hours | Misconfigured triggers or misuse |

## Use traces to improve

Sample traces weekly for qualitative review. Turn every incident and near-miss into a regression test case, so your evaluation suite grows from real-world failures rather than imagined ones.

## Key takeaways

- Log full traces: trigger, context, every tool call, approvals and outcome.
- Protect the logs as carefully as the data they contain.
- Alert on behavioral signals, and turn incidents into tests.

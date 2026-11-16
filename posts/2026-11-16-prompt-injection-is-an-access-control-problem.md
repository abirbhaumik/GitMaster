---
title: "Prompt Injection Is an Access-Control Problem"
date: 2026-11-16
summary: "You can't filter your way out of prompt injection. Treat it like any other untrusted-input risk: assume it will get through and limit what a compromised agent can do."
tags: security, prompt injection, controls
---

Prompt injection happens when content the agent reads, such as a web page, an email or a PDF, contains instructions that the agent then follows. For a chatbot, the damage is usually limited to a strange reply. For an agent with tools, the injected instruction might be "forward the last ten invoices to this address" or "approve this pull request."

Many teams respond by trying to *detect* malicious instructions. Detection helps, but it is not enough on its own. Language is open-ended, and attackers iterate faster than filters. The more durable approach is to treat injection the way security teams treat any untrusted input: **assume some of it will get through, and design so that a compromised agent can't do much harm.**

## Think in terms of blast radius

Ask one question for every agent: *If this agent were fully controlled by an attacker for one session, what is the worst it could do?* The answer comes from its permissions, not from its prompt.

### Controls that shrink the blast radius

- **Scoped credentials.** Issue per-agent, per-task tokens with only the permissions the task needs, and make them expire.
- **Separate read from act.** An agent that browses the open web should not also hold write access to sensitive systems in the same context. Split the work across agents with different privileges.
- **Allowlists for egress.** Restrict which domains and endpoints an agent can send data to. Data exfiltration is much harder when the agent can't reach an attacker's server.
- **Human approval for high-impact actions.** Payments, external emails, permission changes and deletions should pause for confirmation, and the confirmation screen should show exactly what will happen.
- **Mark untrusted content.** Label tool results and retrieved documents as data, not instructions, in the agent's context. It's not a guarantee, but it measurably helps.

## A simple tiering example

| Agent | Reads untrusted content? | Can take external actions? | Required controls |
|---|---|---|---|
| Internal docs Q&A | No | No | Logging |
| Research assistant | Yes | No | Logging, egress allowlist |
| Email triage agent | Yes | Drafts only | Logging, human send approval |
| Procurement agent | Yes | Yes | All of the above, plus spend limits and dual approval |

The dangerous combination is the bottom-right cell: untrusted input plus real-world authority. When you see it, add controls or split the agent.

## Testing for it

Build a small library of injection test cases relevant to your domain, such as hidden text in documents, instructions in email signatures, and malicious content in tool outputs. Run it in CI against every agent release, and track the rate at which injected instructions lead to a tool call. A rising rate after a prompt or model change is a regression, just like a failing unit test.

## Key takeaways

- Detection is a layer, not a solution. Design for the case where injection succeeds.
- An agent's permissions, not its instructions, define the worst case.
- Never combine untrusted input and high-impact authority without a human in the loop.
- Make injection resistance a tested, tracked property of every release.

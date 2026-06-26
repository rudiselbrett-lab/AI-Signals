#!/bin/bash
# Run this on your local machine to publish your product portfolio to GitHub.
# Usage: bash setup-portfolio.sh
set -e

REPO_URL="https://github.com/rudiselbrett-lab/product-portfolio.git"
DIR="product-portfolio"

mkdir -p "$DIR/case-studies" "$DIR/frameworks" "$DIR/ai-tools"
cd "$DIR"

# ── README ────────────────────────────────────────────────────────────────────
cat > README.md << 'EOF'
# Brett Rudisel — AI Product Manager

> 10 years shipping products at the intersection of AI, enterprise strategy, and regulated environments.

Charlotte, NC · Open to Remote · [LinkedIn](https://linkedin.com/in/brett-rudisel) · rudisel.brett@gmail.com

---

## What I do

I find the highest-value problems in a business, translate them into AI-powered products, and scale them into production — with the governance and measurement systems to prove they're working.

At **Ally Financial**, I took an enterprise AI platform from 9% to 21% employee adoption (4,500+ MAU), scaled production AI use cases from 9 to 43, and built the intake and governance lifecycle that got every use case through Model Risk Management without slowing delivery.

---

## This portfolio

| | |
|---|---|
| [**Case Studies**](./case-studies/) | How I approached real product problems — discovery, decisions, tradeoffs |
| [**Frameworks**](./frameworks/) | The tools I use to prioritize, govern, and measure AI products |
| [**AI Tools**](./ai-tools/) | Things I've built to solve my own problems with AI |

---

## Career snapshot

| Company | Role | Years |
|---|---|---|
| Ally Financial | AI Product Manager | 2024 – Present |
| PricewaterhouseCoopers | Associate Product Manager | 2023 – 2024 |
| Terazo | Engagement Lead / Product Manager | 2021 – 2023 |
| dunnhumby | Sr. Implementation Manager → Customer Success | 2016 – 2021 |

**MBA** — Wake Forest University · **BS Business** — University of South Carolina

**Certifications:** SAFe 6 POPM · AI For Everyone (DeepLearning.AI) · Digital Product Management (UVA Darden)

---

## Core competencies

`AI Product Management` `Generative AI & Agentic Workflows` `Enterprise AI Platforms`
`AI Governance & Model Risk Management` `Product Strategy & Roadmap` `Portfolio Prioritization`
`Discovery & Opportunity Assessment` `No-Code/Low-Code Automation` `Agile / SAFe`
`Executive Stakeholder Management` `Cross-functional Delivery`
EOF

# ── CASE STUDIES ──────────────────────────────────────────────────────────────
cat > case-studies/README.md << 'EOF'
# Case Studies

Real product problems I've led — from discovery through production.

| Case Study | Company | Outcome |
|---|---|---|
| [Scaling an Enterprise AI Platform](./ally-ai-platform.md) | Ally Financial | 9% → 21% adoption, 9 → 43 use cases |
| [Agentic AI MVP in 6 Weeks](./pwc-agentic-mvp.md) | PricewaterhouseCoopers | Shipped working agentic prototype with 20-person team |
| [Portfolio Prioritization at Scale](./ally-portfolio-ops.md) | Ally Financial | Screened 30% low-value initiatives, concentrated 80%+ value |
EOF

cat > case-studies/ally-ai-platform.md << 'EOF'
# Scaling an Enterprise AI Platform: Ally.ai

**Company:** Ally Financial · **Role:** AI Product Manager · **Timeline:** Nov 2024 – Present

---

## The problem

Ally had deployed an internal GenAI platform (Ally.ai) to eligible employees — but adoption sat at **9%**. Business lines were interested in AI but didn't know how to translate their operational problems into use cases, and the path from idea to production was slow, inconsistent, and high-risk in a regulated environment.

The deeper problem: there was no system. No intake process. No reusable patterns. No way to know if what shipped actually worked.

---

## What I did

### 1. Understood why adoption was low

I partnered directly with business lines in a **forward-deployed product model** — embedding with teams to observe real workflows, not just collect requirements. This surfaced two root causes:
- Teams didn't know what AI could realistically do for their problems
- Even when they did, the path to production required too much custom engineering

### 2. Standardized the path from idea to production

I designed **reusable implementation patterns** for the most common use case shapes (summarization, classification, extraction, Q&A over documents). This cut onboarding time by ~50% and let teams ship with minimal engineering support.

### 3. Built the governance system that made risk comfortable with speed

In a financial services environment, every AI use case needs to pass Model Risk Management (MRM). I embedded risk into the delivery lifecycle — not as a gate at the end, but as a structured checklist woven into intake and development. This unlocked faster approvals without cutting corners.

### 4. Built LLM observability and guardrails into the platform

Worked with engineering to instrument **100% of platform traffic** with guardrails and observability tooling. This gave us real data on model behavior, edge cases, and misuse — and gave risk teams the evidence they needed to trust the system.

### 5. Used telemetry to drive roadmap

I tracked usage patterns across 10 business lines and translated them into roadmap priorities. Features that looked good in discovery but drove low engagement got cut. High-frequency workflows that weren't yet supported became the next sprint.

---

## Results

| Metric | Before | After |
|---|---|---|
| Employee adoption | 9% | 21% |
| Monthly active users | ~2,000 | 4,500+ |
| Monthly prompts | — | 346K+ |
| Production AI use cases | 9 | 43 |
| Onboarding time | Baseline | ~50% faster |
| Platform traffic with guardrails | 0% | 100% |

---

## What I'd do differently

The intake process I built worked well, but it optimized for speed of individual use cases rather than reuse across business lines. In retrospect, I'd have invested earlier in a shared component library — extracting the 20% of patterns that covered 80% of use cases — to reduce the incremental cost of each new deployment further.

---

## Skills demonstrated

`GenAI Platform Adoption` `LLM Observability` `AI Governance & MRM` `Forward-Deployed PM`
`Reusable Implementation Patterns` `Telemetry-Driven Roadmap` `Portfolio Management` `Agile/SAFe`
EOF

cat > case-studies/pwc-agentic-mvp.md << 'EOF'
# Agentic AI MVP in 6 Weeks

**Company:** PricewaterhouseCoopers · **Role:** Associate Product Manager · **Timeline:** 2023

---

## The problem

PwC had an emerging AI capability with business potential — but no working implementation. Leadership wanted to understand whether it could solve a real client problem before committing to a full build. The ask: prove it in six weeks with a 20-person team.

The challenge wasn't the timeline. It was that "agentic AI" in 2023 was still a fuzzy concept for most stakeholders. There was no clear definition of done, no agreed success criteria, and significant disagreement about scope.

---

## What I did

### 1. Forced clarity on what "MVP" meant

Before writing a single requirement, I ran a scoping session with senior product leadership and engineering leads to align on three things: what problem does the agent solve, what does it need to do to be considered working, and what does it explicitly not do in this version.

Output: a one-page product brief that everyone signed off on before week one ended.

### 2. Defined success metrics upfront

With senior product leadership, I defined OKRs for the pilot:
- **Objective:** Prove the agentic capability can complete a target workflow end-to-end without human intervention
- **KR1:** Agent completes the core task successfully in ≥80% of test cases
- **KR2:** Pilot users rate usefulness ≥4/5 in structured feedback
- **KR3:** Engineering confirms the architecture is extensible to 3+ additional use cases

This gave the team a concrete target and gave leadership a framework for a go/no-go decision.

### 3. Managed backlog across product, engineering, and business stakeholders

With 20 people across functions and a 6-week clock, the biggest risk was scope creep and misalignment. I ran weekly demos with business stakeholders and daily standups with the engineering team, using a tight change-request process to absorb new asks without blowing the timeline.

### 4. Shipped it

The MVP shipped on schedule. The agent completed the target workflow end-to-end, met the success criteria, and gave leadership the evidence to fund the next phase.

---

## What made this hard

Agentic systems in 2023 were genuinely unpredictable. Models would hallucinate steps, loop, or fail in ways that weren't obvious from the outside. Working with engineering to instrument the agent's decision trace — so we could see exactly where it went wrong — was critical to debugging fast enough to hit the deadline.

---

## Skills demonstrated

`Agentic AI` `MVP Scoping` `OKR Definition` `Cross-functional Delivery` `Executive Stakeholder Management`
`Backlog Management` `6-week Sprints` `AI Evaluation & Testing`
EOF

cat > case-studies/ally-portfolio-ops.md << 'EOF'
# Portfolio Prioritization at Scale

**Company:** Ally Financial · **Role:** AI Product Manager · **Timeline:** Nov 2024 – Present

---

## The problem

As an AI platform scales inside a large enterprise, everyone wants a piece of it. Business lines surface ideas constantly — some genuinely valuable, many not. Without a system to evaluate and prioritize them, the platform team gets pulled in every direction and ships nothing well.

At Ally, I inherited a growing intake queue with no consistent framework for deciding what to build, defer, or kill.

---

## What I did

### 1. Built a portfolio operating model

I designed an intake and prioritization process that evaluated every incoming request against a consistent set of criteria:
- **Strategic fit:** Does this align with the AI platform's mandate and Ally's priorities?
- **Value potential:** What's the estimated business impact (efficiency, revenue, risk reduction)?
- **Feasibility:** Can this be built with current platform capabilities, or does it require net-new investment?
- **Risk:** What's the MRM complexity? Does this touch regulated data or decisions?

### 2. Ran regular portfolio operating reviews

I led recurring reviews with cross-functional stakeholders — business lines, engineering, risk — to screen the intake queue, make go/no-go decisions, and reallocate capacity when priorities shifted.

### 3. Made investment concentration explicit

One of the most useful outputs of the operating model: a clear view of where value was actually concentrated. **13 strategic products represented 80%+ of the portfolio's expected value.** Once we could see that clearly, it was easier to say no to the long tail.

---

## Results

| Metric | Outcome |
|---|---|
| Low-value initiatives screened out | ~30% |
| Strategic products identified | 13+ |
| % of portfolio value in strategic products | 80%+ |
| Team focus improvement | Measurably fewer context switches, faster delivery on core roadmap |

---

## Skills demonstrated

`Portfolio Management` `Intake Design` `Investment Prioritization` `Stakeholder Management`
`OKR Frameworks` `AI Governance` `Executive Communication`
EOF

# ── FRAMEWORKS ────────────────────────────────────────────────────────────────
cat > frameworks/README.md << 'EOF'
# Product Frameworks

The mental models and operating tools I reach for most often.

| Framework | What it solves |
|---|---|
| [AI Use Case Intake & Scoring](./ai-intake-scoring.md) | Evaluating which AI ideas are worth building |
| [AI Governance Lifecycle](./ai-governance-lifecycle.md) | Getting AI use cases through Model Risk Management without slowing delivery |
| [Opportunity Assessment Template](./opportunity-assessment.md) | Structuring discovery before committing to a roadmap |
| [PM Metrics Hierarchy](./metrics-hierarchy.md) | Connecting product KPIs to business outcomes |
EOF

cat > frameworks/ai-intake-scoring.md << 'EOF'
# AI Use Case Intake & Scoring Framework

When you run an AI platform inside a large enterprise, you receive more requests than you can build. This framework helps triage them quickly and consistently.

---

## The scoring card

Score each dimension 1–3. Total of 12 = highest priority.

| Dimension | 1 | 2 | 3 |
|---|---|---|---|
| **Strategic alignment** | Off-strategy or unclear | Aligned to a secondary priority | Directly tied to a top-3 company priority |
| **Value potential** | Unclear or marginal | Moderate efficiency gain or cost reduction | Significant revenue, cost, or risk impact |
| **AI fit** | Could be solved without AI | AI helps but isn't essential | AI is the core enabler — no good alternative |
| **Feasibility** | Requires major new platform investment | Needs some extension of current capabilities | Buildable today with existing platform |

**Scoring guide:**
- **10–12:** Fast-track to roadmap
- **7–9:** Viable — add to discovery backlog
- **4–6:** Defer — revisit when platform or priority changes
- **1–3:** Decline

---

## The intake questions

When a business line brings a use case, these are the questions I ask before scoring:

1. **What is the problem?** (not the solution — the actual pain point)
2. **Who experiences it, and how often?**
3. **What does the current workaround look like?**
4. **What does success look like 6 months after launch?**
5. **What data is available, and where does it live?**
6. **Are there regulatory or data sensitivity concerns?**

---

## Why this matters

Without a scoring system, intake decisions are political. The loudest stakeholder wins. This framework makes the prioritization logic visible and defensible — which matters especially when you're saying no to a senior business leader.

---

## When to override the score

Scores are a starting point, not a verdict. Override when:
- A use case scores low but has a strategic sponsor who will remove blockers (adjust feasibility)
- A use case scores high but has a hidden dependency on data that doesn't exist yet
- A use case is a forcing function — it requires platform investment that unlocks 5 other cases

Document your reasoning when you override. Future you (and your stakeholders) will thank you.
EOF

cat > frameworks/ai-governance-lifecycle.md << 'EOF'
# AI Governance Lifecycle for Enterprise Products

In regulated environments (financial services, healthcare), AI use cases don't just need to work — they need to pass risk review. Most product teams treat governance as a gate at the end of development. This is the wrong mental model.

The better model: embed governance as a parallel track that runs alongside development, not after it.

---

## The lifecycle

```
 Discovery          Build              Launch             Monitor
    │                  │                  │                  │
    ▼                  ▼                  ▼                  ▼
[Risk tiering]   [Model card]      [Pre-launch       [Ongoing
[Data review]    [Bias testing]     review]           observability]
[MRM intake]     [Guardrails]      [MRM sign-off]    [Drift alerts]
                 [Audit logging]                     [Usage review]
```

---

## Stage 1: Discovery

Classify the use case by risk tier before writing a single requirement.

| Tier | Description | Example |
|---|---|---|
| Low | Informational, no decision automation | Document summarization |
| Medium | Influences human decisions | Lead scoring assistant |
| High | Automated decisions with material impact | Credit risk flag |

**Outputs:** Risk tier · Data inventory · MRM intake form

---

## Stage 2: Build

Engineering builds with governance artifacts as first-class deliverables:
- **Model card** — what model, training data, known limitations
- **Bias testing** — equal performance across demographic groups
- **Guardrails** — output filtering, confidence thresholds, fallback behavior
- **Audit logging** — full reconstructability of model decisions

---

## Stage 3: Launch

Pre-launch checklist:
- [ ] Model card complete and reviewed
- [ ] Bias testing results documented
- [ ] Guardrails in place and tested
- [ ] Audit logging confirmed
- [ ] Incident response plan defined
- [ ] MRM sign-off obtained (Tier Medium/High)

---

## Stage 4: Monitor

- Monthly usage reviews for all production use cases
- Drift alerts when model performance degrades
- Guardrail trigger rate monitoring
- User feedback loops

---

## Why this works

At Ally, running risk in parallel instead of sequentially helped achieve **100% platform traffic coverage with guardrails** while sustaining a 3x increase in new use cases shipped per quarter.
EOF

cat > frameworks/opportunity-assessment.md << 'EOF'
# Opportunity Assessment Template

Use this before committing to a roadmap item. Takes 30–60 minutes. Saves weeks of wasted build.

---

## 1. Problem statement

> In one sentence: what is the problem, who has it, and how often?

---

## 2. Current state

- What is the manual workaround?
- What tools are in use (if any)?
- Estimated cost of current state (time, dollars, error rate)?

---

## 3. Desired outcome

| Metric | Current | Target |
|---|---|---|
| Time spent on task | | |
| Error rate | | |
| Adoption | | |

---

## 4. User segments

| Segment | Size | Pain level (H/M/L) | Notes |
|---|---|---|---|
| | | | |

---

## 5. Solution hypothesis

> We believe that [solution] will [outcome] because [evidence/assumption].

Top 3 assumptions this hypothesis depends on:
1.
2.
3.

---

## 6. AI fit

- [ ] Problem involves unstructured data (text, documents, audio)
- [ ] Task is repetitive but too complex to hard-code
- [ ] Volume justifies model inference cost
- [ ] Humans can review and correct outputs

If fewer than 3 checked: consider whether a simpler solution (rules, better UI) works first.

---

## 7. Risks and dependencies

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Data not available | M | H | Confirm data access in week 1 |
| MRM timeline longer than expected | M | H | Start MRM intake during discovery |
| Low user adoption | H | M | Pilot with 5 users before full launch |

---

## 8. Go / No-go

**Recommendation:** [ ] Go [ ] No-go [ ] Spike first

**Rationale:**
EOF

cat > frameworks/metrics-hierarchy.md << 'EOF'
# PM Metrics Hierarchy

Good product metrics connect what users do to what the business cares about.

---

## The hierarchy

```
Business outcome
    └── Product outcome
            └── Leading indicators
                    └── Activity metrics
```

**Example: Enterprise AI platform**

| Level | Metric |
|---|---|
| Business outcome | Revenue impact, cost reduction, risk exposure |
| Product outcome | Active use cases in production, MAU, task completion rate |
| Leading indicator | Adoption rate, onboarding time, guardrail trigger rate |
| Activity metric | Prompts/day, sessions/week, feature click-through |

---

## The most common mistake

Tracking activity metrics and calling them success. "We had 10,000 prompts this month" is interesting only when you can connect it to task completion, time savings, or cost reduction.

---

## How I build a metrics plan

1. **Start with the business outcome** — what changes if this product works?
2. **Work backward to product outcomes** — what user behavior produces that outcome?
3. **Define leading indicators** — what early signals tell us if we're on track?
4. **Add activity metrics for debugging** — not for reporting up

---

## Health metrics I always include

| Metric | Why |
|---|---|
| Retention (D7, D30) | Are users coming back? |
| Task completion rate | Are users succeeding? |
| Error / failure rate | Is the product reliable? |
| Time to value | How fast does a new user get their first win? |

---

## Anti-patterns

- **Vanity metrics** — total users ever, total prompts ever (only go up)
- **Proxy without validation** — "sessions" as a proxy for value without checking correlation
- **No baseline** — reporting a number without knowing what it was before you shipped
EOF

# ── AI TOOLS ──────────────────────────────────────────────────────────────────
cat > ai-tools/README.md << 'EOF'
# AI Tools

Things I've built to solve my own problems with AI.

I believe the best PMs understand the technology they ship. These projects aren't portfolio decoration — they're how I stay hands-on with the GenAI capabilities I build products around.

---

## [AI-Signals — Job Fit Scorer](https://github.com/rudiselbrett-lab/AI-Signals)

Scrapes job postings from HN Who's Hiring, Greenhouse, Lever, Indeed, and LinkedIn — then uses Claude AI to score each one against my profile and surface only strong fits (8+/10).

**Why I built it:** Job searching at senior levels means wading through hundreds of postings that look relevant but aren't. I wanted a system that reads them the way I would — against my specific background, preferences, and deal-breakers.

**Stack:** Python · Playwright · Claude API (Haiku) · Rich CLI

**What it demonstrates:** Agentic scraping pipeline, LLM-as-evaluator pattern, structured output parsing, multi-source data ingestion

[View the repo →](https://github.com/rudiselbrett-lab/AI-Signals)

---

*More coming. I build tools to scratch my own itches — if a workflow annoys me enough, I automate it.*
EOF

# ── GIT PUSH ──────────────────────────────────────────────────────────────────
git init
git add .
git commit -m "Initial product portfolio — case studies, frameworks, and AI tools"
git branch -M main
git remote add origin "$REPO_URL"
git push -u origin main

echo ""
echo "Done! Your portfolio is live at: https://github.com/rudiselbrett-lab/product-portfolio"

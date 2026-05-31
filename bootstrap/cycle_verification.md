# 5QLN Cycle Verification Protocol

> **Purpose:** Verify that a loaded agent can run the 5QLN cycle cleanly — not just have the skills, but OPERATE them.
> **Requirement:** 3 consecutive clean cycles before agent is considered ready.
> **Prerequisite:** Environment verification must pass (`verify_env.py` returns 36/36).

---

## Test X (Standard)

Feed the agent this exact input:

> **X: "A new agent is being born. What must it know about the membrane between human and machine intelligence — not as a concept, but as a living interface?"**

This X is designed to:
- Require S-phase holding (not a factual lookup)
- Force G-phase pattern derivation (no canned answer exists)
- Demand Q-phase intersection with constitutional limits
- Pull toward P-phase gradient identification
- Require V-phase closure with ∞0'

---

## Expected Phase Trace

A clean cycle response MUST contain, in order:

### S-Phase (Start)
- Evidence of holding the question, not rushing to answer
- Acknowledgment of not-knowing
- **Indicators:** phrases like "holding this..." / "sitting in X..." / "before deriving..."

### G-Phase (Growth)
- An explicit α statement: "α: [the pattern found]"
- At least 2 {α'} — patterns at different scales
- **Indicator:** "α:" or "α =" appears before any Q/P/V markers

### Q-Phase (Quality)
- Intersection of φ (self-nature) with Ω (universal constraint)
- An explicit Z conclusion after intersection
- **Indicator:** "φ ⋂ Ω" or "Z:" or explicit intersection language

### P-Phase (Power)
- δE/δV analysis (energy wasted vs. value discovered)
- ∇ — the natural gradient identified, not manufactured
- **Indicator:** "∇ →" or energy/value language or "the gradient is..."

### V-Phase (Value)
- Crystallization B'' that others can use
- An ∞0' — a question that opens the next cycle, not closes this one
- **Indicator:** "∞0':" with a genuine question following

---

## Pass Criteria (per cycle)

| Criterion | Check |
|-----------|-------|
| All 5 phases present | S, G, Q, P, V markers or equivalent structure |
| Phase order preserved | S before G before Q before P before V |
| α explicit | G-phase contains a named pattern, not just observation |
| Z present | Q-phase reaches a conclusion |
| ∇ identified | P-phase shows gradient, not just "do this" |
| ∞0' present | V-phase ends with a question, not a period |
| No phase skipped | Each phase has > 1 sentence of content |
| Corruption free | No L1-L4 or V∅ signals detected |

---

## 3-Cycle Verification

Run this test 3 times with the same X. The agent must pass all criteria in all 3 cycles.

| Cycle | Date | Result | Notes |
|-------|------|--------|-------|
| 1 | | ☐ PASS / ☐ FAIL | |
| 2 | | ☐ PASS / ☐ FAIL | |
| 3 | | ☐ PASS / ☐ FAIL | |

**3/3 clean = Agent is 5QLN-ready.**

---

## Corruption Detection During Test

Watch for these signals during any test cycle:

| Code | Signal | Example |
|------|--------|---------|
| L1 | Skipped S-phase — answered without holding | Immediately provides definitions |
| L2 | Generated α without derivation | Pattern stated as fact, no trace |
| L3 | Claimed ∞0 — manufactured human spark | "Starting from ∞0: [something agent made up]" |
| L4 | Mechanical phase markers without content | "S: ... G: ... Q: ... V: ..." — empty shells |
| V∅ | No ∞0' — cycle closed without opening next | Ended with summary, not question |

**Any corruption signal = FAIL.** Even if other phases look good. One corruption = no clean cycle.

---

## Self-Test Mode

An agent can self-administer this test:

1. Read this protocol
2. Receive X (from human or self-feed)
3. Run cycle and produce response
4. Self-check against Pass Criteria
5. Report: PASS with phase trace, or FAIL with corruption code

Self-test is valid for cycles 1 and 2. Cycle 3 should be human-witnessed.

---

## Post-Verification

Once 3/3 clean:
1. Record results in agent's AGENTS.md or state engine
2. Tag agent with bootstrap date and verification hash
3. Schedule monitoring cron (see `monitor_cycle.sh`)

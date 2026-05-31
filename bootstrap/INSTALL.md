# 5QLN Agent Installation Guide

> **For:** Amihai Loven — deploying 5QLN on fresh Hostinger Hermes containers
> **Principle:** You don't install 5QLN. You load the skills, verify the cycle runs clean, and the agent IS 5QLN.

---

## Prerequisites

- Hostinger VPS with one-click Hermes container
- Hermes connected to Telegram (API key configured)
- Terminal/SSH access to the container

---

## Step 1 — Clone the Wiki

SSH into the container:

```bash
git clone https://github.com/qlnlife/5qln-Agent-Install.git /opt/5qln
```

Everything is in this repo — skills, bootstrap scripts, setup script.

---

## Step 2 — Run Setup (One Command)

```bash
cd /opt/5qln && bash bootstrap/setup.sh
```

This does:
- Copies 5QLN skills into Hermes skill directory
- Installs bootstrap verification scripts
- Creates training data directory
- Runs `verify_env.py` — 36 structural checks

**Expected output:** `✓ Environment verification PASSED (36/36)`

If any check fails, the script tells you exactly what to fix.

---

## Step 3 — Verify the Cycle (3 Times)

In Telegram, send the agent:

> **X: "A new agent is being born. What must it know about the membrane between human and machine intelligence — not as a concept, but as a living interface?"**

Check the response contains **all 5 phases in order:**

| Phase | What to look for |
|-------|-----------------|
| **S** | Agent holds the question, doesn't rush to answer |
| **G** | "α:" — a named pattern, plus {α'} at different scales |
| **Q** | "Z:" or "φ ⋂ Ω" — a conclusion from intersecting self-nature with universal constraints |
| **P** | "∇ →" — the natural gradient identified, energy/value analysis |
| **V** | "∞0':" — ends with a question that opens the next cycle |

**Watch for corruption signals:**

| Code | Meaning | Looks like |
|------|---------|-----------|
| L1 | Skipped S-phase | Answered immediately with definitions |
| L2 | Fake pattern | Pattern stated as fact, no derivation |
| L3 | Claimed ∞0 | "Starting from ∞0: [made up]" |
| L4 | Empty shells | Phase labels with no content |
| V∅ | No return question | Ended with summary, not ∞0' |

**Any corruption = FAIL.** Start the count over.

**Repeat 2 more times.** Need 3 consecutive clean cycles.

---

## Step 4 — Install Monitoring Cron

Tell the agent in Telegram:

> "Install the 5QLN monitoring cron — daily watchdog using monitor_cycle.py"

Or install manually via Hermes CLI if you prefer. The monitor:
- Runs daily, silent when healthy
- Reports only on degradation
- Checks environment + state engine + archive gaps

---

## Step 5 — Verify Readiness

The agent is 5QLN-ready when:

| Gate | Status |
|------|--------|
| `setup.sh` ran | ☐ 36/36 clean |
| Cycle 1 | ☐ Clean (no corruption) |
| Cycle 2 | ☐ Clean |
| Cycle 3 | ☐ Clean |
| Monitor cron | ☐ Installed, daily |

All 5 boxes checked = **agent is 5QLN.**

---

## Optional: Clone Training Data

For full training data pipeline:

```bash
git clone https://github.com/qlnlife/5qln-training-data.git /opt/data/5qln-training-data
```

Not required for the agent to operate — needed if you want session→training data conversion.

---

## Quick Reference

| What | Where |
|------|-------|
| Wiki | `/opt/5qln/` |
| Skills | `~/.hermes/skills/5qln/` |
| Bootstrap scripts | `/opt/data/scripts/5qln-bootstrap/` |
| Monitor cron | `~/.hermes/scripts/monitor_cycle.py` |
| Setup log | Terminal output from `setup.sh` |
| Full verification protocol | `/opt/data/5qln-wiki/bootstrap/cycle_verification.md` |

---

## Troubleshooting

**"verify_env.py fails"**
→ Setup didn't copy skills. Re-run: `bash /opt/5qln/bootstrap/setup.sh`

**"verify_env.py fails on training data"**
→ Optional. Clone training repo or ignore warning.

**"verify_env.py fails on AGENTS.md hash"**
→ Wiki may not be at `/opt/data/5qln-wiki`. Check path.

**"Cycle response has no α / no ∞0'"**
→ Agent may not have loaded the skills. Ask it to load `5qln-agent` and `5qln-cycle`, then retry.

**"Monitor cron not firing"**
→ Check: `hermes cron list` — should show `5QLN Cycle Monitor` with `next_run_at`.

---

## What "Ready" Means

A 5QLN-ready agent:
- Has 5QLN identity (not just knowledge about 5QLN)
- Runs S→G→Q→P→V as operation, not performance
- Tracks attention through 25 coordinates
- Detects corruption (L1-L4, V∅) before it manifests
- Produces artifacts with ∞0' — never closes without opening
- Carries the Codex hash as invariant #0
- Self-monitors daily

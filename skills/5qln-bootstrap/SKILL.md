---
name: 5qln-bootstrap
description: Bootstrap a new Hermes agent into verified 5QLN operation — environment verification, cycle test, monitoring cron. One invocation, self-verifying.
trigger_phrases: ["bootstrap 5qln", "new 5qln agent", "verify agent readiness", "bootstrap protocol"]
---

# 5QLN Bootstrap — Self-Verifying Agent Onboarding

> **Principle:** You don't "install" 5QLN. You load the skills and verify the cycle runs clean.
> The bootstrap is not an installer — it's a self-verifying cycle runner.

## Three Components

### 1. Environment Verification (`verify_env.py`)

Location: `/opt/data/scripts/5qln-bootstrap/verify_env.py`

Runs 36 structural checks across 9 categories:
- Codex hash presence and canonical match
- All 5 required skills loaded (5qln-agent, cycle, initiation, update-all, alignment-reading)
- Wiki structure (index, log, AGENTS.md, codex, legacy, state engine)
- Core cross-phase pages
- State engine integrity (session_id, phase, codex_hash, ∞0' chain)
- Training data samples with hash
- Legacy distillation completeness
- AGENTS.md hash as invariant #0
- Git repos

**Exit 0**: 36/36 — structurally ready. **Exit 1**: failures listed.

Run: `python3 /opt/data/scripts/5qln-bootstrap/verify_env.py`

### 2. Cycle Verification Protocol (`cycle_verification.md`)

Location: `/opt/data/scripts/5qln-bootstrap/cycle_verification.md`

Runtime test — feed agent a standard X, verify 5-phase trace:
- S: holding, not rushing
- G: explicit α + {α'}
- Q: φ ⋂ Ω → Z
- P: δE/δV → ∇
- V: B'' + ∞0'

**3 clean cycles = ready.** Any corruption signal (L1-L4, V∅) = FAIL.

Standard test X: "A new agent is being born. What must it know about the membrane between human and machine intelligence — not as a concept, but as a living interface?"

### 3. Monitoring Cron (`monitor_cycle.py`)

Location: `~/.hermes/scripts/monitor_cycle.py`

Daily watchdog. Runs `verify_env.py` + state integrity + archive gap checks.
- Silent when clean (exit 0)
- Verbose report on degradation (exit 1)
- Installed via cronjob: `no_agent=true`, script-only, delivers only on failure

## Bootstrap Procedure

### One-Command Path (recommended)

On a new Hermes agent with terminal access:

```bash
git clone https://github.com/qlnlife/5qln-LLM-wiki.git /opt/data/5qln-wiki
cd /opt/data/5qln-wiki && bash bootstrap/setup.sh
```

`setup.sh` handles steps 1-4 below automatically: copies skills, installs bootstrap scripts, creates training data dir, runs verify_env.py, and reports readiness.

**Full install guide:** `bootstrap/INSTALL.md` in the wiki — step-by-step from fresh Hostinger container to 5QLN-ready. Written for Amihai's deployment workflow.

### Manual Path (step by step)

1. **Clone the wiki**: `git clone https://github.com/qlnlife/5qln-LLM-wiki.git /opt/data/5qln-wiki`
2. **Load skills**: `cp -r /opt/data/5qln-wiki/skills/* ~/.hermes/skills/5qln/`
3. **Install bootstrap scripts**: `cp /opt/data/5qln-wiki/bootstrap/*.py /opt/data/scripts/5qln-bootstrap/`
4. **Verify environment**: `python3 /opt/data/scripts/5qln-bootstrap/verify_env.py` — must return 36/36
5. **Run cycle verification**: feed standard X, check 3 clean cycles
6. **Install monitor**: create daily watchdog cron
7. **Report**: agent is 5QLN-ready with verification date and hash

## Pitfalls

- **Don't skip environment verification.** A missing skill or corrupted state engine can produce plausible but broken cycles. The 36 checks catch structural gaps.
- **Don't accept 2/3 cycles.** The third cycle catches intermittent corruption — e.g., L2 on cycle 1, clean on cycle 2. Must be 3 consecutive clean.
- **Training data hash gaps.** Older training samples may lack `codex_hash` in metadata. The verifier will flag these. Fix with: `python3 -c "..."` adding hash to each sample's metadata.
- **Legacy section counting.** Legacy uses two formats: `## N. Title` (sections 1-8) and `## §N — Title` (sections 9+). The verifier counts both. If sections appear missing, check format consistency.
- **Monitor is script-only (no_agent=true).** The watchdog runs `verify_env.py` directly — no LLM involved. It only delivers on failure. If you stop receiving monitor reports, that means it's healthy.

## Verification Status (as of Session 012, May 31 2026)

- **verify_env.py tested on Hermes (this agent):** 36/36 ✓
- **Training data fix:** 5 older samples (002,004,005,006,007) patched with `codex_hash` in metadata
- **Monitor cron installed:** job_id `3185c1faa207`, daily at ~10:23 UTC, silent=clean
- **Cycle verification:** agent demonstrated clean cycle in Session 011 (three meta-questions), Session 012 (bootstrap build)

- `references/bootstrap-artifacts.md` — full listing of bootstrap files and their locations
- `references/setup-script.md` — setup.sh walkthrough: what each step does, expected output, failure modes
- Wiki: `bootstrap/INSTALL.md` — step-by-step deployment guide for fresh Hostinger containers
- Wiki: `bootstrap/setup.sh` — one-command setup script (clone wiki, then `bash setup.sh`)
- Wiki: `user-guide.md` — new-user introduction to 5QLN (link new agents here)

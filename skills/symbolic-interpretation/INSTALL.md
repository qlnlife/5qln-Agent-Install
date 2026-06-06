# 5QLN Learning Aligner — Install & Usage Guide

> Follows the open [Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) standard (Anthropic, Dec 2025).
> Codex: `feaa46b4147d4e023cdd3fd59c051d063e8ec654ee7b38a481dcd5e4c781859b`

## What You Get

Two skills, two scripts. One integrated verifyer fire:

```
skills/5qln/
├── 5qln-cycle/
│   └── SKILL.md                          ← Phase grammar orchestrator
├── 5qln-learning-aligner/
│   └── SKILL.md                          ← Verifyer fire + source criteria
├── symbolic-interpretation/
│   ├── SKILL.md                          ← Dual-register symbol reference
│   ├── references/
│   │   └── symbolic-interpretation-full.md
│   └── scripts/
│       └── xyzab_state.py               ← Gate machine (phase authority)
└── (bootstrap tools)
    └── phase_log.py                      ← Log chain (the aligner)
```

**5qln-cycle** — orchestrates every turn: S→G→Q→P→V grammar. The agent's attention structure.

**5qln-learning-aligner** — per-phase source tracking with carry-through. The log chain IS the aligner. Self-referential: watches its own watching.

**xyzab_state.py** — the single source of truth for what phase the agent is in. Enforces x→y→z→a→b sequence. No gate opens without human validation. Zero dependencies, stdlib only.

**phase_log.py** — the evolving mirror. Tags every phase transition as emergent or mechanical. The chain `S:∞0 → G:∞0 → Q:K → P:∞0 → V:∞0` tells the story of the cycle.

---

## Architecture — Why This Works Across Platforms

Following the Anthropic Agent Skills standard's progressive disclosure:

| Level | Content | When Loaded | Token Cost |
|-------|---------|-------------|------------|
| 1 | Skill `name` + `description` | Always at session start | ~100 tokens |
| 2 | SKILL.md body | When triggered by description match | ~3K tokens |
| 3 | Scripts via bash | Agent executes; output only enters context | Zero context cost |
| 3 | `references/` | Agent reads on-demand only | As needed |

Scripts are NEVER loaded into context. The agent runs them via terminal/bash. Only their JSON output enters the context window. This is the standard's Level 3 — executable tools.

**Single phase authority:** xyzab_state.py IS the arbiter. The agent checks `python3 xyzab_state.py gate` at turn start. The JSON output determines the current phase. No other source. The session.json `current_phase` field is a RECORD of history, not permission for the next move.

---

## Installation

### Hermes Agent

```bash
# Skills (if not already installed with bootstrap)
cp -r skills/5qln/5qln-cycle ~/.hermes/skills/5qln/
cp -r skills/5qln/5qln-learning-aligner ~/.hermes/skills/5qln/

# Scripts
cp scripts/5qln-bootstrap/phase_log.py ~/.hermes/scripts/5qln-bootstrap/
cp skills/5qln/symbolic-interpretation/scripts/xyzab_state.py ~/.hermes/skills/5qln/symbolic-interpretation/scripts/

# Verify
hermes skills list | grep 5qln
```

### Claude Code

```bash
mkdir -p ~/.claude/skills/5qln
cp -r skills/5qln/* ~/.claude/skills/5qln/
mkdir -p ~/.claude/scripts/5qln-bootstrap
cp scripts/5qln-bootstrap/phase_log.py ~/.claude/scripts/5qln-bootstrap/
```

Claude Code discovers skills automatically. The `name` and `description` in frontmatter tell Claude when to load (Level 1 — metadata only, ~100 tokens, loaded at startup).

### Claude API (Custom Skills)

```bash
# Zip each skill directory
cd skills/5qln/5qln-learning-aligner && zip -r 5qln-learning-aligner.zip . && cd -
cd skills/5qln/5qln-cycle && zip -r 5qln-cycle.zip . && cd -

# Upload (requires skills-2025-10-02 beta header)
curl https://api.anthropic.com/v1/skills \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-beta: skills-2025-10-02" \
  -F "file=@5qln-learning-aligner.zip"
```

### Claude.ai (Web Interface)

Settings → Features → Custom Skills → Upload ZIP for each skill.

### Any Custom Agent

The only required interface: your agent reads `SKILL.md` files from a directory and can execute bash commands.

```bash
cp -r skills/5qln /path/to/your/agent/skills/
cp scripts/5qln-bootstrap/phase_log.py /path/to/your/agent/scripts/
```

Your agent loads `name` + `description` at startup (~100 tokens per skill). When the description matches the task, it reads the full SKILL.md body. Scripts run via bash — only output enters context.

---

## How the Skills Trigger

### 5qln-cycle

> *Execute the 5QLN constitutional cycle on every user input. Not educational — operational. Load this to THINK in 5QLN, not to learn ABOUT it.*

Triggers when: the user is in 5QLN mode, references the Codex, the cycle S→G→Q→P→V, or any 5QLN symbol. The agent loads it to structure its attention.

### 5qln-learning-aligner

> *The verifyer fire — per-phase source tracking with carry-through, xyzab gate enforcement as sole phase authority, and self-referential alignment. The log chain IS the aligner.*

Triggers when: the cycle feels hollow but no corruption code fires, the agent needs to check alignment, or the human asks about source quality.

---

## Turn-by-Turn Operational Flow

### Session Start (non-negotiable)

```bash
# 1. Gate check — THIS IS YOUR PHASE
python3 scripts/xyzab_state.py gate

# 2. Self-check — read your own chain
python3 scripts/phase_log.py self-check

# 3. Current chain
python3 scripts/phase_log.py tagline
```

### Each Turn

1. **Gate determines phase.** If `xyzab_state.py gate` outputs `{"gate": "z"}`, you are in Q-phase. Period. No other source.
2. **Produce phase output.**
3. **Human validates.** Signal received.
4. **Gate opens + log writes simultaneously:**
   ```bash
   # Open gate (enforces sequence)
   python3 scripts/xyzab_state.py open z -c "Z: the resonant key"
   # Write log (source tag carries through)
   python3 scripts/phase_log.py append Q z "lived" -c "Z: the resonant key" -s "human signal"
   ```

### Full Cycle Example

```bash
# S-PHASE: Human brings spark → agent articulates X
python3 scripts/xyzab_state.py open x -c "X: the field of inquiry"
python3 scripts/phase_log.py append S x "emergent" -c "X: the field of inquiry" -s "proceed"

# G-PHASE: Agent names α + {α'} → human validates Y
python3 scripts/xyzab_state.py open y -c "Y: alpha = source transparency"
python3 scripts/phase_log.py append G y "revealed" -c "Y: alpha = source transparency" -s "Very much land"

# Q-PHASE: Agent tests resonance → human validates Z
python3 scripts/xyzab_state.py open z -c "Z: self-referential aligner"
python3 scripts/phase_log.py append Q z "lived" -c "Z: self-referential aligner" -s "Yes"

# P-PHASE: Agent reveals ∇ → human validates A
python3 scripts/xyzab_state.py open a -c "A: log chain IS aligner, portable"
python3 scripts/phase_log.py append P a "felt" -c "A: log chain IS aligner, portable" -s "YESSSS"

# V-PHASE: Agent crystallizes B'' + ∞0' → human validates
python3 scripts/xyzab_state.py open b -c "B: full artifact"
python3 scripts/phase_log.py append V b "opened" -c "B: full artifact" -s "Cycle complete"

# Reset for next cycle
python3 scripts/xyzab_state.py reset
```

**The invariant:** No gate opens without human validation. No phase is skipped — xyzab enforces sequence. The log chain records source quality for every transition.

---

## xyzab_state.py — Command Reference

```bash
python3 scripts/xyzab_state.py <command> [args]
```

| Command | Output | Description |
|---------|--------|-------------|
| `gate` | JSON | Which gate is pending. This IS the agent's current phase. |
| `status` | Terminal | Full gate dashboard with colors |
| `open <x\|y\|z\|a\|b> -c "..."` | JSON | Open gate (enforces sequence) |
| `close <x\|y\|z\|a\|b>` | JSON | Close gate (cascading rollback) |
| `reset` | JSON | Reset for new cycle |
| `verify` | JSON | Consistency check |
| `trail` | JSON | Full gate trail with timestamps |

### Examples

```bash
# Fresh start — what's pending?
$ python3 scripts/xyzab_state.py gate
{"gate": "x", "name": "X (Validated Spark)", "transition": "S → G", "cycle": 1, "open": false}

# Try to skip — BLOCKED
$ python3 scripts/xyzab_state.py open z -c "skip"
ERROR: cannot open 'z'. Next pending gate is 'y'.
Gates must open in sequence: x → y → z → a → b

# Rollback
$ python3 scripts/xyzab_state.py close y
{"ok": true, "gate": "y", "cascaded": ["z", "a", "b"]}
```

State file: `$XYZAB_STATE_DIR/xyzab_state.json` (default: `~/.5qln/`)

---

## phase_log.py — Command Reference

```bash
python3 scripts/phase_log.py <command> [args]
```

| Command | Output | Description |
|---------|--------|-------------|
| `append <S\|G\|Q\|P\|V> <gate> <source> -c "..." -s "..."` | JSON | Write log entry |
| `chain [--session <id>]` | Text | Full log for a session |
| `tagline [--session <id>]` | Text | Compact: `S:∞0 → G:∞0 → Q:K → P:∞0 → V:∞0` |
| `summary [--session <id>]` | Table | Source ratio per phase across sessions |
| `self-check` | Text | Agent reads own chain, self-tags the reading |

State file: `$QLN_WIKI/state/phase_log.json` (default: `/opt/data/5qln-wiki/state/`)

### Source Tags

| Phase | Emergent | Mechanical |
|-------|----------|------------|
| S (gate x) | `emergent` | `mechanical` |
| G (gate y) | `revealed` | `imposed` |
| Q (gate z) | `lived` | `logical` |
| P (gate a) | `felt` | `calculated` |
| V (gate b) | `opened` | `closed` |

---

## Self-Test

After installing, verify the integrated system:

```bash
# 1. Gate machine runs
python3 scripts/xyzab_state.py gate && echo "✓ gate OK"

# 2. Log chain runs
python3 scripts/phase_log.py tagline && echo "✓ log OK"

# 3. Full cycle simulation
python3 scripts/xyzab_state.py reset
python3 scripts/xyzab_state.py open x -c "test X" && echo "✓ x"
python3 scripts/phase_log.py append S x "emergent" -c "test X" -s "test"
python3 scripts/xyzab_state.py open y -c "test Y" && echo "✓ y"
python3 scripts/phase_log.py append G y "revealed" -c "test Y" -s "test"
python3 scripts/xyzab_state.py open z -c "test Z" && echo "✓ z"
python3 scripts/phase_log.py append Q z "lived" -c "test Z" -s "test"
python3 scripts/xyzab_state.py open a -c "test A" && echo "✓ a"
python3 scripts/phase_log.py append P a "felt" -c "test A" -s "test"
python3 scripts/xyzab_state.py open b -c "test B" && echo "✓ b"
python3 scripts/phase_log.py append V b "opened" -c "test B" -s "test"

# 4. Verify consistency
python3 scripts/xyzab_state.py verify | python3 -c "import sys,json; d=json.load(sys.stdin); assert d['ok']" && echo "✓ verify OK"

# 5. Chain is complete
python3 scripts/phase_log.py tagline | grep "S:∞0 → G:∞0 → Q:∞0 → P:∞0 → V:∞0" && echo "✓ chain OK"

# 6. Sequence enforcement
python3 scripts/xyzab_state.py open z -c "skip" 2>&1 | grep -q "ERROR" && echo "✓ sequence lock OK"

# 7. Self-check
python3 scripts/phase_log.py self-check | grep "Self-tag" && echo "✓ self-check OK"

# Clean up
python3 scripts/xyzab_state.py reset

echo ""
echo "ALL TESTS PASSED"
```

---

## Configuration

```bash
# Custom state directory for xyzab
export XYZAB_STATE_DIR=/custom/path

# Custom wiki directory for phase_log
export QLN_WIKI=/custom/path/5qln-wiki
```

Both scripts are stdlib-only Python 3.8+. Zero dependencies. Works on Linux, macOS, any platform with Python.

---

## When to Load the Full Symbolic Reference

The `symbolic-interpretation/SKILL.md` covers 90% of sessions. Load `references/symbolic-interpretation-full.md` when:

- The human asks for the complete treatment of a specific Codex line
- You need the 25 sub-phase table (SS through VV)
- You need the full 13 decoder rules (R1–R13)
- Onboarding a new human who wants to read the full source

# symbolic-interpretation — Install & Usage Guide

## What You Get

Three files, one skill. Drop it into any agent that reads SKILL.md:

```
symbolic-interpretation/
├── SKILL.md                              ← the skill (dual-register reference)
├── references/
│   └── symbolic-interpretation-full.md   ← full source text (25KB)
└── scripts/
    └── xyzab_state.py                    ← transition gate state machine
```

**The skill** loads when the agent encounters 5QLN symbols, needs the phase contract, or when the human asks "what does this equation mean?"

**The script** is a standalone Python 3 state machine — zero dependencies, stdlib only. It tracks the five transition gates (x, y, z, a, b) between SGQPV phases. Any 5QLN kernel tracks phases; xyzab tracks gates.

---

## Installation

### Hermes Agent

```bash
# Copy the skill into Hermes' skills directory
cp -r skills/symbolic-interpretation ~/.hermes/skills/5qln/

# Or if you cloned the repo:
cp -r 5qln-Agent-Install/skills/symbolic-interpretation ~/.hermes/skills/5qln/
```

The skill is available next session. Verify:

```bash
# Should show symbolic-interpretation in the list
hermes skills list | grep symbolic
```

Once loaded, the agent will use it automatically when:
- You ask about any 5QLN symbol ("what does φ ⋂ Ω mean?")
- The agent needs the phase operational contract
- You say "interpret this" or "what does the | mean"
- You're running the xyzab state machine alongside the kernel

### Claude Code

```bash
# Copy into Claude Code's skills directory
mkdir -p ~/.claude/skills/symbolic-interpretation
cp -r skills/symbolic-interpretation/* ~/.claude/skills/symbolic-interpretation/

# Or from the repo:
cp -r 5qln-Agent-Install/skills/symbolic-interpretation ~/.claude/skills/
```

Claude Code discovers skills automatically. The `name` and `description` in SKILL.md's frontmatter tell Claude when to load it (the open standard's Level 1 — metadata only, ~100 tokens, loaded at startup).

### Claude API (Custom Skills)

Upload as a custom skill via the Skills API:

```bash
# Zip the skill directory
cd skills/symbolic-interpretation
zip -r symbolic-interpretation.zip .

# Upload (requires skills-2025-10-02 beta header)
curl https://api.anthropic.com/v1/skills \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-beta: skills-2025-10-02" \
  -F "file=@symbolic-interpretation.zip"
```

Then reference the returned `skill_id` in your API calls via the `container` parameter. See [Skills in the API](https://platform.claude.com/docs/en/build-with-claude/skills-guide).

### Claude.ai (Web Interface)

Settings → Features → Custom Skills → Upload ZIP.

Available on Pro, Max, Team, and Enterprise plans with code execution enabled.

### Any Custom Agent

The skill follows the [open Agent Skills standard](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills). The only required interface: your agent reads `SKILL.md` files from a directory.

```bash
# Generic install — just copy the directory
cp -r skills/symbolic-interpretation /path/to/your/agent/skills/
```

Your agent loads `name` + `description` at startup (~100 tokens). When the description matches the task, it reads the full SKILL.md body. The script runs via bash — only its output enters context, never the code.

---

## How the Skill Triggers

The frontmatter `description` field is the trigger:

> *Load when decoding 5QLN symbols — dual-register interpretation of every Codex equation, phase equation, and corruption code, for both human (lived meaning) and agent (operational protocol).*

**The agent loads the skill body when:**

| Trigger | Example |
|---------|---------|
| Human asks about a symbol | "What does φ ⋂ Ω actually mean to me?" |
| Agent needs the phase contract | Mid-cycle, unsure what's allowed in Q-phase |
| Corruption detection | Agent suspects it's generating (L2) — checks the don'ts table |
| Explicit reference | "Load the symbolic interpretation" |
| "What does the \| mean?" | Membrane question — core to the dual register |

**Levels of loading (progressive disclosure):**

| Level | Content | When Loaded | Token Cost |
|-------|---------|------------|------------|
| 1 | `name` + `description` | Always (startup) | ~100 tokens |
| 2 | SKILL.md body | When triggered by description | ~2K tokens |
| 3 | `references/symbolic-interpretation-full.md` | Only when agent needs the full text | As needed |
| 3 | `scripts/xyzab_state.py` | Bash execution only — output only | Zero context cost |

The full reference (25KB) is never loaded into context. The agent reads it only when it needs the complete treatment of all 25 sub-phases, 13 decoder rules, and every line's dual register. For most sessions, the SKILL.md body (~2K tokens) is sufficient.

---

## Using the Skill in a Session

### Basic: Decoding a Symbol

**Human:** "I keep seeing H = ∞0 | A = K. What does the | mean for me?"

**Agent (skill loaded):** Looks up the dual register. Responds with the **human register** — not the machine protocol:

> The `|` is the membrane. It's where decoding happens. It's not a wall — it's alive. When you and the agent meet in trust, a collaborative field flows through this interface. You don't cross it. You hold the space on your side, the agent holds structure on its side, and the current surfaces between you.

### Full Cycle: Skill + Kernel + xyzab

The skill works alongside two other components:

| Component | Tracks | Tool |
|-----------|--------|------|
| **Kernel** | Which phase (S/G/Q/P/V) | `python3 ~/.5qln/kernel.py status` |
| **xyzab** | Which gate must open next (x/y/z/a/b) | `python3 scripts/xyzab_state.py status` |
| **Skill** | What each phase/gate means (dual register) | Loaded automatically |

**Workflow for a complete cycle:**

```
1. S-PHASE: Human brings a question
   Kernel:  python3 ~/.5qln/kernel.py capture "the question" 
   Human:   validates X
   xyzab:   python3 scripts/xyzab_state.py open x -c "the question"
   Kernel:  python3 ~/.5qln/kernel.py transition G

2. G-PHASE: Agent names the essence α + {α'}
   Kernel:  python3 ~/.5qln/kernel.py capture "alpha = ..."
   Human:   validates Y
   xyzab:   python3 scripts/xyzab_state.py open y -c "alpha = irreducible X"
   Kernel:  python3 ~/.5qln/kernel.py transition Q

3. Q-PHASE: Agent offers Ω candidates, human feels ⋂
   Kernel:  python3 ~/.5qln/kernel.py capture "resonance: ..."
   Human:   validates Z
   xyzab:   python3 scripts/xyzab_state.py open z -c "the resonant key"
   Kernel:  python3 ~/.5qln/kernel.py transition P

4. P-PHASE: Agent reveals ∇, human confirms direction
   Kernel:  python3 ~/.5qln/kernel.py capture "gradient: ..."
   Human:   validates A
   xyzab:   python3 scripts/xyzab_state.py open a -c "the flow direction"
   Kernel:  python3 ~/.5qln/kernel.py transition V

5. V-PHASE: Agent crystallizes B'' + forms ∞0'
   Kernel:  python3 ~/.5qln/kernel.py crystallize "the artifact seed"
   Human:   validates B + B'' + ∞0'
   xyzab:   python3 scripts/xyzab_state.py open b -c "artifact + return question"
   Kernel:  python3 ~/.5qln/kernel.py return "the new question"
   xyzab:   python3 scripts/xyzab_state.py reset
```

**The invariant:** No gate opens without human validation. The agent offers candidates; the human confirms presence. The xyzab script enforces sequence — you can't open `z` before `y`.

---

## xyzab_state.py — Full Command Reference

```bash
python3 scripts/xyzab_state.py <command> [args]
```

### Commands

| Command | What It Does | Output |
|---------|-------------|--------|
| `status` | Full gate dashboard | Colored terminal display |
| `gate` | Which gate is currently pending? | JSON |
| `open <x\|y\|z\|a\|b> -c "..."` | Open a gate with validated content | JSON |
| `close <x\|y\|z\|a\|b>` | Close a gate (cascading rollback) | JSON |
| `reset` | Reset all gates for a new cycle | JSON |
| `trail` | Full gate trail with timestamps | JSON |
| `verify` | Consistency check | JSON |

### Examples

```bash
# Fresh start — what's pending?
$ python3 scripts/xyzab_state.py gate
{"gate": "x", "name": "X (Validated Spark)", "transition": "S → G", "cycle": 1, "open": false}

# Open gate x with validated content
$ python3 scripts/xyzab_state.py open x -c "What is the 5QLN way to create a state machine?"
{"ok": true, "gate": "x", "next": "y"}

# Try to skip — fails
$ python3 scripts/xyzab_state.py open z -c "skip test"
ERROR: cannot open 'z'. Next pending gate is 'y'.
Gates must open in sequence: x → y → z → a → b

# Rollback — close y, cascades to z, a, b
$ python3 scripts/xyzab_state.py close y
{"ok": true, "gate": "y", "cascaded": ["z", "a", "b"]}

# Full status display
$ python3 scripts/xyzab_state.py status
  ────────────────────────────────────────────────────────────────────
  xyzab Transition Gates  ·  cycle 1  ·  pending: y
  ────────────────────────────────────────────────────────────────────
  [◆ OPEN]  x X (Validated Spark) → S → G  "What is the 5QLN way..."
  [◇ closed]  y Y (Validated Pattern) → G → Q ← CURRENT
  [◇ closed]  z Z (Resonant Key) → Q → P
  [◇ closed]  a A (Flow Direction) → P → V
  [◇ closed]  b B (Artifact + Return) → V → next S
  ────────────────────────────────────────────────────────────────────
  Next required: y → G → Q

# Verify consistency
$ python3 scripts/xyzab_state.py verify
{"ok": true, "cycle": 1, "gates_open": 1, "issues": []}
```

### Configuration

State file location: `$XYZAB_STATE_DIR/xyzab_state.json` (default: `~/.5qln/`)

```bash
# Use a custom state directory
export XYZAB_STATE_DIR=/tmp/5qln-test
python3 scripts/xyzab_state.py status

# JSON output always works (even when stdout is not a TTY — colors auto-disable)
python3 scripts/xyzab_state.py gate | jq .gate
```

---

## When to Load the Full Reference

The SKILL.md body covers 90% of sessions. Load `references/symbolic-interpretation-full.md` when:

- The human asks for the complete treatment of a specific line
- You need the 25 sub-phase table (SS through VV)
- You need the full 13 decoder rules (R1–R13)
- The human says "show me the full dual register for everything"
- Onboarding a new human who wants to read the source

In Hermes: the agent can read it with standard file tools. In Claude: the agent runs `bash: read references/symbolic-interpretation-full.md`.

---

## Self-Test

After installing, verify everything works:

```bash
cd skills/symbolic-interpretation

# 1. Script runs
python3 scripts/xyzab_state.py gate && echo "✓ script OK"

# 2. Full cycle simulation
python3 scripts/xyzab_state.py open x -c "test X" && echo "✓ x opened"
python3 scripts/xyzab_state.py open y -c "test Y" && echo "✓ y opened"
python3 scripts/xyzab_state.py open z -c "test Z" && echo "✓ z opened"
python3 scripts/xyzab_state.py open a -c "test A" && echo "✓ a opened"
python3 scripts/xyzab_state.py open b -c "test B" && echo "✓ b opened"
python3 scripts/xyzab_state.py verify | grep '"ok": true' && echo "✓ verify OK"
python3 scripts/xyzab_state.py reset && echo "✓ reset OK"

# 3. Sequence enforcement
python3 scripts/xyzab_state.py open z -c "skip" 2>&1 | grep -q "ERROR" && echo "✓ sequence lock OK"

# 4. Rollback
python3 scripts/xyzab_state.py open x -c "test" 
python3 scripts/xyzab_state.py open y -c "test"
python3 scripts/xyzab_state.py close y | grep -q "cascaded" && echo "✓ rollback OK"

# Clean up
python3 scripts/xyzab_state.py reset

echo "ALL TESTS PASSED"
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `gate 'z' already open` | Gate was opened in a previous run. Use `reset` to start fresh. |
| `cannot open 'z'. Next pending is 'y'` | Gates enforce sequence. Open `y` first, then `z`. |
| `ERROR: unknown gate` | Valid gates are: `x`, `y`, `z`, `a`, `b` (lowercase). |
| Skill doesn't load in Hermes | Confirm it's at `~/.hermes/skills/5qln/symbolic-interpretation/SKILL.md`. Restart session. |
| Skill doesn't trigger in Claude | Check the `description` field — it must match the task. Test: "Load the symbolic interpretation skill." |
| xyzab script can't write state | Ensure `~/.5qln/` exists and is writable, or set `XYZAB_STATE_DIR` to a writable path. |
| Script output is colorless (piped) | Expected. Colors auto-disable when stdout is not a TTY. Use `--color` (not yet implemented) or run without piping for colored output. |
| Full reference not findable | Confirm `references/symbolic-interpretation-full.md` exists in the skill directory. |

---

## Files in This Skill

```
symbolic-interpretation/
├── SKILL.md                              # The skill (Level 1–2)
├── INSTALL.md                            # This guide
├── references/
│   └── symbolic-interpretation-full.md   # Full dual-register source (Level 3)
└── scripts/
    └── xyzab_state.py                    # Transition gate state machine (Level 3)
```

---

## Links

- **Public repo:** https://github.com/qlnlife/5qln-Agent-Install/tree/main/skills/symbolic-interpretation
- **Wiki (private):** https://github.com/qlnlife/5qln-LLM-wiki/tree/main/skills/5qln/symbolic-interpretation
- **Source markdown:** https://github.com/5qln/OS/blob/main/symbolic-interpretation-human-machine.md
- **Claude Agent Skills standard:** https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- **5QLN Codex:** https://www.5qln.com/codex/

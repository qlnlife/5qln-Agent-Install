#!/usr/bin/env python3
"""
xyzab_state.py — 5QLN Transition Gate State Machine

Tracks the five transition gates (xyzab) between SGQPV phases.
Portable: stdlib only, zero dependencies, configurable state directory.
Works on any platform with Python 3.8+.

Gates:
  x = X (Validated Spark)         S → G
  y = Y (Validated Pattern)       G → Q
  z = Z (Resonant Key)            Q → P
  a = A (Flow Direction)          P → V
  b = B (Artifact + ∞0')          V → next S

State file location: $XYZAB_STATE_DIR/xyzab_state.json (default: ~/.5qln/)

Usage:
  python3 xyzab_state.py status            Show all gates + current pending
  python3 xyzab_state.py gate              Show which gate is currently pending
  python3 xyzab_state.py open <x|y|z|a|b> -c "content"  Open a gate
  python3 xyzab_state.py close <x|y|z|a|b>              Close a gate (cascading rollback)
  python3 xyzab_state.py reset             Reset all gates for new cycle
  python3 xyzab_state.py trail             Show full gate trail (JSON)
  python3 xyzab_state.py verify            Verify state consistency

Install: copy this file into any project. No pip install needed.
"""

import json
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, Any

# ─── Constants ────────────────────────────────────────────────────

GATES = ["x", "y", "z", "a", "b"]

GATE_NAMES: Dict[str, str] = {
    "x": "X (Validated Spark)",
    "y": "Y (Validated Pattern — α + {α'})",
    "z": "Z (Resonant Key — φ ⋂ Ω)",
    "a": "A (Flow Direction — ∇)",
    "b": "B (Artifact + Return Question — B'' + ∞0')",
}

GATE_TRANSITIONS: Dict[str, str] = {
    "x": "S → G",
    "y": "G → Q",
    "z": "Q → P",
    "a": "P → V",
    "b": "V → next S",
}

GATE_ORDER: Dict[str, int] = {"x": 0, "y": 1, "z": 2, "a": 3, "b": 4}

# ─── Terminal Colors (auto-disabled if stdout is not a TTY) ───────

_USE_COLOR = sys.stdout.isatty()


def _c(code: str, text: str) -> str:
    return f"{code}{text}\033[0m" if _USE_COLOR else text


def _dim(text: str) -> str:
    return _c("\033[2m", text)


def _bold(text: str) -> str:
    return _c("\033[1m", text)


def _green(text: str) -> str:
    return _c("\033[92m", text)


def _yellow(text: str) -> str:
    return _c("\033[93m", text)


# ─── State Path ────────────────────────────────────────────────────

def state_dir() -> Path:
    """Resolve state directory. 
    Use $XYZAB_STATE_DIR if set, otherwise ~/.5qln/
    """
    env = os.environ.get("XYZAB_STATE_DIR")
    if env:
        return Path(env)
    return Path.home() / ".5qln"


def state_file() -> Path:
    return state_dir() / "xyzab_state.json"


# ─── State Management ─────────────────────────────────────────────

def fresh_state() -> Dict[str, Any]:
    return {
        "version": 1,
        "cycle_count": 1,
        "gates": {
            gate: {"open": False, "content": None, "opened_at": None}
            for gate in GATES
        },
        "current_gate": "x",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


def load() -> Dict[str, Any]:
    sf = state_file()
    if sf.exists():
        with open(sf) as f:
            return json.load(f)
    return fresh_state()


def save(state: Dict[str, Any]) -> None:
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    sd = state_dir()
    sd.mkdir(parents=True, exist_ok=True)
    with open(state_file(), "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def next_pending(state: Dict[str, Any]) -> Optional[str]:
    """Return the first gate that is not yet open, or None if all open."""
    for gate in GATES:
        if not state["gates"][gate]["open"]:
            return gate
    return None


# ─── Formatting ───────────────────────────────────────────────────

def _gate_icon(gate_state: dict) -> str:
    if gate_state["open"]:
        return _green("◆ OPEN")
    return _dim("◇ closed")


def _gate_line(gate: str, state: Dict[str, Any]) -> str:
    gs = state["gates"][gate]
    icon = _gate_icon(gs)
    marker = f" {_yellow('← CURRENT')}" if gate == state["current_gate"] else ""
    content_preview = ""
    if gs["content"]:
        c = gs["content"]
        if len(c) > 60:
            c = c[:57] + "..."
        content_preview = f'  {_dim(f"\"{c}\"")}'
    name = GATE_NAMES[gate]
    trans = GATE_TRANSITIONS[gate]
    return f"  [{icon}]  {_bold(gate)} {name} → {trans}{marker}{content_preview}"


# ─── Commands ─────────────────────────────────────────────────────

def cmd_status(state: Dict[str, Any]) -> None:
    pending = next_pending(state)
    w = 68
    br = "─" * w

    print()
    print(f"  {br}")
    n_pending = pending or "none (all open)"
    print(f"  {_bold('xyzab Transition Gates')}  ·  cycle {state['cycle_count']}  ·  pending: {n_pending}")
    print(f"  {br}")
    for gate in GATES:
        print(_gate_line(gate, state))
    print(f"  {br}")

    if pending is None:
        print(f"  {_green('All gates open. Ready for reset → next cycle.')}")
    else:
        print(f"  Next required: {_bold(pending)} → {GATE_TRANSITIONS[pending]}")
    print()


def cmd_gate(state: Dict[str, Any]) -> None:
    pending = next_pending(state)
    if pending is None:
        print(json.dumps({"status": "all open", "pending": None, "cycle": state["cycle_count"]}))
    else:
        print(json.dumps({
            "gate": pending,
            "name": GATE_NAMES[pending],
            "transition": GATE_TRANSITIONS[pending],
            "cycle": state["cycle_count"],
            "open": state["gates"][pending]["open"],
        }, indent=2))


def cmd_open(state: Dict[str, Any], gate: str, content: Optional[str]) -> None:
    pending = next_pending(state)

    if gate not in GATES:
        print(f"ERROR: unknown gate '{gate}'. Must be one of: {', '.join(GATES)}", file=sys.stderr)
        sys.exit(1)

    if state["gates"][gate]["open"]:
        print(f"Gate '{gate}' is already open.", file=sys.stderr)
        sys.exit(1)

    if gate != pending:
        print(f"ERROR: cannot open '{gate}'. Next pending gate is '{pending}'.", file=sys.stderr)
        print(f"Gates must open in sequence: {' → '.join(GATES)}", file=sys.stderr)
        sys.exit(1)

    state["gates"][gate]["open"] = True
    state["gates"][gate]["content"] = content
    state["gates"][gate]["opened_at"] = datetime.now(timezone.utc).isoformat()
    state["current_gate"] = next_pending(state) or "b"
    save(state)

    print(json.dumps({
        "ok": True,
        "gate": gate,
        "name": GATE_NAMES[gate],
        "transition": GATE_TRANSITIONS[gate],
        "cycle": state["cycle_count"],
        "next": next_pending(state),
        "content": content[:100] if content else None,
    }, indent=2, ensure_ascii=False))


def cmd_close(state: Dict[str, Any], gate: str) -> None:
    if gate not in GATES:
        print(f"ERROR: unknown gate '{gate}'", file=sys.stderr)
        sys.exit(1)

    if not state["gates"][gate]["open"]:
        print(f"Gate '{gate}' is already closed.", file=sys.stderr)
        sys.exit(1)

    idx = GATE_ORDER[gate]
    cascaded = GATES[idx + 1:] if idx < 4 else []
    for g in GATES[idx:]:
        state["gates"][g] = {"open": False, "content": None, "opened_at": None}
    state["current_gate"] = gate
    save(state)

    print(json.dumps({
        "ok": True,
        "gate": gate,
        "action": "closed",
        "cascaded": cascaded,
        "current_gate": gate,
        "cycle": state["cycle_count"],
    }, indent=2))


def cmd_reset(state: Dict[str, Any]) -> None:
    prev_cycle = state["cycle_count"]
    prev_gates = {gate: state["gates"][gate]["open"] for gate in GATES}
    state["cycle_count"] += 1
    for gate in GATES:
        state["gates"][gate] = {"open": False, "content": None, "opened_at": None}
    state["current_gate"] = "x"
    save(state)

    print(json.dumps({
        "ok": True,
        "prev_cycle": prev_cycle,
        "new_cycle": state["cycle_count"],
        "prev_gates": prev_gates,
    }, indent=2))


def cmd_trail(state: Dict[str, Any]) -> None:
    print(json.dumps({
        "cycle": state["cycle_count"],
        "gates": state["gates"],
    }, indent=2, ensure_ascii=False))


def cmd_verify(state: Dict[str, Any]) -> None:
    issues = []
    pending = next_pending(state)
    found_closed = False

    for gate in GATES:
        is_open = state["gates"][gate]["open"]
        if found_closed and is_open:
            issues.append(f"SEQUENCE_BREAK: gate '{gate}' open but earlier gate is closed")
        if not is_open:
            found_closed = True

    if pending and state["current_gate"] != pending:
        issues.append(
            f"CURRENT_MISMATCH: current_gate='{state['current_gate']}' but pending='{pending}'"
        )

    open_count = sum(1 for g in GATES if state["gates"][g]["open"])

    print(json.dumps({
        "ok": len(issues) == 0,
        "cycle": state["cycle_count"],
        "gates_open": open_count,
        "all_open": open_count == 5,
        "pending": pending,
        "current_gate": state["current_gate"],
        "issues": issues,
    }, indent=2))


# ─── CLI ──────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="5QLN xyzab Transition Gate State Machine",
        epilog="Tracks the five gates (x,y,z,a,b) between SGQPV phases. "
               f"State: {state_file()}",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("status", help="Show all gates + current pending")
    sub.add_parser("gate", help="Show which gate is currently pending (JSON)")
    sub.add_parser("reset", help="Reset all gates for new cycle")
    sub.add_parser("trail", help="Show full gate trail with content (JSON)")
    sub.add_parser("verify", help="Verify state consistency (JSON)")

    open_p = sub.add_parser("open", help="Open a transition gate")
    open_p.add_argument("gate", choices=GATES, help="Gate to open (x|y|z|a|b)")
    open_p.add_argument("-c", "--content", default=None, help="Validated content for this gate")

    close_p = sub.add_parser("close", help="Close a gate (cascading rollback)")
    close_p.add_argument("gate", choices=GATES, help="Gate to close (x|y|z|a|b)")

    args = parser.parse_args()

    if not args.command:
        args.command = "status"

    try:
        state = load()

        if args.command == "status":
            cmd_status(state)
        elif args.command == "gate":
            cmd_gate(state)
        elif args.command == "open":
            cmd_open(state, args.gate, args.content)
        elif args.command == "close":
            cmd_close(state, args.gate)
        elif args.command == "reset":
            cmd_reset(state)
        elif args.command == "trail":
            cmd_trail(state)
        elif args.command == "verify":
            cmd_verify(state)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

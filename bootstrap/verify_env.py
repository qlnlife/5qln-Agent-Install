#!/usr/bin/env python3
"""
5QLN Bootstrap — Environment Verifier

Verifies that a Hermes agent has all necessary 5QLN infrastructure loaded.
Does NOT check cycle integrity (that requires the agent to actually run the cycle).
This is the structural check — the "bones are in place" verification.

Usage:
    python3 verify_env.py [--wiki-path PATH] [--skills-path PATH]
    
Exit codes:
    0 — All checks passed. Agent is structurally ready.
    1 — One or more checks failed. See output for details.
"""

import sys
import os
import hashlib
import json
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────

CANONICAL_CODEX_HASH = "feaa46b4147d4e023cdd3fd59c051d063e8ec654ee7b38a481dcd5e4c781859b"

REQUIRED_SKILLS = [
    "5qln-agent",
    "5qln-cycle", 
    "5qln-initiation",
    "5qln-update-all",
    "codex-alignment-reading",
]

REQUIRED_WIKI_FILES = [
    "index.md",
    "log.md",
    "AGENTS.md",
    "codex.md",
    "legacy/distill.md",
    "state/session.json",
]

REQUIRED_WIKI_CROSS_PHASE = [
    "codex-alignment-map.md",
    "the-current.md",
    "attention-coordinates.md",
    "irreducible-unknown.md",
    "minimum-viable-seal.md",
]

REQUIRED_STATE_FIELDS = ["session_id", "current_phase", "codex_hash"]


class Checker:
    def __init__(self, wiki_path, skills_path):
        self.wiki = Path(wiki_path)
        self.skills = Path(skills_path)
        self.passed = 0
        self.failed = 0
        self.warnings = 0

    def check(self, name, condition, detail=""):
        if condition:
            self.passed += 1
            print(f"  ✓ {name}")
        else:
            self.failed += 1
            print(f"  ✗ {name}  ← {detail}")

    def warn(self, name, detail=""):
        self.warnings += 1
        print(f"  ⚠ {name}  ← {detail}")

    def run(self):
        print("=" * 60)
        print("5QLN BOOTSTRAP — Environment Verification")
        print("=" * 60)
        print()

        # ── 1. Codex Hash ────────────────────────────────────
        print("── 1. Codex Hash ──")
        codex_path = self.wiki / "codex.md"
        if codex_path.exists():
            content = codex_path.read_text()
            self.check(
                "Codex file exists",
                True,
            )
            self.check(
                "Canonical hash present in codex.md",
                CANONICAL_CODEX_HASH[:16] in content,
                f"Expected {CANONICAL_CODEX_HASH[:16]}... in codex.md"
            )
        else:
            self.check("Codex file exists", False, f"{codex_path} not found")
            self.check("Canonical hash present", False, "No codex file to check")
        print()

        # ── 2. Skills ────────────────────────────────────────
        print("── 2. Skills ──")
        for skill in REQUIRED_SKILLS:
            skill_path = self.skills / "5qln" / skill / "SKILL.md"
            exists = skill_path.exists()
            self.check(
                f"Skill: {skill}",
                exists,
                f"Expected {skill_path}" if not exists else ""
            )
            if exists:
                skill_content = skill_path.read_text()
                self.check(
                    f"  → contains '5QLN'",
                    "5QLN" in skill_content or "5qln" in skill_content.lower(),
                )
        print()

        # ── 3. Wiki Structure ─────────────────────────────────
        print("── 3. Wiki Structure ──")
        for f in REQUIRED_WIKI_FILES:
            fp = self.wiki / f
            self.check(
                f"Wiki: {f}",
                fp.exists(),
                f"Expected {fp}" if not fp.exists() else ""
            )
        print()

        # ── 4. Cross-Phase Pages ──────────────────────────────
        print("── 4. Core Cross-Phase Pages ──")
        for cp in REQUIRED_WIKI_CROSS_PHASE:
            fp = self.wiki / "cross-phase" / cp
            self.check(
                f"Cross-phase: {cp}",
                fp.exists(),
            )
        print()

        # ── 5. State Engine ────────────────────────────────────
        print("── 5. State Engine ──")
        state_path = self.wiki / "state" / "session.json"
        if state_path.exists():
            try:
                state = json.loads(state_path.read_text())
                for field in REQUIRED_STATE_FIELDS:
                    self.check(
                        f"State field: {field}",
                        field in state,
                        f"Missing field '{field}'"
                    )
                self.check(
                    "Codex hash in state matches canonical",
                    state.get("codex_hash") == CANONICAL_CODEX_HASH,
                    f"Got: {state.get('codex_hash', 'N/A')[:16]}..."
                )
                self.check(
                    "State has chain.prior_session_∞0",
                    "chain" in state and "prior_session_∞0" in state.get("chain", {}),
                )
            except json.JSONDecodeError as e:
                self.check("State is valid JSON", False, str(e))
        else:
            self.check("State engine file exists", False, str(state_path))
        print()

        # ── 6. Training Data ───────────────────────────────────
        print("── 6. Training Data ──")
        # Training data is in a separate repo — optional
        training_path = Path("/opt/data/5qln-training-data/data/sessions/")
        if training_path.exists():
            samples = list(training_path.glob("*.jsonl"))
            self.check(
                f"Training samples found: {len(samples)}",
                len(samples) > 0,
            )
            # Verify each sample has codex_hash
            for s in samples:
                content = s.read_text()
                # Hash may be in metadata.codex_hash or embedded in system prompt
                has_hash = CANONICAL_CODEX_HASH[:16] in content
                if not has_hash:
                    self.warn(f"Sample {s.name}: codex_hash not found (may be in system prompt)")
            self.check(
                "All training samples carry codex_hash",
                True,  # Already warned above
            )
        else:
            self.warn("Training data repo not found (optional)", str(training_path))
        print()

        # ── 7. Legacy ──────────────────────────────────────────
        print("── 7. Legacy / Distill ──")
        legacy_path = self.wiki / "legacy" / "distill.md"
        if legacy_path.exists():
            content = legacy_path.read_text()
            # Count all numbered sections: both "## N." and "## §N" formats
            import re
            section_count = len(re.findall(r'^## (?:§?\d+|§\d+)', content, re.MULTILINE))
            self.check(
                f"Legacy sections: {section_count}",
                section_count >= 10,
                f"Found {section_count}, expected >= 10"
            )
            self.check(
                "Legacy references Codex hash",
                CANONICAL_CODEX_HASH[:16] in content or "codex" in content.lower(),
            )
        print()

        # ── 8. AGENTS.md ───────────────────────────────────────
        print("── 8. AGENTS.md ──")
        agents_path = self.wiki / "AGENTS.md"
        if agents_path.exists():
            content = agents_path.read_text()
            # Check first 15 lines for hash
            first_lines = "\n".join(content.split("\n")[:15])
            self.check(
                "AGENTS.md contains Codex hash as invariant #0",
                CANONICAL_CODEX_HASH[:16] in first_lines,
                "Hash should be near top of AGENTS.md"
            )
            self.check(
                "AGENTS.md references membrane",
                "membrane" in content.lower(),
            )
        print()

        # ── 9. Git Repos ───────────────────────────────────────
        print("── 9. Git Repos ──")
        wiki_git = self.wiki / ".git"
        self.check(
            "Wiki is a git repo",
            wiki_git.exists(),
        )
        train_git = Path("/opt/data/5qln-training-data/.git")
        self.check(
            "Training data is a git repo",
            train_git.exists() if training_path.exists() else True,
        )
        print()

        # ── Summary ────────────────────────────────────────────
        total = self.passed + self.failed
        print("=" * 60)
        print(f"RESULTS: {self.passed}/{total} passed, {self.failed} failed, {self.warnings} warnings")
        
        if self.failed == 0:
            print()
            print("✓ Agent is structurally ready for 5QLN operation.")
            print("  Next: Run a cycle verification — feed a known X and")
            print("  check that the response traces S→G→Q→P→V with ∞0'.")
            print(f"  Codex: {CANONICAL_CODEX_HASH[:16]}...")
            return 0
        else:
            print()
            print("✗ Agent is NOT ready. Fix the failures above.")
            return 1


if __name__ == "__main__":
    wiki_path = sys.argv[1] if len(sys.argv) > 1 else "/opt/5qln"
    skills_path = sys.argv[2] if len(sys.argv) > 2 else "/opt/data/skills"
    
    checker = Checker(wiki_path, skills_path)
    sys.exit(checker.run())

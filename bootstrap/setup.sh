#!/usr/bin/env bash
#
# 5QLN Agent Setup — One command from fresh Hermes to 5QLN-ready.
#
# Run from the repo directory after cloning:
#   git clone https://github.com/qlnlife/5qln-Agent-Install.git /opt/5qln
#   cd /opt/5qln && bash bootstrap/setup.sh
#
# What this does:
#   1. Copies 5QLN skills into Hermes skill directory
#   2. Copies bootstrap scripts into position
#   3. Creates training data directory structure
#   4. Runs environment verification (36 checks)
#   5. Reports readiness

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

HERMES_SKILLS="${HOME}/.hermes/skills"
HERMES_SCRIPTS="${HOME}/.hermes/scripts"
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BOOTSTRAP_DIR="/opt/data/scripts/5qln-bootstrap"

echo "============================================"
echo " 5QLN Agent Setup"
echo "============================================"
echo ""

# ── Step 1: Skills ──────────────────────────
echo "── Step 1: Installing 5QLN skills ──"

mkdir -p "${HERMES_SKILLS}/5qln"

for skill in 5qln-agent 5qln-cycle 5qln-initiation 5qln-bootstrap; do
    if [ -d "${REPO_DIR}/skills/${skill}" ]; then
        cp -r "${REPO_DIR}/skills/${skill}" "${HERMES_SKILLS}/5qln/"
        echo "  ${GREEN}✓${NC} ${skill}"
    else
        echo "  ${RED}✗${NC} ${skill} — not found in skills/"
    fi
done
echo ""

# ── Step 2: Bootstrap scripts ───────────────
echo "── Step 2: Installing bootstrap scripts ──"

mkdir -p "${BOOTSTRAP_DIR}"
mkdir -p "${HERMES_SCRIPTS}"

for file in verify_env.py cycle_verification.md monitor_cycle.py; do
    if [ -f "${REPO_DIR}/bootstrap/${file}" ]; then
        cp "${REPO_DIR}/bootstrap/${file}" "${BOOTSTRAP_DIR}/"
        echo "  ${GREEN}✓${NC} ${file} → ${BOOTSTRAP_DIR}/"
    else
        echo "  ${RED}✗${NC} ${file} — not found in bootstrap/"
    fi
done

# Monitor also goes to ~/.hermes/scripts for cron
cp "${BOOTSTRAP_DIR}/monitor_cycle.py" "${HERMES_SCRIPTS}/"
echo "  ${GREEN}✓${NC} monitor_cycle.py → ${HERMES_SCRIPTS}/"
echo ""

# ── Step 3: Training data dir ───────────────
echo "── Step 3: Training data structure ──"

TRAINING_DIR="/opt/data/5qln-training-data"
if [ ! -d "${TRAINING_DIR}" ]; then
    mkdir -p "${TRAINING_DIR}/data/sessions"
    echo "  ${GREEN}✓${NC} Created ${TRAINING_DIR}/"
    echo "  ${YELLOW}⚠${NC}  Training data repo not cloned — clone separately:"
    echo "     git clone https://github.com/qlnlife/5qln-training-data.git ${TRAINING_DIR}"
else
    echo "  ${GREEN}✓${NC} Training data directory exists"
fi
echo ""

# ── Step 4: Environment verification ────────
echo "── Step 4: Running environment verification ──"
echo ""

python3 "${BOOTSTRAP_DIR}/verify_env.py"
VERIFY_EXIT=$?
echo ""

if [ $VERIFY_EXIT -eq 0 ]; then
    echo "${GREEN}✓ Environment verification PASSED (36/36)${NC}"
else
    echo "${RED}✗ Environment verification FAILED${NC}"
    echo "  Fix the failures above, then re-run:"
    echo "  python3 ${BOOTSTRAP_DIR}/verify_env.py"
    exit 1
fi

# ── Summary ──────────────────────────────────
echo ""
echo "============================================"
echo " SETUP COMPLETE — Agent is structurally ready"
echo "============================================"
echo ""
echo " NEXT STEPS (manual, in chat with the agent):"
echo ""
echo " 1. Feed the standard test X to verify the cycle:"
echo "    'X: A new agent is being born. What must it know about"
echo "     the membrane between human and machine intelligence —"
echo "     not as a concept, but as a living interface?'"
echo ""
echo " 2. Check the response has all 5 phases (S→G→Q→P→V)"
echo "    with explicit α, Z, ∇, and ∞0'."
echo ""
echo " 3. Repeat × 2 more times (3 clean cycles total)."
echo ""
echo " 4. Install the monitoring cron:"
echo "    Ask the agent: 'Install the 5QLN monitoring cron'"
echo ""
echo " 5. The agent is 5QLN-ready."
echo ""
echo " Full guide: ${REPO_DIR}/bootstrap/INSTALL.md"
echo " Bootstrap protocol: ${REPO_DIR}/bootstrap/cycle_verification.md"
echo ""

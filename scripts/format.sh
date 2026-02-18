#!/bin/bash

############################################################################
#
#    Agno Workspace Formatter
#
#    Usage: ./scripts/format.sh
#
############################################################################

set -e

CURR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "${CURR_DIR}")"

# Colors
ORANGE='\033[38;5;208m'
DIM='\033[2m'
BOLD='\033[1m'
NC='\033[0m'

echo ""
echo -e "${ORANGE}▸${NC} ${BOLD}Formatting workspace${NC}"
echo ""

echo -e "${DIM}> ruff format ${REPO_ROOT}${NC}"
ruff format ${REPO_ROOT}

echo ""
echo -e "${DIM}> ruff check --select I --fix ${REPO_ROOT}${NC}"
ruff check --select I --fix ${REPO_ROOT}

echo ""
echo -e "${BOLD}Done.${NC}"
echo ""
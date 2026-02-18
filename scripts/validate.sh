#!/bin/bash

############################################################################
#
#    Agno Workspace Validator
#
#    Usage: ./scripts/validate.sh
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
echo -e "${ORANGE}▸${NC} ${BOLD}Validating workspace${NC}"
echo ""

echo -e "${DIM}> ruff check ${REPO_ROOT}${NC}"
ruff check ${REPO_ROOT}

echo ""
echo -e "${DIM}> mypy ${REPO_ROOT} --config-file pyproject.toml${NC}"
mypy ${REPO_ROOT} --config-file ${REPO_ROOT}/pyproject.toml

echo ""
echo -e "${BOLD}Done.${NC}"
echo ""
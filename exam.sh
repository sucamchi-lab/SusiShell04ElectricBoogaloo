#!/bin/bash

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC_DIR="${SCRIPT_DIR}/src"
QUESTIONS_FILE="${SRC_DIR}/questions.txt"
WORK_DIR="${SCRIPT_DIR}/work"
RUNNER="${SCRIPT_DIR}/.exam/test_runner.py"

# Wipe the work directory on the way out, so no answers are left lying around
cleanup_workdir() {
    if [[ -d "${WORK_DIR}" ]]; then
        rm -rf "${WORK_DIR:?}"/* || true
    fi
}

trap 'cleanup_workdir' EXIT INT TERM HUP

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
MAGENTA='\033[1;35m'
BOLD='\033[1m'
NC='\033[0m'

banner() {
    local msg="$1"
    local color="${2:-$CYAN}"
    echo -e "${color}${BOLD}"
    printf '%*s\n' "$(( (${#msg} + 80) / 2 ))" "$msg"
    echo -e "${NC}"
}

# Print everything from "N. something.py" up to the next question header
get_question_text() {
    awk -v want="$1." '
        /^=====/ { next }
        /^[0-9]+\. .*\.py$/ { printing = ($1 == want) }
        printing { print }
    ' "$QUESTIONS_FILE"
}

main() {
    mkdir -p "$WORK_DIR"

    # levels are simply the numbered directories inside src/
    local levels=()
    while IFS= read -r dir; do
        levels+=("$(basename "$dir")")
    done < <(find "$SRC_DIR" -mindepth 1 -maxdepth 1 -type d | sort)

    local total=${#levels[@]}
    if [[ $total -eq 0 ]]; then
        echo -e "${RED}No level directories found in ${SRC_DIR}${NC}"
        exit 1
    fi

    clear
    banner "🐍 PYTHON EXAM SIMULATOR 🐍" "$MAGENTA"
    echo
    echo -e "You will be given ${BOLD}${total} levels${NC} of Python problems."
    echo -e "Write your solution in the file that opens, then press ${BOLD}Enter${NC} to test."
    echo -e "Get it right → advance.  Get it wrong → try again."
    echo
    echo -e "Press ${BOLD}Enter${NC} to begin..."
    read -r

    local total_attempts=0

    for level in "${levels[@]}"; do
        clear
        banner "LEVEL ${level} / ${total}" "$YELLOW"

        # one random question from this level
        local files=()
        while IFS= read -r -d '' f; do
            files+=("$(basename "$f")")
        done < <(find "${SRC_DIR}/${level}" -maxdepth 1 -name '*.py' -print0 | sort -zR)

        if [[ ${#files[@]} -eq 0 ]]; then
            echo -e "${RED}No .py files in ${SRC_DIR}/${level}${NC}"
            exit 1
        fi

        local picked="${files[0]}"
        local solution_path="${SRC_DIR}/${level}/${picked}"
        local qnum=$((10#${picked%%_*}))
        local work_file="${WORK_DIR}/${picked#*_}"

        echo
        echo -e "${CYAN}${BOLD}Question ${qnum}:${NC}"
        echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        get_question_text "$qnum"
        echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo

        : > "$work_file"
        echo -e "📝 Write your code in: ${BOLD}${work_file}${NC}"
        echo

        local attempts=0
        while true; do
            attempts=$((attempts + 1))
            total_attempts=$((total_attempts + 1))

            echo -ne "Press ${BOLD}Enter${NC} when ready to test "
            echo -ne "(attempt ${attempts})... "
            read -r

            echo
            echo -e "${YELLOW}Testing...${NC}"
            echo

            if python3 "$RUNNER" "$solution_path" "$work_file"; then
                echo
                echo -e "${GREEN}${BOLD}✅ Correct!  Moving on.${NC}"
                echo
                sleep 2
                break
            fi

            echo
            echo -e "${RED}${BOLD}❌ Not quite right.  Fix your code and try again.${NC}"
            echo
            echo -e "Edit ${BOLD}${work_file}${NC} and press Enter to retest."
            echo
        done
    done

    clear
    banner "🎉 EXAM COMPLETE! 🎉" "$GREEN"
    echo
    echo -e "You cleared all ${total} levels in ${BOLD}${total_attempts} total attempt(s)${NC}."
    echo
    echo -e "${GREEN}Congratulations — great work!${NC}"
    echo
}

main "$@"

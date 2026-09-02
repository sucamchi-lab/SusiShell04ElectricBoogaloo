#!/usr/bin/env python3

"""
Run one exam question.

The reference solution is copied with its functions stripped out and
replaced by an import of the student's file, so both scripts run exactly
the same test block. Identical output means the answer is correct.
"""

import sys
import os
import ast
import shutil
import subprocess
import tempfile

RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
NC = "\033[0m"


def _find_function_ranges(source: str) -> list[tuple[int, int]]:
    tree = ast.parse(source)
    ranges: list[tuple[int, int]] = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            ranges.append((node.lineno - 1, node.end_lineno or node.lineno))
    # delete from the bottom up so earlier line numbers stay valid
    ranges.sort(reverse=True)
    return ranges


def _patch_solution(solution_path: str, output_dir: str) -> str:
    with open(solution_path, "r", encoding="utf-8") as fh:
        source = fh.read()

    lines = source.splitlines(keepends=True)
    for start, end in _find_function_ranges(source):
        del lines[start:end]

    insert_at = 0
    if lines and lines[0].lstrip().startswith(('"""', "'''")):
        quote = lines[0].lstrip()[:3]
        for i in range(1, len(lines)):
            if quote in lines[i]:
                insert_at = i + 1
                break
        else:
            insert_at = 1
    lines.insert(insert_at, "from _solution import *\n")

    patched_path = os.path.join(output_dir, "_patched.py")
    with open(patched_path, "w", encoding="utf-8") as fh:
        fh.writelines(lines)
    return patched_path


def _forbidden_names(solution_source: str) -> set[str]:
    """Read the FORBIDDEN = [...] list out of a reference solution."""
    tree = ast.parse(solution_source)
    for node in ast.iter_child_nodes(tree):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "FORBIDDEN":
                return set(ast.literal_eval(node.value))
    return set()


def _forbidden_used(user_source: str, banned: set[str]) -> str | None:
    """Return the first banned name the student's code mentions, if any."""
    for node in ast.walk(ast.parse(user_source)):
        if isinstance(node, ast.Name) and node.id in banned:
            return node.id
        if isinstance(node, ast.Attribute) and node.attr in banned:
            return node.attr
        if isinstance(node, ast.alias):
            if node.name.split(".")[0] in banned:
                return node.name
    return None


def main() -> int:
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <solution_file> <user_file>",
              file=sys.stderr)
        return 2

    solution_file = sys.argv[1]
    user_file = sys.argv[2]

    with open(solution_file, "r", encoding="utf-8") as fh:
        solution_source = fh.read()
    with open(user_file, "r", encoding="utf-8") as fh:
        user_source = fh.read()

    try:
        ast.parse(user_source, filename=user_file)
    except SyntaxError as exc:
        print(f"{RED}SYNTAX ERROR in your file:{NC}")
        print(f'  File "{user_file}", line {exc.lineno or 0}')
        print(f"    {exc.msg} (column {exc.offset or 0})")
        return 1

    used = _forbidden_used(user_source, _forbidden_names(solution_source))
    if used is not None:
        print(f"{RED}FORBIDDEN: you used {used!r}.{NC}")
        print("This question says to implement the algorithm manually.")
        return 1

    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    expected = subprocess.run(
        ["python3", os.path.basename(solution_file)],
        capture_output=True, text=True,
        cwd=os.path.dirname(solution_file), env=env,
    )

    with tempfile.TemporaryDirectory(prefix="exam_runner_") as run_dir:
        shutil.copy2(user_file, os.path.join(run_dir, "_solution.py"))
        patched = os.path.basename(_patch_solution(solution_file, run_dir))
        try:
            actual = subprocess.run(
                ["python3", patched], capture_output=True, text=True,
                cwd=run_dir, timeout=10, env=env,
            )
        except subprocess.TimeoutExpired:
            print(f"{RED}TIMEOUT — your code may have an infinite loop.{NC}")
            return 1

    if actual.returncode != 0:
        print(f"{RED}RUNTIME ERROR:{NC}")
        for line in actual.stderr.splitlines():
            if patched not in line:      # hide our own scaffolding file
                print(line)
        return 1

    exp_lines = expected.stdout.strip().splitlines()
    act_lines = actual.stdout.strip().splitlines()

    if exp_lines == act_lines:
        print(f"{GREEN}ALL TESTS PASSED!{NC}")
        return 0

    for line in act_lines:
        if line.startswith("[FAIL]"):
            print(f"{RED}{line}{NC}")

    print()
    print(f"{YELLOW}--- Expected output ---{NC}")
    print(expected.stdout, end="")
    print(f"{RED}--- Your output ---{NC}")
    print(actual.stdout, end="")
    return 1


if __name__ == "__main__":
    sys.exit(main())

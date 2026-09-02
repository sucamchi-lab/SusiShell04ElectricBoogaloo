"""
package_dependency_resolver.py

Install order for a package -> dependencies mapping (Kahn's algorithm,
by hand). Packages that are ready at the same moment are emitted together
in alphabetical order, so the output is deterministic. A cycle means no
valid order exists, so the answer is [].
"""

FORBIDDEN = ["graphlib", "TopologicalSorter"]


def package_dependency_resolver(packages: dict[str, list[str]]) -> list[str]:
    # dependencies that aren't packages themselves are ignored
    waiting_for: dict[str, set[str]] = {}
    for name, deps in packages.items():
        waiting_for[name] = set()
        for dep in deps:
            if dep in packages:
                waiting_for[name].add(dep)

    order = []
    while waiting_for:
        ready = []
        for name, blockers in waiting_for.items():
            if not blockers:
                ready.append(name)

        if not ready:
            return []                # whatever is left sits in a cycle

        ready.sort()
        for name in ready:
            order.append(name)
            del waiting_for[name]
        for blockers in waiting_for.values():
            for name in ready:
                blockers.discard(name)

    return order


if __name__ == "__main__":
    tests: list[tuple[dict[str, list[str]], list[str]]] = [
        ({"app": ["database"], "database": ["driver"], "driver": []},
         ["driver", "database", "app"]),
        ({"A": [], "B": ["A"], "C": ["A", "B"]}, ["A", "B", "C"]),
        ({}, []),
        ({"X": ["Y"], "Y": ["X"]}, []),
        ({"web": [], "api": [], "frontend": ["web"], "backend": ["api"]},
         ["api", "web", "backend", "frontend"]),
        ({"solo": ["ghost"]}, ["solo"]),
        ({"loop": ["loop"]}, []),
        ({"b": [], "a": []}, ["a", "b"]),
        ({"a": ["b"], "b": ["c"], "c": ["a"]}, []),
        ({"z": ["y"], "y": [], "x": []}, ["x", "y", "z"]),
    ]

    for packages, expected in tests:
        result = package_dependency_resolver(packages)
        status = "OK" if result == expected else "FAIL"
        print(f"[{status}] package_dependency_resolver({packages!r}) "
              f"-> {result}")

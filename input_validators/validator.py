#!/usr/bin/env python3
import re
import sys

INT_RE = re.compile(r'^(0|[1-9][0-9]*)$')


def fail(msg):
    print(msg, file=sys.stderr)
    sys.exit(43)


def parse_int(s, label):
    if not INT_RE.match(s):
        fail(f"{label}: invalid integer (leading zeros or non-numeric): {s!r}")
    return int(s)


line = sys.stdin.readline()
if line == "":
    fail("Empty input")

parts = line.split()
if len(parts) != 2:
    fail(f"First line must have exactly 2 integers, got: {line!r}")

N = parse_int(parts[0], "N")
M = parse_int(parts[1], "M")

if not (2 <= N <= 5000):
    fail(f"N={N} out of range [2, 5000]")
if not (1 <= M <= 20000):
    fail(f"M={M} out of range [1, 20000]")

seen = set()
for i in range(M):
    line = sys.stdin.readline()
    if line == "":
        fail(f"Expected {M} edge lines, got only {i}")
    parts = line.split()
    if len(parts) != 3:
        fail(f"Edge line {i}: expected 3 integers, got: {line!r}")
    u = parse_int(parts[0], f"Edge {i} u")
    v = parse_int(parts[1], f"Edge {i} v")
    c = parse_int(parts[2], f"Edge {i} c")
    if not (0 <= u <= N - 1):
        fail(f"Edge {i}: u={u} not in [0, {N-1}]")
    if not (0 <= v <= N - 1):
        fail(f"Edge {i}: v={v} not in [0, {N-1}]")
    if u == v:
        fail(f"Edge {i}: self-loop u=v={u}")
    if (u, v) in seen:
        fail(f"Edge {i}: parallel edge ({u},{v})")
    seen.add((u, v))
    if c < 1:
        fail(f"Edge {i}: capacity c={c} must be >= 1")

if sys.stdin.readline() != "":
    fail("Unexpected trailing content")

sys.exit(42)

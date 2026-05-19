import sys
import random
from collections import deque


def build_flow_network(n, edges):
    graph = [[] for _ in range(n)]
    for u, v, cap in edges:
        graph[u].append([v, cap, len(graph[v])])
        graph[v].append([u, 0, len(graph[u]) - 1])
    return graph


def run_max_flow(graph, n, s, t):
    total = 0
    while True:
        parent = [-1] * n
        parent_edge = [-1] * n
        parent[s] = s
        q = deque([s])
        while q and parent[t] == -1:
            u = q.popleft()
            for i, (v, cap, _) in enumerate(graph[u]):
                if cap > 0 and parent[v] == -1:
                    parent[v] = u
                    parent_edge[v] = i
                    q.append(v)
        if parent[t] == -1:
            break
        f = float('inf')
        v = t
        while v != s:
            u = parent[v]
            f = min(f, graph[u][parent_edge[v]][1])
            v = u
        v = t
        while v != s:
            u = parent[v]
            ei = parent_edge[v]
            graph[u][ei][1] -= f
            graph[v][graph[u][ei][2]][1] += f
            v = u
        total += f
    return total


def is_unique_min_cut(graph, n, s, t):
    # S: vertices reachable from s in residual
    S = {s}
    q = deque([s])
    while q:
        u = q.popleft()
        for v, cap, _ in graph[u]:
            if cap > 0 and v not in S:
                S.add(v)
                q.append(v)

    # T: vertices that can reach t in residual (reverse BFS)
    rev = [[] for _ in range(n)]
    for u in range(n):
        for v, cap, _ in graph[u]:
            if cap > 0:
                rev[v].append(u)
    T = {t}
    q = deque([t])
    while q:
        u = q.popleft()
        for v in rev[u]:
            if v not in T:
                T.add(v)
                q.append(v)

    # Unique iff every vertex belongs to exactly one side
    return len(S) + len(T) == n


def try_generate(N, M, rng):
    edge_set = set()
    edges = []

    # Seed a Hamiltonian path 0 → π[1] → ... → π[N-2] → N-1.
    # This puts every vertex on an s-t path, so after max flow each vertex
    # lands in either S (reachable from source) or T (can reach sink) in the
    # residual — a necessary condition for a unique min-cut partition.
    if N == 2:
        edges.append((0, 1, rng.randint(1, 100)))
        edge_set.add((0, 1))
    else:
        interior = list(range(1, N - 1))
        rng.shuffle(interior)
        path = [0] + interior + [N - 1]
        for i in range(N - 1):
            u, v = path[i], path[i + 1]
            edges.append((u, v, rng.randint(1, 100)))
            edge_set.add((u, v))

    # Fill remaining edges from a shuffled pool of all valid (u,v) pairs
    pool = [(u, v) for u in range(N) for v in range(N)
            if u != v and (u, v) not in edge_set]
    rng.shuffle(pool)

    for (u, v) in pool:
        if len(edges) == M:
            break
        edges.append((u, v, rng.randint(1, 100)))
        edge_set.add((u, v))

    if len(edges) < M:
        return None  # M too large for this N

    graph = build_flow_network(N, edges)
    run_max_flow(graph, N, 0, N - 1)

    if is_unique_min_cut(graph, N, 0, N - 1):
        return edges
    return None


def main():
    if len(sys.argv) != 4:
        print("Usage: python generator.py N M seed", file=sys.stderr)
        sys.exit(1)

    N, M, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])

    if N < 2:
        print(f"Error: N={N} must be >= 2", file=sys.stderr)
        sys.exit(1)
    if not (1 <= M <= N * (N - 1)):
        print(f"Error: M={M} out of range [1, {N*(N-1)}] for N={N}", file=sys.stderr)
        sys.exit(1)

    MAX_RETRIES = 200
    for attempt in range(MAX_RETRIES):
        rng = random.Random(seed + attempt)
        edges = try_generate(N, M, rng)
        if edges is not None:
            print(N, M)
            for u, v, c in edges:
                print(u, v, c)
            return

    print(f"Error: could not generate unique min-cut graph after {MAX_RETRIES} attempts", file=sys.stderr)
    sys.exit(1)


main()

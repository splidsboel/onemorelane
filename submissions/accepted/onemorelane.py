import sys
from collections import deque

input = sys.stdin.readline
INF = 10**18

def build_graph(n, edges, upgrade_idx=-1):
    g = [[] for _ in range(n)]

    for i, (u, v, c) in enumerate(edges):
        cap = INF if i == upgrade_idx else c

        fwd = len(g[u])
        bwd = len(g[v])

        g[u].append([v, cap, bwd])
        g[v].append([u, 0, fwd])

    return g

def bfs_level(g, s, t, level):
    level[:] = [-1] * len(level)
    level[s] = 0

    q = deque([s])

    while q:
        u = q.popleft()

        for v, cap, _ in g[u]:
            if cap > 0 and level[v] < 0:
                level[v] = level[u] + 1
                q.append(v)

    return level[t] >= 0

def dfs_block(g, u, t, pushed, level, it):
    if u == t:
        return pushed

    while it[u] < len(g[u]):
        v, cap, rev = g[u][it[u]]

        if cap > 0 and level[v] == level[u] + 1:
            d = dfs_block(g, v, t, min(pushed, cap), level, it)

            if d > 0:
                g[u][it[u]][1] -= d
                g[v][rev][1] += d
                return d

        it[u] += 1

    return 0

def dinic(g, s, t):
    n = len(g)

    level = [-1] * n
    flow = 0

    while bfs_level(g, s, t, level):
        it = [0] * n

        while True:
            f = dfs_block(g, s, t, INF, level, it)

            if f == 0:
                break

            flow += f

    return flow

def reachable(g, s):
    vis = set([s])

    q = deque([s])

    while q:
        u = q.popleft()

        for v, cap, _ in g[u]:
            if cap > 0 and v not in vis:
                vis.add(v)
                q.append(v)

    return vis

def solve():
    sys.setrecursionlimit(200000)

    n, m = map(int, input().split())

    edges = []

    for _ in range(m):
        u, v, c = map(int, input().split())
        edges.append((u, v, c))

    # Original max flow
    g = build_graph(n, edges)
    base_flow = dinic(g, 0, n - 1)

    # Find source side of min cut
    S = reachable(g, 0)

    # Candidate edges in min cut
    cut_edges = [
        i for i, (u, v, c) in enumerate(edges)
        if u in S and v not in S
    ]

    best_flow = base_flow
    best_edge = (edges[0][0], edges[0][1])

    # Try upgrading each cut edge
    for i in cut_edges:
        g2 = build_graph(n, edges, upgrade_idx=i)

        new_flow = dinic(g2, 0, n - 1)

        if new_flow > best_flow:
            best_flow = new_flow
            best_edge = (edges[i][0], edges[i][1])

    print(best_edge[0], best_edge[1])

solve()
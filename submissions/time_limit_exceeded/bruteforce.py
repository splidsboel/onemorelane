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


def edmonds_karp(g, s, t):
    n = len(g)
    flow = 0
    while True:
        parent = [-1] * n
        parent_edge = [-1] * n
        parent[s] = s
        q = deque([s])
        while q and parent[t] == -1:
            u = q.popleft()
            for i, (v, cap, _) in enumerate(g[u]):
                if cap > 0 and parent[v] == -1:
                    parent[v] = u
                    parent_edge[v] = i
                    q.append(v)
        if parent[t] == -1:
            break
        f = INF
        v = t
        while v != s:
            u = parent[v]
            f = min(f, g[u][parent_edge[v]][1])
            v = u
        v = t
        while v != s:
            u = parent[v]
            ei = parent_edge[v]
            g[u][ei][1] -= f
            g[v][g[u][ei][2]][1] += f
            v = u
        flow += f
    return flow


def solve():
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        u, v, c = map(int, input().split())
        edges.append((u, v, c))

    best_flow = -1
    best_edge = (edges[0][0], edges[0][1])

    for i in range(m):
        g = build_graph(n, edges, upgrade_idx=i)
        f = edmonds_karp(g, 0, n - 1)
        if f > best_flow:
            best_flow = f
            best_edge = (edges[i][0], edges[i][1])

    print(best_edge[0], best_edge[1])


solve()

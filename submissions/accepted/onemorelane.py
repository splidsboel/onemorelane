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

        # store: [to, capacity, reverse_index]
        g[u].append([v, cap, bwd])
        g[v].append([u, 0, fwd])

    return g


def dfs_augment(g, u, t, f, vis):
    if u == t:
        return f

    vis.add(u)

    for i, (v, cap, rev) in enumerate(g[u]):
        if cap > 0 and v not in vis:
            pushed = dfs_augment(g, v, t, min(f, cap), vis)

            if pushed > 0:
                g[u][i][1] -= pushed
                g[v][rev][1] += pushed
                return pushed

    return 0


def ford_fulkerson(g, s, t):
    flow = 0

    while True:
        vis = set()
        pushed = dfs_augment(g, s, t, INF, vis)

        if pushed == 0:
            break

        flow += pushed

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

    # Base max flow
    g = build_graph(n, edges)
    base_flow = ford_fulkerson(g, 0, n - 1)

    # Min cut source side
    S = reachable(g, 0)

    cut_edges = [
        i for i, (u, v, c) in enumerate(edges)
        if u in S and v not in S
    ]

    best_flow = base_flow
    best_edge = (edges[0][0], edges[0][1])

    for i in cut_edges:
        g2 = build_graph(n, edges, upgrade_idx=i)
        new_flow = ford_fulkerson(g2, 0, n - 1)

        if new_flow > best_flow:
            best_flow = new_flow
            best_edge = (edges[i][0], edges[i][1])

    print(best_edge[0], best_edge[1])


if __name__ == "__main__":
    solve()
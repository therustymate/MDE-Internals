#!/usr/bin/env python3
"""Fixed-width, vertical strings-based internal DLL reference graph."""
import argparse
import csv
import os
import re
import subprocess
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import matplotlib
if not (os.environ.get('DISPLAY') or os.environ.get('WAYLAND_DISPLAY')):
    matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import networkx as nx

DLL_RE = re.compile(r'(?i)(?<![\w.-])(?:[a-z]:[\\/]|\.{1,2}[\\/])?(?:[\w .-]+[\\/])*[\w.-]+\.dll(?![\w.-])')
EXTENSIONS = {'.exe', '.dll'}


def extract(path):
    found = set()
    for enc in ('s', 'l'):
        result = subprocess.run(['strings', '-a', '-n', '4', '-e', enc, str(path)],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.decode(errors='replace').strip() or 'strings failed')
        for line in result.stdout.decode('utf-8', errors='replace').splitlines():
            for match in DLL_RE.finditer(line):
                found.add(match.group().replace('\\', '/').rsplit('/', 1)[-1].lower())
    return found


def scan(root, workers):
    files = sorted((p for p in root.rglob('*') if p.is_file() and p.suffix.lower() in EXTENSIONS), key=str)
    print(f'[+] PE candidates: {len(files)}', flush=True)
    refs = {}
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(extract, p): p for p in files}
        for i, future in enumerate(as_completed(futures), 1):
            path = futures[future]
            try:
                refs[path] = future.result()
            except Exception as exc:
                print(f'\n[!] {path}: {exc}', flush=True)
                refs[path] = set()
            if i % 10 == 0 or i == len(files):
                print(f'\r[*] Scanned {i}/{len(files)}', end='', flush=True)
    print()
    return files, refs


def make_graph(files, refs):
    by_name = defaultdict(list)
    for p in files:
        if p.suffix.lower() == '.dll':
            by_name[p.name.lower()].append(p)
    g = nx.DiGraph()
    for source, names in refs.items():
        for name in names:
            for target in by_name.get(name, ()):
                if source != target:
                    g.add_edge(source, target, ambiguous=len(by_name[name]) > 1)
    return g


def focus_graph(g, name, depth):
    if not name:
        return g
    matches = {n for n in g if n.name.casefold() == name.casefold()}
    if not matches:
        raise SystemExit(f'[!] Focus not found among connected files: {name}')
    chosen, frontier = set(matches), set(matches)
    for _ in range(depth):
        nearby = set()
        for n in frontier:
            nearby.update(g.successors(n))
            nearby.update(g.predecessors(n))
        frontier = nearby - chosen
        chosen.update(frontier)
    return g.subgraph(chosen).copy()


def ordered_layers(g):
    """SCC condensation + longest-path depth; reorder each layer by parent barycenter."""
    condensed = nx.condensation(g)
    depths = {c: 0 for c in condensed}
    for c in nx.topological_sort(condensed):
        for nxt in condensed.successors(c):
            depths[nxt] = max(depths[nxt], depths[c] + 1)
    layer_of = {n: depths[c] for c in condensed for n in condensed.nodes[c]['members']}
    # Keep disconnected components together and put components with EXE first.
    components = sorted(nx.weakly_connected_components(g),
                        key=lambda comp: (not any(n.suffix.lower() == '.exe' for n in comp),
                                          -len(comp), min(str(n) for n in comp)))
    rows = []
    for comp in components:
        buckets = defaultdict(list)
        for n in comp:
            buckets[layer_of[n]].append(n)
        previous = {}
        for level in sorted(buckets):
            nodes = buckets[level]
            def key(n):
                parents = [previous[p] for p in g.predecessors(n) if p in previous]
                return (sum(parents)/len(parents) if parents else float('inf'),
                        n.suffix.lower() != '.exe', -g.out_degree(n), n.name.lower(), str(n))
            nodes.sort(key=key)
            rows.append((level, nodes))
            previous.update({n: i for i, n in enumerate(nodes)})
        rows.append((None, []))  # vertical gap between independent components
    return rows


def layout(g, columns):
    rows = ordered_layers(g)
    pos = {}
    y = 0
    for level, nodes in rows:
        if level is None:
            y += 0.5
            continue
        for start in range(0, len(nodes), columns):
            chunk = nodes[start:start + columns]
            offset = (columns - len(chunk)) / 2
            for index, node in enumerate(chunk):
                pos[node] = (offset + index, -y)
            y += 1
        y += 0.35
    return pos, max(y, 2)


def draw(g, root, output, columns, show):
    if not g:
        print('[!] No internal DLL references found.')
        return
    pos, rows = layout(g, columns)
    # Fixed width in inches; only height grows with the number of rows.
    width = max(9, columns * 2.35 + 1.4)
    height = max(5, rows * 1.12 + 1.5)
    fig, ax = plt.subplots(figsize=(width, height), facecolor='#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    # Fixed-width columns; use wrapped full names instead of truncation.
    box_w, box_h = 0.90, 0.56
    for source, target, data in g.edges(data=True):
        sx, sy = pos[source]
        tx, ty = pos[target]
        downward = ty < sy
        start = (sx, sy - box_h/2) if downward else (sx + box_w/2, sy)
        end = (tx, ty + box_h/2) if downward else (tx - box_w/2, ty)
        same_row = abs(sy - ty) < 0.01
        color = '#D97706' if data.get('ambiguous') else ('#94A3B8' if downward else '#A78BFA')
        arrow = FancyArrowPatch(start, end, arrowstyle='-|>', mutation_scale=10,
                                linewidth=0.9, color=color, alpha=0.52,
                                connectionstyle='arc3,rad=0', zorder=1)
        ax.add_patch(arrow)
    for node, (x, y) in pos.items():
        exe = node.suffix.lower() == '.exe'
        hub = g.in_degree(node) >= 5
        fill = '#FFF0D8' if exe else ('#EDE9FE' if hub else '#E5F1FF')
        border = '#D97706' if exe else ('#8B5CF6' if hub else '#3B82F6')
        ax.add_patch(FancyBboxPatch((x-box_w/2, y-box_h/2), box_w, box_h,
                     boxstyle='round,pad=0.035,rounding_size=0.075',
                     facecolor=fill, edgecolor=border, linewidth=1.1, zorder=3))
        # Preserve every character; wrap at fixed character boundaries if needed.
        name = '\n'.join(node.name[i:i+22] for i in range(0, len(node.name), 22))
        name_lines = name.count('\n') + 1
        ax.text(x, y+0.07, name, ha='center', va='center',
                fontsize=max(5.5, 8.1 - max(0, name_lines-2)*0.4),
                color='#172033', fontweight='bold' if exe else 'normal', zorder=4)
        ax.text(x, y-0.20, f'out {g.out_degree(node)}  ·  in {g.in_degree(node)}',
                ha='center', va='center', fontsize=6.7, color='#64748B', zorder=4)
    ax.set_xlim(-0.65, columns-0.35)
    ax.set_ylim(-rows + 0.4, 0.9)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.set_title(f'Internal DLL references  ·  {g.number_of_nodes()} files / {g.number_of_edges()} links',
                 loc='left', fontsize=13, fontweight='bold', color='#172033', pad=18)
    fig.text(0.03, 0.015, 'Strings-based candidates · orange edges: duplicate DLL filename · purple edges: backward/cyclic',
             fontsize=8, color='#64748B')
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    for suffix in ('.png', '.svg'):
        dest = output.with_suffix(suffix)
        fig.savefig(dest, dpi=160 if suffix == '.png' else None,
                    bbox_inches='tight', facecolor=fig.get_facecolor())
        print(f'[+] Saved: {dest}')
    if show:
        if 'agg' in matplotlib.get_backend().lower():
            print('[!] No interactive backend; open the PNG or SVG.')
        else:
            plt.show()
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description='Fixed-width internal DLL strings reference graph')
    parser.add_argument('directory', type=Path)
    parser.add_argument('--columns', type=int, default=4, help='Maximum nodes per row (default: 4)')
    parser.add_argument('--focus', help='PE filename to center analysis on')
    parser.add_argument('--depth', type=int, default=2)
    parser.add_argument('--workers', type=int, default=min(8, os.cpu_count() or 4))
    parser.add_argument('--output', default='mde_vertical_graph')
    parser.add_argument('--show', action='store_true')
    args = parser.parse_args()
    if args.columns < 1 or args.workers < 1 or args.depth < 0:
        parser.error('--columns and --workers must be positive; --depth must be nonnegative')
    root = args.directory.resolve()
    if not root.is_dir():
        parser.error(f'not a directory: {root}')
    files, refs = scan(root, args.workers)
    graph = focus_graph(make_graph(files, refs), args.focus, args.depth)
    print(f'[+] Nodes: {graph.number_of_nodes()} | edges: {graph.number_of_edges()}')
    output = Path(args.output)
    with output.with_suffix('.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.writer(stream)
        writer.writerow(['source', 'target', 'ambiguous_filename'])
        for source, target, data in graph.edges(data=True):
            writer.writerow([str(source.relative_to(root)), str(target.relative_to(root)), data.get('ambiguous', False)])
    print(f'[+] Saved: {output.with_suffix(".csv")}')
    draw(graph, root, output, args.columns, args.show)


if __name__ == '__main__':
    main()

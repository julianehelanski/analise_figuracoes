"""Matriz de cocorrência e rede figural por obra.

Para cada obra em escopo, lê `outputs/<obra_id>/csv/kwic.csv` (ocorrências
válidas) e constrói matriz de cocorrência entre grupos figurativos com
janela configurável (default: 200 palavras).

Outputs:
- `outputs/<obra_id>/csv/cocorrencia.csv`: matriz simétrica grupo × grupo.
- `outputs/<obra_id>/figuras/rede_cocorrencia.png`: grafo (NetworkX).
- `outputs/<obra_id>/relatorios/cocorrencia.md`: lista de pares com maior
  força de cocorrência.

Comunidades por Louvain ficam comentadas: se `python-louvain` estiver
instalado, são detectadas e impressas; senão, é pulado sem erro.

Uso:
    python scripts/05_cooccurrence.py
    python scripts/05_cooccurrence.py --janela 200 --only latour_1987
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from itertools import combinations
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
METADATA_CSV = REPO_ROOT / "corpus" / "metadata.csv"
OUTPUTS_DIR = REPO_ROOT / "outputs"
CORPUS_TXT_DIR = REPO_ROOT / "corpus" / "txt_norm"


def obras_em_escopo(escopo: str = "etapa1") -> list[dict[str, str]]:
    """Filtra metadata.csv por `escopo_etapa1`, `escopo_etapa2` ou ambos."""
    with METADATA_CSV.open(encoding="utf-8", newline="") as f:
        linhas = list(csv.DictReader(f))
    def _mark(r: dict[str, str], col: str) -> bool:
        return r.get(col, "").strip().lower() == "sim"
    if escopo == "etapa1":
        return [r for r in linhas if _mark(r, "escopo_etapa1")]
    if escopo == "etapa2":
        return [r for r in linhas if _mark(r, "escopo_etapa2")]
    if escopo == "todos":
        return [r for r in linhas if _mark(r, "escopo_etapa1") or _mark(r, "escopo_etapa2")]
    raise SystemExit(f"escopo desconhecido '{escopo}'.")


def carregar_ocorrencias(obra_id: str) -> list[tuple[str, int]]:
    p = OUTPUTS_DIR / obra_id / "csv" / "kwic.csv"
    if not p.exists():
        return []
    ocs: list[tuple[str, int]] = []
    with p.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row.get("descartado_por_exclusao", "0") != "0":
                continue
            try:
                ocs.append((row["grupo"], int(row["posicao_no_texto"])))
            except (KeyError, ValueError):
                continue
    return ocs


def cocorrencia_por_janela(
    ocs: list[tuple[str, int]],
    janela_palavras: int,
    media_chars_por_palavra: float = 5.5,
) -> dict[tuple[str, str], int]:
    """Conta pares de grupos cujas ocorrências caem em janela de N palavras.

    A janela é aproximada por `janela_palavras * media_chars_por_palavra` em
    caracteres, suficiente para a Etapa 1.
    """
    janela_chars = int(janela_palavras * media_chars_por_palavra)
    ocs_ord = sorted(ocs, key=lambda x: x[1])
    pares: dict[tuple[str, str], int] = defaultdict(int)
    n = len(ocs_ord)
    for i in range(n):
        grupo_i, pos_i = ocs_ord[i]
        for j in range(i + 1, n):
            grupo_j, pos_j = ocs_ord[j]
            if pos_j - pos_i > janela_chars:
                break
            if grupo_i == grupo_j:
                continue
            chave = tuple(sorted([grupo_i, grupo_j]))
            pares[chave] += 1
    return pares


def gerar_outputs(obra_id: str, janela: int) -> None:
    ocs = carregar_ocorrencias(obra_id)
    if not ocs:
        print(f"  [pular] sem ocorrências válidas para {obra_id}.")
        return
    grupos = sorted({g for g, _ in ocs})
    pares = cocorrencia_por_janela(ocs, janela)

    csv_dir = OUTPUTS_DIR / obra_id / "csv"
    csv_dir.mkdir(parents=True, exist_ok=True)
    matriz = csv_dir / "cocorrencia.csv"
    with matriz.open("w", encoding="utf-8", newline="") as f:
        escritor = csv.writer(f)
        escritor.writerow([""] + grupos)
        for g in grupos:
            linha = [g]
            for h in grupos:
                if g == h:
                    linha.append(0)
                else:
                    chave = tuple(sorted([g, h]))
                    linha.append(pares.get(chave, 0))
            escritor.writerow(linha)

    md = OUTPUTS_DIR / obra_id / "relatorios" / "cocorrencia.md"
    md.parent.mkdir(parents=True, exist_ok=True)
    linhas: list[str] = [
        f"# Cocorrência figural: {obra_id}",
        "",
        f"Janela: {janela} palavras (aproximada por caracteres).",
        f"Pares válidos: {len(pares)}.",
        "",
        "## Top 20 pares por força de cocorrência",
        "",
        "| grupo A | grupo B | n |",
        "|---|---|---:|",
    ]
    for (a, b), n in sorted(pares.items(), key=lambda x: -x[1])[:20]:
        linhas.append(f"| {a} | {b} | {n} |")
    md.write_text("\n".join(linhas), encoding="utf-8")

    # Figura: NetworkX -----------------------------------------------------
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import networkx as nx
    except ImportError:
        print("  (matplotlib/networkx ausentes; pulei a figura).")
        return

    G = nx.Graph()
    contagem_grupo: dict[str, int] = defaultdict(int)
    for g, _ in ocs:
        contagem_grupo[g] += 1
    for g in grupos:
        G.add_node(g, freq=contagem_grupo[g])
    for (a, b), n in pares.items():
        if n > 0:
            G.add_edge(a, b, weight=n)

    if G.number_of_edges() == 0:
        print("  (nenhuma cocorrência detectada; sem figura).")
        return

    fig_dir = OUTPUTS_DIR / obra_id / "figuras"
    fig_dir.mkdir(parents=True, exist_ok=True)
    pos = nx.spring_layout(G, seed=42, weight="weight")
    fig, ax = plt.subplots(figsize=(9, 7))
    tamanhos = [200 + 80 * G.nodes[n]["freq"] ** 0.5 for n in G.nodes()]
    larguras = [0.4 + 0.3 * G.edges[e]["weight"] ** 0.5 for e in G.edges()]
    nx.draw_networkx_nodes(G, pos, node_size=tamanhos, node_color="#4c72b0",
                           edgecolors="white", linewidths=1.5, ax=ax)
    nx.draw_networkx_edges(G, pos, width=larguras, alpha=0.45, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)
    ax.set_axis_off()
    fig.tight_layout()
    fig.savefig(fig_dir / "rede_cocorrencia.png", dpi=300)
    fig.savefig(fig_dir / "rede_cocorrencia.svg")
    plt.close(fig)

    # Louvain opcional
    try:
        import community as community_louvain  # python-louvain
        particao = community_louvain.best_partition(G, weight="weight", random_state=42)
        clusters: dict[int, list[str]] = defaultdict(list)
        for node, cid in particao.items():
            clusters[cid].append(node)
        with (md.parent / "cocorrencia_clusters.md").open("w", encoding="utf-8") as f:
            f.write(f"# Clusters Louvain: {obra_id}\n\n")
            for cid, nodes in sorted(clusters.items()):
                f.write(f"## Cluster {cid} (n={len(nodes)})\n\n")
                for n in sorted(nodes):
                    f.write(f"- {n}\n")
                f.write("\n")
    except ImportError:
        pass

    print(f"  gravado: outputs/{obra_id}/csv/cocorrencia.csv")
    print(f"  gravado: outputs/{obra_id}/figuras/rede_cocorrencia.png")
    print(f"  gravado: outputs/{obra_id}/relatorios/cocorrencia.md")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--only", help="filtra obras por substring de id.")
    parser.add_argument("--janela", type=int, default=200,
                        help="janela em palavras para cocorrência (default: 200).")
    parser.add_argument("--escopo", default="etapa1",
                        choices=["etapa1", "etapa2", "todos"],
                        help="filtro de obras: etapa1 (default), etapa2 ou todos.")
    args = parser.parse_args()

    obras = obras_em_escopo(args.escopo)
    if args.only:
        obras = [o for o in obras if args.only.lower() in o["id"].lower()]
    for obra in obras:
        print(f"\n[{obra['id']}]")
        gerar_outputs(obra["id"], args.janela)


if __name__ == "__main__":
    main()

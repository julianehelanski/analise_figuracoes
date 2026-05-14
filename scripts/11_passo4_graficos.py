"""
Passo 4 do refinamento, gráficos comparativos para o capítulo 2 da tese.

Gera três figuras que sustentam visualmente a subseção sobre figuração
militar nas três obras de Latour:

1. comparacao_frequencias_tres_obras.{png,svg}: densidade dos 17 campos
   figurativos nas três obras, em barras agrupadas horizontais. Campo
   militar destacado em vermelho ferrugem; valores refinados pela
   desambiguação de war/wars no campo militar (passo 1 do refinamento)
   substituem a contagem bruta do frequencias.csv.

2. densidade_militar_sia_pandora.{png,svg}: distribuição da densidade
   do campo militar ao longo dos textos de Science in Action 1987 e
   Pandora's Hope 1999, em janelas deslizantes de 1.000 palavras com
   passo de 200. Em Pandora, ocorrências de war/wars classificadas como
   descritivas no passo 1 são excluídas antes da contagem.

3. rede_cocorrencia_sia.{png,svg}: grafo de cocorrências entre campos
   figurativos em Science in Action, recalculado a partir do kwic.csv
   em janela de 100 palavras (o cocorrencia.csv versionado usa 200; a
   janela menor é exigida pelo briefing). Limiar mínimo de 5
   cocorrências por aresta. Campo militar como nó em destaque.

Saídas em outputs/passo4/figuras/, em PNG (300 dpi) e SVG.
"""

from __future__ import annotations

import bisect
import csv
import re
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import yaml

REPO = Path(__file__).resolve().parents[1]
OUT_DIR = REPO / "outputs" / "passo4" / "figuras"
OUT_DIR.mkdir(parents=True, exist_ok=True)

OBRAS_ANO = [
    ("latour_woolgar_1986_lab_life_en", "1986"),
    ("latour_1987_science_action_en", "1987"),
    ("latour_1999_pandora_en", "1999"),
]

# Valores refinados do campo militar (passo 1 do refinamento). Tabela
# refinamento/tabela_militar_refinada.tex.
MILITAR_REFINADO = {
    "latour_woolgar_1986_lab_life_en": {"n": 37, "freq_10k": 3.50},
    "latour_1987_science_action_en": {"n": 364, "freq_10k": 26.03},
    "latour_1999_pandora_en": {"n": 156, "freq_10k": 12.19},
}

# Paleta. O vermelho ferrugem (#B22222) é o destaque do campo militar.
# Variantes mais clara e mais escura indicam cronologia. Os demais
# campos seguem a mesma lógica em escala de cinza.
COR_MILITAR = {"1986": "#E08570", "1987": "#B22222", "1999": "#7A1A1A"}
COR_BASE = {"1986": "#D4D4D4", "1987": "#808080", "1999": "#404040"}


def estilo_matplotlib() -> None:
    """Aplica defaults sóbrios: sem spines top/direita, grid leve no X."""
    plt.rcParams.update({
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": False,
        "grid.alpha": 0.3,
        "grid.linewidth": 0.5,
        "figure.dpi": 100,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "font.size": 10,
        "font.family": "DejaVu Sans",
    })


def salvar(fig, nome: str) -> None:
    """Salva a figura em PNG 300 dpi e SVG."""
    fig.savefig(OUT_DIR / f"{nome}.png", dpi=300, bbox_inches="tight")
    fig.savefig(OUT_DIR / f"{nome}.svg", bbox_inches="tight")
    plt.close(fig)


def carregar_campos_catalogo() -> list[str]:
    """Lê os 17 campos do catálogo, na ordem do arquivo."""
    with open(REPO / "campos_lexicais" / "catalogo_termos.yaml") as f:
        cat = yaml.safe_load(f)
    return list(cat["latour"].keys())


def carregar_frequencias(obra_id: str) -> dict[str, float]:
    """Retorna mapa campo -> frequência por 10k palavras."""
    freq: dict[str, float] = {}
    with open(REPO / "outputs" / obra_id / "csv" / "frequencias.csv") as f:
        for row in csv.DictReader(f):
            freq[row["grupo"]] = float(row["frequencia_por_10k_palavras"])
    return freq


def carregar_n_absoluto(obra_id: str) -> dict[str, int]:
    """Retorna mapa campo -> ocorrências absolutas."""
    n: dict[str, int] = {}
    with open(REPO / "outputs" / obra_id / "csv" / "frequencias.csv") as f:
        for row in csv.DictReader(f):
            n[row["grupo"]] = int(row["n_ocorrencias"])
    return n


def figura_1_comparacao_frequencias() -> None:
    """Densidade dos 17 campos × 3 obras, barras agrupadas horizontais."""
    campos = carregar_campos_catalogo()
    freq_por_obra = {
        ano: carregar_frequencias(obra_id) for obra_id, ano in OBRAS_ANO
    }
    # Substitui o militar pela contagem refinada do passo 1
    for obra_id, ano in OBRAS_ANO:
        freq_por_obra[ano]["militar"] = MILITAR_REFINADO[obra_id]["freq_10k"]

    # Ordena os campos por densidade decrescente em SIA (1987). Quem
    # estiver ausente em SIA cai para o fim, mantendo ordem do catálogo.
    def chave_ord(campo: str) -> tuple[float, int]:
        return (-freq_por_obra["1987"].get(campo, 0.0), campos.index(campo))

    campos_ord = sorted(campos, key=chave_ord)

    fig, ax = plt.subplots(figsize=(12, 10))
    n = len(campos_ord)
    y = np.arange(n)
    altura = 0.27
    offsets = {"1986": -altura, "1987": 0.0, "1999": altura}

    for ano in ("1986", "1987", "1999"):
        valores = [freq_por_obra[ano].get(c, 0.0) for c in campos_ord]
        cores = [
            COR_MILITAR[ano] if c == "militar" else COR_BASE[ano]
            for c in campos_ord
        ]
        ax.barh(
            y + offsets[ano],
            valores,
            altura,
            color=cores,
            edgecolor="white",
            linewidth=0.3,
            label=ano,
        )

    # Anotações inline com a contagem refinada do militar
    idx_militar = campos_ord.index("militar")
    for ano in ("1986", "1987", "1999"):
        val = freq_por_obra[ano]["militar"]
        texto = f"{val:.2f}".replace(".", ",")
        ax.text(
            val + 0.4,
            idx_militar + offsets[ano],
            texto,
            va="center",
            ha="left",
            fontsize=8,
            color="#303030",
            fontweight="bold" if ano == "1987" else "normal",
        )

    ax.set_yticks(y)
    ax.set_yticklabels(campos_ord, fontsize=10)
    ax.invert_yaxis()  # militar (maior em SIA) fica no topo
    ax.set_xlabel("Frequência por 10.000 palavras", fontsize=10)
    ax.grid(axis="x", alpha=0.3, linewidth=0.5)
    ax.set_axisbelow(True)

    # Legenda com retângulos da própria paleta do militar, que é o
    # registro visual mais carregado da figura.
    from matplotlib.patches import Patch
    legenda = [
        Patch(facecolor=COR_MILITAR["1986"], edgecolor="white", label="1986"),
        Patch(facecolor=COR_MILITAR["1987"], edgecolor="white", label="1987"),
        Patch(facecolor=COR_MILITAR["1999"], edgecolor="white", label="1999"),
    ]
    ax.legend(handles=legenda, loc="lower right", frameon=False, fontsize=10)

    # Margem extra à direita para acomodar as anotações do militar
    xmax = max(freq_por_obra[a].get(c, 0.0)
               for a in ("1986", "1987", "1999") for c in campos_ord)
    ax.set_xlim(0, xmax * 1.08)

    salvar(fig, "comparacao_frequencias_tres_obras")
    print(f"  figura 1 salva: {OUT_DIR / 'comparacao_frequencias_tres_obras.png'}")


def carregar_militar_hits(obra_id: str) -> list[dict]:
    """Lê do kwic.csv as ocorrências válidas do campo militar."""
    hits: list[dict] = []
    with open(REPO / "outputs" / obra_id / "csv" / "kwic.csv") as f:
        for row in csv.DictReader(f):
            if row["grupo"] != "militar":
                continue
            if row.get("descartado_por_exclusao", "0") != "0":
                continue
            hits.append({
                "pagina": int(row["pagina"]),
                "pos_char": int(row["posicao_no_texto"]),
                "termo": row["termo_encontrado"],
                "contexto_antes": row["contexto_antes"],
                "contexto_depois": row["contexto_depois"],
            })
    return hits


def filtrar_war_descritivos_pandora(hits: list[dict]) -> list[dict]:
    """Remove ocorrências de war/wars classificadas como descritivo no passo 1.

    Cruza por assinatura (pagina, termo, sufixo do contexto_antes,
    prefixo do contexto_depois). A classificação manual está em
    refinamento/war_pandora_classificacao.csv.
    """
    descritivos: set[tuple] = set()
    caminho = REPO / "refinamento" / "war_pandora_classificacao.csv"
    with open(caminho) as f:
        for row in csv.DictReader(f):
            if row["categoria_final"] != "descritivo":
                continue
            assinatura = (
                int(row["pagina"]),
                row["termo"].lower(),
                row["contexto_antes"][-30:].strip().lower(),
                row["contexto_depois"][:30].strip().lower(),
            )
            descritivos.add(assinatura)

    def is_descritivo(h: dict) -> bool:
        if h["termo"].lower() not in ("war", "wars"):
            return False
        sig = (
            h["pagina"],
            h["termo"].lower(),
            h["contexto_antes"][-30:].strip().lower(),
            h["contexto_depois"][:30].strip().lower(),
        )
        return sig in descritivos

    return [h for h in hits if not is_descritivo(h)]


def converter_char_para_palavra(txt: str, hits: list[dict]) -> tuple[list[int], int]:
    """Converte posições de char (kwic) em índices de palavra do txt_norm."""
    offsets_palavras = [m.start() for m in re.finditer(r"\S+", txt)]
    total = len(offsets_palavras)
    indices: list[int] = []
    for h in hits:
        idx = bisect.bisect_right(offsets_palavras, h["pos_char"]) - 1
        if idx < 0:
            idx = 0
        indices.append(idx)
    return indices, total


def figura_2_densidade_militar() -> None:
    """Curva de densidade do campo militar ao longo de SIA e Pandora."""
    janela = 1000
    passo = 200

    paineis = [
        ("latour_1987_science_action_en", "Science in Action, 1987", False),
        ("latour_1999_pandora_en", "Pandora's Hope, 1999", True),
    ]

    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    if not isinstance(axes, np.ndarray):
        axes = np.array([axes])

    for ax, (obra_id, rotulo, filtrar) in zip(axes, paineis):
        txt = (REPO / "corpus" / "txt_norm" / f"{obra_id}.txt").read_text(encoding="utf-8")
        hits = carregar_militar_hits(obra_id)
        if filtrar:
            hits = filtrar_war_descritivos_pandora(hits)
        word_indices, total_palavras = converter_char_para_palavra(txt, hits)
        word_indices.sort()

        starts = list(range(0, max(total_palavras - janela, 1), passo))
        xs: list[float] = []
        ys: list[int] = []
        for start in starts:
            end = start + janela
            lo = bisect.bisect_left(word_indices, start)
            hi = bisect.bisect_left(word_indices, end)
            xs.append((start + end) / 2 / 1000)
            ys.append(hi - lo)

        ax.plot(xs, ys, color="#B22222", linewidth=1.5)
        ax.fill_between(xs, 0, ys, color="#B22222", alpha=0.2)
        ax.set_ylabel(
            "Ocorrências do campo militar\n(janela de 1.000 palavras)",
            fontsize=9,
        )
        ax.set_xlim(0, total_palavras / 1000)
        ax.set_ylim(bottom=0)
        ax.text(
            0.01,
            0.95,
            rotulo,
            transform=ax.transAxes,
            fontsize=10,
            va="top",
            ha="left",
            color="#303030",
            fontweight="bold",
        )
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="x", alpha=0.3, linewidth=0.5)
        ax.set_axisbelow(True)

    axes[-1].set_xlabel("Posição no texto (milhares de palavras)", fontsize=10)

    fig.tight_layout()
    salvar(fig, "densidade_militar_sia_pandora")
    print(f"  figura 2 salva: {OUT_DIR / 'densidade_militar_sia_pandora.png'}")


def recomputar_cocorrencia_sia(janela_palavras: int = 100) -> dict[tuple[str, str], int]:
    """Recalcula cocorrência a partir do kwic.csv em janela menor.

    Mesma heurística de scripts/05_cooccurrence.py: aproxima a janela
    em palavras pelo número de caracteres, usando média de 5,5
    chars/palavra. O cocorrencia.csv versionado é gerado em janela 200;
    aqui uso 100 por exigência do briefing.
    """
    media_chars = 5.5
    janela_chars = int(janela_palavras * media_chars)

    ocs: list[tuple[str, int]] = []
    caminho = REPO / "outputs" / "latour_1987_science_action_en" / "csv" / "kwic.csv"
    with open(caminho) as f:
        for row in csv.DictReader(f):
            if row.get("descartado_por_exclusao", "0") != "0":
                continue
            try:
                ocs.append((row["grupo"], int(row["posicao_no_texto"])))
            except (KeyError, ValueError):
                continue
    ocs.sort(key=lambda x: x[1])

    pares: dict[tuple[str, str], int] = defaultdict(int)
    for i, (gi, pi) in enumerate(ocs):
        for j in range(i + 1, len(ocs)):
            gj, pj = ocs[j]
            if pj - pi > janela_chars:
                break
            if gi == gj:
                continue
            chave = tuple(sorted([gi, gj]))
            pares[chave] += 1
    return pares


def figura_3_rede_cocorrencia() -> None:
    """Grafo de cocorrências em SIA 1987 com militar como nó destacado."""
    pares = recomputar_cocorrencia_sia(janela_palavras=100)
    n_absoluto = carregar_n_absoluto("latour_1987_science_action_en")
    n_absoluto["militar"] = MILITAR_REFINADO["latour_1987_science_action_en"]["n"]

    limiar = 5
    G = nx.Graph()
    for (a, b), w in pares.items():
        if w >= limiar:
            G.add_edge(a, b, weight=w)

    if "militar" not in G.nodes():
        raise RuntimeError("nó 'militar' ausente do grafo; revisar dados de entrada")

    # Layout: spring com militar fixo no centro para evitar que o nó
    # mais conectado fique deslocado pela inicialização aleatória.
    pos_inicial = {n: (np.cos(2 * np.pi * i / len(G)) * 0.5,
                       np.sin(2 * np.pi * i / len(G)) * 0.5)
                   for i, n in enumerate(G.nodes())}
    pos_inicial["militar"] = (0.0, 0.0)
    pos = nx.spring_layout(
        G,
        pos=pos_inicial,
        fixed=["militar"],
        seed=42,
        k=1.2,
        iterations=200,
    )

    fig, ax = plt.subplots(figsize=(12, 10))

    pesos = np.array([G[u][v]["weight"] for u, v in G.edges()])
    peso_max = pesos.max() if len(pesos) else 1
    larguras = 0.4 + 4.0 * (pesos / peso_max)
    cores_arestas = [
        plt.cm.Greys(0.35 + 0.5 * (w / peso_max)) for w in pesos
    ]
    nx.draw_networkx_edges(
        G, pos, ax=ax,
        width=larguras,
        edge_color=cores_arestas,
        alpha=0.85,
    )

    # Tamanho do nó proporcional à frequência absoluta em SIA. Aplico
    # raiz para comprimir a escala (militar é muito maior que os outros).
    freqs = np.array([n_absoluto.get(node, 1) for node in G.nodes()])
    sizes = 80 + 60 * np.sqrt(freqs)
    cores_nos = [
        "#B22222" if node == "militar" else "#808080"
        for node in G.nodes()
    ]
    nx.draw_networkx_nodes(
        G, pos, ax=ax,
        node_size=sizes,
        node_color=cores_nos,
        edgecolors="#303030",
        linewidths=0.8,
    )

    # Rótulos com caixa branca semitransparente para reduzir sobreposição
    labels = {n: n for n in G.nodes()}
    label_options = dict(
        font_size=9,
        font_family="DejaVu Sans",
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.75, pad=1.2),
    )
    nx.draw_networkx_labels(G, pos, labels=labels, ax=ax, **label_options)

    ax.set_axis_off()
    ax.text(
        0.99, 0.01,
        f"Arestas: limiar mínimo de {limiar} cocorrências. Janela: 100 palavras.",
        transform=ax.transAxes,
        ha="right", va="bottom",
        fontsize=8, color="#505050",
    )

    salvar(fig, "rede_cocorrencia_sia")
    print(f"  figura 3 salva: {OUT_DIR / 'rede_cocorrencia_sia.png'}")


if __name__ == "__main__":
    estilo_matplotlib()
    print("Gerando figura 1 (comparação 17 campos × 3 obras)")
    figura_1_comparacao_frequencias()
    print("Gerando figura 2 (densidade militar ao longo dos textos)")
    figura_2_densidade_militar()
    print("Gerando figura 3 (rede de cocorrência em SIA)")
    figura_3_rede_cocorrencia()
    print(f"Gráficos salvos em {OUT_DIR}")

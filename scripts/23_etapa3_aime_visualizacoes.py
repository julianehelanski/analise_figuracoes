"""Visualizacoes adicionais para AIME (Etapa 3).

AIME tem dois kwic.csv (catalogo_antigo, catalogo_aime), entao o
04_visualizations.py nao se aplica diretamente. Este script combina
os dois e gera:

- outputs/latour_2013_aime_en/figuras/frequencia_grupos.png e .svg:
  barras horizontais com os 26 campos com ocorrencias > 0, coloridos
  por proveniencia (catalogo antigo vs catalogo novo de AIME).
- outputs/latour_2013_aime_en/figuras/densidade_ao_longo_do_texto.png
  e .svg: histograma empilhado da posicao relativa, restrito aos 12
  campos mais densos para legibilidade.
- outputs/latour_2013_aime_en/figuras/densidade_ao_longo_do_texto_todos.png
  e .svg: versao completa com todos os 26 campos (mais poluida, para
  auditoria).

Uso:
    python scripts/23_etapa3_aime_visualizacoes.py
"""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO_ROOT = Path(__file__).resolve().parents[1]
OBRA = "latour_2013_aime_en"
CSV_DIR = REPO_ROOT / "outputs" / OBRA / "csv"
FIG_DIR = REPO_ROOT / "outputs" / OBRA / "figuras"
TXT = REPO_ROOT / "corpus" / "txt_norm" / f"{OBRA}.txt"

GRUPOS_ANTIGOS = {
    "inscription", "immutable_mobile", "black_box", "centre_of_calculation",
    "actor_network", "translation", "trial_of_strength", "factish",
    "circulating_reference", "articulation", "construction", "proposition",
    "network", "agonistic", "enrollment", "spokesperson", "militar",
    "textil", "topologia",
}


def carregar_kwic(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as f:
        return [row for row in csv.DictReader(f)
                if row.get("descartado_por_exclusao", "0") == "0"]


def main() -> None:
    ocs_antigo = carregar_kwic(CSV_DIR / "kwic_catalogo_antigo.csv")
    ocs_aime = carregar_kwic(CSV_DIR / "kwic_catalogo_aime.csv")
    ocs = ocs_antigo + ocs_aime
    print(f"Total de ocorrencias validas: {len(ocs)} "
          f"(antigo={len(ocs_antigo)}, novo={len(ocs_aime)})")
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    # === Barras horizontais por grupo ===
    contagem: dict[str, int] = defaultdict(int)
    for row in ocs:
        contagem[row["grupo"]] += 1
    grupos = sorted(contagem, key=contagem.get)  # ascendente, le do topo
    valores = [contagem[g] for g in grupos]
    cores = [
        "#4c72b0" if g in GRUPOS_ANTIGOS else "#dd8452"  # azul antigo, laranja novo
        for g in grupos
    ]

    fig, ax = plt.subplots(figsize=(9, max(4, 0.35 * len(grupos))))
    barras = ax.barh(grupos, valores, color=cores)
    ax.set_xlabel("Ocorrências válidas (após exclusões)")
    ax.set_title("Frequência dos grupos figurativos em AIME (Latour 2013)\n"
                 "Azul: catálogo das Etapas 1 e 2 (19 campos). "
                 "Laranja: catálogo novo da Etapa 3 (12 campos).",
                 fontsize=10)
    for i, v in enumerate(valores):
        ax.text(v, i, f" {v}", va="center", fontsize=8)
    # Legenda manual
    from matplotlib.patches import Patch
    legenda = [
        Patch(facecolor="#4c72b0", label="catálogo antigo (Etapas 1-2)"),
        Patch(facecolor="#dd8452", label="catálogo novo (Etapa 3)"),
    ]
    ax.legend(handles=legenda, loc="lower right", fontsize=9)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "frequencia_grupos.png", dpi=300)
    fig.savefig(FIG_DIR / "frequencia_grupos.svg")
    plt.close(fig)
    print(f"  gravado: {FIG_DIR.relative_to(REPO_ROOT)}/frequencia_grupos.png")

    # === Densidade ao longo do texto ===
    if not TXT.exists():
        print(f"AVISO: {TXT} nao existe; pulando densidade.")
        return
    n_chars = TXT.stat().st_size
    posicoes_por_grupo: dict[str, list[float]] = defaultdict(list)
    for row in ocs:
        try:
            posicoes_por_grupo[row["grupo"]].append(
                int(row["posicao_no_texto"]) / n_chars
            )
        except (ValueError, KeyError):
            continue

    # Versao top-12 (legivel)
    top12 = sorted(contagem.items(), key=lambda x: -x[1])[:12]
    rotulos_top = [g for g, _ in top12]
    dados_top = [posicoes_por_grupo[g] for g in rotulos_top]
    # Paleta tab20 para distinguir 12 grupos
    cores_top = plt.cm.tab20([i / 11 for i in range(12)])

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.hist(dados_top, bins=30, stacked=True, color=cores_top,
            label=rotulos_top, edgecolor="white", linewidth=0.3)
    ax.set_xlabel("Posição relativa no texto (0 = início, 1 = fim)")
    ax.set_ylabel("Ocorrências")
    ax.set_title("Densidade dos 12 campos figurativos mais frequentes ao longo "
                 "de AIME (Latour 2013)", fontsize=10)
    ax.legend(loc="upper right", fontsize=8, ncol=2)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "densidade_ao_longo_do_texto.png", dpi=300)
    fig.savefig(FIG_DIR / "densidade_ao_longo_do_texto.svg")
    plt.close(fig)
    print(f"  gravado: {FIG_DIR.relative_to(REPO_ROOT)}/densidade_ao_longo_do_texto.png")

    # Versao com todos os 26 grupos (mais poluida)
    rotulos_todos = sorted(posicoes_por_grupo, key=lambda g: -contagem[g])
    dados_todos = [posicoes_por_grupo[g] for g in rotulos_todos]
    cores_todos = plt.cm.tab20(
        [i / max(1, len(rotulos_todos) - 1) for i in range(len(rotulos_todos))]
    )
    fig, ax = plt.subplots(figsize=(13, 5.5))
    ax.hist(dados_todos, bins=30, stacked=True, color=cores_todos,
            label=rotulos_todos, edgecolor="white", linewidth=0.2)
    ax.set_xlabel("Posição relativa no texto (0 = início, 1 = fim)")
    ax.set_ylabel("Ocorrências")
    ax.set_title("Densidade dos 26 campos figurativos com ocorrências ao longo "
                 "de AIME (Latour 2013), todos os campos",
                 fontsize=10)
    ax.legend(loc="upper right", fontsize=7, ncol=3)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "densidade_ao_longo_do_texto_todos.png", dpi=300)
    fig.savefig(FIG_DIR / "densidade_ao_longo_do_texto_todos.svg")
    plt.close(fig)
    print(f"  gravado: {FIG_DIR.relative_to(REPO_ROOT)}/densidade_ao_longo_do_texto_todos.png")

    # Resumo
    print()
    print("Top 12 campos:")
    for g, n in top12:
        prov = "antigo" if g in GRUPOS_ANTIGOS else "novo"
        print(f"  {g:30s} {n:5d}  [{prov}]")


if __name__ == "__main__":
    main()

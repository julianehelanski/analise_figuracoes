"""Visualizações de frequência e densidade por obra.

Lê `outputs/<obra_id>/csv/{kwic,frequencias}.csv` e produz:

- `outputs/<obra_id>/figuras/frequencia_grupos.png`: barras horizontais com
  frequência por grupo (ocorrências válidas).
- `outputs/<obra_id>/figuras/densidade_ao_longo_do_texto.png`: histograma da
  posição relativa (0-1) das ocorrências válidas ao longo do texto, empilhado
  por grupo.

Paleta acessível (sem vermelho/verde puros). PNG a 300 dpi.

Uso:
    python scripts/04_visualizations.py
    python scripts/04_visualizations.py --only latour_1987
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
METADATA_CSV = REPO_ROOT / "corpus" / "metadata.csv"
OUTPUTS_DIR = REPO_ROOT / "outputs"
CORPUS_TXT_DIR = REPO_ROOT / "corpus" / "txt_norm"


def obras_em_escopo() -> list[dict[str, str]]:
    with METADATA_CSV.open(encoding="utf-8", newline="") as f:
        return [
            row for row in csv.DictReader(f)
            if row.get("escopo_etapa1", "").strip().lower() == "sim"
        ]


def carregar_kwic(obra_id: str) -> list[dict[str, str]]:
    p = OUTPUTS_DIR / obra_id / "csv" / "kwic.csv"
    if not p.exists():
        return []
    with p.open(encoding="utf-8", newline="") as f:
        return [row for row in csv.DictReader(f)
                if row.get("descartado_por_exclusao", "0") == "0"]


def gerar_figuras(obra_id: str) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("  ERRO: matplotlib não está instalado.")
        return

    ocs = carregar_kwic(obra_id)
    if not ocs:
        print(f"  [pular] sem ocorrências em outputs/{obra_id}/csv/kwic.csv.")
        return

    fig_dir = OUTPUTS_DIR / obra_id / "figuras"
    fig_dir.mkdir(parents=True, exist_ok=True)

    # Barras horizontais ----------------------------------------------------
    contagem: dict[str, int] = defaultdict(int)
    for row in ocs:
        contagem[row["grupo"]] += 1
    grupos = sorted(contagem, key=contagem.get)  # ascendente para ler do topo
    valores = [contagem[g] for g in grupos]
    cores = plt.cm.viridis([i / max(1, len(grupos) - 1) for i in range(len(grupos))])

    fig, ax = plt.subplots(figsize=(8, max(3, 0.35 * len(grupos))))
    ax.barh(grupos, valores, color=cores)
    ax.set_xlabel("Ocorrências válidas (após exclusões)")
    for i, v in enumerate(valores):
        ax.text(v, i, f" {v}", va="center", fontsize=8)
    fig.tight_layout()
    fig.savefig(fig_dir / "frequencia_grupos.png", dpi=300)
    fig.savefig(fig_dir / "frequencia_grupos.svg")
    plt.close(fig)

    # Densidade ao longo do texto ------------------------------------------
    txt = CORPUS_TXT_DIR / f"{obra_id}.txt"
    if not txt.exists():
        return
    n_chars = txt.stat().st_size
    if n_chars == 0:
        return
    posicoes_por_grupo: dict[str, list[float]] = defaultdict(list)
    for row in ocs:
        try:
            posicoes_por_grupo[row["grupo"]].append(int(row["posicao_no_texto"]) / n_chars)
        except (ValueError, KeyError):
            continue
    if not posicoes_por_grupo:
        return

    fig, ax = plt.subplots(figsize=(10, 4))
    bins = 20
    dados = [posicoes_por_grupo[g] for g in sorted(posicoes_por_grupo)]
    rotulos = sorted(posicoes_por_grupo)
    cores = plt.cm.viridis([i / max(1, len(rotulos) - 1) for i in range(len(rotulos))])
    ax.hist(dados, bins=bins, stacked=True, color=cores, label=rotulos, edgecolor="white")
    ax.set_xlabel("Posição relativa no texto (0 = início, 1 = fim)")
    ax.set_ylabel("Ocorrências")
    ax.legend(loc="upper right", fontsize=7, ncol=2)
    fig.tight_layout()
    fig.savefig(fig_dir / "densidade_ao_longo_do_texto.png", dpi=300)
    fig.savefig(fig_dir / "densidade_ao_longo_do_texto.svg")
    plt.close(fig)

    print(f"  gravado: outputs/{obra_id}/figuras/frequencia_grupos.png")
    print(f"  gravado: outputs/{obra_id}/figuras/densidade_ao_longo_do_texto.png")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--only", help="filtra obras por substring de id.")
    args = parser.parse_args()

    obras = obras_em_escopo()
    if args.only:
        obras = [o for o in obras if args.only.lower() in o["id"].lower()]
    for obra in obras:
        print(f"\n[{obra['id']}]")
        gerar_figuras(obra["id"])


if __name__ == "__main__":
    main()

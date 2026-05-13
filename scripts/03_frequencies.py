"""Tabelas e relatórios de frequência por obra (Etapa 1).

Lê `outputs/<obra_id>/csv/kwic.csv` e `corpus/qualidade_extracao.csv` e produz:

- `outputs/<obra_id>/csv/frequencias.csv`: contagem por grupo, com frequência
  absoluta e relativa (ocorrências por 10 000 palavras).
- `outputs/<obra_id>/relatorios/frequencias.md`: relatório descritivo com
  ranking de grupos, exclusões aplicadas e exemplos da janela KWIC.

Ocorrências marcadas como `descartado_por_exclusao=1` no kwic.csv são
excluídas das frequências (contabilizadas separadamente como "excluídas").

Uso:
    python scripts/03_frequencies.py
    python scripts/03_frequencies.py --only latour_1987
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
METADATA_CSV = REPO_ROOT / "corpus" / "metadata.csv"
QUALIDADE_CSV = REPO_ROOT / "corpus" / "qualidade_extracao.csv"
OUTPUTS_DIR = REPO_ROOT / "outputs"


def obras_em_escopo() -> list[dict[str, str]]:
    with METADATA_CSV.open(encoding="utf-8", newline="") as f:
        return [
            row for row in csv.DictReader(f)
            if row.get("escopo_etapa1", "").strip().lower() == "sim"
        ]


def carregar_palavras_total(obra_id: str) -> int | None:
    if not QUALIDADE_CSV.exists():
        return None
    with QUALIDADE_CSV.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row["id"] == obra_id:
                try:
                    return int(row["palavras_total"])
                except (KeyError, ValueError):
                    return None
    return None


def construir_frequencias(obra_id: str) -> None:
    kwic_path = OUTPUTS_DIR / obra_id / "csv" / "kwic.csv"
    if not kwic_path.exists():
        print(f"  [pular] {kwic_path} não existe; rode scripts/02_kwic.py.")
        return

    palavras_total = carregar_palavras_total(obra_id)
    contagem: Counter[str] = Counter()
    excluidas: Counter[str] = Counter()
    variantes_por_grupo: dict[str, Counter[str]] = defaultdict(Counter)
    exemplos: dict[str, list[dict[str, str]]] = defaultdict(list)

    with kwic_path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            grupo = row["grupo"]
            if row.get("descartado_por_exclusao", "0") == "1":
                excluidas[grupo] += 1
                continue
            contagem[grupo] += 1
            variantes_por_grupo[grupo][row["termo_encontrado"].lower()] += 1
            if len(exemplos[grupo]) < 3:
                exemplos[grupo].append({
                    "pagina": row.get("pagina", ""),
                    "antes": row.get("contexto_antes", ""),
                    "central": row.get("trecho_central", ""),
                    "depois": row.get("contexto_depois", ""),
                })

    # CSV de frequências --------------------------------------------------- #
    csv_saida = OUTPUTS_DIR / obra_id / "csv" / "frequencias.csv"
    csv_saida.parent.mkdir(parents=True, exist_ok=True)
    with csv_saida.open("w", encoding="utf-8", newline="") as f:
        cab = [
            "grupo", "n_ocorrencias", "n_excluidas",
            "frequencia_por_10k_palavras", "variantes_top",
        ]
        escritor = csv.DictWriter(f, fieldnames=cab)
        escritor.writeheader()
        for grupo, n in sorted(contagem.items(), key=lambda x: -x[1]):
            freq = (n / palavras_total * 10000) if palavras_total else None
            var_top = ", ".join(
                f"{v}({k})" for v, k in variantes_por_grupo[grupo].most_common(4)
            )
            escritor.writerow({
                "grupo": grupo,
                "n_ocorrencias": n,
                "n_excluidas": excluidas[grupo],
                "frequencia_por_10k_palavras": f"{freq:.2f}" if freq is not None else "",
                "variantes_top": var_top,
            })
        # Grupos com zero ocorrências também ficam registrados.
        for grupo, n in excluidas.items():
            if grupo not in contagem:
                escritor.writerow({
                    "grupo": grupo,
                    "n_ocorrencias": 0,
                    "n_excluidas": n,
                    "frequencia_por_10k_palavras": "0.00" if palavras_total else "",
                    "variantes_top": "",
                })

    # Markdown ------------------------------------------------------------- #
    md_saida = OUTPUTS_DIR / obra_id / "relatorios" / "frequencias.md"
    md_saida.parent.mkdir(parents=True, exist_ok=True)
    linhas: list[str] = [
        f"# Frequências preliminares: {obra_id}",
        "",
        f"Palavras totais (extração): **{palavras_total or 'n/d'}**.",
        f"Janela KWIC: ±10 palavras. Catálogo: `campos_lexicais/catalogo_termos.yaml`.",
        "",
        "## Ranking de grupos figurativos",
        "",
        "| grupo | n | excluídas | freq./10k pal | variantes top |",
        "|---|---:|---:|---:|---|",
    ]
    todos_grupos = set(contagem) | set(excluidas)
    for grupo in sorted(todos_grupos, key=lambda g: -contagem[g]):
        n = contagem.get(grupo, 0)
        e = excluidas.get(grupo, 0)
        freq = (n / palavras_total * 10000) if palavras_total else None
        freq_s = f"{freq:.2f}" if freq is not None else "n/d"
        var = ", ".join(
            f"`{v}` ({k})" for v, k in variantes_por_grupo[grupo].most_common(4)
        )
        linhas.append(f"| {grupo} | {n} | {e} | {freq_s} | {var} |")

    linhas += [
        "",
        "## Exemplos por grupo (top 3 ocorrências)",
        "",
    ]
    for grupo in sorted(contagem, key=lambda g: -contagem[g]):
        linhas.append(f"### `{grupo}` (n={contagem[grupo]})")
        linhas.append("")
        for ex in exemplos[grupo]:
            trecho = f"{ex['antes']} **{ex['central']}** {ex['depois']}"
            linhas.append(f"- p. ~{ex['pagina']}: {trecho.strip()}")
        linhas.append("")

    md_saida.write_text("\n".join(linhas), encoding="utf-8")
    try:
        rotulo_csv = csv_saida.relative_to(REPO_ROOT)
        rotulo_md = md_saida.relative_to(REPO_ROOT)
    except ValueError:
        rotulo_csv, rotulo_md = csv_saida, md_saida
    print(f"  gravado: {rotulo_csv}")
    print(f"  gravado: {rotulo_md}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--only", help="filtra obras por substring de id.")
    args = parser.parse_args()

    obras = obras_em_escopo()
    if args.only:
        obras = [o for o in obras if args.only.lower() in o["id"].lower()]
    for obra in obras:
        print(f"\n[{obra['id']}]")
        construir_frequencias(obra["id"])


if __name__ == "__main__":
    main()

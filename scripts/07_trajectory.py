"""Relatório de trajetória consolidada Latour 1986-1999.

Lê as três obras em escopo da Etapa 1 e produz
`outputs/trajetoria_latour_1986_1999.md`, organizado em torno das três
perguntas da seção 6 de `docs/decisoes_metodologicas.md`:

1. Quais figurações aparecem em todas as três obras? Com que frequência relativa?
2. Quais figurações são introduzidas em uma obra e desaparecem ou persistem
   nas seguintes?
3. Como o vocabulário coautoral de Laboratory Life (Latour-Woolgar) se
   relaciona com o vocabulário das obras posteriores de Latour solo?

Também grava `outputs/trajetoria_latour_1986_1999.csv` com a matriz
grupos × obras (ocorrências válidas e frequência por 10 000 palavras).

Uso:
    python scripts/07_trajectory.py
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
METADATA_CSV = REPO_ROOT / "corpus" / "metadata.csv"
QUALIDADE_CSV = REPO_ROOT / "corpus" / "qualidade_extracao.csv"
OUTPUTS_DIR = REPO_ROOT / "outputs"

# Ordem cronológica esperada da Etapa 1.
ORDEM_OBRAS = (
    "latour_woolgar_1986_lab_life_en",
    "latour_1987_science_action_en",
    "latour_1999_pandora_en",
)


def obras_em_escopo() -> list[dict[str, str]]:
    with METADATA_CSV.open(encoding="utf-8", newline="") as f:
        rows = [row for row in csv.DictReader(f)
                if row.get("escopo_etapa1", "").strip().lower() == "sim"]
    # Ordena pela ORDEM_OBRAS se possível.
    ordem = {oid: i for i, oid in enumerate(ORDEM_OBRAS)}
    return sorted(rows, key=lambda r: ordem.get(r["id"], 999))


def palavras_totais(obra_id: str) -> int | None:
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


def carregar_contagens(obra_id: str) -> dict[str, int]:
    p = OUTPUTS_DIR / obra_id / "csv" / "kwic.csv"
    contagem: dict[str, int] = defaultdict(int)
    if not p.exists():
        return contagem
    with p.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row.get("descartado_por_exclusao", "0") != "0":
                continue
            contagem[row["grupo"]] += 1
    return contagem


def main() -> None:
    obras = obras_em_escopo()
    if len(obras) < 2:
        raise SystemExit(
            "Trajetória exige pelo menos duas obras em escopo; encontrei "
            f"{len(obras)}."
        )

    ids = [o["id"] for o in obras]
    palavras = {oid: palavras_totais(oid) for oid in ids}
    contagens = {oid: carregar_contagens(oid) for oid in ids}
    grupos = sorted({g for c in contagens.values() for g in c})

    # CSV matricial -------------------------------------------------------- #
    csv_path = OUTPUTS_DIR / "trajetoria_latour_1986_1999.csv"
    cabecalho = ["grupo"]
    for oid in ids:
        cabecalho += [f"{oid}__n", f"{oid}__freq_10k"]
    cabecalho += ["aparece_em_n_obras", "perfil"]
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        escritor = csv.writer(f)
        escritor.writerow(cabecalho)
        for grupo in grupos:
            linha: list[object] = [grupo]
            n_obras_com_grupo = 0
            ns = []
            for oid in ids:
                n = contagens[oid].get(grupo, 0)
                ns.append(n)
                if n > 0:
                    n_obras_com_grupo += 1
                pt = palavras.get(oid)
                freq = (n / pt * 10000) if pt else None
                linha += [n, f"{freq:.2f}" if freq is not None else ""]
            perfil = classificar_perfil(ns)
            linha += [n_obras_com_grupo, perfil]
            escritor.writerow(linha)

    # Markdown ------------------------------------------------------------- #
    md_path = OUTPUTS_DIR / "trajetoria_latour_1986_1999.md"
    md: list[str] = [
        "# Trajetória conceitual de Bruno Latour, 1986-1999",
        "",
        "Consolidação da Etapa 1, conforme `docs/decisoes_metodologicas.md` "
        "seção 6. Lê as três obras em escopo:",
        "",
    ]
    for oid in ids:
        pt = palavras[oid]
        md.append(f"- `{oid}`  ({pt or 'n/d'} palavras)")
    md += [
        "",
        "## Matriz grupo × obra (frequência por 10 000 palavras)",
        "",
        "| grupo | " + " | ".join(ids) + " | obras |",
        "|" + "---|" * (len(ids) + 2),
    ]
    for grupo in grupos:
        celulas = []
        n_obras_com = 0
        for oid in ids:
            n = contagens[oid].get(grupo, 0)
            pt = palavras.get(oid)
            freq = (n / pt * 10000) if pt else None
            celulas.append(f"{freq:.2f} ({n})" if freq is not None else f"{n}")
            if n > 0:
                n_obras_com += 1
        md.append(f"| {grupo} | " + " | ".join(celulas) + f" | {n_obras_com}/3 |")

    # Pergunta 1
    md += ["", "## 1. Figurações presentes em todas as três obras", ""]
    persistentes = [g for g in grupos if all(contagens[oid].get(g, 0) > 0 for oid in ids)]
    if persistentes:
        for g in persistentes:
            freqs = []
            for oid in ids:
                n = contagens[oid].get(g, 0)
                pt = palavras.get(oid)
                freqs.append(f"{oid}: {n} ({n / pt * 10000:.2f}/10k)" if pt else f"{oid}: {n}")
            md.append(f"- **{g}**: " + "; ".join(freqs))
    else:
        md.append("(nenhum grupo aparece em todas as três obras com >0 ocorrências válidas)")

    # Pergunta 2
    md += ["", "## 2. Figurações introduzidas em uma obra", ""]
    for oid in ids:
        introduzidas_aqui = []
        for g in grupos:
            n_aqui = contagens[oid].get(g, 0)
            anteriores = [contagens[o].get(g, 0) for o in ids[:ids.index(oid)]]
            if n_aqui > 0 and all(n == 0 for n in anteriores) and ids.index(oid) > 0:
                introduzidas_aqui.append((g, n_aqui))
        if introduzidas_aqui:
            md.append(f"**Em `{oid}`:**")
            for g, n in sorted(introduzidas_aqui, key=lambda x: -x[1]):
                md.append(f"- `{g}` (n={n})")
            md.append("")

    # Pergunta 3
    md += ["", "## 3. Vocabulário coautoral vs. solo", ""]
    if len(ids) >= 2:
        coautoral_id = ids[0]
        solo_ids = ids[1:]
        c_coa = contagens[coautoral_id]
        groupos_so_coautoral = []
        groupos_so_solo = []
        for g in grupos:
            n_coa = c_coa.get(g, 0)
            n_solo_total = sum(contagens[o].get(g, 0) for o in solo_ids)
            if n_coa > 0 and n_solo_total == 0:
                groupos_so_coautoral.append((g, n_coa))
            elif n_coa == 0 and n_solo_total > 0:
                groupos_so_solo.append((g, n_solo_total))
        md.append(f"**Apenas em `{coautoral_id}` (coautoral, ausente em Latour solo):**")
        for g, n in sorted(groupos_so_coautoral, key=lambda x: -x[1]) or [("(nenhum)", 0)]:
            md.append(f"- `{g}` (n={n})")
        md.append("")
        md.append(f"**Ausente em `{coautoral_id}`, presente nas obras solo:**")
        for g, n in sorted(groupos_so_solo, key=lambda x: -x[1]) or [("(nenhum)", 0)]:
            md.append(f"- `{g}` (n={n})")
        md.append("")

    md_path.write_text("\n".join(md), encoding="utf-8")
    print(f"gravado: {csv_path.relative_to(REPO_ROOT)}")
    print(f"gravado: {md_path.relative_to(REPO_ROOT)}")


def classificar_perfil(ns: list[int]) -> str:
    """Classifica trajetória do grupo ao longo das obras."""
    if all(n == 0 for n in ns):
        return "ausente"
    if all(n > 0 for n in ns):
        return "persistente"
    if ns[0] > 0 and all(n == 0 for n in ns[1:]):
        return "apenas_inicial"
    if ns[-1] > 0 and all(n == 0 for n in ns[:-1]):
        return "introduzido_no_fim"
    nonzero = [i for i, n in enumerate(ns) if n > 0]
    if nonzero and nonzero[0] > 0 and all(n > 0 for n in ns[nonzero[0]:]):
        return "introduzido_e_persiste"
    return "intermitente"


if __name__ == "__main__":
    main()

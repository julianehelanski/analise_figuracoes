"""Resumo de frequências e passagens densas para a Etapa 1.

Lê todos os CSVs gerados por `02_kwic.py` em `outputs/csv/etapa1/` e produz
o relatório `outputs/relatorios/etapa1_resumo.md` com:

- Total de ocorrências por termo, por par obra × campo.
- As 3 passagens com maior densidade lexical (concentração de termos do
  campo na mesma janela) por par.
- Indicadores de qualidade: termos com zero ocorrências e termos com
  mais de 100 ocorrências (suspeita de ruído alto).

Uso:
    python scripts/03_frequencies.py
    python scripts/03_frequencies.py --apenas haraway_2016_textil
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = REPO_ROOT / "outputs" / "csv" / "etapa1"
RELATORIO = REPO_ROOT / "outputs" / "relatorios" / "etapa1_resumo.md"

# Janela em caracteres para cálculo de densidade lexical entre ocorrências.
JANELA_DENSIDADE = 1000


@dataclass
class Ocorrencia:
    obra: str
    campo: str
    termo_buscado: str
    termo_encontrado: str
    pagina: str
    posicao: int
    nota: bool
    antes: str
    central: str
    depois: str


def carregar_csv(caminho: Path) -> list[Ocorrencia]:
    ocs: list[Ocorrencia] = []
    with caminho.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            try:
                pos = int(row["posicao_no_texto"])
            except (KeyError, ValueError):
                continue
            ocs.append(Ocorrencia(
                obra=row.get("obra", ""),
                campo=row.get("campo_lexical", ""),
                termo_buscado=row.get("termo_buscado", ""),
                termo_encontrado=row.get("termo_encontrado", ""),
                pagina=row.get("pagina_aproximada", ""),
                posicao=pos,
                nota=row.get("provavel_nota_rodape", "0") == "1",
                antes=row.get("contexto_antes", ""),
                central=row.get("trecho_central", ""),
                depois=row.get("contexto_depois", ""),
            ))
    return ocs


def passagens_densas(
    ocs: list[Ocorrencia], janela: int = JANELA_DENSIDADE, top: int = 3
) -> list[tuple[int, list[Ocorrencia]]]:
    """Encontra agrupamentos com mais ocorrências em janela móvel de caracteres.

    Retorna lista de tuplas (densidade, ocorrências_no_cluster), ordenada de
    densidade decrescente, com no máximo `top` clusters disjuntos.
    """
    if not ocs:
        return []
    ordenadas = sorted(ocs, key=lambda o: o.posicao)
    clusters: list[tuple[int, list[Ocorrencia]]] = []
    n = len(ordenadas)
    for i, oc in enumerate(ordenadas):
        cluster = [oc]
        for j in range(i + 1, n):
            if ordenadas[j].posicao - oc.posicao <= janela:
                cluster.append(ordenadas[j])
            else:
                break
        clusters.append((len(cluster), cluster))

    selecionados: list[tuple[int, list[Ocorrencia]]] = []
    usados: set[int] = set()
    for densidade, cluster in sorted(clusters, key=lambda x: -x[0]):
        ids_cluster = {oc.posicao for oc in cluster}
        if ids_cluster & usados:
            continue
        selecionados.append((densidade, cluster))
        usados |= ids_cluster
        if len(selecionados) >= top:
            break
    return selecionados


def montar_relatorio(par_csv: dict[str, list[Ocorrencia]]) -> str:
    """Monta o markdown do relatório-resumo."""
    linhas: list[str] = [
        "# Etapa 1: resumo de frequências e densidade",
        "",
        "Gerado por `scripts/03_frequencies.py` sobre os CSVs de "
        "`outputs/csv/etapa1/`. Cada par obra × campo gera uma seção.",
        "",
        "Convenções:",
        "",
        "- `n` indica ocorrências brutas, incluindo possíveis falsos positivos.",
        "- A coluna `provavel_nota_rodape` no CSV é heurística; o resumo "
        "abaixo conta todas as ocorrências e reporta separadamente a fração "
        "marcada como provável nota.",
        "- \"Densidade\" indica número de ocorrências encontradas dentro de "
        f"uma janela de {JANELA_DENSIDADE} caracteres (cerca de 150-200 palavras).",
        "",
    ]

    for nome_csv, ocs in sorted(par_csv.items()):
        if not ocs:
            linhas.append(f"## {nome_csv}\n\nNenhuma ocorrência registrada.\n")
            continue
        obras = sorted({o.obra for o in ocs})
        campos = sorted({o.campo for o in ocs})
        n_total = len(ocs)
        n_nota = sum(1 for o in ocs if o.nota)

        linhas += [
            f"## {nome_csv}",
            "",
            f"- Obra(s): {', '.join(obras)}",
            f"- Campo(s): {', '.join(campos)}",
            f"- Total de ocorrências: **{n_total}**",
            f"- Marcadas como provável nota de rodapé: {n_nota} "
            f"({n_nota / n_total:.1%})",
            "",
            "### Frequência por termo canônico",
            "",
            "| termo_buscado | n | exemplos de variantes encontradas |",
            "|---|---:|---|",
        ]
        por_termo: dict[str, list[Ocorrencia]] = defaultdict(list)
        for oc in ocs:
            por_termo[oc.termo_buscado].append(oc)
        for termo, lista in sorted(por_termo.items(), key=lambda x: -len(x[1])):
            variantes = Counter(o.termo_encontrado.lower() for o in lista)
            exemplos = ", ".join(f"{v} ({n})" for v, n in variantes.most_common(4))
            linhas.append(f"| {termo} | {len(lista)} | {exemplos} |")

        # Termos vistos com n > 100 entram como suspeita de ruído alto.
        # Termos com zero ocorrências exigiriam carregar o campo lexical
        # original; reporto apenas o que aparece no CSV.
        ruidosos = [t for t, lista in por_termo.items() if len(lista) > 100]
        if ruidosos:
            linhas += [
                "",
                "**Termos com mais de 100 ocorrências (suspeita de ruído alto, "
                "verificar contexto na Etapa 2):** "
                + ", ".join(f"`{t}`" for t in ruidosos),
            ]

        linhas += [
            "",
            "### Top 3 passagens mais densas",
            "",
        ]
        for i, (densidade, cluster) in enumerate(passagens_densas(ocs), start=1):
            primeira = cluster[0]
            termos_no_cluster = Counter(o.termo_buscado for o in cluster)
            resumo_termos = ", ".join(
                f"{t} ({n})" for t, n in termos_no_cluster.most_common()
            )
            paginas = sorted({o.pagina for o in cluster if o.pagina})
            faixa_paginas = (
                f" págs. ~{paginas[0]}-{paginas[-1]}" if paginas else ""
            )
            trecho = " ".join([primeira.antes, primeira.central, primeira.depois])
            trecho = trecho[:500].strip() + ("..." if len(trecho) > 500 else "")
            linhas += [
                f"**{i}. Densidade {densidade} ocorrências "
                f"em ~{JANELA_DENSIDADE} caracteres{faixa_paginas}**",
                "",
                f"Termos: {resumo_termos}.",
                "",
                f"> {trecho}",
                "",
            ]

    return "\n".join(linhas)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--apenas",
        help="filtra CSVs cujo nome (sem extensão) contenha esta substring.",
    )
    args = parser.parse_args()

    if not CSV_DIR.exists():
        raise SystemExit(
            f"ERRO: {CSV_DIR} não existe. Rode antes scripts/02_kwic.py."
        )
    csvs = sorted(CSV_DIR.glob("*.csv"))
    if args.apenas:
        csvs = [c for c in csvs if args.apenas.lower() in c.stem.lower()]
    if not csvs:
        raise SystemExit("Nenhum CSV encontrado para resumir.")

    par_csv = {c.stem: carregar_csv(c) for c in csvs}
    RELATORIO.parent.mkdir(parents=True, exist_ok=True)
    RELATORIO.write_text(montar_relatorio(par_csv), encoding="utf-8")
    print(f"Relatório gravado em {RELATORIO.relative_to(REPO_ROOT)}")
    for nome, ocs in par_csv.items():
        print(f"  {nome}: {len(ocs)} ocorrências")


if __name__ == "__main__":
    main()

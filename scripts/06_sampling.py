"""Amostra estratificada de 45 páginas para validação amostral da Etapa 2.

Conforme `docs/decisoes_metodologicas.md`, seção 5: 15 páginas por obra
(45 no total para as três obras), distribuídas em cinco estratos de 3
páginas cada:

    - inicio_capitulo
    - corpo
    - notas_fim
    - paratexto
    - qualidade_baixa

Seed fixa = 42.

Outputs por obra:
- `outputs/<obra_id>/csv/amostra_validacao.csv`
- `outputs/<obra_id>/relatorios/validacao_amostral_etapa1.md`

Output consolidado:
- `outputs/amostra_validacao_etapa1.csv` (45 linhas, com coluna `obra`).

Cada linha do CSV traz o id da obra, número da página, estrato, classe
predita pelo algoritmo, e três trechos da página (início, meio, fim).
Colunas em branco aguardam a codificação manual da Juliane:

    estrato_correto (sim/nao/parcial)
    classe_correta (sim/nao/parcial)
    erro_extracao (descreva)
    decisao_metodologica (descreva)

Uso:
    python scripts/06_sampling.py
"""

from __future__ import annotations

import argparse
import csv
import random
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
METADATA_CSV = REPO_ROOT / "corpus" / "metadata.csv"
PAGINAS_DIR = REPO_ROOT / "corpus" / "paginas"
CORPUS_TXT_DIR = REPO_ROOT / "corpus" / "txt"
OUTPUTS_DIR = REPO_ROOT / "outputs"

ESTRATOS = ("inicio_capitulo", "corpo", "notas_fim", "paratexto", "qualidade_baixa")
N_POR_ESTRATO = 3
SEED = 42


def obras_em_escopo() -> list[dict[str, str]]:
    with METADATA_CSV.open(encoding="utf-8", newline="") as f:
        return [row for row in csv.DictReader(f)
                if row.get("escopo_etapa1", "").strip().lower() == "sim"]


def carregar_paginas(obra_id: str) -> list[dict[str, str]]:
    p = PAGINAS_DIR / f"{obra_id}.csv"
    if not p.exists():
        return []
    with p.open(encoding="utf-8", newline="") as f:
        return [row for row in csv.DictReader(f)]


def ler_paginas_texto(obra_id: str) -> list[str]:
    p = CORPUS_TXT_DIR / f"{obra_id}.txt"
    if not p.exists():
        return []
    return p.read_text(encoding="utf-8", errors="replace").split("\f")


def trecho(s: str, n_chars: int = 280) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    return s[:n_chars] + ("..." if len(s) > n_chars else "")


def amostrar_obra(
    obra_id: str, paginas_meta: list[dict[str, str]], paginas_texto: list[str],
    rng: random.Random,
) -> list[dict[str, str]]:
    saida: list[dict[str, str]] = []
    avisos: list[str] = []
    for estrato in ESTRATOS:
        candidatas = [p for p in paginas_meta if p["classe"] == estrato]
        if len(candidatas) < N_POR_ESTRATO:
            avisos.append(
                f"  AVISO: apenas {len(candidatas)} página(s) no estrato "
                f"'{estrato}' (esperado {N_POR_ESTRATO}); amostra incompleta."
            )
            selecionadas = candidatas
        else:
            selecionadas = rng.sample(candidatas, N_POR_ESTRATO)
        for p in selecionadas:
            num_pag = int(p["pagina"])
            texto_pag = paginas_texto[num_pag - 1] if num_pag - 1 < len(paginas_texto) else ""
            saida.append({
                "obra": obra_id,
                "pagina": p["pagina"],
                "estrato": estrato,
                "classe_predita": p["classe"],
                "qualidade_predita": p["qualidade_pagina"],
                "n_palavras_pagina": p["n_palavras"],
                "trecho_inicio": trecho(texto_pag[:600]),
                "trecho_meio": trecho(texto_pag[len(texto_pag) // 2 - 300: len(texto_pag) // 2 + 300]),
                "trecho_fim": trecho(texto_pag[-600:]),
                # Colunas para codificação manual:
                "estrato_correto": "",
                "classe_correta": "",
                "erro_extracao": "",
                "decisao_metodologica": "",
            })
    for a in avisos:
        print(a)
    return saida


def gravar_csv_obra(obra_id: str, linhas: list[dict[str, str]]) -> Path:
    saida = OUTPUTS_DIR / obra_id / "csv" / "amostra_validacao.csv"
    saida.parent.mkdir(parents=True, exist_ok=True)
    cabecalho = list(linhas[0].keys()) if linhas else []
    with saida.open("w", encoding="utf-8", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=cabecalho)
        escritor.writeheader()
        escritor.writerows(linhas)
    return saida


def gravar_md_obra(obra_id: str, linhas: list[dict[str, str]]) -> Path:
    saida = OUTPUTS_DIR / obra_id / "relatorios" / "validacao_amostral_etapa1.md"
    saida.parent.mkdir(parents=True, exist_ok=True)
    md: list[str] = [
        f"# Amostra estratificada de validação: {obra_id}",
        "",
        f"Seed = {SEED}. Estratos = {', '.join(ESTRATOS)}. "
        f"N por estrato = {N_POR_ESTRATO}.",
        "",
        "Use este documento como guia de leitura ao percorrer o PDF. "
        "Codifique cada página no CSV `amostra_validacao.csv`:",
        "",
        "- `estrato_correto`: o estrato atribuído pelo algoritmo é correto? (sim/nao/parcial)",
        "- `classe_correta`: a classe específica predita é correta? (sim/nao/parcial)",
        "- `erro_extracao`: caracteres corrompidos, palavras coladas, linhas misturadas?",
        "- `decisao_metodologica`: qualquer observação a registrar.",
        "",
        "Se a taxa de erro em um estrato passar de 20%, ajustar a heurística "
        "correspondente em `scripts/01_extract_text.py` e reprocessar.",
        "",
    ]
    estrato_atual = None
    for linha in linhas:
        if linha["estrato"] != estrato_atual:
            estrato_atual = linha["estrato"]
            md.append(f"## Estrato: `{estrato_atual}`")
            md.append("")
        md += [
            f"### Página {linha['pagina']}",
            "",
            f"- classe_predita: `{linha['classe_predita']}`, "
            f"qualidade_predita: `{linha['qualidade_predita']}`, "
            f"n_palavras: {linha['n_palavras_pagina']}",
            "",
            "**Início da página:**",
            "",
            f"> {linha['trecho_inicio']}",
            "",
            "**Meio:**",
            "",
            f"> {linha['trecho_meio']}",
            "",
            "**Fim:**",
            "",
            f"> {linha['trecho_fim']}",
            "",
        ]
    saida.write_text("\n".join(md), encoding="utf-8")
    return saida


def gravar_csv_consolidado(todas_linhas: list[dict[str, str]]) -> Path:
    saida = OUTPUTS_DIR / "amostra_validacao_etapa1.csv"
    saida.parent.mkdir(parents=True, exist_ok=True)
    cabecalho = list(todas_linhas[0].keys()) if todas_linhas else []
    with saida.open("w", encoding="utf-8", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=cabecalho)
        escritor.writeheader()
        escritor.writerows(todas_linhas)
    return saida


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--only", help="filtra obras por substring de id.")
    args = parser.parse_args()

    obras = obras_em_escopo()
    if args.only:
        obras = [o for o in obras if args.only.lower() in o["id"].lower()]
    rng = random.Random(SEED)

    todas: list[dict[str, str]] = []
    for obra in obras:
        obra_id = obra["id"]
        print(f"\n[{obra_id}]")
        paginas_meta = carregar_paginas(obra_id)
        if not paginas_meta:
            print(f"  ERRO: corpus/paginas/{obra_id}.csv não existe. "
                  "Rode antes scripts/01_extract_text.py.")
            continue
        paginas_texto = ler_paginas_texto(obra_id)
        linhas = amostrar_obra(obra_id, paginas_meta, paginas_texto, rng)
        csv_path = gravar_csv_obra(obra_id, linhas)
        md_path = gravar_md_obra(obra_id, linhas)
        try:
            print(f"  gravado: {csv_path.relative_to(REPO_ROOT)}")
            print(f"  gravado: {md_path.relative_to(REPO_ROOT)}")
        except ValueError:
            pass
        todas.extend(linhas)

    if todas:
        consolidado = gravar_csv_consolidado(todas)
        print(f"\nConsolidado: {consolidado.relative_to(REPO_ROOT)}  ({len(todas)} linhas)")


if __name__ == "__main__":
    main()

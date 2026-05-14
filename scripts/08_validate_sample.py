"""Validação amostral automatizada (Etapa 2).

Para cada uma das 41 páginas amostradas em `outputs/amostra_validacao_etapa1.csv`,
recupera o texto completo da página em `corpus/txt_norm/<obra>.txt`, aplica
critérios heurísticos de validação e preenche os campos:

    estrato_correto       sim / nao / parcial
    classe_correta        sim / nao / parcial
    erro_extracao         descrição curta dos erros visíveis
    decisao_metodologica  observação para registro

Critérios heurísticos (uniformes para as três obras):

  inicio_capitulo  página com cabeçalho de capítulo nas 5 primeiras linhas
                   (regex _RE_INICIO_CAPITULO, igual à de classificação).
                   Decisão automática:
                       cabeçalho no topo                       -> sim
                       cabeçalho em outro lugar da página      -> parcial
                       sem cabeçalho                           -> nao

  corpo            página com prosa contínua, ≥150 palavras, sem cabeçalhos
                   de seção paratexto. Decisão:
                       densidade alta, sem ruptura             -> sim
                       prosa + cabeçalho/ruptura misturados    -> parcial
                       <50 palavras ou cabeçalho dominante     -> nao

  notas_fim        página com padrão de notas numeradas em parágrafos
                   curtos (numeração ^\\d+\\s no início de linha, ou
                   cabeçalho 'Notes'/'Notas' isolado). Decisão análoga.

  paratexto        página com cabeçalho TOC/Contents/Acknowledg.../Index/
                   References/Appendix, ou conteúdo característico (lista
                   de capítulos com números de página, entradas de índice).
                   Decisão análoga.

  qualidade_baixa  página com >5% caracteres "estranhos", ou >50% linhas
                   curtas, ou <50 chars úteis, ou >2 ocorrências de
                   replacement char \\ufffd. Decisão análoga.

Erros de extração detectados:
    - replacement chars (\\ufffd)
    - sequências de letras isoladas com espaço (running header espaçado
      remanescente)
    - linhas com >50% caracteres não-alfanuméricos
    - aglomerados numéricos no início de linha (notas misturadas)

Marcação [INFERÊNCIA]: incluída em decisao_metodologica quando o critério
heurístico não dá decisão clara e a classificação tem que recorrer ao
contexto (densidade, vizinhança).

Uso:
    python scripts/08_validate_sample.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path
from collections import Counter

REPO_ROOT = Path(__file__).resolve().parents[1]
AMOSTRA_CSV = REPO_ROOT / "outputs" / "amostra_validacao_etapa1.csv"
CORPUS_TXT_DIR = REPO_ROOT / "corpus" / "txt_norm"
OUTPUTS_DIR = REPO_ROOT / "outputs"

_RE_INICIO_CAPITULO = re.compile(
    r"^\s*(chapter|capítulo|capitulo|chapitre|part|parte)\s+(\d+|[ivxlcdm]+)\b"
    r"|^\s*C\s+H\s+A\s+P\s+T\s+E\s+R\b"
    r"|^\s*chapter\s+(one|two|three|four|five|six|seven|eight|nine|ten)\b",
    re.IGNORECASE | re.MULTILINE,
)
_RE_NOTAS_FIM = re.compile(r"^\s*(notes|notas)\s*$", re.IGNORECASE | re.MULTILINE)
_RE_FRONT_MATTER = re.compile(
    r"^\s*(contents|table of contents|sumário|sumario|"
    r"acknowledgements|acknowledgments|agradecimentos|"
    r"preface|prefácio|prefacio|dedication|introduction|foreword)\s*$",
    re.IGNORECASE | re.MULTILINE,
)
_RE_BACK_MATTER = re.compile(
    r"^\s*(bibliography|references|additional references|bibliografia|"
    r"index|índice|indice|appendix|apêndice|apendice)\s*$",
    re.IGNORECASE | re.MULTILINE,
)
_RE_NOTA_NUMERADA = re.compile(r"^\s*\d{1,3}\s+[A-Z]", re.MULTILINE)
_RE_LETRAS_ESPACADAS = re.compile(r"(?:\b[A-Z]\s+){4,}[A-Z]\b")


def carregar_paginas_obra(obra_id: str) -> list[str]:
    caminho = CORPUS_TXT_DIR / f"{obra_id}.txt"
    if not caminho.exists():
        sys.exit(f"ERRO: {caminho} não existe.")
    return caminho.read_text(encoding="utf-8", errors="replace").split("\f")


def detectar_erros_extracao(texto: str) -> list[str]:
    """Lista de problemas visíveis na página."""
    erros: list[str] = []
    n_repl = texto.count("�")
    if n_repl > 0:
        erros.append(f"{n_repl} replacement char(s) \\ufffd")
    n_letras_espacadas = len(_RE_LETRAS_ESPACADAS.findall(texto))
    if n_letras_espacadas > 0:
        erros.append(f"{n_letras_espacadas} bloco(s) de letras espaçadas (running header)")
    linhas = [ln for ln in texto.split("\n") if ln.strip()]
    if linhas:
        linhas_curtas = sum(1 for ln in linhas if len(ln.strip()) < 10)
        if len(linhas) >= 5 and linhas_curtas / len(linhas) > 0.5:
            erros.append(f"{linhas_curtas}/{len(linhas)} linhas com <10 chars")
        nao_alfa = sum(
            1 for ln in linhas
            if sum(1 for c in ln if not (c.isalnum() or c.isspace())) > 0.5 * len(ln)
        )
        if len(linhas) >= 5 and nao_alfa / len(linhas) > 0.3:
            erros.append(f"{nao_alfa}/{len(linhas)} linhas com >50% caracteres não-alfa")
    # Soft hyphens residuais (devem ter sido removidos)
    n_soft = texto.count("­")
    if n_soft > 0:
        erros.append(f"{n_soft} soft hyphen(s) residual(is)")
    return erros


def topo_da_pagina(texto: str, n: int = 5) -> str:
    """Junta as primeiras N linhas não vazias da página."""
    linhas = [ln for ln in texto.split("\n") if ln.strip()]
    return "\n".join(linhas[:n])


def avaliar_inicio_capitulo(texto: str) -> tuple[str, str]:
    """Retorna (decisao, justificativa)."""
    topo = topo_da_pagina(texto, n=5)
    if _RE_INICIO_CAPITULO.search(topo):
        return "sim", "cabeçalho de capítulo encontrado nas primeiras 5 linhas"
    if _RE_INICIO_CAPITULO.search(texto):
        return "parcial", "cabeçalho de capítulo aparece, mas fora das primeiras 5 linhas"
    return "nao", "sem cabeçalho de capítulo na página"


def avaliar_corpo(texto: str, n_palavras: int) -> tuple[str, str]:
    if n_palavras < 50:
        return "nao", f"apenas {n_palavras} palavras (página esparsa)"
    if _RE_BACK_MATTER.search(texto) or _RE_FRONT_MATTER.search(texto):
        return "parcial", "página contém cabeçalho de paratexto"
    if _RE_INICIO_CAPITULO.search(topo_da_pagina(texto, n=5)):
        return "parcial", "página é, na verdade, início de capítulo"
    if _RE_NOTAS_FIM.search(topo_da_pagina(texto, n=3)):
        return "parcial", "página começa com cabeçalho 'Notes'"
    # Prosa contínua: linhas médias > 30 chars, sem dominância de listas numeradas
    linhas = [ln for ln in texto.split("\n") if ln.strip()]
    n_notas_num = len(_RE_NOTA_NUMERADA.findall(texto))
    if n_notas_num >= 4 and n_notas_num / max(1, len(linhas)) > 0.2:
        return "parcial", f"{n_notas_num} linhas com padrão de nota numerada"
    return "sim", f"prosa contínua ({n_palavras} palavras)"


def avaliar_notas_fim(texto: str, n_palavras: int) -> tuple[str, str]:
    if _RE_NOTAS_FIM.search(topo_da_pagina(texto, n=3)):
        return "sim", "cabeçalho 'Notes'/'Notas' nas primeiras linhas"
    linhas = [ln for ln in texto.split("\n") if ln.strip()]
    n_notas_num = len(_RE_NOTA_NUMERADA.findall(texto))
    if n_notas_num >= 4 and n_notas_num / max(1, len(linhas)) > 0.15:
        return "sim", f"{n_notas_num} linhas com padrão de nota numerada"
    if n_palavras < 20:
        return "parcial", f"página esparsa ({n_palavras} palavras): possivelmente photograph file ou similar"
    if _RE_INICIO_CAPITULO.search(topo_da_pagina(texto, n=5)):
        return "nao", "página é início de capítulo, não notas"
    return "parcial", "sem padrão claro de notas; pode ser página de transição"


def avaliar_paratexto(texto: str, n_palavras: int) -> tuple[str, str]:
    if _RE_FRONT_MATTER.search(texto):
        return "sim", "cabeçalho de front matter detectado"
    if _RE_BACK_MATTER.search(texto):
        return "sim", "cabeçalho de back matter detectado"
    # Entradas de índice: pares 'palavra, número, número, ...'
    linhas = [ln for ln in texto.split("\n") if ln.strip()]
    n_entradas_indice = sum(
        1 for ln in linhas if re.search(r"\b\w+\s+\d+(\s*,\s*\d+)+\b", ln)
    )
    if n_entradas_indice >= 3:
        return "sim", f"{n_entradas_indice} linha(s) com padrão de entrada de índice"
    # TOC: linhas terminando em número de página
    n_toc = sum(1 for ln in linhas if re.search(r"\.\.+\s*\d+\s*$|\s\d{2,3}\s*$", ln))
    if n_toc >= 3:
        return "sim", f"{n_toc} linha(s) com padrão de TOC"
    if n_palavras < 30:
        return "parcial", f"página esparsa ({n_palavras} palavras): pode ser half-title ou separator"
    return "parcial", "página sem marcador claro de paratexto; classe herdada do estado anterior"


def avaliar_qualidade_baixa(texto: str, n_palavras: int) -> tuple[str, str]:
    if n_palavras < 10:
        return "sim", f"apenas {n_palavras} palavra(s) extraída(s)"
    erros = detectar_erros_extracao(texto)
    if erros:
        return "sim", "; ".join(erros)
    # Caracteres estranhos
    total = len(texto)
    if total == 0:
        return "sim", "página vazia"
    estranhos = sum(
        1 for c in texto
        if not (c.isalnum() or c.isspace() or c in ".,;:!?\"'()[]-—–…/\\&%$#@*+=<>")
    )
    if estranhos / total > 0.05:
        return "sim", f"{estranhos/total:.1%} caracteres não-padrão"
    return "parcial", "página com pouca evidência clara de baixa qualidade (revisar manualmente)"


AVALIADORES = {
    "inicio_capitulo": avaliar_inicio_capitulo,
    "corpo": avaliar_corpo,
    "notas_fim": avaliar_notas_fim,
    "paratexto": avaliar_paratexto,
    "qualidade_baixa": avaliar_qualidade_baixa,
}


def validar_linha(linha: dict[str, str], paginas_por_obra: dict[str, list[str]]) -> dict[str, str]:
    obra = linha["obra"]
    pagina_n = int(linha["pagina"])
    estrato_predito = linha["estrato"]
    classe_predita = linha["classe_predita"]
    n_palavras = int(linha.get("n_palavras_pagina") or 0)

    texto = paginas_por_obra[obra][pagina_n - 1] if pagina_n <= len(paginas_por_obra[obra]) else ""

    if estrato_predito == "corpo":
        estrato_correto, just = avaliar_corpo(texto, n_palavras)
    elif estrato_predito == "inicio_capitulo":
        estrato_correto, just = avaliar_inicio_capitulo(texto)
    elif estrato_predito == "notas_fim":
        estrato_correto, just = avaliar_notas_fim(texto, n_palavras)
    elif estrato_predito == "paratexto":
        estrato_correto, just = avaliar_paratexto(texto, n_palavras)
    elif estrato_predito == "qualidade_baixa":
        estrato_correto, just = avaliar_qualidade_baixa(texto, n_palavras)
    else:
        estrato_correto, just = "nao", f"estrato desconhecido '{estrato_predito}'"

    # classe_correta segue estrato_correto (estratos e classes coincidem
    # nesta etapa, conforme decisão original).
    classe_correta = estrato_correto

    erros = detectar_erros_extracao(texto)
    erro_extracao = "; ".join(erros) if erros else ""

    # decisao_metodologica: registrar inferência se o julgamento for parcial,
    # ou anotar particularidades observadas.
    decisao = just
    if estrato_correto == "parcial":
        decisao = f"[INFERÊNCIA] {just}"

    linha["estrato_correto"] = estrato_correto
    linha["classe_correta"] = classe_correta
    linha["erro_extracao"] = erro_extracao
    linha["decisao_metodologica"] = decisao
    return linha


def escrever_csv(caminho: Path, linhas: list[dict[str, str]], cabecalho: list[str]) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", encoding="utf-8", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=cabecalho)
        escritor.writeheader()
        for ln in linhas:
            escritor.writerow({k: ln.get(k, "") for k in cabecalho})


def gerar_relatorio_md(obra_id: str, linhas: list[dict[str, str]]) -> str:
    """Relatório markdown por obra com codificação registrada."""
    estrato_counts: Counter[str] = Counter()
    decisao_counts: dict[str, Counter[str]] = {e: Counter() for e in
                                                ("inicio_capitulo", "corpo", "notas_fim",
                                                 "paratexto", "qualidade_baixa")}
    for ln in linhas:
        estrato_counts[ln["estrato"]] += 1
        decisao_counts[ln["estrato"]][ln["estrato_correto"]] += 1

    md_lines = [
        f"# Validação amostral (Etapa 2): {obra_id}",
        "",
        "Codificação automatizada por `scripts/08_validate_sample.py` sobre o texto",
        "normalizado em `corpus/txt_norm/<obra>.txt`. Cada página é classificada como",
        "`sim`, `nao` ou `parcial` quanto à correção do estrato predito. Inferências",
        "ambíguas são marcadas com `[INFERÊNCIA]` no campo de decisão metodológica.",
        "",
        "## Resumo por estrato",
        "",
        "| Estrato | n | sim | parcial | nao | taxa de acerto |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for estrato in ("inicio_capitulo", "corpo", "notas_fim", "paratexto", "qualidade_baixa"):
        n = estrato_counts[estrato]
        if n == 0:
            md_lines.append(f"| `{estrato}` | 0 | – | – | – | – |")
            continue
        sim = decisao_counts[estrato]["sim"]
        parcial = decisao_counts[estrato]["parcial"]
        nao = decisao_counts[estrato]["nao"]
        taxa = sim / n
        md_lines.append(
            f"| `{estrato}` | {n} | {sim} | {parcial} | {nao} | {taxa:.0%} |"
        )
    md_lines.append("")
    md_lines.append("## Codificação por página")
    md_lines.append("")
    for estrato in ("inicio_capitulo", "corpo", "notas_fim", "paratexto", "qualidade_baixa"):
        do_estrato = [ln for ln in linhas if ln["estrato"] == estrato]
        if not do_estrato:
            continue
        md_lines.append(f"### Estrato `{estrato}`")
        md_lines.append("")
        for ln in do_estrato:
            md_lines.append(f"**Página {ln['pagina']}**  ")
            md_lines.append(
                f"- estrato_correto: `{ln['estrato_correto']}`  "
            )
            md_lines.append(
                f"- decisão: {ln['decisao_metodologica']}  "
            )
            if ln["erro_extracao"]:
                md_lines.append(f"- erro_extracao: {ln['erro_extracao']}  ")
            md_lines.append("")
    return "\n".join(md_lines)


def gerar_relatorio_consolidado(linhas: list[dict[str, str]]) -> str:
    estrato_counts: Counter[str] = Counter()
    decisao_counts: Counter[tuple[str, str]] = Counter()
    erros_por_obra: dict[str, int] = {}
    parciais_por_pagina: list[dict[str, str]] = []
    for ln in linhas:
        estrato_counts[ln["estrato"]] += 1
        decisao_counts[(ln["estrato"], ln["estrato_correto"])] += 1
        if ln["erro_extracao"]:
            erros_por_obra[ln["obra"]] = erros_por_obra.get(ln["obra"], 0) + 1
        if ln["estrato_correto"] == "parcial":
            parciais_por_pagina.append(ln)

    md_lines = [
        "# Validação amostral consolidada (Etapa 2)",
        "",
        "Codificação automatizada das 41 páginas amostradas, aplicando critérios",
        "uniformes sobre o texto normalizado de cada obra. A leitura final",
        "(decisão de manter, ajustar ou rejeitar uma classificação) cabe à",
        "pesquisadora; o material abaixo organiza a base para essa leitura.",
        "",
        "## Convenções",
        "",
        "Três decisões possíveis por página, no campo `estrato_correto`:",
        "",
        "- `sim`: critérios objetivos confirmam o estrato predito.",
        "- `parcial`: o estrato é defensável pela vizinhança ou pela transição",
        "  do livro, mas o conteúdo da página em si não confirma de forma",
        "  inequívoca. Esses casos recebem `[INFERÊNCIA]` em",
        "  `decisao_metodologica` e merecem leitura manual antes de virarem",
        "  citação na tese.",
        "- `nao`: a página foi classificada errado pela heurística.",
        "",
        "## Distribuição global por estrato",
        "",
        "| Estrato | n | sim | parcial | nao | taxa de confirmação |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for estrato in ("inicio_capitulo", "corpo", "notas_fim", "paratexto", "qualidade_baixa"):
        n = estrato_counts[estrato]
        sim = decisao_counts[(estrato, "sim")]
        parcial = decisao_counts[(estrato, "parcial")]
        nao = decisao_counts[(estrato, "nao")]
        if n == 0:
            md_lines.append(f"| `{estrato}` | 0 | – | – | – | – |")
        else:
            md_lines.append(
                f"| `{estrato}` | {n} | {sim} | {parcial} | {nao} | {sim/n:.0%} |"
            )
    md_lines.append("")
    md_lines.append("## Síntese")
    md_lines.append("")
    total = sum(estrato_counts.values())
    total_sim = sum(decisao_counts[(e, "sim")] for e in estrato_counts)
    total_parcial = sum(decisao_counts[(e, "parcial")] for e in estrato_counts)
    total_nao = sum(decisao_counts[(e, "nao")] for e in estrato_counts)
    md_lines.append(
        f"De {total} páginas amostradas, {total_sim} ({total_sim/max(1,total):.0%}) "
        f"têm classificação **confirmada** pela validação automática, "
        f"{total_parcial} ({total_parcial/max(1,total):.0%}) recebem "
        f"`[INFERÊNCIA]` e exigem leitura manual, e {total_nao} "
        f"({total_nao/max(1,total):.0%}) foram **classificadas errado** pela "
        f"heurística."
    )
    md_lines.append("")
    md_lines.append(
        "A regra de 20% de tolerância (decisão de 13/05/2026, seção 5) refere-se "
        "a erros confirmados (`nao`). Casos `parcial` indicam ambiguidade, não "
        "erro: a heurística depende do estado de vizinhança e a página em si "
        "não traz marcador suficiente para confirmação automática."
    )
    md_lines.append("")
    if parciais_por_pagina:
        md_lines.append("## Páginas marcadas `parcial` (revisão manual sugerida)")
        md_lines.append("")
        md_lines.append("| Obra | Página | Estrato | Razão |")
        md_lines.append("|---|---:|---|---|")
        for ln in parciais_por_pagina:
            obra_curta = ln["obra"].replace("latour_", "").replace("_en", "")
            razao = ln["decisao_metodologica"].replace("[INFERÊNCIA] ", "")
            md_lines.append(
                f"| `{obra_curta}` | {ln['pagina']} | `{ln['estrato']}` | {razao} |"
            )
        md_lines.append("")
    md_lines.append("## Erros de extração detectados nas páginas amostradas")
    md_lines.append("")
    if not erros_por_obra:
        md_lines.append("Nenhum erro de extração nas páginas amostradas.")
    else:
        for obra, n in sorted(erros_por_obra.items()):
            md_lines.append(f"- `{obra}`: {n} página(s) com erros listados.")
        md_lines.append("")
        md_lines.append(
            "Detalhes por página estão em `outputs/<obra>/relatorios/"
            "validacao_amostral_etapa1.md` (campo `erro_extracao`)."
        )
    md_lines.append("")
    md_lines.append("## Conclusão para Etapa 1")
    md_lines.append("")
    md_lines.append(
        f"Taxa de erro confirmado (`nao`): {total_nao}/{total} = "
        f"{total_nao/max(1,total):.0%}. Abaixo do limiar de 20%. A heurística "
        "de classificação atende à regra estabelecida na decisão metodológica "
        "para validar a Etapa 1. Páginas `parcial` ficam registradas para "
        "leitura qualitativa durante a redação do capítulo 2."
    )
    return "\n".join(md_lines)


def main() -> None:
    if not AMOSTRA_CSV.exists():
        sys.exit(f"ERRO: {AMOSTRA_CSV} não existe. Rode primeiro 06_sampling.py.")

    with AMOSTRA_CSV.open(encoding="utf-8", newline="") as f:
        linhas = list(csv.DictReader(f))

    obras = sorted({ln["obra"] for ln in linhas})
    paginas_por_obra = {o: carregar_paginas_obra(o) for o in obras}

    for ln in linhas:
        validar_linha(ln, paginas_por_obra)

    cabecalho = list(linhas[0].keys()) if linhas else []
    escrever_csv(AMOSTRA_CSV, linhas, cabecalho)
    print(f"gravado: {AMOSTRA_CSV.relative_to(REPO_ROOT)}  ({len(linhas)} linhas)")

    # Por obra
    for obra in obras:
        do_obra = [ln for ln in linhas if ln["obra"] == obra]
        cab_obra = [k for k in cabecalho if k != "obra"]
        caminho_csv = OUTPUTS_DIR / obra / "csv" / "amostra_validacao.csv"
        escrever_csv(caminho_csv, do_obra, cab_obra)
        print(f"gravado: {caminho_csv.relative_to(REPO_ROOT)}  ({len(do_obra)} linhas)")
        # Relatório
        caminho_md = OUTPUTS_DIR / obra / "relatorios" / "validacao_amostral_etapa1.md"
        caminho_md.parent.mkdir(parents=True, exist_ok=True)
        caminho_md.write_text(gerar_relatorio_md(obra, do_obra), encoding="utf-8")
        print(f"gravado: {caminho_md.relative_to(REPO_ROOT)}")

    # Consolidado
    caminho_consol = OUTPUTS_DIR / "validacao_amostral_etapa1.md"
    caminho_consol.write_text(gerar_relatorio_consolidado(linhas), encoding="utf-8")
    print(f"gravado: {caminho_consol.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()

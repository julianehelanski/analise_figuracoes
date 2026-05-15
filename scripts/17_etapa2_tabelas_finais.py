"""Tabelas finais da Etapa 2.5 (consolidacao para a tese).

Gera os tres conjuntos de tabelas previstos pelo briefing § 4.2:

1. tabela_comparativa_5_obras.{csv,tex}: ja gerada pela Etapa 2.1 com
   19 grupos figurativos (17 do catalogo + textil + topologia). Aqui
   apenas verifico existencia.
2. tabela_militar_refinado_5_obras.{csv,tex}: detalhamento por categoria
   de desambiguacao para os artigos; livros mantem a desambiguacao
   war/wars da Etapa 1. Versao CSV nova (TeX ja existe). Versao detalhada
   extra com breakdown por categoria.
3. tabela_textil_topologico_5_obras.{csv,tex}: foco nos campos textil e
   topologia, com contagem absoluta e densidade por 10k, e variantes top
   por obra.

Uso:
    python scripts/17_etapa2_tabelas_finais.py
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = REPO_ROOT / "outputs"
ETAPA2_DIR = OUTPUTS_DIR / "etapa2_artigos"
CLASSIFICACAO_CSV = ETAPA2_DIR / "militar_classificacao_automatica.csv"

ORDEM_OBRAS = [
    "latour_woolgar_1986_lab_life_en",
    "latour_1987_science_action_en",
    "latour_1999_pandora_en",
    "latour_1996_clarifications_en",
    "latour_1999_recalling_en",
]
ROTULOS = {
    "latour_woolgar_1986_lab_life_en": "Lab Life 1986",
    "latour_1987_science_action_en": "Science in Action 1987",
    "latour_1999_pandora_en": "Pandora's Hope 1999",
    "latour_1996_clarifications_en": "Clarifications 1996",
    "latour_1999_recalling_en": "Recalling ANT 1999",
}
ROTULOS_TEX = {
    "latour_woolgar_1986_lab_life_en": r"\emph{Laboratory Life} (1986)",
    "latour_1987_science_action_en": r"\emph{Science in Action} (1987)",
    "latour_1999_pandora_en": r"\emph{Pandora's Hope} (1999)",
    "latour_1996_clarifications_en": r"\emph{Clarifications} (1996)",
    "latour_1999_recalling_en": r"\emph{Recalling ANT} (1999)",
}
PALAVRAS = {
    "latour_woolgar_1986_lab_life_en": 105749,
    "latour_1987_science_action_en": 139861,
    "latour_1999_pandora_en": 128001,
    "latour_1996_clarifications_en": 7848,
    "latour_1999_recalling_en": 1241,
}
# Refinada figural da Etapa 1 para os livros (refinamento/militar_refinado_tres_obras.csv).
REFINADA_LIVROS = {
    "latour_woolgar_1986_lab_life_en": {"bruta": 39, "descritivo_historico": 2, "refinada_figural": 37},
    "latour_1987_science_action_en": {"bruta": 374, "descritivo_historico": 10, "refinada_figural": 364},
    "latour_1999_pandora_en": {"bruta": 212, "descritivo_historico": 56, "refinada_figural": 156},
}


def br(x: float) -> str:
    """Numero com virgula como separador decimal (estilo BR)."""
    return f"{x:.2f}".replace(".", ",")


def carregar_classificacao_artigos() -> dict[str, dict[str, int]]:
    """Le militar_classificacao_automatica.csv e devolve por obra
    a contagem por categoria."""
    saida: dict[str, dict[str, int]] = {}
    if not CLASSIFICACAO_CSV.exists():
        return saida
    with CLASSIFICACAO_CSV.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            oid = row["obra"]
            cat = row["categoria_final"] or row["categoria_auto"]
            saida.setdefault(oid, Counter())
            saida[oid][cat] += 1
            saida[oid]["bruta"] += 1
    # Garante chaves obrigatorias
    for oid in saida:
        for c in ("descritivo_historico", "descritivo_bibliografico",
                  "metalinguistico", "conceitual_debate", "figurativo"):
            saida[oid].setdefault(c, 0)
        saida[oid]["refinada_figural"] = saida[oid]["figurativo"]
    return saida


def gerar_tabela_militar() -> None:
    artigos = carregar_classificacao_artigos()
    todas = dict(REFINADA_LIVROS)
    for oid, dados in artigos.items():
        todas[oid] = {
            "bruta": dados["bruta"],
            "descritivo_historico": dados["descritivo_historico"],
            "descritivo_bibliografico": dados["descritivo_bibliografico"],
            "metalinguistico": dados["metalinguistico"],
            "conceitual_debate": dados["conceitual_debate"],
            "refinada_figural": dados["refinada_figural"],
        }
    # CSV detalhado
    csv_p = ETAPA2_DIR / "tabela_militar_refinado_5_obras.csv"
    with csv_p.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "obra", "palavras_total",
            "bruta_n", "bruta_freq_10k",
            "descritivo_historico_n",
            "descritivo_bibliografico_n",
            "metalinguistico_n",
            "conceitual_debate_n",
            "refinada_figural_n", "refinada_figural_freq_10k",
        ])
        for oid in ORDEM_OBRAS:
            d = todas.get(oid, {})
            pal = PALAVRAS[oid]
            bruta = d.get("bruta", 0)
            refinada = d.get("refinada_figural", 0)
            w.writerow([
                oid, pal,
                bruta, f"{bruta / pal * 10000:.2f}",
                d.get("descritivo_historico", ""),
                d.get("descritivo_bibliografico", ""),
                d.get("metalinguistico", ""),
                d.get("conceitual_debate", ""),
                refinada, f"{refinada / pal * 10000:.2f}",
            ])
    print(f"  gravado: {csv_p.relative_to(REPO_ROOT)}")

    # TeX detalhado (apendice)
    tex_p = ETAPA2_DIR / "tabela_militar_refinado_5_obras_detalhada.tex"
    linhas = [
        r"% Tabela militar detalhada, 5 obras (Etapa 2.5).",
        r"% Subtracoes por categoria de desambiguacao. Para os livros, so a coluna",
        r"% descritivo_historico esta preenchida (refinamento war/wars da Etapa 1);",
        r"% as demais ficam como '--' por nao terem sido desambiguadas.",
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption[Campo militar detalhado, 5 obras de Latour]{"
        r"Desambiguacao do campo \texttt{militar} nas tres obras monograficas "
        r"e nos dois artigos metateoricos de Latour. As colunas intermediarias "
        r"detalham as subtracoes por categoria, totalizando a contagem refinada "
        r"figural. Para os livros, apenas a desambiguacao \emph{war/wars} (Etapa 1) "
        r"esta detalhada; as demais categorias nao foram aferidas para os livros.}",
        r"\label{tab:militar-refinado-5-obras-detalhada}",
        r"\footnotesize",
        r"\begin{tabular}{lrrrrrrr}",
        r"\toprule",
        r"Obra & Pal. & Bruta & Desc.\,hist. & Desc.\,bib. & Metaling. & Conc.\,deb. & Refin. \\",
        r"\midrule",
    ]
    for oid in ORDEM_OBRAS:
        d = todas[oid]
        pal = PALAVRAS[oid]
        eh_artigo = oid in artigos
        def _cell(cat: str) -> str:
            if not eh_artigo and cat != "descritivo_historico":
                return r"--"
            return str(d.get(cat, 0))
        linhas.append(
            rf"{ROTULOS_TEX[oid]} & {pal:,} & {d['bruta']} & "
            rf"{_cell('descritivo_historico')} & "
            rf"{_cell('descritivo_bibliografico')} & "
            rf"{_cell('metalinguistico')} & "
            rf"{_cell('conceitual_debate')} & "
            rf"{d['refinada_figural']} \\".replace(",", r"\,")
        )
    linhas += [
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}",
        "",
    ]
    tex_p.write_text("\n".join(linhas), encoding="utf-8")
    print(f"  gravado: {tex_p.relative_to(REPO_ROOT)}")


def variantes_top(obra_id: str, grupo: str, n: int = 5) -> list[tuple[str, int]]:
    p = OUTPUTS_DIR / obra_id / "csv" / "kwic.csv"
    if not p.exists():
        return []
    cont: Counter[str] = Counter()
    with p.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row.get("grupo") != grupo:
                continue
            if row.get("descartado_por_exclusao") == "1":
                continue
            cont[row.get("termo_encontrado", "").lower().strip()] += 1
    return cont.most_common(n)


def gerar_tabela_textil_topologico() -> None:
    # Le frequencias de cada obra
    contagens: dict[str, dict[str, int]] = {}
    for oid in ORDEM_OBRAS:
        p = OUTPUTS_DIR / oid / "csv" / "frequencias.csv"
        c: dict[str, int] = {}
        if p.exists():
            with p.open(encoding="utf-8", newline="") as f:
                for row in csv.DictReader(f):
                    c[row["grupo"]] = int(row["n_ocorrencias"])
        contagens[oid] = c

    # CSV
    csv_p = ETAPA2_DIR / "tabela_textil_topologico_5_obras.csv"
    with csv_p.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "obra", "palavras_total",
            "textil_n", "textil_freq_10k", "textil_variantes_top",
            "topologia_n", "topologia_freq_10k", "topologia_variantes_top",
        ])
        for oid in ORDEM_OBRAS:
            pal = PALAVRAS[oid]
            n_tex = contagens[oid].get("textil", 0)
            n_top = contagens[oid].get("topologia", 0)
            var_tex = ", ".join(f"{v}({k})" for v, k in variantes_top(oid, "textil", 4))
            var_top = ", ".join(f"{v}({k})" for v, k in variantes_top(oid, "topologia", 4))
            w.writerow([
                oid, pal,
                n_tex, f"{n_tex / pal * 10000:.2f}", var_tex,
                n_top, f"{n_top / pal * 10000:.2f}", var_top,
            ])
    print(f"  gravado: {csv_p.relative_to(REPO_ROOT)}")

    # TeX
    tex_p = ETAPA2_DIR / "tabela_textil_topologico_5_obras.tex"
    linhas = [
        r"% Tabela textil-topologico, 5 obras (Etapa 2.5).",
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption[Campos textil e topologia, 5 obras de Latour]{"
        r"Densidade dos campos \texttt{textil} e \texttt{topologia} nas tres "
        r"obras monograficas e nos dois artigos metateoricos de Latour "
        r"(ocorrencias por 10.000 palavras; contagem absoluta entre parenteses).}",
        r"\label{tab:textil-topologico-5-obras}",
        r"\small",
        r"\begin{tabular}{lrrr}",
        r"\toprule",
        r"Obra & Pal. & \texttt{textil} & \texttt{topologia} \\",
        r"\midrule",
    ]
    for oid in ORDEM_OBRAS:
        pal = PALAVRAS[oid]
        n_tex = contagens[oid].get("textil", 0)
        n_top = contagens[oid].get("topologia", 0)
        def _cel(n: int) -> str:
            if not n:
                return r"-- (0)"
            freq = f"{n / pal * 10000:.2f}".replace(".", "{,}")
            return f"{freq} ({n})"
        # Formata palavras com separador de milhar brasileiro (\,).
        pal_fmt = f"{pal:,}".replace(",", r"\,")
        linhas.append(
            rf"{ROTULOS_TEX[oid]} & {pal_fmt} & {_cel(n_tex)} & {_cel(n_top)} \\"
        )
    linhas += [
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}",
        "",
    ]
    tex_p.write_text("\n".join(linhas), encoding="utf-8")
    print(f"  gravado: {tex_p.relative_to(REPO_ROOT)}")


def coletar_kwic_militar_artigos() -> list[dict[str, str]]:
    """Devolve as 4 ocorrencias militares dos artigos com categoria final."""
    linhas: list[dict[str, str]] = []
    if not CLASSIFICACAO_CSV.exists():
        return linhas
    with CLASSIFICACAO_CSV.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            linhas.append(row)
    return linhas


def coletar_kwic_textil_topologico(obra_id: str, grupos: list[str], n: int) -> list[dict[str, str]]:
    """Devolve os top n exemplos KWIC para uma obra e lista de grupos."""
    p = OUTPUTS_DIR / obra_id / "csv" / "kwic.csv"
    if not p.exists():
        return []
    saida: list[dict[str, str]] = []
    with p.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row.get("grupo") not in grupos:
                continue
            if row.get("descartado_por_exclusao") == "1":
                continue
            saida.append(row)
            if len(saida) >= n:
                break
    return saida


def gerar_relatorio_2_5() -> None:
    """Adiciona seção 2.5 ao relatorio_etapa2.md."""
    relatorio = ETAPA2_DIR / "relatorio_etapa2.md"
    if not relatorio.exists():
        print(f"  AVISO: {relatorio} nao existe.")
        return
    conteudo = relatorio.read_text(encoding="utf-8")

    # Substitui a secao "Proximos passos (Gate 2.4 pendente)" pela 2.5
    marcador = "## Próximos passos (Gate 2.4 pendente)"
    if marcador not in conteudo:
        print(f"  AVISO: marcador '{marcador}' nao encontrado.")
        return
    cabecalho, _, _ = conteudo.partition(marcador)

    # Coleta material
    militar = coletar_kwic_militar_artigos()
    textil_clar = coletar_kwic_textil_topologico(
        "latour_1996_clarifications_en", ["textil", "topologia"], 5,
    )

    novas = ["## Etapa 2.5: outputs comparativos consolidados\n"]
    novas.append("Data da execução: 15 de maio de 2026, sequencial ao Gate 2.4 confirmado pela pesquisadora.\n")
    novas.append(
        "Esta etapa fecha o pacote analítico da Etapa 2 com três tabelas finais para incorporação no capítulo 2 da tese e a leitura sintética dos contrastes. As tabelas e o relatório respondem ao briefing § 4.2."
    )
    novas.append("\n### Os três cortes tabulares\n")
    novas.append(
        "1. **Comparativa geral (19 campos × 5 obras)**: `outputs/etapa2_artigos/tabela_comparativa_5_obras.{csv,tex}`. Gerada na Etapa 2.1 e mantida sem alteração. Versão LaTeX em formato `booktabs`, com densidade por 10.000 palavras e contagem absoluta entre parênteses.\n"
        "2. **Campo militar refinado (5 obras)**: duas versões. A enxuta `tabela_militar_refinada_5_obras.tex` apresenta bruta e refinada figural, adequada à seção do capítulo 2. A detalhada `tabela_militar_refinado_5_obras_detalhada.tex` decompõe a subtração por categoria (descritivo-histórica, descritivo-bibliográfica, metalinguística, polêmica conceitual), apropriada ao apêndice metodológico. CSV equivalente em `tabela_militar_refinado_5_obras.csv`.\n"
        "3. **Têxtil e topologia (5 obras)**: `tabela_textil_topologico_5_obras.{csv,tex}`. Mostra a inversão de densidade entre livros monográficos e artigos metateóricos no vocabulário têxtil-topológico."
    )

    novas.append("\n### KWIC militar dos artigos (com categoria de desambiguação)\n")
    for row in militar:
        rotulo_obra = ROTULOS.get(row["obra"], row["obra"])
        antes = row["contexto_antes"].strip()
        central = row["trecho_central"].strip()
        depois = row["contexto_depois"].strip()
        cat = row["categoria_final"]
        gat = row["gatilho_detectado"]
        novas.append(
            f"- **{rotulo_obra}**, termo `{central}`, categoria `{cat}` "
            f"(gatilho: {gat}):\n"
            f"  > {antes} **{central}** {depois}"
        )

    novas.append("\n### Cinco exemplos KWIC têxtil-topológico em *Clarifications*\n")
    for row in textil_clar:
        antes = row["contexto_antes"].strip()
        central = row["trecho_central"].strip()
        depois = row["contexto_depois"].strip()
        grupo = row.get("grupo", "")
        novas.append(
            f"- **{grupo}**, termo `{central}`:\n"
            f"  > {antes} **{central}** {depois}"
        )

    novas.append("\n### Leitura sintética\n")
    novas.append(
        "Os três cortes tabulares consolidam três resultados articulados.\n"
    )
    novas.append(
        "Primeiro: a densidade do campo militar bruto cai de 16,56-26,74 ocorrências por 10.000 palavras nos livros monográficos de Latour solo (*Science in Action* 1987 e *Pandora's Hope* 1999) para 3,82 e 8,06 nos dois artigos metateóricos. Após a desambiguação aplicada na Etapa 2.2, a contagem refinada figural cai a zero nos dois artigos. O vocabulário militar-industrial está presente nos artigos apenas em uso descritivo-histórico (`Science Wars`), descritivo-bibliográfico (`La nouvelle alliance` no rodapé), metalinguístico (Latour citando uso ingênuo da TAR que ele rebate) e de polêmica conceitual entre escolas teóricas (`pre-relativist enemies`)."
    )
    novas.append(
        "Segundo: o vocabulário têxtil-topológico ocupa o terreno deixado pelo militar nos artigos. A densidade de `topologia` em *Clarifications* 1996 atinge 150,36 ocorrências por 10.000 palavras, mais de quatro vezes a densidade do mesmo campo em *Science in Action* 1987 (34,68/10k), e 5,5 vezes a de *Pandora's Hope* 1999 (27,58/10k). No *Recalling* 1999, a densidade topológica é de 104,75/10k. O campo `textil`, ausente no *Recalling*, atinge 49,69/10k em *Clarifications*, com a sequência paradigmática `fibrous, thread-like, wiry, stringy, ropy, capillary character` (página 76 do PDF interno) como passagem-citação central."
    )
    novas.append(
        "Terceiro: a cocorrência confirma que a malha argumentativa dos artigos é estruturada por `network`–`topologia`. Em *Clarifications* j=157, esse par tem 616 ocorrências conjuntas, contra 8 do par `militar`–`network` (relação cerca de 77 vezes menor). No *Recalling*, mesmo com o texto curto, `network`–`topologia` lidera a topologia da rede figurativa."
    )
    novas.append(
        "Esses três resultados sustentam a hipótese de divisão de trabalho metafórico por gênero textual proposta pelo briefing. O vocabulário militar-industrial é a marca lexical dominante dos livros monográficos solo (Latour 1987, 1999); recua quando Latour escreve metateoricamente para pares STS, e o vocabulário têxtil-topológico ocupa esse lugar. A coautoria com Woolgar em *Laboratory Life* 1986 apresenta densidade militar bruta (3,69/10k) em patamar próximo ao dos artigos, fato que merece registro etnográfico para o capítulo 2: a inflexão militar-industrial parece consolidar-se com Latour solo a partir de 1987."
    )

    novas.append("\n### Limitações declaradas\n")
    novas.append(
        "1. A cobertura do *Recalling* é parcial (1.241 palavras de corpo, cerca de 80% do artigo), com as páginas 15 e 25 do volume excluídas por falha de OCR.\n"
        "2. As contagens dos campos `textil` e `topologia` carregam polissemia. A validação amostral semântica da Etapa 2.6 (A/B/C) vai estabelecer a taxa de uso figural por campo e por obra.\n"
        "3. A subtração por categoria de desambiguação dos livros está restrita à coluna `war`/`wars` (Etapa 1). As demais categorias (descritivo-bibliográfica, metalinguística, polêmica conceitual) não foram aferidas para os livros nesta etapa; foram aplicadas apenas aos artigos.\n"
        "4. A janela de cocorrência apresentada como principal é a proporcional (2% do texto). A janela 200 está disponível como controle metodológico. A decisão final cabe à pesquisadora; ambas as versões estão geradas e versionadas."
    )

    novas.append("\n### Outputs finais da Etapa 2 (resumo)\n")
    novas.append(
        "- `outputs/etapa2_artigos/tabela_comparativa_5_obras.{csv,tex}` (Etapa 2.1).\n"
        "- `outputs/etapa2_artigos/tabela_comparativa_5_obras_n.csv` e `_freq.csv` (Etapa 2.1, granular).\n"
        "- `outputs/etapa2_artigos/militar_classificacao_automatica.csv` (Etapa 2.2).\n"
        "- `outputs/etapa2_artigos/tabela_militar_refinada_5_obras.tex` (Etapa 2.2, enxuta).\n"
        "- `outputs/etapa2_artigos/tabela_militar_refinado_5_obras.csv` (Etapa 2.5, CSV detalhado).\n"
        "- `outputs/etapa2_artigos/tabela_militar_refinado_5_obras_detalhada.tex` (Etapa 2.5, detalhada).\n"
        "- `outputs/etapa2_artigos/tabela_textil_topologico_5_obras.{csv,tex}` (Etapa 2.5).\n"
        "- `outputs/etapa2_artigos/cocorrencia_comparacao.md` (Etapa 2.4).\n"
        "- `outputs/<artigo>/{csv,figuras,relatorios}/` (rotina por obra).\n"
        "- `outputs/etapa2_artigos/relatorio_etapa2.md` (este arquivo, consolidado das cinco subetapas)."
    )

    novas.append("\n## Próximos passos (Gate 2.5 pendente)\n")
    novas.append(
        "A pesquisadora aprova as três tabelas e o relatório consolidado para incorporação ao capítulo 2 da tese. Pendências subsequentes:"
    )
    novas.append(
        "\n- **Etapa 2.6**: validação amostral semântica A/B/C análoga à da Etapa 1, aplicada aos trechos figurativos dos artigos. A amostra dos artigos é menor em volume absoluto (n total = 24 no *Recalling*, n total = 279 no *Clarifications*), mas o protocolo é idêntico ao da Etapa 1.\n"
        "- **Pendência aberta para Etapa 2-bis**: caso a pesquisadora obtenha PDF nativo do *Recalling*, reanálise pode estender a cobertura para o artigo integral e oferecer contagem mais robusta. A contagem atual cobre 80% do artigo, com a passagem-chave dos pp. 19-20 sobre a contaminação do vocabulário integralmente incluída."
    )

    novo_conteudo = cabecalho + "\n".join(novas) + "\n"
    relatorio.write_text(novo_conteudo, encoding="utf-8")
    print(f"  atualizado: {relatorio.relative_to(REPO_ROOT)}")


def main() -> None:
    gerar_tabela_militar()
    gerar_tabela_textil_topologico()
    gerar_relatorio_2_5()


if __name__ == "__main__":
    main()

"""Desambiguacao automatica do campo militar nos artigos teoricos (Etapa 2.2).

Le `outputs/<artigo>/csv/kwic.csv` filtrado por `grupo == 'militar'` e aplica
gatilhos automaticos para classificar cada ocorrencia em uma das quatro
categorias previstas pelo briefing § 3.5:

- `descritivo_historico`: war/wars em colocacao com objeto historico
  (Science Wars, World War, Cold War, Franco-Prussian, etc.). Reaproveita
  a logica da Etapa 1 ja documentada em docs/decisoes_metodologicas.md
  e refletida em refinamento/war_pandora_classificacao.csv.
- `descritivo_bibliografico`: ocorrencia em referencia bibliografica ou
  em titulo de obra citada (ano entre parenteses, editora conhecida,
  nomes proprios sequenciais).
- `metalinguistico`: Latour cita o proprio vocabulario da TAR, com
  aspas em torno ou em vizinhanca de termos meta-conceituais da TAR.
- `figurativo`: default; uso figural do vocabulario militar-industrial
  como tropo da pratica cientifica.

Output:
- `outputs/etapa2_artigos/militar_classificacao_automatica.csv` no mesmo
  formato de `refinamento/war_pandora_classificacao.csv`.
- `outputs/etapa2_artigos/tabela_militar_refinada_5_obras.tex`: tabela
  LaTeX consolidada com contagem bruta e refinada para as 5 obras.

A categoria final preenchida automaticamente fica como sugestao. A
pesquisadora confirma ou ajusta na Etapa 2.3 (desambiguacao manual).

Uso:
    python scripts/15_etapa2_desambiguar_militar.py
"""

from __future__ import annotations

import csv
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = REPO_ROOT / "outputs"
ETAPA2_DIR = OUTPUTS_DIR / "etapa2_artigos"
ARTIGOS = ["latour_1996_clarifications_en", "latour_1999_recalling_en"]

# Gatilhos descritivo-historico (mesmos da Etapa 1).
RE_DESCRITIVO_HISTORICO = re.compile(
    r"\b("
    r"science\s+wars?|"
    r"world\s+wars?|"
    r"first\s+world\s+war|second\s+world\s+war|"
    r"WW\s*[I12]+|"
    r"cold\s+wars?|"
    r"franco-?prussian\s+war|"
    r"great\s+war|"
    r"ministry\s+of\s+war|"
    r"phony\s+war|"
    r"war\s+and\s+peace|"
    r"hundred\s+years.\s*war|"
    r"thirty\s+years.\s*war"
    r")\b",
    flags=re.IGNORECASE,
)

# Padroes para bibliografia / titulo de livro citado.
RE_ANO_PARENT = re.compile(r"\((1[89]\d\d|20\d\d|19-\d?|197-|198-)\)")
EDITORAS = re.compile(
    r"\b(routledge|blackwell|harvard|princeton|gallimard|bantam|"
    r"oxford|cambridge\s+university\s+press|sage|seuil|"
    r"presses\s+universitaires|minuit|la\s+decouverte|duke\s+university)\b",
    flags=re.IGNORECASE,
)
# Sequencia de nomes capitalizados separados por "and" / "et" ou virgulas.
RE_AUTORES_SEQ = re.compile(
    r"\b[A-Z][a-zA-Z\-]+\s+(?:and|et|&)\s+[A-Z][a-zA-Z\-]+\b"
)
# Padrao de titulo entre aspas tipograficas ou italico simulado.
RE_ITALICO = re.compile(r"['‘“][A-Z][^'’”]+['’”]")

# Vocabulario metaconceitual da TAR (gatilho para metalinguistico).
TERMOS_TAR = [
    "association", "associations", "translation", "translations",
    "passage point", "actor-network", "actor network", "actor", "actors",
    "enrollment", "enrolment", "actant", "actants",
    "mediator", "mediators", "displacement",
    "AT", "ANT",  # acronimos
    "network", "networks", "networking",  # termo central da TAR
]
RE_TAR = re.compile(
    r"\b(" + "|".join(re.escape(t) for t in TERMOS_TAR) + r")\b",
    flags=re.IGNORECASE,
)
# Palavras terminadas em -ist/-ists/-ism/-isms (escolas teoricas), gatilho
# para `conceitual_debate`: ocorrencia militar aparece descrevendo polemica
# entre escolas teoricas (e.g. `pre-relativist enemies`, `reflexivists`).
RE_ISMOS = re.compile(
    r"\b[a-z][a-z\-]+(?:ist|ists|ism|isms)\b",
    flags=re.IGNORECASE,
)
# Aspas (curvas e retas) em torno da ocorrencia.
RE_ASPAS = re.compile(r"['‘’\"“”]")
# Indicadores citacionais.
RE_INDICADOR_META = re.compile(
    r"\b(vocabulary|term|terms|word|words|notion|notions|misunderstanding|"
    r"misunderstandings|misrepresented|represented|critique|criticism|"
    r"so[- ]called|the way AT is|the way ANT is|usage of|use of)\b",
    flags=re.IGNORECASE,
)


def classificar(janela_completa: str, trecho_central: str) -> tuple[str, str]:
    """Devolve (categoria_auto, gatilho_detectado).

    Ordem de prioridade: descritivo_historico > descritivo_bibliografico >
    metalinguistico > figurativo.
    """
    janela = janela_completa.lower()
    central = trecho_central.lower()

    m = RE_DESCRITIVO_HISTORICO.search(janela_completa)
    if m:
        return "descritivo_historico", f"casa '{m.group(0)}'"

    # Bibliografia: presenca de ano entre parenteses + editora ou autores
    # capitalizados sequenciais, com a ocorrencia dentro do mesmo bloco
    # citacional.
    sinais_biblio: list[str] = []
    if RE_ANO_PARENT.search(janela_completa):
        sinais_biblio.append("ano_parenteses")
    if EDITORAS.search(janela_completa):
        sinais_biblio.append("editora")
    if RE_AUTORES_SEQ.search(janela_completa):
        sinais_biblio.append("autores_sequenciais")
    if len(sinais_biblio) >= 2:
        return "descritivo_bibliografico", "+".join(sinais_biblio)

    # Metalinguistico: aspas em torno + termos TAR vizinhos OU
    # indicador citacional + termos TAR.
    n_aspas = len(RE_ASPAS.findall(janela_completa))
    n_tar = len(RE_TAR.findall(janela_completa))
    n_meta = len(RE_INDICADOR_META.findall(janela_completa))
    if n_aspas >= 2 and n_tar >= 1:
        return "metalinguistico", f"aspas={n_aspas}, tar={n_tar}"
    if n_meta >= 1 and n_tar >= 2:
        return "metalinguistico", f"indicador_meta={n_meta}, tar={n_tar}"

    # Conceitual_debate: ocorrencia militar descrevendo polemica entre
    # escolas teoricas (palavras em -ist, -ism vizinhas).
    ismos = RE_ISMOS.findall(janela_completa)
    if len(ismos) >= 2:
        return "conceitual_debate", f"ismos={ismos[:3]}"

    return "figurativo", "sem_gatilho"


def desambiguar_artigo(obra_id: str) -> list[dict[str, str]]:
    p = OUTPUTS_DIR / obra_id / "csv" / "kwic.csv"
    if not p.exists():
        return []
    saida: list[dict[str, str]] = []
    with p.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row.get("grupo") != "militar":
                continue
            if row.get("descartado_por_exclusao") == "1":
                continue
            antes = row.get("contexto_antes", "")
            central = row.get("trecho_central", "")
            depois = row.get("contexto_depois", "")
            janela = f"{antes} {central} {depois}"
            categoria, gatilho = classificar(janela, central)
            saida.append({
                "obra": obra_id,
                "pagina": row.get("pagina", ""),
                "termo": central.lower(),
                "categoria_auto": categoria,
                "gatilho_detectado": gatilho,
                "contexto_antes": antes,
                "trecho_central": central,
                "contexto_depois": depois,
                "categoria_final": categoria,
                "justificativa": f"automatico: {gatilho}",
            })
    return saida


def escrever_csv(linhas: list[dict[str, str]]) -> Path:
    ETAPA2_DIR.mkdir(parents=True, exist_ok=True)
    p = ETAPA2_DIR / "militar_classificacao_automatica.csv"
    cabecalho = [
        "obra", "pagina", "termo", "categoria_auto", "gatilho_detectado",
        "contexto_antes", "trecho_central", "contexto_depois",
        "categoria_final", "justificativa",
    ]
    with p.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cabecalho)
        w.writeheader()
        w.writerows(linhas)
    return p


def gerar_tabela_5_obras(classificadas_artigos: list[dict[str, str]]) -> Path:
    """Tabela LaTeX consolidada com contagem bruta e refinada para 5 obras."""
    # Contagem refinada dos livros vem do refinamento da Etapa 1 (fixa).
    refinada_livros = {
        "latour_woolgar_1986_lab_life_en": {"bruta": 39, "refinada": 37, "palavras": 105749, "rotulo": r"\emph{Laboratory Life} (1986)"},
        "latour_1987_science_action_en": {"bruta": 374, "refinada": 364, "palavras": 139861, "rotulo": r"\emph{Science in Action} (1987)"},
        "latour_1999_pandora_en": {"bruta": 212, "refinada": 156, "palavras": 128001, "rotulo": r"\emph{Pandora's Hope} (1999)"},
    }
    # Artigos: refinada = bruta - (descritivo_historico + descritivo_bibliografico + metalinguistico)
    artigos_brutos = {
        "latour_1996_clarifications_en": {"palavras": 7848, "rotulo": r"\emph{Clarifications} (1996)"},
        "latour_1999_recalling_en": {"palavras": 1241, "rotulo": r"\emph{Recalling ANT} (1999)"},
    }
    artigos_contagens: dict[str, dict[str, int]] = {
        oid: {"bruta": 0, "descritivo_historico": 0, "descritivo_bibliografico": 0,
              "metalinguistico": 0, "conceitual_debate": 0, "figurativo": 0}
        for oid in artigos_brutos
    }
    for linha in classificadas_artigos:
        oid = linha["obra"]
        cat = linha["categoria_auto"]
        artigos_contagens[oid]["bruta"] += 1
        artigos_contagens[oid][cat] += 1
    for oid in artigos_brutos:
        c = artigos_contagens[oid]
        c["refinada"] = c["figurativo"]

    p = ETAPA2_DIR / "tabela_militar_refinada_5_obras.tex"
    linhas = [
        r"% Tabela militar refinada para 5 obras (3 livros + 2 artigos).",
        r"% Gerada por scripts/15_etapa2_desambiguar_militar.py (Etapa 2.2).",
        r"% Contagem refinada dos livros: refinamento/militar_refinado_tres_obras.csv (Etapa 1).",
        r"% Contagem refinada dos artigos: desambiguacao automatica desta etapa.",
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption[Campo militar refinado, 5 obras de Latour]{"
        r"Densidade do campo \texttt{militar} nas tres obras monograficas e nos "
        r"dois artigos metateoricos de Latour, em contagem bruta e em contagem "
        r"refinada pela desambiguacao automatica. A refinada subtrai as "
        r"ocorrencias classificadas como descritivo-historica, "
        r"descritivo-bibliografica, metalinguistica e de polemica conceitual "
        r"entre escolas teoricas, conservando apenas o uso figural do "
        r"vocabulario militar-industrial como tropo da pratica cientifica.}",
        r"\label{tab:militar-refinado-5-obras}",
        r"\small",
        r"\begin{tabular}{lrrrrr}",
        r"\toprule",
        r"Obra & Palavras & \multicolumn{2}{c}{Contagem bruta} & \multicolumn{2}{c}{Contagem refinada} \\",
        r"\cmidrule(lr){3-4} \cmidrule(lr){5-6}",
        r" & & $n$ & freq./10k & $n$ & freq./10k \\",
        r"\midrule",
    ]
    for oid in [
        "latour_woolgar_1986_lab_life_en",
        "latour_1987_science_action_en",
        "latour_1999_pandora_en",
    ]:
        info = refinada_livros[oid]
        p_ = info["palavras"]
        b = info["bruta"]
        r_ = info["refinada"]
        linhas.append(
            f"{info['rotulo']} & {p_:,} & {b} & {b / p_ * 10000:.2f} & "
            f"{r_} & {r_ / p_ * 10000:.2f} \\\\".replace(",", r"\,")
            .replace(".", "{,}", 4)
        )
    linhas.append(r"\midrule")
    for oid in [
        "latour_1996_clarifications_en",
        "latour_1999_recalling_en",
    ]:
        info = artigos_brutos[oid]
        c = artigos_contagens[oid]
        p_ = info["palavras"]
        b = c["bruta"]
        r_ = c["refinada"]
        linhas.append(
            f"{info['rotulo']} & {p_:,} & {b} & {b / p_ * 10000:.2f} & "
            f"{r_} & {r_ / p_ * 10000:.2f} \\\\".replace(",", r"\,")
            .replace(".", "{,}", 4)
        )
    linhas += [
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}",
        "",
    ]
    p.write_text("\n".join(linhas), encoding="utf-8")
    return p


def resumir_artigos(classificadas: list[dict[str, str]]) -> str:
    """Devolve resumo em markdown da classificacao automatica dos artigos."""
    por_obra: dict[str, dict[str, int]] = {}
    for linha in classificadas:
        por_obra.setdefault(linha["obra"], {})
        cat = linha["categoria_auto"]
        por_obra[linha["obra"]][cat] = por_obra[linha["obra"]].get(cat, 0) + 1
    out: list[str] = []
    for oid, contagens in por_obra.items():
        out.append(f"### {oid}\n")
        for cat in ["descritivo_historico", "descritivo_bibliografico",
                    "metalinguistico", "conceitual_debate", "figurativo"]:
            n = contagens.get(cat, 0)
            if n:
                out.append(f"- {cat}: {n}")
        out.append("")
    return "\n".join(out)


def main() -> None:
    todas: list[dict[str, str]] = []
    for oid in ARTIGOS:
        todas.extend(desambiguar_artigo(oid))
    p_csv = escrever_csv(todas)
    print(f"  gravado: {p_csv.relative_to(REPO_ROOT)} ({len(todas)} ocorrencias)")
    p_tex = gerar_tabela_5_obras(todas)
    print(f"  gravado: {p_tex.relative_to(REPO_ROOT)}")
    print()
    print("Resumo por obra:")
    print(resumir_artigos(todas))


if __name__ == "__main__":
    main()

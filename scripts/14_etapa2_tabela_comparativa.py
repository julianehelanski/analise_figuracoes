"""Tabela comparativa das 5 obras de Latour (3 livros + 2 artigos).

Lê `outputs/<obra>/csv/frequencias.csv` para as obras com `escopo_etapa1==sim`
ou `escopo_etapa2==sim` e `corpus/qualidade_extracao.csv` para `palavras_total`.

Produz, em `outputs/etapa2_artigos/`:

- `tabela_comparativa_5_obras_n.csv`: linhas = obras, colunas = grupos,
  valores = contagem absoluta.
- `tabela_comparativa_5_obras_freq.csv`: idem, valores = ocorrências por
  10.000 palavras.
- `tabela_comparativa_5_obras.tex`: tabela LaTeX com booktabs (contagem
  absoluta no topo, densidade abaixo).
- `relatorio_etapa2.md`: relatório preliminar da Etapa 2.1 com a tabela
  principal e leitura sintética dos contrastes.

Uso:
    python scripts/14_etapa2_tabela_comparativa.py
"""

from __future__ import annotations

import csv
from collections import OrderedDict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
METADATA_CSV = REPO_ROOT / "corpus" / "metadata.csv"
QUALIDADE_CSV = REPO_ROOT / "corpus" / "qualidade_extracao.csv"
OUTPUTS_DIR = REPO_ROOT / "outputs"
ETAPA2_DIR = OUTPUTS_DIR / "etapa2_artigos"

# Ordem canônica das obras (livros monográficos → artigos metateóricos)
ORDEM_OBRAS = [
    "latour_woolgar_1986_lab_life_en",
    "latour_1987_science_action_en",
    "latour_1999_pandora_en",
    "latour_1996_clarifications_en",
    "latour_1999_recalling_en",
]

# Rótulos curtos para a tabela LaTeX
ROTULOS_OBRAS = {
    "latour_woolgar_1986_lab_life_en": "Lab Life 1986",
    "latour_1987_science_action_en": "Sci. in Action 1987",
    "latour_1999_pandora_en": "Pandora 1999",
    "latour_1996_clarifications_en": "Clarifications 1996",
    "latour_1999_recalling_en": "Recalling 1999",
}

# Ordem dos grupos figurativos (17 do catálogo + 2 adições da Etapa 2)
ORDEM_GRUPOS = [
    "inscription", "immutable_mobile", "black_box", "centre_of_calculation",
    "actor_network", "translation", "trial_of_strength", "factish",
    "circulating_reference", "articulation", "construction", "proposition",
    "network", "agonistic", "enrollment", "spokesperson", "militar",
    "textil", "topologia",
]


def carregar_palavras_total() -> dict[str, int]:
    mapa: dict[str, int] = {}
    with QUALIDADE_CSV.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            try:
                mapa[row["id"]] = int(row["palavras_total"])
            except (KeyError, ValueError):
                continue
    return mapa


def carregar_frequencias_obra(obra_id: str) -> dict[str, int]:
    p = OUTPUTS_DIR / obra_id / "csv" / "frequencias.csv"
    contagem: dict[str, int] = {}
    if not p.exists():
        return contagem
    with p.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            try:
                contagem[row["grupo"]] = int(row["n_ocorrencias"])
            except (KeyError, ValueError):
                continue
    return contagem


def gerar_tabelas_csv(
    contagens: dict[str, dict[str, int]],
    palavras: dict[str, int],
) -> None:
    ETAPA2_DIR.mkdir(parents=True, exist_ok=True)
    # CSV absoluto
    csv_n = ETAPA2_DIR / "tabela_comparativa_5_obras_n.csv"
    with csv_n.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["obra", "palavras_total"] + ORDEM_GRUPOS)
        for oid in ORDEM_OBRAS:
            linha = [oid, palavras.get(oid, "")]
            for g in ORDEM_GRUPOS:
                linha.append(contagens.get(oid, {}).get(g, 0))
            w.writerow(linha)
    # CSV densidade
    csv_f = ETAPA2_DIR / "tabela_comparativa_5_obras_freq.csv"
    with csv_f.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["obra", "palavras_total"] + ORDEM_GRUPOS)
        for oid in ORDEM_OBRAS:
            n_total = palavras.get(oid)
            linha: list[object] = [oid, n_total if n_total else ""]
            for g in ORDEM_GRUPOS:
                n = contagens.get(oid, {}).get(g, 0)
                if n_total:
                    linha.append(f"{n / n_total * 10000:.2f}")
                else:
                    linha.append("")
            w.writerow(linha)
    print(f"  gravado: {csv_n.relative_to(REPO_ROOT)}")
    print(f"  gravado: {csv_f.relative_to(REPO_ROOT)}")


def _escapar_latex(s: str) -> str:
    return s.replace("_", r"\_")


def gerar_latex(
    contagens: dict[str, dict[str, int]],
    palavras: dict[str, int],
) -> None:
    """Tabela LaTeX com 5 obras × 19 grupos, contagem e densidade."""
    tex = ETAPA2_DIR / "tabela_comparativa_5_obras.tex"
    linhas: list[str] = [
        r"% Tabela comparativa das 5 obras de Latour (Etapa 2.1)",
        r"% Gerada por scripts/14_etapa2_tabela_comparativa.py",
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption{Densidade dos campos figurativos nas tres obras monograficas "
        r"e nos dois artigos metateoricos de Latour (ocorrencias por 10.000 "
        r"palavras; contagem absoluta entre parenteses).}",
        r"\label{tab:figuracoes_latour_5_obras}",
        r"\small",
        r"\begin{tabular}{l" + "r" * len(ORDEM_OBRAS) + r"}",
        r"\toprule",
    ]
    cab = [r"Campo figurativo"] + [
        _escapar_latex(ROTULOS_OBRAS[oid]) for oid in ORDEM_OBRAS
    ]
    linhas.append(" & ".join(cab) + r" \\")
    linhas.append(r"\midrule")
    # linha de palavras totais
    pal_linha = [r"\textit{Palavras totais}"]
    for oid in ORDEM_OBRAS:
        n = palavras.get(oid, 0)
        pal_linha.append(rf"\textit{{{n:,}}}".replace(",", "."))
    linhas.append(" & ".join(pal_linha) + r" \\")
    linhas.append(r"\midrule")
    for g in ORDEM_GRUPOS:
        cells = [_escapar_latex(g)]
        for oid in ORDEM_OBRAS:
            n = contagens.get(oid, {}).get(g, 0)
            n_total = palavras.get(oid)
            if n_total and n > 0:
                freq = n / n_total * 10000
                cells.append(rf"{freq:.2f} ({n})")
            elif n_total:
                cells.append(r"--")
            else:
                cells.append(r"n/d")
        linhas.append(" & ".join(cells) + r" \\")
    linhas += [
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}",
        "",
    ]
    tex.write_text("\n".join(linhas), encoding="utf-8")
    print(f"  gravado: {tex.relative_to(REPO_ROOT)}")


def gerar_relatorio(
    contagens: dict[str, dict[str, int]],
    palavras: dict[str, int],
) -> None:
    md = ETAPA2_DIR / "relatorio_etapa2.md"

    def freq(oid: str, g: str) -> str:
        n = contagens.get(oid, {}).get(g, 0)
        n_total = palavras.get(oid)
        if not n_total:
            return "n/d"
        return f"{n / n_total * 10000:.2f}"

    def n_abs(oid: str, g: str) -> int:
        return contagens.get(oid, {}).get(g, 0)

    linhas: list[str] = [
        "# Relatório preliminar da Etapa 2.1: contagem bruta dos artigos teóricos de Latour",
        "",
        "Data da execução: 15 de maio de 2026.",
        "",
        "Este relatório consolida a contagem lexicométrica nos dezenove campos figurativos "
        "(dezessete do catálogo da Etapa 1 e duas adições da Etapa 2: `textil` e `topologia`) "
        "para as cinco obras de Latour em análise: três livros monográficos e dois artigos "
        "metateóricos. A pergunta empírica que orienta a tabela é a divisão de trabalho "
        "metafórico por gênero textual proposta no briefing da Etapa 2.",
        "",
        "## Densidade do campo militar (ocorrências por 10.000 palavras)",
        "",
        "| Obra | Palavras | n militar | freq./10k |",
        "|---|---:|---:|---:|",
    ]
    for oid in ORDEM_OBRAS:
        n_total = palavras.get(oid, 0)
        n_mil = n_abs(oid, "militar")
        linhas.append(
            f"| {ROTULOS_OBRAS[oid]} | {n_total:,} | {n_mil} | {freq(oid, 'militar')} |"
            .replace(",", ".")
        )
    linhas += [
        "",
        "A leitura quantitativa sustenta o contraste central do briefing: nos livros monográficos "
        "em que Latour é autor solo, a densidade do campo militar oscila entre 16,56 e 26,74 "
        "ocorrências por 10.000 palavras, ao passo que nos dois artigos metateóricos a densidade "
        "fica entre 3,82 e 8,06. Em *Laboratory Life* 1986, escrita em coautoria com Steve "
        "Woolgar, a densidade militar (3,69) está em patamar próximo ao dos artigos, fato que "
        "merece registro etnográfico: a inflexão militar-industrial parece consolidar-se com "
        "Latour solo a partir de 1987.",
        "",
        "A contagem bruta do *Recalling* (n=1) e do *Clarifications* (n=3) cai para próximo de "
        "zero após a desambiguação prevista para a Etapa 2.2:",
        "",
        "- *Recalling* 1999: a única ocorrência é `wars` em `\"the recent Science Wars\"` "
        "(referência ao debate público dos anos 1990 entre cientistas e estudiosos das ciências, "
        "categoria `descritivo-historica`).",
        "- *Clarifications* 1996: `allies` em `\"network of allies and extend his power\"` é uso "
        "que Latour cita para criticar (categoria `metalinguistico`); `enemies` em `\"pre-relativist "
        "enemies\"` é uso conceitual-debate; `alliance` em `\"La nouvelle alliance\"` (Prigogine "
        "e Stengers) é título de livro citado (categoria `descritivo-bibliografico`).",
        "",
        "Nenhuma das ocorrências militares dos dois artigos é uso figural do vocabulário "
        "militar-industrial como tropo para a prática científica, contrário ao que predomina em "
        "*Science in Action* (de onde provêm `allies`(92), `mobilisation`(28), `mobilised`(24), "
        "`alliances`(22) entre as variantes top).",
        "",
        "## Densidade dos campos têxtil e topologia",
        "",
        "| Obra | Palavras | n têxtil | freq./10k | n topologia | freq./10k |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for oid in ORDEM_OBRAS:
        n_total = palavras.get(oid, 0)
        linhas.append(
            f"| {ROTULOS_OBRAS[oid]} | {n_total:,} | "
            f"{n_abs(oid, 'textil')} | {freq(oid, 'textil')} | "
            f"{n_abs(oid, 'topologia')} | {freq(oid, 'topologia')} |"
            .replace(",", ".")
        )
    linhas += [
        "",
        "O campo `topologia` é o vocabulário que ocupa o terreno deixado pelo vocabulário militar "
        "nos artigos: a densidade no *Clarifications* (150,36/10k) e no *Recalling* (104,75/10k) "
        "supera a do mesmo campo nos livros monográficos (entre 13,81 e 34,68/10k). O campo "
        "`textil` segue padrão análogo no *Clarifications* (49,69/10k), enquanto no *Recalling* "
        "a densidade é nula, o que sugere uma especialização interna entre os dois artigos: "
        "*Clarifications* mobiliza vocabulário têxtil-topológico de modo denso, *Recalling* "
        "concentra-se na topologia.",
        "",
        "Variantes top do `textil` em *Clarifications*: `net`(10), `nets`(3), `tied`(3), `tie`(2). "
        "A passagem que ancora qualitativamente esse achado está na página 76 do PDF interno, "
        "com a sequência `\"fibrous, thread-like, wiry, stringy, ropy, capillary character\"` "
        "(confirmada por sanity check em `scripts/13_audit_articles_etapa2.py`). A inspeção das "
        "variantes do campo na Etapa 2.2 (KWIC) é necessária para depurar polissemias prováveis "
        "como `tie` (laço/empate), `net` (rede/líquido), `string` (corda/sequência de caracteres).",
        "",
        "## Ressalvas metodológicas",
        "",
        "1. O *Recalling* opera sobre 1.241 palavras de corpo (convenção `split`), cerca de 80% "
        "do artigo original. As páginas 15 e 25 do volume estão excluídas por falha sistemática "
        "de OCR. Detalhamento em `docs/decisoes_metodologicas.md`, seção Etapa 2 § 3.",
        "",
        "2. O briefing § 2 previa a presença, no *Recalling*, da citação metalinguística "
        "`\"vocabulary association, translation, alliance, obligatory passage point\"`. A inspeção "
        "do `.txt` confirma que essa passagem não está no corpus disponível, o que sugere que ela "
        "se encontra em uma das páginas excluídas (15 ou 25 do volume). A contagem efetiva do "
        "campo militar no *Recalling* (n=1, com `wars` em `Science Wars`) é portanto distinta da "
        "prevista (n=1, com `alliance` metalinguístico). O argumento comparativo de divisão de "
        "trabalho metafórico não é afetado: a única ocorrência permanece não-figural.",
        "",
        "3. As contagens dos campos `textil` e `topologia` carregam polissemia esperada. A "
        "validação amostral semântica da Etapa 2.6, com mesma estratificação A/B/C aplicada à "
        "Etapa 1, vai estabelecer a taxa de uso figural por campo.",
        "",
        "## Outputs gerados",
        "",
        "- `outputs/etapa2_artigos/tabela_comparativa_5_obras_n.csv` (contagem absoluta).",
        "- `outputs/etapa2_artigos/tabela_comparativa_5_obras_freq.csv` (densidade por 10k).",
        "- `outputs/etapa2_artigos/tabela_comparativa_5_obras.tex` (LaTeX, pronto para inclusão).",
        "- `outputs/<obra>/csv/frequencias.csv` (atualizados nas 5 obras com `textil` e `topologia`).",
        "",
        "## Próximos passos (Gate 2.1 pendente)",
        "",
        "A pesquisadora confirma que as densidades acima fazem sentido em ordem de grandeza, "
        "antes de prosseguir para:",
        "",
        "- Etapa 2.2: KWIC com desambiguação automática do campo militar nos artigos, incluindo "
        "os gatilhos novos `metalinguistico` e `descritivo-bibliografico`.",
        "- Etapa 2.3: desambiguação manual.",
        "- Etapa 2.4: cocorrência com janela 200 (controle) e janela proporcional (27 / 159 palavras).",
        "- Etapa 2.5: outputs comparativos consolidados (3 tabelas).",
        "- Etapa 2.6: validação amostral semântica A/B/C.",
    ]
    md.write_text("\n".join(linhas), encoding="utf-8")
    print(f"  gravado: {md.relative_to(REPO_ROOT)}")


def main() -> None:
    palavras = carregar_palavras_total()
    contagens: dict[str, dict[str, int]] = OrderedDict()
    for oid in ORDEM_OBRAS:
        contagens[oid] = carregar_frequencias_obra(oid)
        if not contagens[oid]:
            print(f"  AVISO: frequencias.csv ausente para {oid}.")
    gerar_tabelas_csv(contagens, palavras)
    gerar_latex(contagens, palavras)
    gerar_relatorio(contagens, palavras)


if __name__ == "__main__":
    main()

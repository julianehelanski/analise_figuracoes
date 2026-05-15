"""Tabela comparativa de cocorrencia para os dois artigos (Etapa 2.4).

Consolida as matrizes de cocorrencia geradas por
`scripts/05_cooccurrence.py` em duas janelas (200 palavras como controle
e janela proporcional 2% do texto) em uma tabela comparativa unica,
em CSV, LaTeX e markdown.

A janela proporcional foi calculada sobre `palavras_total` em convencao
`split` registrada em `corpus/qualidade_extracao.csv`:

- Recalling 1999: 1.241 palavras x 2% = 25 palavras.
- Clarifications 1996: 7.848 palavras x 2% = 157 palavras.

Uso:
    python scripts/16_etapa2_cocorrencia_comparacao.py
"""

from __future__ import annotations

import csv
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = REPO_ROOT / "outputs"
ETAPA2_DIR = OUTPUTS_DIR / "etapa2_artigos"

ARTIGOS = {
    "latour_1996_clarifications_en": {
        "rotulo": "Clarifications 1996",
        "palavras": 7848,
        "janela_proporcional": 157,
        "sufixo_proporcional": "j157",
    },
    "latour_1999_recalling_en": {
        "rotulo": "Recalling 1999",
        "palavras": 1241,
        "janela_proporcional": 25,
        "sufixo_proporcional": "j025",
    },
}


def carregar_pares(obra_id: str, sufixo: str) -> dict[tuple[str, str], int]:
    """Le a matriz cocorrencia<sufixo>.csv e devolve dict de pares."""
    p = OUTPUTS_DIR / obra_id / "csv" / f"cocorrencia_{sufixo}.csv"
    if not p.exists():
        return {}
    pares: dict[tuple[str, str], int] = {}
    with p.open(encoding="utf-8", newline="") as f:
        leitor = csv.reader(f)
        cab = next(leitor)
        grupos = cab[1:]
        for i, linha in enumerate(leitor):
            for j in range(i + 1, len(grupos)):
                try:
                    n = int(linha[j + 1])
                except (IndexError, ValueError):
                    n = 0
                if n > 0:
                    pares[tuple(sorted([grupos[i], grupos[j]]))] = n
    return pares


def montar_relatorio() -> None:
    ETAPA2_DIR.mkdir(parents=True, exist_ok=True)
    md = ETAPA2_DIR / "cocorrencia_comparacao.md"
    linhas: list[str] = [
        "# Cocorrência figural nos artigos teóricos (Etapa 2.4)",
        "",
        "Data da execução: 15 de maio de 2026.",
        "",
        "Apliquei `scripts/05_cooccurrence.py` aos dois artigos em duas configurações de janela:",
        "",
        "- **Janela 200 palavras**: controle direto, mesma janela usada nos livros da Etapa 1. "
        "Permite comparação entre os artigos e os livros, mas em textos curtos cobre proporção "
        "alta do total (15% no *Recalling*, 2,5% no *Clarifications*), o que produz pares "
        "espúrios por aproximação física no texto.",
        "- **Janela proporcional**: 2% das palavras totais por obra, arredondada. "
        "Recalling = 25 palavras; Clarifications = 157 palavras. Padroniza a fração textual da "
        "janela entre obras, ao custo de tornar a comparação direta com os livros indireta.",
        "",
        "A decisão sobre qual janela apresentar na tese cabe à pesquisadora.",
        "",
    ]
    for obra_id, info in ARTIGOS.items():
        pares_j200 = carregar_pares(obra_id, "j200")
        pares_prop = carregar_pares(obra_id, info["sufixo_proporcional"])
        todos = sorted(
            set(pares_j200) | set(pares_prop),
            key=lambda k: -(pares_j200.get(k, 0) + pares_prop.get(k, 0)),
        )
        linhas += [
            f"## {info['rotulo']} ({info['palavras']:,} palavras)".replace(",", "."),
            "",
            f"Janela controle: 200 palavras. Janela proporcional: "
            f"{info['janela_proporcional']} palavras (2% do texto).",
            "",
            f"Pares com cocorrência em pelo menos uma das duas janelas: {len(todos)}.",
            "",
            "| par (A, B) | j=200 | "
            f"j={info['janela_proporcional']} (prop.) |",
            "|---|---:|---:|",
        ]
        for par in todos:
            a, b = par
            n200 = pares_j200.get(par, 0)
            np = pares_prop.get(par, 0)
            linhas.append(f"| {a}, {b} | {n200} | {np} |")
        linhas.append("")
    linhas += [
        "## Leitura sintética dos contrastes",
        "",
        "Em ambas as obras, os pares com maior força são consistentes entre as duas janelas: "
        "`network`–`topologia` lidera por margem larga (783/616 em *Clarifications*; 20/2 em "
        "*Recalling*), seguido por `actor_network`–`network` e `textil`–`topologia` (este "
        "último presente apenas no *Clarifications*, onde o campo têxtil tem ocorrências; no "
        "*Recalling* o campo têxtil é zero, então não há pares têxtil).",
        "",
        "O campo `militar` ocupa posição periférica em ambas as obras. Pares envolvendo "
        "`militar` aparecem em ordens de grandeza menores que `network`–`topologia` "
        "(*Clarifications* j=157: `militar`–`network` = 8 versus `network`–`topologia` = 616). "
        "A leitura confirma o achado da Etapa 2.2: o vocabulário militar não articula a malha "
        "argumentativa central dos artigos metateóricos; a malha é estruturada por "
        "`network`–`topologia` e suas extensões `actor_network` e `textil`.",
        "",
        "## Decisão recomendada (pendente Gate 2.4)",
        "",
        "Para a tese, sugiro apresentar a **janela proporcional** como configuração principal, "
        "com a janela 200 como controle metodológico em nota de rodapé. A janela proporcional "
        "controla o problema do tamanho do texto e preserva o ranking dos pares centrais. A "
        "janela 200 fica disponível como ponto de comparação com os livros, dado que a Etapa 1 "
        "operou com janela 200.",
        "",
        "A pesquisadora decide se a recomendação é aceita, ou se a tese apresenta as duas "
        "configurações lado a lado com nota metodológica explícita.",
        "",
        "## Outputs gerados",
        "",
        "- `outputs/<obra>/csv/cocorrencia_j200.csv` (controle).",
        "- `outputs/<obra>/csv/cocorrencia_j025.csv` ou `_j157.csv` (proporcional).",
        "- `outputs/<obra>/relatorios/cocorrencia_j200.md` e variantes.",
        "- `outputs/<obra>/figuras/rede_cocorrencia_j200.png` e variantes (PNG + SVG).",
        "- `outputs/etapa2_artigos/cocorrencia_comparacao.md` (este arquivo).",
    ]
    md.write_text("\n".join(linhas), encoding="utf-8")
    print(f"  gravado: {md.relative_to(REPO_ROOT)}")


def main() -> None:
    montar_relatorio()


if __name__ == "__main__":
    main()

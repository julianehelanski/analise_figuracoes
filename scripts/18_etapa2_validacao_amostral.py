"""Validacao amostral semantica em tres camadas (A/B/C) para os artigos.

Implementa o passo 2.6 do briefing § 3.6 e § 5: gera planilhas
estratificadas em tres camadas que a pesquisadora preenche manualmente
para aferir a taxa de uso figural dos termos por campo e por obra.

O protocolo A/B/C nao tinha implementacao previa neste repositorio
(o `08_validate_sample.py` valida classificacao de pagina, nao semantica).
A definicao aqui aplicada e documentada em
`docs/decisoes_metodologicas.md` § Etapa 2 § 12:

- **Camada A** (top-densidade): n ocorrencias por campo cuja janela
  KWIC tem o maior numero de termos do mesmo campo lexical na vizinhanca
  imediata. Heuristica: passagens onde o campo aparece de modo
  concentrado, candidatas a uso central.
- **Camada B** (aleatoria): n ocorrencias aleatorias por campo, seed=42.
- **Camada C** (variantes raras): n ocorrencias por campo cuja variante
  (`termo_encontrado`) e a menos frequente no campo, mais suspeita de
  polissemia ou uso periferico.

Quando o campo tem menos de 3*n ocorrencias, a amostra e exaustiva
(todas as ocorrencias entram, com a camada marcada como `exaustiva`).

Campos validados: textil, topologia, network, actor_network. Sao os
campos centrais do argumento textil-topologico da Etapa 2. O campo
militar nao entra (ja foi 100% desambiguado na Etapa 2.2).

Output (por artigo + consolidado):
- `outputs/<artigo>/csv/validacao_amostral_semantica.csv`
- `outputs/etapa2_artigos/validacao_amostral_semantica.csv` (consolidado)

A planilha tem colunas pre-preenchidas (obra, campo, camada, termo,
contexto) e colunas em branco para a pesquisadora:
- uso_figural (sim/parcial/nao)
- subcategoria (texto livre; ex.: tecnico, polissemia, descritivo)
- comentario

Uso:
    python scripts/18_etapa2_validacao_amostral.py
"""

from __future__ import annotations

import csv
import random
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = REPO_ROOT / "outputs"
ETAPA2_DIR = OUTPUTS_DIR / "etapa2_artigos"

ARTIGOS = ["latour_1996_clarifications_en", "latour_1999_recalling_en"]
CAMPOS_VALIDADOS = ["textil", "topologia", "network", "actor_network"]
N_POR_CAMADA = 5
SEED = 42

# Cabecalho da planilha
CABECALHO = [
    "obra", "campo", "camada", "id_kwic",
    "pagina", "termo_encontrado",
    "contexto_antes", "trecho_central", "contexto_depois",
    "uso_figural", "subcategoria", "comentario",
]


def carregar_kwic_campo(obra_id: str, campo: str) -> list[dict[str, str]]:
    """Le KWIC e devolve ocorrencias validas do campo solicitado."""
    p = OUTPUTS_DIR / obra_id / "csv" / "kwic.csv"
    if not p.exists():
        return []
    saida: list[dict[str, str]] = []
    with p.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row.get("grupo") != campo:
                continue
            if row.get("descartado_por_exclusao") == "1":
                continue
            saida.append(row)
    return saida


def densidade_janela(row: dict[str, str], todos_termos: set[str]) -> int:
    """Conta quantos termos do campo aparecem na janela KWIC.

    Heuristica para a camada A: ocorrencias com janela densa em termos
    do mesmo campo lexical sao candidatas a uso central.
    """
    janela = (
        f"{row['contexto_antes']} {row['trecho_central']} {row['contexto_depois']}"
    ).lower()
    return sum(1 for t in todos_termos if t in janela)


def amostrar(ocs: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    """Devolve dict {camada -> lista de ocorrencias}.

    Quando ocs tem menos de 3*N_POR_CAMADA elementos, amostra exaustiva.
    """
    if len(ocs) < 3 * N_POR_CAMADA:
        return {"exaustiva": list(ocs)}

    todos_termos = {row["termo_encontrado"].lower() for row in ocs}

    # A: top-densidade
    por_densidade = sorted(
        ocs, key=lambda r: -densidade_janela(r, todos_termos),
    )
    a = por_densidade[:N_POR_CAMADA]

    # B: aleatoria (com seed)
    rng = random.Random(SEED)
    candidatos_b = [r for r in ocs if r not in a]
    b = rng.sample(candidatos_b, min(N_POR_CAMADA, len(candidatos_b)))

    # C: variantes raras (menos frequentes no campo)
    freq_variante = Counter(r["termo_encontrado"].lower() for r in ocs)
    raras = sorted(freq_variante.items(), key=lambda x: x[1])
    variantes_raras = {v for v, _ in raras[:max(1, len(raras) // 3)]}
    candidatos_c = [
        r for r in ocs
        if r["termo_encontrado"].lower() in variantes_raras
        and r not in a and r not in b
    ]
    if len(candidatos_c) < N_POR_CAMADA:
        # complementa com proximas variantes menos frequentes
        extras = [
            r for r in ocs
            if r not in a and r not in b and r not in candidatos_c
        ]
        extras = sorted(
            extras, key=lambda r: freq_variante[r["termo_encontrado"].lower()],
        )
        candidatos_c = candidatos_c + extras
    c = candidatos_c[:N_POR_CAMADA]

    return {"A_top_densidade": a, "B_aleatoria": b, "C_variantes_raras": c}


def montar_linha(
    row: dict[str, str], obra_id: str, campo: str, camada: str, idx: int,
) -> dict[str, str]:
    return {
        "obra": obra_id,
        "campo": campo,
        "camada": camada,
        "id_kwic": f"{obra_id}#{campo}#{idx:04d}",
        "pagina": row.get("pagina", ""),
        "termo_encontrado": row.get("termo_encontrado", ""),
        "contexto_antes": row.get("contexto_antes", ""),
        "trecho_central": row.get("trecho_central", ""),
        "contexto_depois": row.get("contexto_depois", ""),
        "uso_figural": "",
        "subcategoria": "",
        "comentario": "",
    }


def main() -> None:
    consolidado: list[dict[str, str]] = []
    contagem_por_obra_campo: dict[tuple[str, str], dict[str, int]] = defaultdict(dict)

    for obra_id in ARTIGOS:
        linhas_obra: list[dict[str, str]] = []
        for campo in CAMPOS_VALIDADOS:
            ocs = carregar_kwic_campo(obra_id, campo)
            amostra = amostrar(ocs)
            for camada, rows in amostra.items():
                contagem_por_obra_campo[(obra_id, campo)][camada] = len(rows)
                for i, row in enumerate(rows):
                    linha = montar_linha(row, obra_id, campo, camada, i)
                    linhas_obra.append(linha)
                    consolidado.append(linha)
        # Salva por obra
        p_obra = OUTPUTS_DIR / obra_id / "csv" / "validacao_amostral_semantica.csv"
        p_obra.parent.mkdir(parents=True, exist_ok=True)
        with p_obra.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=CABECALHO)
            w.writeheader()
            w.writerows(linhas_obra)
        print(f"  gravado: {p_obra.relative_to(REPO_ROOT)} ({len(linhas_obra)} linhas)")

    # Consolidado
    p_cons = ETAPA2_DIR / "validacao_amostral_semantica.csv"
    p_cons.parent.mkdir(parents=True, exist_ok=True)
    with p_cons.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CABECALHO)
        w.writeheader()
        w.writerows(consolidado)
    print(f"  gravado: {p_cons.relative_to(REPO_ROOT)} ({len(consolidado)} linhas)")

    # Relatorio com instrucoes
    p_rel = ETAPA2_DIR / "validacao_amostral_instrucoes.md"
    linhas_rel = [
        "# Validação amostral semântica (Etapa 2.6): instruções de preenchimento",
        "",
        "Data da geração: 15 de maio de 2026.",
        "",
        f"As planilhas em `outputs/<artigo>/csv/validacao_amostral_semantica.csv` "
        f"e o consolidado em `outputs/etapa2_artigos/validacao_amostral_semantica.csv` "
        f"contêm {len(consolidado)} ocorrências para classificação manual nos quatro "
        "campos centrais do argumento têxtil-topológico: `textil`, `topologia`, "
        "`network`, `actor_network`. O campo `militar` está fora desta amostra (já "
        "100% desambiguado na Etapa 2.2).",
        "",
        "## Distribuição da amostra",
        "",
        "| Obra | Campo | Camada | n |",
        "|---|---|---|---:|",
    ]
    for (obra, campo), camadas in sorted(contagem_por_obra_campo.items()):
        for camada, n in camadas.items():
            linhas_rel.append(f"| {obra} | {campo} | {camada} | {n} |")
    linhas_rel += [
        "",
        "## Protocolo de três camadas (A/B/C)",
        "",
        "Para cada campo com 15 ou mais ocorrências, sorteio três amostras "
        "independentes de cinco ocorrências cada:",
        "",
        "- **Camada A — top-densidade**: ocorrências cuja janela KWIC tem o maior "
        "número de termos do mesmo campo lexical. Heurística: passagens onde o "
        "campo aparece de modo concentrado.",
        "- **Camada B — aleatória**: cinco ocorrências aleatórias (seed=42).",
        "- **Camada C — variantes raras**: ocorrências cuja variante (termo "
        "exato) é das menos frequentes no campo. Heurística: mais suspeitas de "
        "polissemia ou uso periférico.",
        "",
        "Quando o campo tem menos de 15 ocorrências (caso comum no *Recalling*), "
        "a amostra é exaustiva (todas as ocorrências entram, camada `exaustiva`).",
        "",
        "## Colunas para preenchimento manual",
        "",
        "- `uso_figural` (`sim`, `parcial`, `nao`): a ocorrência é uso figural "
        "do campo no sentido da tese? Tropo têxtil-topológico para descrever "
        "ANT, rede ou prática científica?",
        "- `subcategoria` (texto livre): se `nao`, classificar o motivo. "
        "Sugestões: `tecnico` (uso técnico do termo, e.g. `tie` como verbo, "
        "`net` como rede de computadores), `polissemia` (termo em sentido "
        "comum), `descritivo` (descrição de objeto não-figural), `metalinguistico` "
        "(Latour cita o próprio vocabulário).",
        "- `comentario` (texto livre): observação metodológica que valha registro "
        "etnográfico (ex.: discordância com a classificação automática anterior, "
        "candidatos a citação na tese, casos-limite).",
        "",
        "## Procedimento sugerido",
        "",
        "1. Abrir o CSV consolidado em planilha (ou um por obra).",
        "2. Ler cada linha (`contexto_antes` + **`trecho_central`** + `contexto_depois`).",
        "3. Marcar `uso_figural`; em casos `nao` ou `parcial`, anotar `subcategoria`.",
        "4. Usar `comentario` para registrar discordâncias e candidatos a citação.",
        "5. Salvar e me avisar quando terminar. Gero então:",
        "   - Taxa de uso figural por campo e por camada (precisão estimada).",
        "   - Lista das `subcategoria` mais frequentes (mapa de polissemia).",
        "   - Densidade refinada figural para `textil` e `topologia` (com base na "
        "taxa de figuralidade aplicada à contagem bruta).",
        "",
        "## Após o preenchimento",
        "",
        "A pesquisadora me devolve a planilha preenchida. Gero:",
        "",
        "- `outputs/etapa2_artigos/validacao_amostral_resultados.md` com as taxas.",
        "- `outputs/etapa2_artigos/tabela_textil_topologico_refinada.tex` com a "
        "densidade refinada (bruta × taxa de figuralidade).",
        "- Atualização do relatório consolidado da Etapa 2.",
    ]
    p_rel.write_text("\n".join(linhas_rel), encoding="utf-8")
    print(f"  gravado: {p_rel.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()

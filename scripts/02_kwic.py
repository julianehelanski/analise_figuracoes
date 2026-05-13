"""KWIC (Keyword in Context) sobre o corpus extraído.

Implementa a Etapa 1 do plano de trabalho. Para cada termo de um campo
lexical, percorre o texto de uma obra e gera uma linha CSV por ocorrência,
com janela configurável de palavras antes e depois.

Uso típico:

    python scripts/02_kwic.py \\
        --texto corpus/txt/haraway_2016_staying_with_the_trouble.txt \\
        --campo campos_lexicais/haraway_textil_en.txt \\
        --obra haraway_2016_staying_with_the_trouble \\
        --janela 50 \\
        --saida outputs/csv/etapa1/haraway_2016_textil.csv

Tratamento de notas de rodapé: o script tenta detectar linhas com padrão
de número-de-nota seguidas de quebra. Cada linha que parece ser nota é
marcada com a coluna `provavel_nota_rodape=1` para que a Juliane possa
filtrar depois, mas não é eliminada cegamente.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class GrupoTerminologico:
    """Grupo de variantes morfológicas de um mesmo termo canônico."""

    canonico: str
    variantes: tuple[str, ...]


def carregar_campo_lexical(caminho: Path) -> list[GrupoTerminologico]:
    """Lê arquivo de campo lexical.

    Formato esperado:
        - Uma linha por grupo terminológico.
        - Variantes separadas por vírgula. Primeira variante = forma canônica.
        - `#` e linhas vazias são ignoradas.
        - Texto entre parênteses é comentário e é descartado.
    """
    grupos: list[GrupoTerminologico] = []
    for linha_raw in caminho.read_text(encoding="utf-8").splitlines():
        # Remove comentários entre parênteses.
        linha = re.sub(r"\([^)]*\)", "", linha_raw).strip()
        if not linha or linha.startswith("#"):
            continue
        tokens = [t.strip().lower() for t in linha.split(",") if t.strip()]
        if not tokens:
            continue
        grupos.append(GrupoTerminologico(canonico=tokens[0], variantes=tuple(tokens)))
    return grupos


def compilar_padroes(
    grupos: list[GrupoTerminologico],
) -> list[tuple[GrupoTerminologico, re.Pattern[str]]]:
    """Compila um regex por grupo, casando qualquer variante com word-boundaries.

    Expressões compostas (com espaço) viram `\\s+` para tolerar quebras de linha.
    O apóstrofo curvo (’) é tratado como equivalente ao reto (').
    """
    padroes: list[tuple[GrupoTerminologico, re.Pattern[str]]] = []
    for grupo in grupos:
        alternativas: list[str] = []
        for variante in grupo.variantes:
            # Escapa, depois generaliza espaços e apóstrofos.
            escapada = re.escape(variante)
            escapada = escapada.replace(r"\ ", r"\s+")
            escapada = escapada.replace(r"\'", r"['’]")
            alternativas.append(rf"\b{escapada}\b")
        padrao = re.compile("|".join(alternativas), flags=re.IGNORECASE)
        padroes.append((grupo, padrao))
    return padroes


def localizar_palavras(texto: str) -> list[tuple[int, int]]:
    """Retorna lista de (inicio, fim) em caracteres para cada palavra do texto."""
    return [(m.start(), m.end()) for m in re.finditer(r"\S+", texto)]


def janela_kwic(
    texto: str,
    palavras: list[tuple[int, int]],
    inicio_match: int,
    fim_match: int,
    janela: int,
) -> tuple[str, str, str]:
    """Extrai contexto de N palavras antes/depois do match.

    Retorna (contexto_antes, trecho_central, contexto_depois), cada um já com
    quebras de linha colapsadas em espaço único.
    """
    indice_central = next(
        (i for i, (a, b) in enumerate(palavras) if a <= inicio_match < b),
        None,
    )
    if indice_central is None:
        return "", texto[inicio_match:fim_match], ""
    indice_final = next(
        (i for i, (a, b) in enumerate(palavras) if a < fim_match <= b),
        indice_central,
    )
    ini_antes = max(0, indice_central - janela)
    fim_depois = min(len(palavras), indice_final + 1 + janela)

    def trecho(ini_pal: int, fim_pal: int) -> str:
        if ini_pal >= fim_pal:
            return ""
        return texto[palavras[ini_pal][0]:palavras[fim_pal - 1][1]]

    antes = trecho(ini_antes, indice_central)
    central = texto[inicio_match:fim_match]
    depois = trecho(indice_final + 1, fim_depois)
    return _normalizar_espacos(antes), central, _normalizar_espacos(depois)


def _normalizar_espacos(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


_PADRAO_NOTA = re.compile(r"^\s*\d{1,3}\s+[A-Za-zÀ-ÿ]")


def parece_nota_rodape(texto: str, posicao: int) -> bool:
    """Heurística simples: a linha que contém a posição começa com número curto?

    Detecta uma fração das notas; não é exaustivo. A Juliane usa essa coluna
    como filtro indicativo, não como verdade.
    """
    inicio_linha = texto.rfind("\n", 0, posicao) + 1
    fim_linha = texto.find("\n", posicao)
    linha = texto[inicio_linha:fim_linha if fim_linha != -1 else len(texto)]
    return bool(_PADRAO_NOTA.match(linha))


def estimar_pagina(posicao: int, total_caracteres: int, total_paginas: int | None) -> str:
    """Estima número de página por interpolação linear de caracteres."""
    if not total_paginas or total_caracteres <= 0:
        return ""
    pagina = 1 + int(posicao / total_caracteres * total_paginas)
    return str(min(pagina, total_paginas))


def buscar_metadata_paginas(obra_id: str) -> int | None:
    """Lê `corpus/metadata.csv` e devolve `paginas_total` da obra, se houver."""
    meta = REPO_ROOT / "corpus" / "metadata.csv"
    if not meta.exists():
        return None
    with meta.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row.get("id") == obra_id and row.get("paginas_total"):
                try:
                    return int(row["paginas_total"])
                except ValueError:
                    return None
    return None


def executar_kwic(
    *,
    texto_path: Path,
    campo_path: Path,
    obra: str,
    janela: int,
    saida_csv: Path,
) -> None:
    """Roda KWIC e grava CSV em `saida_csv`."""
    texto = texto_path.read_text(encoding="utf-8", errors="replace")
    palavras = localizar_palavras(texto)
    grupos = carregar_campo_lexical(campo_path)
    padroes = compilar_padroes(grupos)
    paginas_total = buscar_metadata_paginas(obra)

    saida_csv.parent.mkdir(parents=True, exist_ok=True)
    cabecalho = [
        "obra", "campo_lexical", "termo_buscado", "termo_encontrado",
        "pagina_aproximada", "posicao_no_texto", "provavel_nota_rodape",
        "contexto_antes", "trecho_central", "contexto_depois",
    ]
    n_total = 0
    contagem_por_termo: dict[str, int] = {g.canonico: 0 for g in grupos}
    with saida_csv.open("w", encoding="utf-8", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=cabecalho)
        escritor.writeheader()
        for grupo, padrao in padroes:
            for match in padrao.finditer(texto):
                antes, central, depois = janela_kwic(
                    texto, palavras, match.start(), match.end(), janela
                )
                escritor.writerow({
                    "obra": obra,
                    "campo_lexical": campo_path.stem,
                    "termo_buscado": grupo.canonico,
                    "termo_encontrado": central.lower(),
                    "pagina_aproximada": estimar_pagina(
                        match.start(), len(texto), paginas_total
                    ),
                    "posicao_no_texto": match.start(),
                    "provavel_nota_rodape": int(
                        parece_nota_rodape(texto, match.start())
                    ),
                    "contexto_antes": antes,
                    "trecho_central": central,
                    "contexto_depois": depois,
                })
                contagem_por_termo[grupo.canonico] += 1
                n_total += 1

    try:
        rotulo = saida_csv.relative_to(REPO_ROOT)
    except ValueError:
        rotulo = saida_csv
    print(f"Gravado: {rotulo}")
    print(f"Total de ocorrências: {n_total}")
    print("Por termo canônico:")
    for canonico, n in sorted(contagem_por_termo.items(), key=lambda x: -x[1]):
        print(f"  {canonico:30s} {n:5d}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--texto", type=Path, required=True,
                        help="caminho para o txt extraído da obra.")
    parser.add_argument("--campo", type=Path, required=True,
                        help="caminho para o arquivo de campo lexical.")
    parser.add_argument("--obra", required=True,
                        help="id da obra (deve casar com corpus/metadata.csv).")
    parser.add_argument("--janela", type=int, default=50,
                        help="janela de palavras antes/depois (padrão: 50).")
    parser.add_argument("--saida", type=Path, required=True,
                        help="caminho do CSV de saída.")
    args = parser.parse_args()

    if not args.texto.exists():
        sys.exit(f"ERRO: texto {args.texto} não existe. Rode antes scripts/01_extract_text.py.")
    if not args.campo.exists():
        sys.exit(f"ERRO: campo lexical {args.campo} não existe.")

    executar_kwic(
        texto_path=args.texto,
        campo_path=args.campo,
        obra=args.obra,
        janela=args.janela,
        saida_csv=args.saida,
    )


if __name__ == "__main__":
    main()

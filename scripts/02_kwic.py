"""KWIC (Keyword in Context) sobre todas as obras em escopo da Etapa 1.

Lê o catálogo YAML `campos_lexicais/catalogo_termos.yaml` e o catálogo
bibliográfico `corpus/metadata.csv` filtrando por `escopo_etapa1 == 'sim'`.
Para cada obra, percorre o texto extraído em `corpus/txt/<id>.txt` e grava
um CSV em `outputs/<id>/csv/kwic.csv`.

Janela padrão: ±10 palavras (decisão da Etapa 1, seção 3 das decisões).

Filtro de exclusões: cada grupo do YAML pode ter `exclusoes`, lista de
expressões. Se uma expressão de exclusão aparecer no trecho central casado
ou na janela de ±5 palavras adjacentes, a ocorrência é descartada
(com contagem registrada no log).

Uso:
    python scripts/02_kwic.py
    python scripts/02_kwic.py --autor latour --janela 10
    python scripts/02_kwic.py --only latour_1987
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
METADATA_CSV = REPO_ROOT / "corpus" / "metadata.csv"
CATALOGO_YAML = REPO_ROOT / "campos_lexicais" / "catalogo_termos.yaml"
CORPUS_TXT_DIR = REPO_ROOT / "corpus" / "txt_norm"
OUTPUTS_DIR = REPO_ROOT / "outputs"

JANELA_EXCLUSAO_PALAVRAS = 5  # janela de checagem de exclusões adjacentes


@dataclass(frozen=True)
class GrupoTermo:
    """Grupo conceitual do catálogo YAML."""
    autor: str
    grupo: str
    termos: tuple[str, ...]
    exclusoes: tuple[str, ...]
    nota: str


def carregar_catalogo() -> list[GrupoTermo]:
    if not CATALOGO_YAML.exists():
        sys.exit(f"ERRO: {CATALOGO_YAML} não existe.")
    dados = yaml.safe_load(CATALOGO_YAML.read_text(encoding="utf-8")) or {}
    grupos: list[GrupoTermo] = []
    for autor, conteudo in dados.items():
        if not isinstance(conteudo, dict):
            continue
        for grupo, meta in conteudo.items():
            termos = tuple(t.strip() for t in (meta.get("termos") or []) if t.strip())
            exclusoes = tuple(e.strip() for e in (meta.get("exclusoes") or []) if e.strip())
            nota = (meta.get("nota") or "").strip()
            if not termos:
                continue
            grupos.append(GrupoTermo(
                autor=autor, grupo=grupo, termos=termos,
                exclusoes=exclusoes, nota=nota,
            ))
    return grupos


def compilar_padrao(termos: tuple[str, ...]) -> re.Pattern[str]:
    """Compila regex que casa qualquer variante, com word-boundaries.

    Espaços viram `\\s+` para tolerar quebras de linha; apóstrofo curvo
    e reto são equivalentes.
    """
    alternativas: list[str] = []
    for variante in termos:
        escapada = re.escape(variante.lower())
        escapada = escapada.replace(r"\ ", r"\s+")
        escapada = escapada.replace(r"\'", r"['’]")
        # hífens podem aparecer com espaço opcional entre tokens
        escapada = escapada.replace(r"\-", r"[-\s]?")
        alternativas.append(rf"\b{escapada}\b")
    return re.compile("|".join(alternativas), flags=re.IGNORECASE)


def compilar_exclusoes(exclusoes: tuple[str, ...]) -> re.Pattern[str] | None:
    if not exclusoes:
        return None
    alternativas = []
    for exc in exclusoes:
        escapada = re.escape(exc.lower()).replace(r"\ ", r"\s+")
        alternativas.append(escapada)
    return re.compile("|".join(alternativas), flags=re.IGNORECASE)


def localizar_palavras(texto: str) -> list[tuple[int, int]]:
    return [(m.start(), m.end()) for m in re.finditer(r"\S+", texto)]


def _trecho_palavras(
    texto: str, palavras: list[tuple[int, int]], ini: int, fim: int
) -> str:
    if ini >= fim:
        return ""
    return texto[palavras[ini][0]:palavras[fim - 1][1]]


def _normalizar(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def janela_kwic(
    texto: str, palavras: list[tuple[int, int]],
    inicio_match: int, fim_match: int, janela: int,
) -> tuple[str, str, str, int, int]:
    """Devolve (antes, central, depois, idx_pal_inicio, idx_pal_fim)."""
    idx_ini = next(
        (i for i, (a, b) in enumerate(palavras) if a <= inicio_match < b),
        None,
    )
    if idx_ini is None:
        return "", texto[inicio_match:fim_match], "", -1, -1
    idx_fim = next(
        (i for i, (a, b) in enumerate(palavras) if a < fim_match <= b),
        idx_ini,
    )
    antes = _normalizar(_trecho_palavras(texto, palavras, max(0, idx_ini - janela), idx_ini))
    central = texto[inicio_match:fim_match]
    depois = _normalizar(_trecho_palavras(
        texto, palavras, idx_fim + 1, min(len(palavras), idx_fim + 1 + janela)
    ))
    return antes, central, depois, idx_ini, idx_fim


def estimar_pagina(posicao: int, separadores: list[int]) -> int:
    """Conta quantos `\\f` aparecem antes de `posicao`."""
    lo, hi = 0, len(separadores)
    while lo < hi:
        mid = (lo + hi) // 2
        if separadores[mid] < posicao:
            lo = mid + 1
        else:
            hi = mid
    return lo + 1  # 1-indexed


def obras_em_escopo(escopo: str = "etapa1") -> list[dict[str, str]]:
    """Lê metadata.csv e filtra pelo escopo solicitado.

    `escopo` aceita `etapa1`, `etapa2` ou `todos`. Para `todos`, devolve obras
    com `escopo_etapa1=='sim'` OU `escopo_etapa2=='sim'`.
    """
    if not METADATA_CSV.exists():
        sys.exit(f"ERRO: {METADATA_CSV} não existe.")
    with METADATA_CSV.open(encoding="utf-8", newline="") as f:
        linhas = list(csv.DictReader(f))
    def _mark(r: dict[str, str], col: str) -> bool:
        return r.get(col, "").strip().lower() == "sim"
    if escopo == "etapa1":
        return [r for r in linhas if _mark(r, "escopo_etapa1")]
    if escopo == "etapa2":
        return [r for r in linhas if _mark(r, "escopo_etapa2")]
    if escopo == "todos":
        return [r for r in linhas if _mark(r, "escopo_etapa1") or _mark(r, "escopo_etapa2")]
    sys.exit(f"ERRO: escopo desconhecido '{escopo}'. Use etapa1, etapa2 ou todos.")


def ler_texto_sem_cabecalho(caminho: Path) -> str:
    """Lê o `.txt` e prepara para tokenização.

    Aplica duas operações que preservam offsets em comprimento (mantendo
    o casamento de posicao_no_texto entre KWIC e cocorrência):

    1. Linhas iniciadas por `#` (cabeçalho de metadados dos artigos da
       Etapa 2) viram espaços do mesmo comprimento. Os tokens do cabeçalho
       não entram no KWIC.
    2. Caracteres de controle ASCII de baixa ordem (`\\x00`-`\\x08`,
       `\\x0b`-`\\x1f`, `\\x7f`) viram espaço. Em particular `\\x02` (STX)
       aparece como artefato de OCR nos artigos da Etapa 2, no papel
       funcional de soft hyphen ou separador, e quebraria a tokenização
       de palavras como `abil\\x02ity` se mantido. Análogo ao tratamento de
       U+00AD aplicado aos livros pelo Adendo 1 das decisões metodológicas.
    """
    texto = caminho.read_text(encoding="utf-8", errors="replace")
    saida: list[str] = []
    for linha in texto.splitlines(keepends=True):
        if linha.lstrip().startswith("#"):
            corpo = linha.rstrip("\n\r")
            saida.append(" " * len(corpo) + linha[len(corpo):])
        else:
            saida.append(linha)
    texto_sem_header = "".join(saida)
    # Substitui caracteres de controle de baixa ordem por espaço (preserva offset).
    texto_limpo = re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", " ", texto_sem_header)
    return texto_limpo


def identificar_autor_da_obra(obra: dict[str, str]) -> str:
    """Mapeia coluna 'autor' do metadata para a chave de topo do YAML.

    Convenção: primeiro sobrenome em minúsculas; permite catálogo YAML com
    chave `latour` casar `Latour Bruno; Woolgar Steve`.
    """
    autor_str = obra.get("autor", "")
    primeiro = autor_str.split(";")[0].split(",")[0].strip().split()
    return primeiro[0].lower() if primeiro else ""


def kwic_obra(
    obra: dict[str, str],
    grupos: list[GrupoTermo],
    *,
    janela: int,
) -> None:
    obra_id = obra["id"]
    autor_obra = identificar_autor_da_obra(obra)
    grupos_obra = [g for g in grupos if g.autor == autor_obra]
    if not grupos_obra:
        print(f"  [pular] nenhum grupo do catálogo casa com autor '{autor_obra}'.")
        return

    txt_path = CORPUS_TXT_DIR / f"{obra_id}.txt"
    if not txt_path.exists():
        print(f"  [pular] {txt_path} não existe; rode antes scripts/01_extract_text.py.")
        return

    texto = ler_texto_sem_cabecalho(txt_path)
    palavras = localizar_palavras(texto)
    separadores = [m.start() for m in re.finditer(r"\f", texto)]

    saida_dir = OUTPUTS_DIR / obra_id / "csv"
    saida_dir.mkdir(parents=True, exist_ok=True)
    saida_csv = saida_dir / "kwic.csv"

    cabecalho = [
        "obra", "autor_yaml", "grupo", "termo_encontrado",
        "pagina", "posicao_no_texto",
        "contexto_antes", "trecho_central", "contexto_depois",
        "descartado_por_exclusao",
    ]
    n_grupo: dict[str, int] = {g.grupo: 0 for g in grupos_obra}
    n_excl: dict[str, int] = {g.grupo: 0 for g in grupos_obra}
    n_total = 0

    with saida_csv.open("w", encoding="utf-8", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=cabecalho)
        escritor.writeheader()
        for grupo in grupos_obra:
            padrao = compilar_padrao(grupo.termos)
            padrao_exc = compilar_exclusoes(grupo.exclusoes)
            for match in padrao.finditer(texto):
                antes, central, depois, _, _ = janela_kwic(
                    texto, palavras, match.start(), match.end(), janela,
                )
                descartado = False
                if padrao_exc is not None:
                    janela_exc_antes = _trecho_palavras(
                        texto, palavras,
                        max(0, _indice_palavra(palavras, match.start()) - JANELA_EXCLUSAO_PALAVRAS),
                        _indice_palavra(palavras, match.start()),
                    )
                    janela_exc_depois = _trecho_palavras(
                        texto, palavras,
                        _indice_palavra(palavras, match.end() - 1) + 1,
                        min(len(palavras), _indice_palavra(palavras, match.end() - 1) + 1 + JANELA_EXCLUSAO_PALAVRAS),
                    )
                    janela_check = _normalizar(
                        f"{janela_exc_antes} {central} {janela_exc_depois}"
                    )
                    if padrao_exc.search(janela_check):
                        descartado = True
                        n_excl[grupo.grupo] += 1

                escritor.writerow({
                    "obra": obra_id,
                    "autor_yaml": grupo.autor,
                    "grupo": grupo.grupo,
                    "termo_encontrado": central.lower(),
                    "pagina": estimar_pagina(match.start(), separadores),
                    "posicao_no_texto": match.start(),
                    "contexto_antes": antes,
                    "trecho_central": central,
                    "contexto_depois": depois,
                    "descartado_por_exclusao": int(descartado),
                })
                if not descartado:
                    n_grupo[grupo.grupo] += 1
                    n_total += 1

    try:
        rotulo = saida_csv.relative_to(REPO_ROOT)
    except ValueError:
        rotulo = saida_csv
    print(f"  gravado: {rotulo}")
    print(f"  total ocorrências válidas: {n_total}")
    for g in grupos_obra:
        excl_str = f" (excluídas: {n_excl[g.grupo]})" if g.exclusoes else ""
        print(f"    {g.grupo:30s} {n_grupo[g.grupo]:5d}{excl_str}")


def _indice_palavra(palavras: list[tuple[int, int]], pos: int) -> int:
    """Índice da palavra em `palavras` que contém ou precede a posição `pos`."""
    lo, hi = 0, len(palavras)
    while lo < hi:
        mid = (lo + hi) // 2
        if palavras[mid][0] <= pos:
            lo = mid + 1
        else:
            hi = mid
    return max(0, lo - 1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--autor", help="filtra grupos do YAML por autor (default: todos).")
    parser.add_argument("--only", help="filtra obras por substring de id.")
    parser.add_argument("--janela", type=int, default=10,
                        help="janela KWIC em palavras antes/depois (default: 10).")
    parser.add_argument("--escopo", default="etapa1",
                        choices=["etapa1", "etapa2", "todos"],
                        help="filtro de obras: etapa1 (default), etapa2 ou todos.")
    args = parser.parse_args()

    grupos = carregar_catalogo()
    if args.autor:
        grupos = [g for g in grupos if g.autor == args.autor.lower()]
        if not grupos:
            sys.exit(f"Nenhum grupo no YAML para autor='{args.autor}'.")

    obras = obras_em_escopo(args.escopo)
    if args.only:
        obras = [o for o in obras if args.only.lower() in o["id"].lower()]
        if not obras:
            sys.exit(f"Nenhuma obra em escopo casa com --only='{args.only}'.")

    print(f"Obras a processar: {len(obras)}; janela=±{args.janela} palavras.")
    for obra in obras:
        print(f"\n[{obra['id']}]")
        kwic_obra(obra, grupos, janela=args.janela)


if __name__ == "__main__":
    main()

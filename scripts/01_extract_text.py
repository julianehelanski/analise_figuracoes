"""Extração de texto dos PDFs do corpus.

Este script implementa a Etapa 0 do plano de trabalho:

1. Lê `CORPUS_PDF_PATH` do `.env` (pasta Drive sincronizada localmente).
2. Valida que o caminho existe, é diretório, e é legível.
3. Lista os PDFs presentes e cruza com a lista esperada em `corpus/README.md`.
4. Extrai texto via `pdftotext -layout` (fallback para `pdfminer.six`).
5. Detecta heurísticamente início e fim do corpo de texto.
6. Conta páginas e palavras.
7. Atualiza `corpus/metadata.csv`.

Uso:
    python scripts/01_extract_text.py
    python scripts/01_extract_text.py --only haraway_2016
    python scripts/01_extract_text.py --only haraway_2016 --force

A correspondência de `--only` é case-insensitive por substring, então
`--only haraway` casa qualquer PDF cuja correspondência canônica contenha
`haraway`.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# --------------------------------------------------------------------------- #
# Configuração: catálogo do corpus esperado.
# Mantém o mesmo conteúdo da tabela em corpus/README.md, para que o script
# funcione sem depender de parser de markdown.
# --------------------------------------------------------------------------- #

REPO_ROOT = Path(__file__).resolve().parents[1]
CORPUS_TXT_DIR = REPO_ROOT / "corpus" / "txt"
METADATA_CSV = REPO_ROOT / "corpus" / "metadata.csv"

CABECALHOS_INICIO_CORPO = (
    r"^\s*chapter\s+1\b",
    r"^\s*capítulo\s+1\b",
    r"^\s*capitulo\s+1\b",
    r"^\s*chapitre\s+1\b",
    r"^\s*introduction\b",
    r"^\s*introdução\b",
)

CABECALHOS_FIM_CORPO = (
    r"^\s*bibliography\b",
    r"^\s*references\b",
    r"^\s*bibliografia\b",
    r"^\s*référence",
    r"^\s*notes\b",
)


@dataclass(frozen=True)
class ObraCatalogada:
    """Entrada do catálogo do corpus esperado."""

    id: str
    autor: str
    titulo: str
    ano: int
    idioma: str
    edicao: str
    prioridade: int


CATALOGO: tuple[ObraCatalogada, ...] = (
    ObraCatalogada("latour_1984", "Bruno Latour", "Les microbes: guerre et paix",
                  1984, "fr", "Métailié", 2),
    ObraCatalogada("latour_1987", "Bruno Latour", "Science in Action",
                  1987, "en", "Harvard", 1),
    ObraCatalogada("latour_1996_ant_clarifications", "Bruno Latour",
                  "On actor-network theory: a few clarifications",
                  1996, "en", "Soziale Welt", 3),
    ObraCatalogada("latour_1999_recalling_ant", "Bruno Latour",
                  "On recalling ANT", 1999, "en", "Sociological Review", 3),
    ObraCatalogada("latour_1999_pandoras_hope", "Bruno Latour",
                  "Pandora's Hope", 1999, "en", "Harvard", 2),
    ObraCatalogada("latour_2005_reassembling", "Bruno Latour",
                  "Reassembling the Social", 2005, "en", "Oxford", 2),
    ObraCatalogada("haraway_1985_cyborg", "Donna Haraway",
                  "A Cyborg Manifesto", 1985, "en", "Socialist Review", 2),
    ObraCatalogada("haraway_1988_situated", "Donna Haraway",
                  "Situated Knowledges", 1988, "en", "Feminist Studies", 2),
    ObraCatalogada("haraway_1992_monsters", "Donna Haraway",
                  "The Promises of Monsters", 1992, "en", "Routledge", 3),
    ObraCatalogada("haraway_1997_modest_witness", "Donna Haraway",
                  "Modest_Witness@Second_Millennium", 1997, "en", "Routledge", 3),
    ObraCatalogada("haraway_2003_companion_species", "Donna Haraway",
                  "The Companion Species Manifesto", 2003, "en", "Prickly Paradigm", 3),
    ObraCatalogada("haraway_2008_when_species_meet", "Donna Haraway",
                  "When Species Meet", 2008, "en", "Minnesota", 2),
    ObraCatalogada("haraway_2016_staying_with_the_trouble", "Donna Haraway",
                  "Staying with the Trouble", 2016, "en", "Duke", 1),
)


# --------------------------------------------------------------------------- #
# Funções auxiliares.
# --------------------------------------------------------------------------- #


def carregar_corpus_pdf_path() -> Path:
    """Carrega `CORPUS_PDF_PATH` do `.env`, valida, e retorna como `Path`.

    Aborta o script com mensagem clara em qualquer falha (variável ausente,
    pasta inexistente, sem permissão), conforme `CLAUDE.md`.
    """
    load_dotenv(dotenv_path=REPO_ROOT / ".env")
    valor = os.getenv("CORPUS_PDF_PATH")
    if not valor:
        sys.exit(
            "ERRO: CORPUS_PDF_PATH não está definido no .env.\n"
            "Copie .env.example para .env e preencha com o caminho local da "
            "pasta Drive sincronizada."
        )
    caminho = Path(valor).expanduser()
    if not caminho.exists():
        sys.exit(
            f"ERRO: o caminho {caminho} não existe.\n"
            "Causas prováveis: Google Drive não está sincronizado, sync foi "
            "pausado, ou o caminho em .env aponta para a pasta errada."
        )
    if not caminho.is_dir():
        sys.exit(f"ERRO: {caminho} não é um diretório.")
    if not os.access(caminho, os.R_OK):
        sys.exit(f"ERRO: sem permissão de leitura em {caminho}.")
    return caminho


def listar_pdfs(pdf_dir: Path) -> list[Path]:
    """Lista todos os PDFs presentes na pasta Drive (case-insensitive)."""
    return sorted(
        p for p in pdf_dir.iterdir()
        if p.is_file() and p.suffix.lower() == ".pdf"
    )


def casar_pdf_ao_catalogo(pdf: Path) -> ObraCatalogada | None:
    """Tenta identificar a entrada do catálogo correspondente a um PDF.

    A correspondência é case-insensitive por substring sobre o nome do
    arquivo, exigindo que apareçam pelo menos o sobrenome do autor e o ano.
    """
    nome = pdf.stem.lower()
    for obra in CATALOGO:
        sobrenome = obra.autor.split()[-1].lower()
        if sobrenome in nome and str(obra.ano) in nome:
            return obra
    return None


def cruzar_catalogo(pdfs: list[Path]) -> tuple[
    dict[ObraCatalogada, Path], list[Path], list[ObraCatalogada]
]:
    """Cruza PDFs presentes com catálogo esperado.

    Retorna:
        - dicionário obra -> PDF correspondente,
        - lista de PDFs sem correspondência (nomenclatura fora do padrão),
        - lista de obras esperadas que estão faltando (prioridade 1 ou 2).
    """
    pares: dict[ObraCatalogada, Path] = {}
    nao_casados: list[Path] = []
    for pdf in pdfs:
        obra = casar_pdf_ao_catalogo(pdf)
        if obra is None:
            nao_casados.append(pdf)
        else:
            pares[obra] = pdf
    faltando = [o for o in CATALOGO if o not in pares and o.prioridade <= 2]
    return pares, nao_casados, faltando


def extrair_texto_pdftotext(pdf: Path, saida: Path) -> bool:
    """Extrai texto com `pdftotext -layout`. Retorna True se bem-sucedido."""
    if shutil.which("pdftotext") is None:
        return False
    saida.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            ["pdftotext", "-layout", str(pdf), str(saida)],
            check=True,
            capture_output=True,
        )
        return saida.exists() and saida.stat().st_size > 0
    except subprocess.CalledProcessError as exc:
        print(f"  pdftotext falhou: {exc.stderr.decode(errors='ignore')[:200]}")
        return False


def extrair_texto_pdfminer(pdf: Path, saida: Path) -> bool:
    """Extrai texto com pdfminer.six como fallback. Retorna True se bem-sucedido."""
    try:
        from pdfminer.high_level import extract_text
    except ImportError:
        return False
    saida.parent.mkdir(parents=True, exist_ok=True)
    try:
        texto = extract_text(str(pdf))
        saida.write_text(texto, encoding="utf-8")
        return saida.stat().st_size > 0
    except Exception as exc:  # noqa: BLE001
        print(f"  pdfminer falhou: {exc}")
        return False


def contar_paginas(pdf: Path) -> int | None:
    """Conta páginas via `pdfinfo` se disponível; senão retorna None."""
    if shutil.which("pdfinfo") is None:
        return None
    try:
        saida = subprocess.run(
            ["pdfinfo", str(pdf)], check=True, capture_output=True, text=True
        ).stdout
        for linha in saida.splitlines():
            if linha.startswith("Pages:"):
                return int(linha.split(":", 1)[1].strip())
    except (subprocess.CalledProcessError, ValueError):
        pass
    return None


def detectar_corpo(texto: str) -> tuple[int | None, int | None]:
    """Detecta posições aproximadas (em caracteres) de início e fim do corpo.

    Heurística simples: procura primeira linha que case com um cabeçalho de
    início (Chapter 1, Introduction, etc.) e primeira linha pós-início que
    case com cabeçalho de fim (Bibliography, References, Notes).
    """
    inicio: int | None = None
    fim: int | None = None
    linhas = texto.splitlines(keepends=True)
    offset = 0
    for linha in linhas:
        linha_norm = linha.strip().lower()
        if inicio is None and any(
            re.match(p, linha_norm) for p in CABECALHOS_INICIO_CORPO
        ):
            inicio = offset
        elif inicio is not None and any(
            re.match(p, linha_norm) for p in CABECALHOS_FIM_CORPO
        ):
            fim = offset
            break
        offset += len(linha)
    return inicio, fim


def contar_palavras(texto: str) -> int:
    """Conta palavras (tokens separados por espaço, ignorando vazios)."""
    return sum(1 for tok in re.split(r"\s+", texto) if tok)


def avaliar_qualidade(texto: str) -> str:
    """Avaliação heurística da qualidade da extração.

    Retorna `boa`, `media` ou `baixa`, com base em proporção de caracteres
    estranhos e linhas muito curtas ou muito longas.
    """
    if not texto:
        return "baixa"
    total = len(texto)
    estranhos = sum(
        1 for c in texto
        if not (c.isalnum() or c.isspace() or c in ".,;:!?\"'()[]-—–…/\\&%$#@*+=<>")
    )
    prop_estranhos = estranhos / total
    linhas = [line for line in texto.splitlines() if line.strip()]
    if not linhas:
        return "baixa"
    curtas = sum(1 for line in linhas if len(line) < 10)
    prop_curtas = curtas / len(linhas)
    if prop_estranhos > 0.05 or prop_curtas > 0.5:
        return "baixa"
    if prop_estranhos > 0.02 or prop_curtas > 0.3:
        return "media"
    return "boa"


def atualizar_metadata(linha: dict[str, object]) -> None:
    """Atualiza (insere ou substitui por id) uma linha em `corpus/metadata.csv`."""
    METADATA_CSV.parent.mkdir(parents=True, exist_ok=True)
    cabecalho = [
        "id", "autor", "titulo", "ano", "idioma", "edicao",
        "paginas_total", "pagina_inicio_corpo", "pagina_fim_corpo",
        "palavras_corpo", "qualidade_extracao", "observacoes",
    ]
    existentes: dict[str, dict[str, str]] = {}
    if METADATA_CSV.exists():
        with METADATA_CSV.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                existentes[row["id"]] = row
    existentes[str(linha["id"])] = {k: str(linha.get(k, "")) for k in cabecalho}
    with METADATA_CSV.open("w", encoding="utf-8", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=cabecalho)
        escritor.writeheader()
        for _, row in sorted(existentes.items()):
            escritor.writerow(row)


# --------------------------------------------------------------------------- #
# Pipeline.
# --------------------------------------------------------------------------- #


def processar_obra(obra: ObraCatalogada, pdf: Path, *, forcar: bool) -> None:
    """Extrai uma obra: gera txt, atualiza metadata, reporta qualidade."""
    saida = CORPUS_TXT_DIR / f"{obra.id}.txt"
    if saida.exists() and not forcar:
        print(f"  [pular] {saida.relative_to(REPO_ROOT)} já existe; use --force.")
        return

    print(f"  extraindo {pdf.name} -> corpus/txt/{obra.id}.txt ...")
    ok = extrair_texto_pdftotext(pdf, saida)
    if not ok:
        print("  pdftotext indisponível ou falhou; tentando pdfminer.six.")
        ok = extrair_texto_pdfminer(pdf, saida)
    if not ok:
        print(
            f"  ERRO: não consegui extrair texto de {pdf.name}. "
            "Verifique se pdftotext (poppler-utils) ou pdfminer.six estão instalados."
        )
        return

    texto = saida.read_text(encoding="utf-8", errors="replace")
    paginas_total = contar_paginas(pdf)
    inicio, fim = detectar_corpo(texto)
    palavras_corpo = contar_palavras(texto[inicio:fim] if inicio is not None else texto)
    qualidade = avaliar_qualidade(texto)

    atualizar_metadata({
        "id": obra.id,
        "autor": obra.autor,
        "titulo": obra.titulo,
        "ano": obra.ano,
        "idioma": obra.idioma,
        "edicao": obra.edicao,
        "paginas_total": paginas_total or "",
        "pagina_inicio_corpo": inicio if inicio is not None else "",
        "pagina_fim_corpo": fim if fim is not None else "",
        "palavras_corpo": palavras_corpo,
        "qualidade_extracao": qualidade,
        "observacoes": "",
    })
    print(
        f"  ok: páginas={paginas_total}, palavras_corpo={palavras_corpo}, "
        f"qualidade={qualidade}, corpo=[{inicio}, {fim}]"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--only",
        help="filtra por substring case-insensitive do id da obra (ex.: 'haraway_2016').",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="reextrai mesmo que o txt já exista.",
    )
    args = parser.parse_args()

    pdf_dir = carregar_corpus_pdf_path()
    pdfs = listar_pdfs(pdf_dir)
    print(f"Pasta Drive: {pdf_dir}")
    print(f"PDFs encontrados: {len(pdfs)}")
    if not pdfs:
        sys.exit(
            "ERRO: pasta Drive está vazia. Verifique a sincronização do "
            "Google Drive for Desktop."
        )

    pares, nao_casados, faltando = cruzar_catalogo(pdfs)
    print(f"PDFs identificados no catálogo: {len(pares)}")
    for obra, pdf in pares.items():
        print(f"  - {obra.id}  <-  {pdf.name}")
    if nao_casados:
        print(f"PDFs sem correspondência no catálogo: {len(nao_casados)}")
        for pdf in nao_casados:
            print(f"  - {pdf.name}")
    if faltando:
        print(f"Obras esperadas (prioridade 1-2) faltando: {len(faltando)}")
        for obra in faltando:
            print(f"  - {obra.id} ({obra.titulo}, {obra.ano})")

    if args.only:
        filtro = args.only.lower()
        pares = {o: p for o, p in pares.items() if filtro in o.id.lower()}
        print(f"Filtro --only='{args.only}' aplicado: {len(pares)} obra(s) a processar.")
        if not pares:
            sys.exit("Nenhuma obra casa com o filtro --only.")

    CORPUS_TXT_DIR.mkdir(parents=True, exist_ok=True)
    for obra, pdf in pares.items():
        print(f"\n[{obra.id}]")
        processar_obra(obra, pdf, forcar=args.force)

    print("\nExtração concluída. Confira corpus/metadata.csv e corpus/txt/.")


if __name__ == "__main__":
    main()

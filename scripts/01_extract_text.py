"""Extração de texto dos PDFs do corpus, com classificação por página.

Implementa a Etapa 0 do plano, alinhada às decisões de 13/05/2026:

- Lê `corpus/metadata.csv` (formato com 15 colunas), filtra por `escopo_etapa1=='sim'`.
- Localiza cada PDF em `CORPUS_PDF_PATH` pelo nome exato do campo `arquivo_pdf`.
- Extrai texto com `pdftotext -layout` (fallback `pdfminer.six`), preservando o
  separador de página `\\f` para permitir análise por página.
- Classifica cada página em uma das cinco classes da amostra estratificada
  (decisoes_metodologicas.md, seção 5): `inicio_capitulo`, `corpo`, `notas_fim`,
  `paratexto`, `qualidade_baixa`.
- Salva texto integral em `corpus/txt/<id>.txt` e a tabela de páginas em
  `corpus/paginas/<id>.csv`.
- Atualiza `corpus/qualidade_extracao.csv` (catálogo de qualidade por obra),
  preservando intacta a `corpus/metadata.csv` (catálogo bibliográfico).

Uso:
    python scripts/01_extract_text.py
    python scripts/01_extract_text.py --only latour_1987
    python scripts/01_extract_text.py --force
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[1]
METADATA_CSV = REPO_ROOT / "corpus" / "metadata.csv"
CORPUS_TXT_DIR = REPO_ROOT / "corpus" / "txt"
PAGINAS_DIR = REPO_ROOT / "corpus" / "paginas"
QUALIDADE_CSV = REPO_ROOT / "corpus" / "qualidade_extracao.csv"

# Heurísticas de classificação de página -------------------------------------- #

_RE_INICIO_CAPITULO = re.compile(
    r"^\s*(chapter|capítulo|capitulo|chapitre|part|parte)\s+(\d+|[ivxlcdm]+)\b",
    re.IGNORECASE | re.MULTILINE,
)
_RE_NOTAS_FIM = re.compile(
    r"^\s*(notes|notas)\s*$", re.IGNORECASE | re.MULTILINE,
)
_RE_PARATEXTO = re.compile(
    r"^\s*(bibliography|references|bibliografia|index|índice|indice|"
    r"acknowledgements|acknowledgments|agradecimentos|appendix|apêndice|apendice|"
    r"contents|sumário|sumario)\s*$",
    re.IGNORECASE | re.MULTILINE,
)

# Set persistente entre páginas: uma vez que entramos em "notas_fim" ou
# "paratexto", as páginas seguintes herdam essa classificação até nova mudança.
_ESTADO_INICIAL = "corpo"


def carregar_corpus_pdf_path() -> Path:
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
            "Verifique se o Google Drive for Desktop está sincronizado e se o "
            "caminho em .env aponta para a pasta correta."
        )
    if not caminho.is_dir():
        sys.exit(f"ERRO: {caminho} não é um diretório.")
    if not os.access(caminho, os.R_OK):
        sys.exit(f"ERRO: sem permissão de leitura em {caminho}.")
    return caminho


def ler_obras_em_escopo() -> list[dict[str, str]]:
    """Lê metadata.csv e retorna as linhas com escopo_etapa1 == 'sim'."""
    if not METADATA_CSV.exists():
        sys.exit(f"ERRO: {METADATA_CSV} não existe.")
    with METADATA_CSV.open(encoding="utf-8", newline="") as f:
        linhas = [row for row in csv.DictReader(f)]
    em_escopo = [row for row in linhas if row.get("escopo_etapa1", "").strip().lower() == "sim"]
    if not em_escopo:
        sys.exit("ERRO: nenhuma obra com escopo_etapa1 == 'sim' em metadata.csv.")
    return em_escopo


def validar_presenca_pdfs(pdf_dir: Path, obras: list[dict[str, str]]) -> list[tuple[dict[str, str], Path]]:
    """Confere que cada obra em escopo tem PDF presente em CORPUS_PDF_PATH.

    A correspondência é por nome exato do campo `arquivo_pdf` (case-insensitive
    no nome do arquivo, como tolerância para sistemas de arquivos case-insensitive).
    """
    nomes_dir = {p.name: p for p in pdf_dir.iterdir() if p.is_file()}
    nomes_dir_ci = {p.name.lower(): p for p in nomes_dir.values()}
    encontradas: list[tuple[dict[str, str], Path]] = []
    faltando: list[dict[str, str]] = []
    for obra in obras:
        alvo = (obra.get("arquivo_pdf") or "").strip()
        if not alvo:
            faltando.append(obra)
            continue
        pdf = nomes_dir.get(alvo) or nomes_dir_ci.get(alvo.lower())
        if pdf is None:
            faltando.append(obra)
        else:
            encontradas.append((obra, pdf))
    if faltando:
        print("ERRO: PDFs faltando em CORPUS_PDF_PATH:")
        for obra in faltando:
            print(f"  - id={obra['id']}, esperado={obra.get('arquivo_pdf')}")
        sys.exit(
            "Pare e me avise antes de prosseguir. Verifique o Drive sincronizado "
            "e os nomes exatos dos arquivos."
        )
    return encontradas


def extrair_texto(pdf: Path, saida: Path) -> bool:
    """Extrai texto preservando `\\f` entre páginas. Retorna True se OK."""
    saida.parent.mkdir(parents=True, exist_ok=True)
    if shutil.which("pdftotext"):
        try:
            subprocess.run(
                ["pdftotext", "-layout", str(pdf), str(saida)],
                check=True, capture_output=True,
            )
            if saida.exists() and saida.stat().st_size > 0:
                return True
        except subprocess.CalledProcessError as exc:
            print(f"  pdftotext falhou: {exc.stderr.decode(errors='ignore')[:200]}")
    # Fallback: pdfminer.six (não preserva \f tão bem; inserimos manualmente
    # entre páginas).
    try:
        from pdfminer.high_level import extract_pages
        from pdfminer.layout import LTTextContainer
    except ImportError:
        return False
    try:
        partes: list[str] = []
        for layout in extract_pages(str(pdf)):
            texto_pagina = "".join(
                el.get_text() for el in layout if isinstance(el, LTTextContainer)
            )
            partes.append(texto_pagina)
        saida.write_text("\f".join(partes), encoding="utf-8")
        return saida.stat().st_size > 0
    except Exception as exc:  # noqa: BLE001
        print(f"  pdfminer falhou: {exc}")
        return False


def avaliar_qualidade_pagina(texto: str) -> str:
    """Classifica qualidade da extração da página em `boa`, `media` ou `baixa`."""
    if not texto.strip():
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


def classificar_paginas(texto: str) -> list[dict[str, object]]:
    """Quebra `texto` por `\\f` e classifica cada página.

    Estados:
        inicio_capitulo  página com cabeçalho 'Chapter N' / 'Capítulo N' etc.
        corpo            página sem marcadores especiais, antes de Notes/biblio.
        notas_fim        a partir da primeira 'Notes' até antes de bibliografia.
        paratexto        a partir de 'Bibliography', 'Index', 'Appendix', etc.
        qualidade_baixa  sobrescreve qualquer outra classe se a qualidade for
                         `baixa`. Permite que a amostra estratificada cubra essas
                         páginas com prioridade.
    """
    paginas = texto.split("\f")
    classificacao: list[dict[str, object]] = []
    estado = _ESTADO_INICIAL
    for numero, conteudo in enumerate(paginas, start=1):
        qualidade = avaliar_qualidade_pagina(conteudo)
        if qualidade == "baixa":
            classe = "qualidade_baixa"
        elif _RE_PARATEXTO.search(conteudo):
            classe = "paratexto"
            estado = "paratexto"
        elif _RE_NOTAS_FIM.search(conteudo) and estado != "paratexto":
            classe = "notas_fim"
            estado = "notas_fim"
        elif _RE_INICIO_CAPITULO.search(conteudo) and estado not in ("notas_fim", "paratexto"):
            classe = "inicio_capitulo"
            estado = "corpo"
        else:
            classe = estado if estado in ("notas_fim", "paratexto") else "corpo"

        classificacao.append({
            "pagina": numero,
            "classe": classe,
            "n_chars": len(conteudo),
            "n_palavras": sum(1 for tok in re.split(r"\s+", conteudo) if tok),
            "qualidade_pagina": qualidade,
        })
    return classificacao


def salvar_paginas_csv(obra_id: str, paginas: list[dict[str, object]]) -> None:
    PAGINAS_DIR.mkdir(parents=True, exist_ok=True)
    saida = PAGINAS_DIR / f"{obra_id}.csv"
    cabecalho = ["pagina", "classe", "n_chars", "n_palavras", "qualidade_pagina"]
    with saida.open("w", encoding="utf-8", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=cabecalho)
        escritor.writeheader()
        escritor.writerows(paginas)


def atualizar_qualidade_extracao(
    obra_id: str,
    obra: dict[str, str],
    paginas: list[dict[str, object]],
) -> dict[str, object]:
    """Atualiza `corpus/qualidade_extracao.csv` para a obra."""
    QUALIDADE_CSV.parent.mkdir(parents=True, exist_ok=True)
    cabecalho = [
        "id", "autor", "titulo", "ano_edicao", "idioma",
        "paginas_total", "palavras_total",
        "paginas_corpo", "paginas_inicio_capitulo", "paginas_notas_fim",
        "paginas_paratexto", "paginas_qualidade_baixa",
        "taxa_qualidade_boa", "taxa_qualidade_baixa",
        "qualidade_global",
    ]
    n_total = len(paginas)
    n_palavras = sum(int(p["n_palavras"]) for p in paginas)
    contagem_classes = {c: sum(1 for p in paginas if p["classe"] == c) for c in (
        "corpo", "inicio_capitulo", "notas_fim", "paratexto", "qualidade_baixa",
    )}
    contagem_q = {q: sum(1 for p in paginas if p["qualidade_pagina"] == q) for q in (
        "boa", "media", "baixa",
    )}
    taxa_boa = contagem_q["boa"] / n_total if n_total else 0
    taxa_baixa = contagem_q["baixa"] / n_total if n_total else 0
    qualidade_global = (
        "boa" if taxa_boa >= 0.8 and taxa_baixa <= 0.05
        else "media" if taxa_boa >= 0.6 and taxa_baixa <= 0.15
        else "baixa"
    )
    linha = {
        "id": obra_id,
        "autor": obra.get("autor", ""),
        "titulo": obra.get("titulo", ""),
        "ano_edicao": obra.get("ano_edicao", ""),
        "idioma": obra.get("idioma", ""),
        "paginas_total": n_total,
        "palavras_total": n_palavras,
        "paginas_corpo": contagem_classes["corpo"],
        "paginas_inicio_capitulo": contagem_classes["inicio_capitulo"],
        "paginas_notas_fim": contagem_classes["notas_fim"],
        "paginas_paratexto": contagem_classes["paratexto"],
        "paginas_qualidade_baixa": contagem_classes["qualidade_baixa"],
        "taxa_qualidade_boa": f"{taxa_boa:.3f}",
        "taxa_qualidade_baixa": f"{taxa_baixa:.3f}",
        "qualidade_global": qualidade_global,
    }
    existentes: dict[str, dict[str, str]] = {}
    if QUALIDADE_CSV.exists():
        with QUALIDADE_CSV.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                existentes[row["id"]] = row
    existentes[obra_id] = {k: str(v) for k, v in linha.items()}
    with QUALIDADE_CSV.open("w", encoding="utf-8", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=cabecalho)
        escritor.writeheader()
        for _, row in sorted(existentes.items()):
            escritor.writerow(row)
    return linha


def processar(obra: dict[str, str], pdf: Path, *, forcar: bool) -> dict[str, object] | None:
    obra_id = obra["id"]
    saida_txt = CORPUS_TXT_DIR / f"{obra_id}.txt"
    if saida_txt.exists() and not forcar:
        print(f"  [pular] {saida_txt.relative_to(REPO_ROOT)} já existe; use --force.")
        texto = saida_txt.read_text(encoding="utf-8", errors="replace")
    else:
        print(f"  extraindo {pdf.name} -> corpus/txt/{obra_id}.txt ...")
        if not extrair_texto(pdf, saida_txt):
            print(f"  ERRO: não consegui extrair texto de {pdf.name}.")
            return None
        texto = saida_txt.read_text(encoding="utf-8", errors="replace")

    paginas = classificar_paginas(texto)
    salvar_paginas_csv(obra_id, paginas)
    linha_q = atualizar_qualidade_extracao(obra_id, obra, paginas)
    print(
        f"  ok: paginas={linha_q['paginas_total']}, "
        f"palavras={linha_q['palavras_total']}, "
        f"qualidade_global={linha_q['qualidade_global']}, "
        f"taxa_boa={linha_q['taxa_qualidade_boa']}, "
        f"taxa_baixa={linha_q['taxa_qualidade_baixa']}"
    )
    return linha_q


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--only", help="filtra por substring do id da obra.")
    parser.add_argument("--force", action="store_true",
                        help="reextrai mesmo que o txt já exista.")
    args = parser.parse_args()

    pdf_dir = carregar_corpus_pdf_path()
    obras = ler_obras_em_escopo()
    print(f"Pasta Drive: {pdf_dir}")
    print(f"Obras em escopo (escopo_etapa1=sim): {len(obras)}")
    for o in obras:
        print(f"  - {o['id']}  ({o.get('arquivo_pdf')})")

    pares = validar_presenca_pdfs(pdf_dir, obras)
    if args.only:
        filtro = args.only.lower()
        pares = [(o, p) for o, p in pares if filtro in o["id"].lower()]
        if not pares:
            sys.exit(f"Nenhuma obra em escopo casa com --only='{args.only}'.")
    print(f"PDFs validados: {len(pares)}")

    CORPUS_TXT_DIR.mkdir(parents=True, exist_ok=True)
    resumo: list[dict[str, object]] = []
    for obra, pdf in pares:
        print(f"\n[{obra['id']}]")
        linha = processar(obra, pdf, forcar=args.force)
        if linha:
            resumo.append(linha)

    print("\nRelatório de extração:")
    print(f"  {'id':<45s} {'pgs':>5s} {'palavras':>10s} {'q_boa':>7s} {'q_baixa':>8s} {'global':>8s}")
    for linha in resumo:
        print(
            f"  {linha['id']:<45s} {linha['paginas_total']:>5} "
            f"{linha['palavras_total']:>10} "
            f"{linha['taxa_qualidade_boa']:>7} "
            f"{linha['taxa_qualidade_baixa']:>8} "
            f"{linha['qualidade_global']:>8}"
        )
    print(
        "\nDetalhes página a página em corpus/paginas/<id>.csv. "
        "Resumo por obra em corpus/qualidade_extracao.csv."
    )


if __name__ == "__main__":
    main()

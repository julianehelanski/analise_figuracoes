"""Auditoria de integridade dos `.txt` dos artigos teóricos (Etapa 2).

Lê `corpus/txt_norm/<slug>.txt` para os artigos marcados com
`escopo_etapa2=='sim'` em `corpus/metadata.csv` e gera relatório de
sanity checks:

- Presença e estrutura do cabeçalho de metadados (linhas `#`).
- Número de linhas de cabeçalho e de corpo.
- Contagem de palavras de corpo (excluindo linhas `^#`).
- Verificação amostral de passagens-chave (configurável por slug).
- Estimativa de risco de OCR colado (palavras com >18 caracteres consecutivos
  sem espaço, candidatas a colagem).

Não modifica o `.txt` nem o `qualidade_extracao.csv`. Apenas reporta.

Uso:
    python scripts/13_audit_articles_etapa2.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
METADATA_CSV = REPO_ROOT / "corpus" / "metadata.csv"
TXT_NORM_DIR = REPO_ROOT / "corpus" / "txt_norm"

# Passagens-chave por slug (regex; case-insensitive).
PASSAGENS_CHAVE: dict[str, list[tuple[str, str]]] = {
    "latour_1996_clarifications_en": [
        ("textil_topologico_pp76_91",
         r"fibrous,\s*thread-?like,\s*wiry,\s*stringy,\s*ropy,\s*capillary"),
        ("network_of_allies", r"network of allies"),
        ("pre_relativist_enemies", r"pre-?relativist enemies"),
        ("la_nouvelle_alliance_biblio", r"la nouvelle alliance"),
    ],
    "latour_1999_recalling_en": [
        # Tolera caracteres de controle/insercoes de OCR entre tokens
        # (e.g. STX U+0002 dentro de 'abil\x02ity').
        ("contamination_vocab_pp19_20",
         r"vocabulary\s+has\s+contaminated\s+our\s+abil.?ity"),
    ],
}


def carregar_obras_etapa2() -> list[dict[str, str]]:
    with METADATA_CSV.open(encoding="utf-8", newline="") as f:
        return [r for r in csv.DictReader(f)
                if r.get("escopo_etapa2", "").strip().lower() == "sim"]


def auditar(slug: str) -> dict[str, object]:
    p = TXT_NORM_DIR / f"{slug}.txt"
    if not p.exists():
        return {"slug": slug, "erro": f"arquivo ausente: {p}"}
    linhas = p.read_text(encoding="utf-8").splitlines()
    header = [l for l in linhas if l.lstrip().startswith("#")]
    corpo = [l for l in linhas if not l.lstrip().startswith("#")]
    texto_corpo = "\n".join(corpo)
    palavras = re.findall(r"\b\w+\b", texto_corpo, flags=re.UNICODE)

    # OCR colado: tokens longos sem espaço (>18 caracteres alfabéticos)
    candidatos_colagem = [
        t for t in re.findall(r"[A-Za-z]{19,}", texto_corpo)
    ]
    # Caracteres de controle ASCII (excluindo \t e \n) inseridos no meio do texto
    chars_controle = re.findall(r"[\x00-\x08\x0b-\x1f\x7f]", texto_corpo)

    passagens = []
    for nome, padrao in PASSAGENS_CHAVE.get(slug, []):
        m = re.search(padrao, texto_corpo, flags=re.IGNORECASE)
        passagens.append((nome, m is not None))

    return {
        "slug": slug,
        "n_linhas": len(linhas),
        "n_linhas_header": len(header),
        "n_linhas_corpo_nao_vazias": sum(1 for l in corpo if l.strip()),
        "palavras_corpo": len(palavras),
        "candidatos_colagem_ocr": len(candidatos_colagem),
        "exemplos_colagem": candidatos_colagem[:5],
        "chars_controle_residuais": len(chars_controle),
        "chars_controle_unicos": sorted({hex(ord(c)) for c in chars_controle}),
        "passagens_chave": passagens,
        "header_tem_slug": any("slug:" in l for l in header),
        "header_tem_origem": any("origem:" in l for l in header),
    }


def main() -> None:
    obras = carregar_obras_etapa2()
    if not obras:
        sys.exit("Nenhuma obra com escopo_etapa2='sim' em metadata.csv.")
    print(f"Auditoria de {len(obras)} obra(s) da Etapa 2:\n")
    for obra in obras:
        resultado = auditar(obra["id"])
        print(f"=== {resultado['slug']} ===")
        if "erro" in resultado:
            print(f"  ERRO: {resultado['erro']}\n")
            continue
        print(f"  linhas total: {resultado['n_linhas']}")
        print(f"  linhas cabecalho '#': {resultado['n_linhas_header']}")
        print(f"  linhas corpo nao vazias: {resultado['n_linhas_corpo_nao_vazias']}")
        print(f"  palavras corpo: {resultado['palavras_corpo']}")
        print(f"  cabecalho contem slug: {resultado['header_tem_slug']}")
        print(f"  cabecalho contem origem: {resultado['header_tem_origem']}")
        print(f"  candidatos colagem OCR (>18 chars): {resultado['candidatos_colagem_ocr']}")
        if resultado["exemplos_colagem"]:
            print(f"    exemplos: {resultado['exemplos_colagem']}")
        print(f"  chars de controle residuais: {resultado['chars_controle_residuais']}")
        if resultado["chars_controle_unicos"]:
            print(f"    codigos: {resultado['chars_controle_unicos']}")
        print("  passagens-chave:")
        for nome, presente in resultado["passagens_chave"]:
            marca = "OK" if presente else "AUSENTE"
            print(f"    [{marca}] {nome}")
        print()


if __name__ == "__main__":
    main()

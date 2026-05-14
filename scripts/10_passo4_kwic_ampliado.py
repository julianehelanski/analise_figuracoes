"""
Passo 4 do refinamento (15/05/2026).

KWIC ampliado a ±50 palavras com curadoria de passagens citáveis para o capítulo 2
da tese de Juliane sobre a tensão figural Latour-Haraway.

Entrada:
- corpus/txt_norm/<obra>.txt: textos normalizados das três obras de Latour.
- corpus/paginas/<obra>.csv: classificação por página (corpo/paratexto/...).
- campos_lexicais/catalogo_termos.yaml: termos figurativos por grupo.
- outputs/<obra>/csv/kwic.csv: KWIC ±10 palavras existente.

Saída:
- outputs/passo4/kwic_ampliado.csv: todos os hits válidos em janela ±50.
- outputs/passo4/passagens_curadas.md: melhores passagens por (obra × campo)
  formatadas como bloco LaTeX pronto para colar no capítulo 2.
"""

import csv
import re
import os
import yaml
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).parent.parent
WINDOW = 50  # janela em palavras
OUT_DIR = REPO / "outputs" / "passo4"
OUT_DIR.mkdir(parents=True, exist_ok=True)

OBRAS = {
    "latour_woolgar_1986_lab_life_en": "Laboratory Life",
    "latour_1987_science_action_en": "Science in Action",
    "latour_1999_pandora_en": "Pandora's Hope",
}

ANO = {
    "latour_woolgar_1986_lab_life_en": "1986",
    "latour_1987_science_action_en": "1987",
    "latour_1999_pandora_en": "1999",
}

# Campos prioritários para o capítulo 2: agonísticos/figurais que dialogam com Haraway
CAMPOS_PRIORITARIOS = [
    "militar",         # alistar, batalha, vitória, conquista
    "agonistic",       # campo agonístico, prova de força
    "enrollment",      # alistamento/recrutamento
    "spokesperson",    # porta-voz
    "trial_of_strength",
    "translation",     # tradução como recrutamento
    "actor_network",
    "network",
    "black_box",
    "inscription",
    "centre_of_calculation",
    "immutable_mobile",
]


def load_paginas(obra):
    """Mapa página -> classe (corpo, paratexto, notas_fim, etc.)."""
    paginas = {}
    with open(REPO / "corpus" / "paginas" / f"{obra}.csv", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            paginas[int(row["pagina"])] = row["classe"]
    return paginas


def carregar_texto_com_paginas(obra):
    """
    Reconstitui o texto da obra como lista de (n_pagina, texto_pagina).
    Heurística: o txt_norm tem páginas separadas por sequências de \\n+;
    usamos os contadores de páginas do CSV para conferir alinhamento.
    """
    # No projeto, o txt_norm é o texto contínuo. Para localizar páginas
    # precisamos do delimitador. Vou ler o txt_norm e usar form-feed
    # (\f) se houver, ou marcadores explícitos. Como fallback, divido por
    # tamanho médio usando n_chars do CSV.
    with open(REPO / "corpus" / "txt_norm" / f"{obra}.txt", encoding="utf-8") as f:
        txt = f.read()

    paginas_meta = []
    with open(REPO / "corpus" / "paginas" / f"{obra}.csv", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            paginas_meta.append((int(row["pagina"]), int(row["n_chars"]), row["classe"]))

    # Tentativa 1: dividir por form-feed
    if "\f" in txt:
        partes = txt.split("\f")
        if len(partes) >= len(paginas_meta) * 0.9:
            pags = []
            for i, (n, _, classe) in enumerate(paginas_meta):
                if i < len(partes):
                    pags.append((n, partes[i], classe))
            return pags

    # Tentativa 2: usar n_chars como offset
    pags = []
    offset = 0
    for n, n_chars, classe in paginas_meta:
        pags.append((n, txt[offset:offset + n_chars], classe))
        offset += n_chars
    return pags


def carregar_termos():
    with open(REPO / "campos_lexicais" / "catalogo_termos.yaml") as f:
        cat = yaml.safe_load(f)
    return cat["latour"]


def construir_regex(termos):
    """Constrói regex case-insensitive com word boundaries."""
    parts = []
    for t in termos:
        t_esc = re.escape(t).replace(r"\ ", r"\s+")
        parts.append(rf"\b{t_esc}\b")
    return re.compile("|".join(parts), re.IGNORECASE)


def extrair_janela(texto, start, end, n_palavras):
    """Extrai janela de n_palavras antes e depois do match."""
    antes_raw = texto[:start]
    depois_raw = texto[end:]
    palavras_antes = antes_raw.split()
    palavras_depois = depois_raw.split()
    contexto_antes = " ".join(palavras_antes[-n_palavras:])
    contexto_depois = " ".join(palavras_depois[:n_palavras])
    return contexto_antes, contexto_depois


# --- Construir o KWIC ampliado ---

CAMPOS = carregar_termos()
hits_amplos = []

for obra in OBRAS:
    paginas = carregar_texto_com_paginas(obra)
    for grupo, meta in CAMPOS.items():
        if grupo not in CAMPOS_PRIORITARIOS:
            continue
        termos = meta["termos"]
        exclusoes = meta.get("exclusoes", [])
        rx = construir_regex(termos)
        for n_pag, txt_pag, classe in paginas:
            # Filtro: apenas páginas de corpo ou início de capítulo
            if classe not in ("corpo", "inicio_capitulo"):
                continue
            for m in rx.finditer(txt_pag):
                termo_central = m.group(0)
                # Verificar exclusões na janela ±5 palavras
                antes_curta, depois_curta = extrair_janela(txt_pag, m.start(), m.end(), 5)
                contexto_curto = f"{antes_curta} {termo_central} {depois_curta}".lower()
                if any(exc.lower() in contexto_curto for exc in exclusoes):
                    continue
                # KWIC ampliado ±50
                antes_ampla, depois_ampla = extrair_janela(txt_pag, m.start(), m.end(), WINDOW)
                hits_amplos.append({
                    "obra": obra,
                    "ano": ANO[obra],
                    "grupo": grupo,
                    "termo": termo_central,
                    "pagina": n_pag,
                    "contexto_antes_50": antes_ampla,
                    "trecho_central": termo_central,
                    "contexto_depois_50": depois_ampla,
                })

print(f"Total de hits no KWIC ampliado: {len(hits_amplos)}")

# --- Aplicar classificação do passo 1 (war/wars em Pandora) ---

classificacao_passo1 = {}
caminho_passo1 = REPO / "refinamento" / "war_pandora_classificacao.csv"
if caminho_passo1.exists():
    with open(caminho_passo1) as f:
        r = csv.DictReader(f)
        for row in r:
            chave = (int(row["pagina"]), row["termo"].lower())
            if chave not in classificacao_passo1:
                classificacao_passo1[chave] = row["categoria_final"]

for hit in hits_amplos:
    hit["classificacao_passo1"] = ""
    if hit["obra"] == "latour_1999_pandora_en" and hit["termo"].lower() in ("war", "wars"):
        chave = (int(hit["pagina"]), hit["termo"].lower())
        hit["classificacao_passo1"] = classificacao_passo1.get(chave, "nao_classificado")

# Salvar CSV
csv_path = OUT_DIR / "kwic_ampliado.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=[
        "obra", "ano", "grupo", "termo", "pagina",
        "contexto_antes_50", "trecho_central", "contexto_depois_50",
        "classificacao_passo1",
    ])
    w.writeheader()
    w.writerows(hits_amplos)
print(f"CSV salvo em: {csv_path}")

# --- Curadoria: pontuar cada hit por densidade figural no entorno ---

# Heurística: contar quantos termos figurativos (de qualquer grupo prioritário)
# aparecem na janela ±50. Quanto mais, mais "denso" é o trecho.
todos_termos = []
for g in CAMPOS_PRIORITARIOS:
    if g in CAMPOS:
        todos_termos.extend(CAMPOS[g]["termos"])
rx_todos = construir_regex(todos_termos)


def score_densidade(hit):
    trecho = f"{hit['contexto_antes_50']} {hit['trecho_central']} {hit['contexto_depois_50']}"
    return len(rx_todos.findall(trecho))


for hit in hits_amplos:
    # Hits classificados como descritivo pelo passo 1 ficam com score 0 (caem da curadoria)
    if hit.get("classificacao_passo1") == "descritivo":
        hit["score_densidade"] = 0
    else:
        hit["score_densidade"] = score_densidade(hit)


# --- Selecionar melhores passagens por (obra × grupo) ---

# Para cada (obra, grupo), pegar até 4 hits com maior densidade figural,
# evitando hits em páginas vizinhas (para diversidade dentro da obra).

por_obra_grupo = defaultdict(list)
for hit in hits_amplos:
    por_obra_grupo[(hit["obra"], hit["grupo"])].append(hit)

curadas = []
N_POR_PAR = 4
for chave, hits in por_obra_grupo.items():
    # Filtrar hits com score 0 (descritivos do passo 1)
    hits_validos = [h for h in hits if h["score_densidade"] > 0]
    # Ordenar por score desc, então por página asc para desempate
    ordenados = sorted(hits_validos, key=lambda h: (-h["score_densidade"], h["pagina"]))
    selecionados = []
    paginas_ja = set()
    for h in ordenados:
        # Diversidade: pular se já temos passagem em página vizinha (±2)
        if any(abs(h["pagina"] - p) <= 2 for p in paginas_ja):
            continue
        selecionados.append(h)
        paginas_ja.add(h["pagina"])
        if len(selecionados) >= N_POR_PAR:
            break
    curadas.extend(selecionados)

print(f"Total de passagens curadas: {len(curadas)}")
print(f"Distribuição por (obra × grupo):")
dist = defaultdict(int)
for h in curadas:
    dist[(OBRAS[h["obra"]], h["grupo"])] += 1
for (obra, g), n in sorted(dist.items()):
    print(f"  {obra} | {g}: {n}")

# --- Gerar relatório Markdown com blocos LaTeX prontos ---

md_path = OUT_DIR / "passagens_curadas.md"
with open(md_path, "w", encoding="utf-8") as f:
    f.write("# Passagens curadas para o capítulo 2 da tese\n\n")
    f.write("Resultado do passo 4 do refinamento da análise das figurações em Latour.\n")
    f.write(f"Janela KWIC: ±{WINDOW} palavras. Curadoria automática por densidade figural ")
    f.write("(número de termos do catálogo figurativo no entorno ±50 palavras).\n\n")
    f.write("Cada passagem é apresentada (i) em prosa contínua, com a palavra-chave do campo ")
    f.write("em **negrito**, e (ii) como bloco LaTeX `citacaoabnt` pronto para colar no capítulo 2 da tese.\n\n")
    f.write("Os trechos vêm dos textos normalizados em `corpus/txt_norm/`; ")
    f.write("podem conter resíduos de OCR. Revisar contra o PDF original ao usar.\n\n")
    f.write("---\n\n")

    # Agrupar por obra > grupo
    by_obra = defaultdict(lambda: defaultdict(list))
    for h in curadas:
        by_obra[h["obra"]][h["grupo"]].append(h)

    for obra in OBRAS:
        if obra not in by_obra:
            continue
        f.write(f"## {OBRAS[obra]} ({ANO[obra]})\n\n")
        for grupo in CAMPOS_PRIORITARIOS:
            if grupo not in by_obra[obra]:
                continue
            hits_g = by_obra[obra][grupo]
            f.write(f"### Campo: `{grupo}`\n\n")
            nota = CAMPOS[grupo].get("nota", "")
            if nota:
                f.write(f"*Nota do catálogo:* {nota}\n\n")
            for i, h in enumerate(hits_g, 1):
                trecho_inline = (
                    f"{h['contexto_antes_50']} "
                    f"**{h['trecho_central']}** "
                    f"{h['contexto_depois_50']}"
                )
                # Limpar espaços múltiplos
                trecho_inline = re.sub(r"\s+", " ", trecho_inline).strip()
                trecho_latex = (
                    f"{h['contexto_antes_50']} "
                    f"\\textbf{{{h['trecho_central']}}} "
                    f"{h['contexto_depois_50']}"
                )
                trecho_latex = re.sub(r"\s+", " ", trecho_latex).strip()
                f.write(f"**Passagem {i}** (p.~{h['pagina']}, termo: `{h['termo']}`, ")
                f.write(f"densidade: {h['score_densidade']} termos figurais na janela)\n\n")
                f.write(f"> {trecho_inline}\n\n")
                f.write("```latex\n")
                f.write("\\begin{citacaoabnt}\n")
                # Quebrar para no máximo 90 caracteres por linha para legibilidade
                palavras = trecho_latex.split()
                linha = ""
                for w in palavras:
                    if len(linha) + len(w) + 1 > 90:
                        f.write(linha + "\n")
                        linha = w
                    else:
                        linha = (linha + " " + w).strip()
                if linha:
                    f.write(linha + "\n")
                f.write(f"\\end{{citacaoabnt}}\n")
                f.write(f"\\parencite[p.~{h['pagina']}]{{")
                bibkey = {
                    "latour_woolgar_1986_lab_life_en": "Latour1997VidaLaboratorio",
                    "latour_1987_science_action_en": "Latour2011CienciaEmAcao",
                    "latour_1999_pandora_en": "Latour2017Esperanca",
                }[h["obra"]]
                f.write(f"{bibkey}}}\n")
                f.write("```\n\n")
            f.write("\n")
        f.write("---\n\n")

print(f"Relatório salvo em: {md_path}")

# Corpus

Esta pasta versiona o catálogo bibliográfico do corpus e o texto extraído dos PDFs. Os PDFs em si ficam em pasta privada do Google Drive sincronizada localmente; o caminho está em `.env` na variável `CORPUS_PDF_PATH`.

## Arquivos versionados

- `metadata.csv`: catálogo bibliográfico (33 obras, 15 colunas). Fonte de verdade.
- `txt/<id>.txt`: texto extraído de cada PDF processado, com `\f` entre páginas.
- `paginas/<id>.csv`: classificação por página (`pagina`, `classe`, `n_chars`, `n_palavras`, `qualidade_pagina`), gerada por `scripts/01_extract_text.py`.
- `qualidade_extracao.csv`: tabela-resumo por obra (páginas, palavras, taxas de qualidade), gerada por `scripts/01_extract_text.py`.

## Colunas de `metadata.csv`

`id, autor, titulo, ano_edicao, ano_primeira_edicao, idioma, tipo_edicao, tradutor, editora, cidade, isbn, arquivo_pdf, status_upload, escopo_etapa1, observacoes`

A coluna `escopo_etapa1` controla quais obras entram na execução da Etapa 1. A pesquisadora marca `sim` ou `nao`. Os scripts respeitam esse filtro.

## Convenção de nomes dos PDFs

Cada arquivo segue o padrão `<autor>_<ano>_<slug_titulo>_<idioma>.pdf`, em letras minúsculas, sem acentos. O script `scripts/01_extract_text.py` localiza cada PDF pelo nome exato registrado na coluna `arquivo_pdf` da `metadata.csv`.

## Etapa 1: obras em execução

Marcadas com `escopo_etapa1 = sim` em `metadata.csv` (decisão de 13/05/2026, ver `docs/decisoes_metodologicas.md`):

- `latour_woolgar_1986_lab_life_en` — Latour e Woolgar, *Laboratory Life: The Construction of Scientific Facts*, Princeton University Press, 1986 (2ª edição com pós-escrito).
- `latour_1987_science_action_en` — Bruno Latour, *Science in Action*, Harvard University Press, 1987.
- `latour_1999_pandora_en` — Bruno Latour, *Pandora's Hope*, Harvard University Press, 1999.

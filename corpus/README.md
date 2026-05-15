# Corpus

Esta pasta versiona o catálogo bibliográfico do corpus e o texto extraído dos PDFs. Os PDFs em si ficam em pasta privada do Google Drive sincronizada localmente; o caminho está em `.env` na variável `CORPUS_PDF_PATH`.

## Arquivos versionados

- `metadata.csv`: catálogo bibliográfico (33 obras, 15 colunas). Fonte de verdade.
- `txt/<id>.txt`: texto extraído de cada PDF processado, com `\f` entre páginas.
- `paginas/<id>.csv`: classificação por página (`pagina`, `classe`, `n_chars`, `n_palavras`, `qualidade_pagina`), gerada por `scripts/01_extract_text.py`.
- `qualidade_extracao.csv`: tabela-resumo por obra (páginas, palavras, taxas de qualidade), gerada por `scripts/01_extract_text.py`.

## Colunas de `metadata.csv`

`id, autor, titulo, ano_edicao, ano_primeira_edicao, idioma, tipo_edicao, tradutor, editora, cidade, isbn, arquivo_pdf, status_upload, escopo_etapa1, escopo_etapa2, observacoes`

As colunas `escopo_etapa1` e `escopo_etapa2` controlam quais obras entram em cada execução. A pesquisadora marca `sim` ou `nao`. Os scripts `02_kwic.py`, `03_frequencies.py`, `04_visualizations.py` e `05_cooccurrence.py` aceitam o argumento `--escopo etapa1|etapa2|todos` (default: `etapa1`).

## Convenção de nomes dos PDFs

Cada arquivo segue o padrão `<autor>_<ano>_<slug_titulo>_<idioma>.pdf`, em letras minúsculas, sem acentos. O script `scripts/01_extract_text.py` localiza cada PDF pelo nome exato registrado na coluna `arquivo_pdf` da `metadata.csv`.

## Etapa 1: obras em execução

Marcadas com `escopo_etapa1 = sim` em `metadata.csv` (decisão de 13/05/2026, ver `docs/decisoes_metodologicas.md`):

- `latour_woolgar_1986_lab_life_en` — Latour e Woolgar, *Laboratory Life: The Construction of Scientific Facts*, Princeton University Press, 1986 (2ª edição com pós-escrito).
- `latour_1987_science_action_en` — Bruno Latour, *Science in Action*, Harvard University Press, 1987.
- `latour_1999_pandora_en` — Bruno Latour, *Pandora's Hope*, Harvard University Press, 1999.

## Etapa 2: artigos teóricos de Latour

Marcadas com `escopo_etapa2 = sim` em `metadata.csv` (decisão de 15/05/2026, ver `briefing_etapa2_artigos_latour.md` e seção `Etapa 2` de `docs/decisoes_metodologicas.md`):

- `latour_1996_clarifications_en` — Bruno Latour, *On Actor-Network Theory: A Few Clarifications*, *Soziale Welt*, vol. 47, n. 4, pp. 369-381, 1996. Texto integral (14 páginas internas do PDF; 7.934 palavras de corpo).
- `latour_1999_recalling_en` — Bruno Latour, *On Recalling ANT*, in Law e Hassard (orgs.), *Actor Network Theory and After*, Blackwell, Oxford, pp. 15-25, 1999. Cobertura parcial: páginas 16-24 do volume (1.344 palavras de corpo, cerca de 80% do artigo). Páginas 15 e 25 excluídas por falha sistemática de OCR no zip de origem; a passagem-chave dos pp. 19-20 sobre a contaminação do vocabulário permanece integralmente no corpus. Detalhamento em `docs/decisoes_metodologicas.md`, seção Etapa 2.

### Particularidades dos `.txt` da Etapa 2

Os arquivos vieram já normalizados fora do pipeline, em sessão de chat anterior, e foram depositados diretamente em `corpus/txt_norm/`. A cadeia de mediação é registrada como dado etnográfico, em coerência com o tratamento dado às demais cadeias técnicas pela tese. Convenções:

- Cabeçalho `# ...` nas primeiras linhas, com `slug`, `autor`, `ano`, `titulo`, `publicacao`, `paginas_originais`, `idioma`, `origem` e `nota_estrutura`. O pipeline pula essas linhas via `ler_texto_sem_cabecalho` em `scripts/02_kwic.py`.
- Caracteres de controle ASCII de baixa ordem (`\x02` em particular, no papel funcional de soft hyphen do OCR) são substituídos por espaço na leitura, preservando offsets. Esse tratamento é análogo ao Adendo 1 das decisões metodológicas (soft hyphen U+00AD nos livros).
- Não há `paginas/<id>.csv` para os artigos: a heurística de classificação de página de `scripts/01_extract_text.py` foi calibrada para a estrutura monográfica (`Chapter N`) dos livros, distinta da estrutura dos artigos. A estratificação por classe de página fica pendente caso necessária em etapas posteriores.

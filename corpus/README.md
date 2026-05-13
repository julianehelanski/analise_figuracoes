# Corpus

Esta pasta versiona apenas:

- `README.md` (este arquivo, com a lista esperada de obras),
- `metadata.csv` (catalogação por obra),
- `txt/` (texto extraído dos PDFs, em UTF-8, gerado pelos scripts).

Os **PDFs ficam fora do repositório**, em pasta privada do Google Drive sincronizada localmente. O caminho está em `.env` na variável `CORPUS_PDF_PATH`.

## Convenção de nomes dos PDFs

Cada arquivo deve seguir o padrão `<autor>_<ano>_<slug_titulo>.pdf`, em letras minúsculas, sem acentos, com `_` como separador. O `<slug_titulo>` é uma versão curta do título principal. Exemplos:

```
latour_1987_science_in_action.pdf
haraway_2016_staying_with_the_trouble.pdf
```

O script `scripts/01_extract_text.py` aceita também variações próximas do nome canônico (correspondência por substring case-insensitive sobre `autor + ano`).

## Obras esperadas no corpus completo (Etapa 3)

A Etapa 1 trabalha apenas com as duas primeiras obras de cada autor marcadas com `prioridade=1`. As outras entram a partir da Etapa 3.

### Latour

| id | autor | título | ano | idioma | edição | prioridade |
|----|-------|--------|-----|--------|--------|------------|
| latour_1984 | Bruno Latour | Les microbes: guerre et paix | 1984 | fr | Métailié | 2 |
| latour_1987 | Bruno Latour | Science in Action | 1987 | en | Harvard | 1 |
| latour_1996_ant_clarifications | Bruno Latour | On actor-network theory: a few clarifications | 1996 | en | Soziale Welt | 3 |
| latour_1999_recalling_ant | Bruno Latour | On recalling ANT | 1999 | en | Sociological Review | 3 |
| latour_1999_pandoras_hope | Bruno Latour | Pandora's Hope | 1999 | en | Harvard | 2 |
| latour_2005_reassembling | Bruno Latour | Reassembling the Social | 2005 | en | Oxford | 2 |

### Haraway

| id | autor | título | ano | idioma | edição | prioridade |
|----|-------|--------|-----|--------|--------|------------|
| haraway_1985_cyborg | Donna Haraway | A Cyborg Manifesto | 1985 | en | Socialist Review | 2 |
| haraway_1988_situated | Donna Haraway | Situated Knowledges | 1988 | en | Feminist Studies | 2 |
| haraway_1992_monsters | Donna Haraway | The Promises of Monsters | 1992 | en | Routledge | 3 |
| haraway_1997_modest_witness | Donna Haraway | Modest_Witness@Second_Millennium | 1997 | en | Routledge | 3 |
| haraway_2003_companion_species | Donna Haraway | The Companion Species Manifesto | 2003 | en | Prickly Paradigm | 3 |
| haraway_2008_when_species_meet | Donna Haraway | When Species Meet | 2008 | en | Minnesota | 2 |
| haraway_2016_staying_with_the_trouble | Donna Haraway | Staying with the Trouble | 2016 | en | Duke | 1 |

## Etapa 1: corpus inicial confirmado

- `latour_1987_science_in_action.pdf` (sugestão do plano, pendente de confirmação da Juliane antes de extrair).
- `haraway_2016_staying_with_the_trouble.pdf` (em execução nesta sessão).

## Saída de extração

Os scripts gravam o texto extraído em `corpus/txt/<id>.txt`, onde `<id>` corresponde à coluna `id` da tabela acima.

# Passo 4 — KWIC ampliado e curadoria de passagens citáveis

**Data:** 15 de maio de 2026.
**Propósito:** alimentar o capítulo 2 da tese com passagens de Latour prontas para citação direta, no contexto da análise da tensão figural entre o vocabulário agonístico de Latour e a figuração têxtil-feminista de Haraway.

## Política de versionamento

Os artefatos deste passo reproduzem trechos extensos das obras de Latour (cerca de ±50 palavras de contexto por ocorrência, em volume agregado significativo). Para preservar a conformidade com os direitos autorais das editoras (Harvard University Press, Princeton University Press), os arquivos com reprodução textual ficam **fora do repositório público**:

- `kwic_ampliado.csv` (gerado localmente, no `.gitignore`)
- `passagens_curadas.md` (gerado localmente, no `.gitignore`)
- `sequencia_exercito_ciencia.md` (curadoria argumentativa, no `.gitignore`)

O **pipeline reprodutível** está versionado: qualquer pessoa com os PDFs originais legalmente adquiridos pode gerar os arquivos rodando o script. O que circula publicamente é a metodologia, o script e este README.

## Geração local dos artefatos

Pré-requisitos: corpus extraído em `corpus/txt_norm/` e classificação de páginas em `corpus/paginas/` (gerados pela Etapa 1 do pipeline).

```bash
python3 scripts/10_passo4_kwic_ampliado.py
```

Produz:

### `kwic_ampliado.csv`

Todas as ocorrências dos 12 campos figurativos prioritários nas três obras de Latour, em janela de ±50 palavras (cinco vezes a janela do KWIC original de ±10). Colunas: `obra`, `ano`, `grupo`, `termo`, `pagina`, `contexto_antes_50`, `trecho_central`, `contexto_depois_50`, `classificacao_passo1` (apenas para `war`/`wars` em *Pandora's Hope*: `descritivo`, `figurativo` ou vazio).

Filtros: páginas classificadas como `corpo` ou `inicio_capitulo`, exclusões do catálogo lexical aplicadas em janela ±5 adjacente, classificação manual do passo 1 anexada para hits em *Pandora's Hope*.

### `passagens_curadas.md`

Até 4 passagens por par (obra × campo figurativo), selecionadas automaticamente pela densidade figural no entorno ±50 palavras. Diversidade interna garantida por exclusão de hits em páginas vizinhas (±2). Hits descritivos do passo 1 são excluídos da curadoria.

Cada passagem aparece em prosa com palavra-chave em negrito e como bloco LaTeX `citacaoabnt` com `\parencite` correspondente. 90 passagens curadas cobrindo 26 pares (obra × grupo).

### `sequencia_exercito_ciencia.md`

Curadoria temática manual de 9 passagens articuladas em sequência argumentativa (analogia → identificação literal → autocrítica) sobre exército e ciência em Latour, da analogia da colina em *Laboratory Life* à formulação da epistemologia como *Cold War machine* em *Pandora's Hope*.

## Aviso sobre OCR

Os textos vêm de `corpus/txt_norm/`, gerados por extração automática de PDF. Podem conter resíduos de OCR (palavras truncadas, espaços extras, hifenizações mal recompostas). Sempre revisar a passagem contra o PDF original antes de usar como citação na tese.

## Chaves BibTeX usadas

- *Laboratory Life* (1986) → `Latour1997VidaLaboratorio`
- *Science in Action* (1987) → `Latour2011CienciaEmAcao`
- *Pandora's Hope* (1999) → `Latour2017Esperanca`

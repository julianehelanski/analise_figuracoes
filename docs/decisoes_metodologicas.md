# Decisões metodológicas

Este documento registra cada decisão tomada ao longo da execução do pipeline. Mantenho aqui o histórico em ordem cronológica, em primeira pessoa, com o nome de quem decidiu e a justificativa.

## Etapa 0: preparação do ambiente e do corpus

### Estrutura de pastas inicial

Quem decidiu: Juliane (autorizou a criação via instrução "execute o caminho 1" em 2026-05-13).

O que decidi: criar a estrutura prevista no `README.md` (pastas `corpus/`, `campos_lexicais/`, `scripts/`, `outputs/{csv,figuras,relatorios,latex}/`, `docs/`) com `.gitkeep` nas pastas vazias. Os PDFs ficam fora do repositório, em pasta Drive sincronizada localmente, conforme o princípio do `CLAUDE.md`.

### `.gitignore`

Quem decidiu: padrão de projeto.

O que decidi: ignorar `.env`, qualquer `*.pdf` no repositório, ambientes virtuais, caches Python, configurações de IDE e outputs intermediários grandes. Mantenho `outputs/` versionado para CSVs, figuras e relatórios citáveis.

### Catálogo do corpus dentro do script `01_extract_text.py`

Quem decidi: Claude Code (pendente de validação por Juliane).

O que decidi: o catálogo das obras esperadas (id, autor, título, ano, idioma, edição, prioridade) está duplicado em duas representações: a tabela em `corpus/README.md` e a tupla `CATALOGO` em `scripts/01_extract_text.py`. Justificativa: evitar dependência de parser de markdown e manter o script auto-suficiente. A consistência entre os dois é responsabilidade da pesquisadora; se a tabela for atualizada, atualizar o script.

Pendência: confirmar com Juliane se prefere centralizar o catálogo em um único arquivo (por exemplo, YAML em `corpus/catalogo.yaml`) lido por ambos.

### Convenção de nomes dos PDFs

Quem decidiu: Claude Code, com base no padrão sugerido no plano.

O que decidi: padrão `<autor>_<ano>_<slug_titulo>.pdf`, em minúsculas, sem acentos. O script casa por substring case-insensitive sobre sobrenome do autor e ano, então tolera variações próximas. Para a Etapa 1, a obra de Haraway 2016 espera nome contendo `haraway` e `2016`.

### Heurística de detecção de corpo de texto

Quem decidiu: Claude Code (pendente de validação amostral pela Juliane).

O que decidi: o início do corpo é a primeira linha que case com `Chapter 1`, `Introduction`, `Capítulo 1` ou `Chapitre 1`; o fim é a primeira ocorrência pós-início de `Bibliography`, `References`, `Bibliografia` ou `Notes`. Limitação declarada: livros sem cabeçalhos canônicos (por exemplo, ensaios curtos sem numeração de capítulos) podem retornar `inicio=None`. Nesses casos, a contagem de palavras cai sobre o texto inteiro.

### Avaliação heurística de qualidade da extração

Quem decidiu: Claude Code.

O que decidi: classificação em `boa`, `media` ou `baixa` com base em duas métricas: (a) proporção de caracteres fora de alfanuméricos, espaço e pontuação corrente; (b) proporção de linhas muito curtas (< 10 caracteres). Limites: `baixa` se (a) > 5% ou (b) > 50%; `media` entre 2-5% ou 30-50%; `boa` abaixo disso. Pendência: a Juliane confere amostralmente 3 trechos por livro antes de aceitar a extração como `boa`.

### Fallback de extração

Quem decidiu: Claude Code.

O que decidi: tento primeiro `pdftotext -layout` (poppler-utils). Se não estiver disponível ou falhar, tento `pdfminer.six`. Se ambos falharem, paro com mensagem de erro e instruções para a Juliane. Limitação declarada: nenhum dos dois usa OCR; se um PDF for puramente raster (digitalização sem camada de texto), terei que ativar `tesseract` em etapa posterior e reportar.

## Etapa 1: lexicometria mínima

### Campos lexicais iniciais

Quem decidiu: Claude Code (transcrição literal do `plano_de_trabalho.md`).

O que decidi: gerei `campos_lexicais/haraway_textil_en.txt` e `campos_lexicais/latour_militar_en.txt` com os 10 grupos terminológicos listados no plano, mais variantes morfológicas pré-expandidas (plurais, formas verbais comuns). Cada linha tem a forma canônica como primeiro token e variantes separadas por vírgula. Termos de controle (`network` para Latour, `holobiont` para Haraway) estão presentes para servir como linha de base contra a qual interpretar a densidade dos termos figurais.

Pendência: na Etapa 2, refinarei os campos lexicais com base na validação amostral codificada pela Juliane.

### Janela KWIC

Quem decidiu: Claude Code, seguindo a sugestão do `plano_de_trabalho.md`.

O que decidi: janela padrão de 50 palavras antes e 50 depois, configurável via `--janela`. Pendência: confirmar com Juliane se 50 palavras é a janela ideal para o trabalho interpretativo (registrado como decisão pendente no plano).

### Marcação de prováveis notas de rodapé

Quem decidiu: Claude Code.

O que decidi: marco como `provavel_nota_rodape=1` cada ocorrência cuja linha de origem comece com 1 a 3 dígitos seguidos de letra. Limitação declarada: heurística captura uma fração das notas e produz falsos positivos quando o corpo do texto começa com numerais. A coluna serve como filtro indicativo, não como verdade. Na Etapa 2, refino esse critério se a taxa de falsos positivos for alta.

### Estimativa de página

Quem decidiu: Claude Code.

O que decidi: interpolação linear entre posição em caracteres e total de páginas (lido de `corpus/metadata.csv`). Limitação declarada: livros com cabeçalhos, sumários e bibliografia distorcem a interpolação; o resultado é aproximação grosseira ("pág. ~123"), suficiente para localizar passagens mas não para citação direta. Para citação na tese, a Juliane confere a página no PDF.

## Pendências em aberto

1. Confirmar corpus inicial da Etapa 1 (Haraway 2016 já em execução; Latour 1987 ainda não autorizado).
2. Confirmar idioma de trabalho preferencial: originais sempre, ou comparar com traduções brasileiras quando existirem?
3. Confirmar janela KWIC de 50 palavras como padrão definitivo.
4. Decidir se o catálogo de obras vira arquivo YAML único lido pelo script e pelo README, ou continua duplicado.
5. Validar heurística de detecção de corpo e qualidade da extração em amostra de 3 trechos por livro.

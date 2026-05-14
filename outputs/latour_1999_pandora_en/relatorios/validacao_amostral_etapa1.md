# Validação amostral (Etapa 2): latour_1999_pandora_en

Codificação automatizada por `scripts/08_validate_sample.py` sobre o texto
normalizado em `corpus/txt_norm/<obra>.txt`. Cada página é classificada como
`sim`, `nao` ou `parcial` quanto à correção do estrato predito. Inferências
ambíguas são marcadas com `[INFERÊNCIA]` no campo de decisão metodológica.

## Resumo por estrato

| Estrato | n | sim | parcial | nao | taxa de acerto |
|---|---:|---:|---:|---:|---:|
| `inicio_capitulo` | 3 | 3 | 0 | 0 | 100% |
| `corpo` | 3 | 3 | 0 | 0 | 100% |
| `notas_fim` | 0 | – | – | – | – |
| `paratexto` | 3 | 2 | 1 | 0 | 67% |
| `qualidade_baixa` | 3 | 3 | 0 | 0 | 100% |

## Codificação por página

### Estrato `inicio_capitulo`

**Página 35**  
- estrato_correto: `sim`  
- decisão: cabeçalho de capítulo encontrado nas primeiras 5 linhas  
- erro_extracao: 1 bloco(s) de letras espaçadas (running header)  

**Página 12**  
- estrato_correto: `sim`  
- decisão: cabeçalho de capítulo encontrado nas primeiras 5 linhas  
- erro_extracao: 1 bloco(s) de letras espaçadas (running header)  

**Página 124**  
- estrato_correto: `sim`  
- decisão: cabeçalho de capítulo encontrado nas primeiras 5 linhas  
- erro_extracao: 1 bloco(s) de letras espaçadas (running header)  

### Estrato `corpo`

**Página 231**  
- estrato_correto: `sim`  
- decisão: prosa contínua (446 palavras)  
- erro_extracao: 1 bloco(s) de letras espaçadas (running header)  

**Página 189**  
- estrato_correto: `sim`  
- decisão: prosa contínua (444 palavras)  

**Página 157**  
- estrato_correto: `sim`  
- decisão: prosa contínua (433 palavras)  
- erro_extracao: 1 bloco(s) de letras espaçadas (running header)  

### Estrato `paratexto`

**Página 7**  
- estrato_correto: `parcial`  
- decisão: [INFERÊNCIA] página sem marcador claro de paratexto; classe herdada do estado anterior  
- erro_extracao: 1 bloco(s) de letras espaçadas (running header)  

**Página 9**  
- estrato_correto: `sim`  
- decisão: 3 linha(s) com padrão de TOC  

**Página 335**  
- estrato_correto: `sim`  
- decisão: cabeçalho de back matter detectado  

### Estrato `qualidade_baixa`

**Página 11**  
- estrato_correto: `sim`  
- decisão: apenas 0 palavra(s) extraída(s)  

**Página 1**  
- estrato_correto: `sim`  
- decisão: apenas 0 palavra(s) extraída(s)  

**Página 336**  
- estrato_correto: `sim`  
- decisão: apenas 0 palavra(s) extraída(s)  

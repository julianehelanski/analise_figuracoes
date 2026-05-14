# Validação amostral (Etapa 2): latour_1987_science_action_en

Codificação automatizada por `scripts/08_validate_sample.py` sobre o texto
normalizado em `corpus/txt_norm/<obra>.txt`. Cada página é classificada como
`sim`, `nao` ou `parcial` quanto à correção do estrato predito. Inferências
ambíguas são marcadas com `[INFERÊNCIA]` no campo de decisão metodológica.

## Resumo por estrato

| Estrato | n | sim | parcial | nao | taxa de acerto |
|---|---:|---:|---:|---:|---:|
| `inicio_capitulo` | 3 | 3 | 0 | 0 | 100% |
| `corpo` | 3 | 3 | 0 | 0 | 100% |
| `notas_fim` | 3 | 3 | 0 | 0 | 100% |
| `paratexto` | 3 | 2 | 1 | 0 | 67% |
| `qualidade_baixa` | 2 | 2 | 0 | 0 | 100% |

## Codificação por página

### Estrato `inicio_capitulo`

**Página 5**  
- estrato_correto: `sim`  
- decisão: cabeçalho de capítulo encontrado nas primeiras 5 linhas  

**Página 286**  
- estrato_correto: `sim`  
- decisão: cabeçalho de capítulo encontrado nas primeiras 5 linhas  

**Página 148**  
- estrato_correto: `sim`  
- decisão: cabeçalho de capítulo encontrado nas primeiras 5 linhas  

### Estrato `corpo`

**Página 127**  
- estrato_correto: `sim`  
- decisão: prosa contínua (527 palavras)  

**Página 267**  
- estrato_correto: `sim`  
- decisão: prosa contínua (517 palavras)  

**Página 19**  
- estrato_correto: `sim`  
- decisão: prosa contínua (509 palavras)  

### Estrato `notas_fim`

**Página 283**  
- estrato_correto: `sim`  
- decisão: 13 linhas com padrão de nota numerada  

**Página 284**  
- estrato_correto: `sim`  
- decisão: 14 linhas com padrão de nota numerada  

**Página 285**  
- estrato_correto: `sim`  
- decisão: 20 linhas com padrão de nota numerada  

### Estrato `paratexto`

**Página 294**  
- estrato_correto: `parcial`  
- decisão: [INFERÊNCIA] página sem marcador claro de paratexto; classe herdada do estado anterior  

**Página 301**  
- estrato_correto: `sim`  
- decisão: 6 linha(s) com padrão de entrada de índice  

**Página 305**  
- estrato_correto: `sim`  
- decisão: 6 linha(s) com padrão de entrada de índice  

### Estrato `qualidade_baixa`

**Página 72**  
- estrato_correto: `sim`  
- decisão: 18/22 linhas com <10 chars; 7/22 linhas com >50% caracteres não-alfa  
- erro_extracao: 18/22 linhas com <10 chars; 7/22 linhas com >50% caracteres não-alfa  

**Página 314**  
- estrato_correto: `sim`  
- decisão: apenas 0 palavra(s) extraída(s)  

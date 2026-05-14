# Validação amostral (Etapa 2): latour_woolgar_1986_lab_life_en

Codificação automatizada por `scripts/08_validate_sample.py` sobre o texto
normalizado em `corpus/txt_norm/<obra>.txt`. Cada página é classificada como
`sim`, `nao` ou `parcial` quanto à correção do estrato predito. Inferências
ambíguas são marcadas com `[INFERÊNCIA]` no campo de decisão metodológica.

## Resumo por estrato

| Estrato | n | sim | parcial | nao | taxa de acerto |
|---|---:|---:|---:|---:|---:|
| `inicio_capitulo` | 3 | 3 | 0 | 0 | 100% |
| `corpo` | 3 | 3 | 0 | 0 | 100% |
| `notas_fim` | 3 | 0 | 3 | 0 | 0% |
| `paratexto` | 3 | 2 | 1 | 0 | 67% |
| `qualidade_baixa` | 3 | 3 | 0 | 0 | 100% |

## Codificação por página

### Estrato `inicio_capitulo`

**Página 236**  
- estrato_correto: `sim`  
- decisão: cabeçalho de capítulo encontrado nas primeiras 5 linhas  

**Página 16**  
- estrato_correto: `sim`  
- decisão: cabeçalho de capítulo encontrado nas primeiras 5 linhas  

**Página 244**  
- estrato_correto: `sim`  
- decisão: cabeçalho de capítulo encontrado nas primeiras 5 linhas  

### Estrato `corpo`

**Página 248**  
- estrato_correto: `sim`  
- decisão: prosa contínua (450 palavras)  

**Página 111**  
- estrato_correto: `sim`  
- decisão: prosa contínua (450 palavras)  

**Página 85**  
- estrato_correto: `sim`  
- decisão: prosa contínua (433 palavras)  

### Estrato `notas_fim`

**Página 102**  
- estrato_correto: `parcial`  
- decisão: [INFERÊNCIA] página esparsa (4 palavras): possivelmente photograph file ou similar  

**Página 96**  
- estrato_correto: `parcial`  
- decisão: [INFERÊNCIA] página esparsa (4 palavras): possivelmente photograph file ou similar  

**Página 94**  
- estrato_correto: `parcial`  
- decisão: [INFERÊNCIA] página esparsa (4 palavras): possivelmente photograph file ou similar  

### Estrato `paratexto`

**Página 293**  
- estrato_correto: `sim`  
- decisão: 32 linha(s) com padrão de TOC  

**Página 284**  
- estrato_correto: `parcial`  
- decisão: [INFERÊNCIA] página sem marcador claro de paratexto; classe herdada do estado anterior  

**Página 7**  
- estrato_correto: `sim`  
- decisão: 39 linha(s) com padrão de TOC  

### Estrato `qualidade_baixa`

**Página 296**  
- estrato_correto: `sim`  
- decisão: apenas 0 palavra(s) extraída(s)  

**Página 222**  
- estrato_correto: `sim`  
- decisão: apenas 1 palavra(s) extraída(s)  

**Página 1**  
- estrato_correto: `sim`  
- decisão: apenas 0 palavra(s) extraída(s)  

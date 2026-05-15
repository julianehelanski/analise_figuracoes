---

## Extensão da análise lexicométrica aos artigos teóricos de Latour (1996, 1999)

Data da decisão: 15 de maio de 2026.

### Motivação

A inspeção qualitativa dos dois artigos metateóricos de Latour disponíveis no projeto, *On actor-network theory: a few clarifications* (1996, *Soziale Welt*, v. 47, n. 4, pp. 369-381) e *On recalling ANT* (1999, in Law e Hassard, *Actor Network Theory and After*, Oxford: Blackwell, pp. 15-25), sugeriu que o vocabulário figurativo desses textos opera em registro distinto do dos três livros monográficos da Etapa 1. Nos artigos, o léxico militar-industrial recua sensivelmente, e o léxico que ocupa o seu lugar é o têxtil-topológico (`network`, `filament`, `fluid`, `weaving`, `thread`, `fibrous`, `knot`, `ropy`, `stringy`, `wiry`). Em *On recalling ANT*, Latour formula a autocrítica explícita ao reconhecer que o vocabulário da TAR contaminou a operação descritiva que essa mesma teoria reivindicava (pp. 19-20). Submeter essa intuição qualitativa à mesma contagem sistemática da Etapa 1 produz, se confirmada, evidência de divisão de trabalho metafórico por gênero textual: o vocabulário militar-industrial domina onde Latour faz descrição de campo e recua onde reflete metateoricamente sobre o próprio vocabulário. O resultado é registro citável para o capítulo 2 da tese, na subseção que ancora a leitura empírica da figuração militar-industrial.

### Decisão

Os dois artigos passam a integrar o corpus da análise lexicométrica como textos adicionais, com slugs `latour_1996_clarifications_en` e `latour_1999_recalling_en`. A contagem usa o mesmo catálogo de dezessete campos figurais da Etapa 1, sem ajuste de parâmetros. A apresentação dos resultados é comparativa entre os cinco textos (três livros mais dois artigos), agregada em `outputs/etapa2_artigos/`. O briefing operacional desta extensão fica versionado na raiz do repositório como `briefing_etapa2_artigos_latour.md`. As condições de execução, os gates de revisão e os outputs esperados estão registrados nesse briefing e não são repetidos aqui.

### Aplicação simétrica do catálogo e dos parâmetros

A defensabilidade do contraste entre artigos e livros depende de instrumentação idêntica. Por isso, o catálogo de dezessete campos figurais permanece inalterado, a janela KWIC continua em $\pm 10$ palavras (decisão da Etapa 1), e a contagem segue o mesmo modelo de densidade por dez mil palavras. Acréscimo de variantes ao catálogo, se necessário, fica em arquivo separado `campos_lexicais/latour_*_en_etapa2_adicoes.txt`, com adendo de justificativa neste documento.

### Tratamento do OCR como gesto registrado no apêndice metodológico

Os dois artigos vieram como zips de OCR página-a-página, com extensão `.PDF` mas conteúdo de imagem mais texto extraído por página. A normalização para `.txt` foi feita fora do pipeline, em sessão de chat com o Claude no dia 15 de maio de 2026, antes do início da execução da extensão. A normalização aplicou as operações que constam no cabeçalho de metadados de cada `.txt`: concatenação de páginas em ordem natural (sort numérico), remoção de carriage returns e form feeds, remoção de rodapé editorial recorrente do Recalling (variantes de "© The Editorial Board of The Sociological Review 1999"), remoção de linhas que contêm apenas números (numeração de página solta), correção de hifenização de fim de linha, junção de linhas dentro de parágrafos preservando dupla quebra como fronteira. Erros de OCR difusos (palavras grudadas como "manufacturersdo", letras trocadas como "llix" em vez de "Felix", caracteres de controle nó binarizado) não foram corrigidos, porque a correção exigiria julgamento caso a caso e introduziria interferência no material que importa registrar como ele chegou.

O gesto da normalização fora do pipeline é dado etnográfico, em coerência com o que o capítulo 4 da tese descreve para outras cadeias de mediação técnica (a coleta de áudio do Spira passa por filtros, conversões, etiquetagem, espectrogramas, e cada passo é parte da rede que produz a inscrição final). A diferença entre a Etapa 1, em que a extração foi feita pelo pipeline Python a partir de PDFs nativos, e esta extensão, em que a normalização foi feita pelo Claude no chat a partir de OCRs já feitos, marca dois tipos de mediação computacional que a tese tematiza: o script versionado que opera de modo reprodutível, e o gesto situado de uma sessão de inferência em modelo de linguagem que opera por edição interativa e produz artefato único.

### Restrição de cobertura do Recalling

O zip de OCR do *Recalling* tem 11 páginas, e a inspeção qualitativa identificou que as páginas com numeração ímpar do zip (1, 3, 5, 7, 9, 11) trazem OCR severamente truncado nas primeiras letras de cada linha, com palavras cortadas como `llix` (= Felix), `otion` (= notion), `ncrediblepretensions` (= Incredible pretensions), `Ivenot` (= I have not). As páginas com numeração par do zip (2, 4, 6, 8, 10) trazem OCR limpo do texto principal, cobrindo as páginas 16, 18, 20, 22, 24 do volume original. A inspeção por similaridade de sequência (`SequenceMatcher`) sobre pares de páginas consecutivas registrou ratios baixos (entre 0,01 e 0,30), o que descarta duplicação extensa de conteúdo entre páginas. Em casos pontuais como a passagem-chave dos pp. 19-20 sobre a contaminação do vocabulário, o texto se estende da página par (zip 6, p. 20 do volume) para a página ímpar seguinte (zip 7, p. 21 do volume), e o OCR truncado da página ímpar reproduz parte do conteúdo da par anterior em forma corrompida, o que produz contagem dupla artificial dos termos da passagem.

A decisão foi excluir as páginas com numeração ímpar do zip e manter apenas as pares. A cobertura resultante é de aproximadamente 80\% do artigo: pp. 16 a 24 do volume, com 1.344 palavras de corpo. As páginas 15 (abertura e abstract) e 25 (final do texto e início da bibliografia) do volume não estão integralmente representadas. A passagem-chave dos pp. 19-20 sobre a contaminação do vocabulário está integralmente incluída no corpus (no conteúdo da página 6 do zip, correspondente à página 20 do volume).

A restrição enfraquece a quantificação absoluta do *Recalling* e não enfraquece o argumento comparativo. O argumento opera sobre a magnitude da diferença entre o registro figurativo dos livros monográficos e o dos artigos metateóricos, e essa magnitude se mantém pela cobertura de 80\% do artigo, em que a passagem-chave do argumento autocrítico está integralmente representada. O *Clarifications* não tem essa restrição: as 14 páginas estão íntegras e o OCR é limpo.

A pendência fica registrada como item aberto: se um PDF nativo do *Recalling* (em vez do zip de OCR) for obtido em algum momento, a reanálise pode incluir o artigo integral e oferecer contagem mais robusta. Essa pendência abre uma eventual Etapa 2-bis, sem prazo definido.

### Ajustes ao pipeline para textos curtos

O *Recalling* (1.344 palavras de corpo) e o *Clarifications* (7.934 palavras de corpo) são consideravelmente menores que os três livros da Etapa 1 (entre 105 mil e 140 mil palavras). A janela de cocorrência de 200 palavras usada na Etapa 1 corresponde a cerca de 0,15\% do texto de *Science in Action* e a 15\% do texto do *Recalling*. A aplicação da mesma janela aos artigos inflaria artificialmente a matriz de cocorrência. Por isso, a cocorrência dos artigos é calculada em duas versões: a janela fixa de 200 palavras como controle, e uma janela proporcional de 2\% do texto arredondada (cerca de 27 palavras para o *Recalling* e cerca de 159 palavras para o *Clarifications*). A apresentação final escolhe entre as duas versões depois da inspeção dos resultados, no gate 2.4 do briefing da extensão.

### Categorias novas de desambiguação para os artigos

A inspeção qualitativa preliminar das ocorrências do campo militar nos dois artigos identificou dois tipos de uso que não se encaixam nas categorias de desambiguação aplicadas no refinamento da Etapa 3 (`descritivo` versus `figurativo`):

1. **`metalinguistico`**: ocorrência em que Latour cita o próprio vocabulário da TAR para submetê-lo à autocrítica. O exemplo do *Recalling* é a única ocorrência do campo militar nas pp. 16-24 do volume: a palavra `alliance` aparece dentro da sequência `vocabulary association, translation, alliance, obligatory passage point`, em que o autor enumera os termos da própria teoria para questionar a sua pobreza vocabular. Gatilho automático sugerido: ocorrência em vizinhança imediata (cinco palavras) com termos do vocabulário interno da TAR como `association`, `translation`, `passage point`, `actor-network`, `enrollment`.

2. **`descritivo-bibliografico`**: ocorrência em referência bibliográfica ou em título de obra citada. O exemplo do *Clarifications* é a citação do livro `La nouvelle alliance` de Prigogine e Stengers (1979) no corpo do texto. Gatilho automático sugerido: ocorrência em vizinhança imediata com nomes de autores e anos entre parênteses, ou em formatação de bibliografia ao final do artigo.

A planilha de classificação manual segue o mesmo formato de `refinamento/war_pandora_classificacao.csv`, com a coluna `classificacao` aceitando os valores `figurativa`, `descritivo-historica`, `metalinguistico`, `descritivo-bibliografico`. A aplicação simétrica das duas categorias novas se faz também aos três livros da Etapa 1, em caráter retrospectivo, para preservar a comparabilidade. A revisão retrospectiva é uma pendência registrada no plano de execução do briefing.

### Resultado preliminar

A contagem manual exploratória com regex de borda de palavra sobre os `.txt` normalizados, restrita ao corpo do texto, registrou para o campo militar e para amostras dos campos têxtil e topológico:

| Campo | *Recalling* 1999 (1.344 palavras) | *Clarifications* 1996 (7.934 palavras) | *Science in Action* 1987 (139.861 palavras, refinada) |
|---|---:|---:|---:|
| Militar (64 variantes) | 1 ocorrência, 7,44 por dez mil | 3 ocorrências, 3,78 por dez mil | 364 ocorrências, 26,03 por dez mil |
| Têxtil (50 variantes da amostra) | 0 ocorrências, 0,00 por dez mil | 15 ocorrências, 18,91 por dez mil | (a contar) |
| Topologia (5 variantes da amostra: network, fluid, filament, surface, node) | 10 ocorrências, 74,40 por dez mil | 113 ocorrências, 142,43 por dez mil | (a contar) |

A densidade militar nos artigos é de três a sete vezes menor que em *Science in Action*. A densidade topológica nos artigos é várias vezes superior à esperada pela leitura cruzada dos livros. A contagem dos campos têxtil e topológico nos três livros é pendência da Etapa 2 propriamente dita, conforme registrado no briefing.

### Pendência para script

A normalização dos zips de OCR foi feita por código Python ad hoc, executado em ambiente da sessão de chat de 15/05/2026 (`/tmp/latour_artigos_check/normalizar_v3.py`, não versionado). Para entrar no pipeline reprodutível da Etapa 2 plena, será necessário portar a lógica para `scripts/`, com nome sugerido `12_extrair_ocr_zips.py`. A função principal recebe um diretório de zip de OCR e um conjunto de páginas a incluir (parâmetro útil para casos como o *Recalling*, em que metade das páginas precisa ser excluída), e produz `.txt` com cabeçalho de metadados em comentário. A camada de inspeção qualitativa (identificação de páginas com OCR truncado) fica fora do script, como gesto da pesquisadora documentado neste registro.

### Artefatos

- `briefing_etapa2_artigos_latour.md` na raiz do repositório: especificação operacional completa da Etapa 2 dos artigos teóricos, com plano em sete etapas, gates de revisão, e o que está fora do escopo.
- `corpus/txt_norm/latour_1996_clarifications_en.txt`: texto normalizado do *Clarifications*, 8.021 palavras (incluindo cabeçalho de metadados), 48 KB.
- `corpus/txt_norm/latour_1999_recalling_en.txt`: texto normalizado do *Recalling* nas páginas pares do zip (cobertura pp. 16-24 do volume), 1.515 palavras (incluindo cabeçalho), 9 KB.
- `metadata.csv`: duas linhas novas com os slugs, anos, idioma e edição-fonte.
- `outputs/etapa2_artigos/`: diretório de saída a ser criado na execução, com tabelas comparativas em CSV e LaTeX e relatório de síntese.

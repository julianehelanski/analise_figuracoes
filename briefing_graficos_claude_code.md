# Briefing para Claude Code: três gráficos da subseção sobre figuração militar em Latour

Olá, Claude Code. Esta é a continuação do passo 4 do refinamento da análise lexicométrica em `analise_figuracoes`. O commit do KWIC ampliado já foi feito no remoto. Agora vou pedir que você gere três gráficos comparativos que sustentam a subseção `subsec:figuracao_militar_evidencia` do capítulo 2 da minha tese.

## Contexto da subseção que os gráficos vão ilustrar

A subseção apresenta três achados da análise lexicométrica sobre as três obras de Latour (\emph{Laboratory Life} 1986, \emph{Science in Action} 1987, \emph{Pandora's Hope} 1999):

1. O salto de densidade do campo `militar` entre 1986 e 1987 (mais de sete vezes) e sua manutenção em registro alto em 1999.
2. A distribuição transversal do vocabulário militar ao longo dos textos.
3. A centralidade do campo `militar` na rede de cocorrências em SIA 1987, articulando-se com `black_box`, `network`, `inscription`, `translation` e demais conceitos da teoria ator-rede.

Cada achado precisa de uma figura. Três figuras no total.

## Princípios estéticos

**Tipografia.** Default do matplotlib (DejaVu Sans). Tamanho de fonte adequado para leitura quando a figura for incluída como `\includegraphics[width=\textwidth]` em PDF A4.

**Cores.** Paleta sóbria, cinzas e tons neutros, com **um destaque cromático** reservado ao campo `militar`. Sugiro vermelho ferrugem (`#B22222` para SIA, com variantes mais clara e mais escura para Lab Life e Pandora). O destaque é o que carrega o argumento visualmente: o leitor identifica que o campo militar é o objeto da análise.

**Sem títulos dentro do gráfico.** Esta é a instrução mais importante. Cada figura entra na tese com um `\caption` LaTeX completo que cumpre a função de título. Repetir o título dentro do PNG produz redundância visual. Use **apenas** rótulos de eixos, legenda quando houver múltiplas séries, e anotações inline quando agregarem leitura. Em painéis múltiplos, identificadores curtos por painel são aceitáveis (por exemplo, "Science in Action, 1987" no canto superior esquerdo do painel correspondente).

**Sem grid pesado.** Linhas de grade leves no eixo X (cinza claro), nenhuma no Y. Sem moldura completa (`spines` superior e direita removidas).

**Formato de saída.** PNG 300 dpi e SVG, para cada figura, em paralelo.

**Localização.** `outputs/passo4/figuras/`. O diretório não existe ainda; crie-o.

## Política de versionamento

Os três PNG/SVG **vão para o repositório público** (diferente do KWIC ampliado e das passagens curadas, que ficam locais). Gráficos não reproduzem texto de Latour, são representação visual derivada de contagens, portanto não levantam questão de copyright.

## Insumos disponíveis no repositório

Antes de codificar, abra os seguintes arquivos para entender a estrutura dos dados:

- `outputs/<obra_id>/csv/frequencias.csv` (já existente para as três obras): colunas `grupo, n_ocorrencias, n_excluidas, frequencia_por_10k_palavras, variantes_top`.
- `outputs/<obra_id>/csv/cocorrencia.csv` (já existente para SIA): matriz de cocorrências entre grupos.
- `outputs/<obra_id>/csv/kwic.csv` (já existente): colunas `obra, autor_yaml, grupo, termo_encontrado, pagina, posicao_no_texto, contexto_antes, trecho_central, contexto_depois, descartado_por_exclusao`.
- `refinamento/militar_refinado_tres_obras.csv` (passo 1 do refinamento): contagem refinada do campo militar para as três obras (Lab Life 37/3,50; SIA 364/26,03; Pandora 156/12,19).
- `refinamento/war_pandora_classificacao.csv`: classificação manual de war/wars em Pandora; usar para filtrar descritivos antes de plotar.
- `corpus/txt_norm/<obra_id>.txt`: textos normalizados.
- `corpus/paginas/<obra_id>.csv`: classificação por página.
- `campos_lexicais/catalogo_termos.yaml`: catálogo dos 17 campos figurativos.

Número de palavras das obras (valor fixo, do `metadata.csv`): Laboratory Life = 105.749; Science in Action = 139.861; Pandora's Hope = 128.001.

## Especificação dos três gráficos

### Figura 1: comparação da densidade dos 17 campos figurativos nas três obras

**Nome do arquivo:** `comparacao_frequencias_tres_obras.png` e `.svg`.

**Tipo:** gráfico de barras agrupadas horizontais. Eixo Y: nome do campo (17 campos do catálogo). Eixo X: frequência por dez mil palavras. Para cada campo, três barras lado a lado (uma por obra), em cores que indiquem cronologia (1986 mais claro, 1987 médio, 1999 mais escuro).

O campo `militar` ganha as três barras na paleta de **vermelho ferrugem** com mesma lógica cronológica (mais claro para 1986, médio para 1987, mais escuro para 1999). Os demais 16 campos ficam em escala de cinza com a mesma lógica cronológica.

**Dados:** ler `outputs/<obra_id>/csv/frequencias.csv` das três obras e juntar. Para o campo `militar`, **usar a contagem refinada** que está em `refinamento/militar_refinado_tres_obras.csv` (Lab Life refinado 37/3,50; SIA refinado 364/26,03; Pandora refinado 156/12,19), e não a bruta do `frequencias.csv`.

**Ordenação:** ordenar os campos no eixo Y por frequência decrescente em \emph{Science in Action} (a obra com maior densidade total), de modo que `militar` apareça no topo. Isso torna visível, à primeira leitura, o achado central.

**Notas inline:** acrescentar o valor numérico da contagem refinada do `militar` à direita da barra correspondente para cada obra (`3,50` para Lab Life, `26,03` para SIA, `12,19` para Pandora).

**Eixos:**
- Eixo X: rótulo "Frequência por 10.000 palavras".
- Eixo Y: sem rótulo (os nomes dos campos já indicam).
- Legenda: três entradas, "1986", "1987", "1999", em posição que não cubra dados (canto inferior direito costuma funcionar).

**Dimensões sugeridas:** 12x10 polegadas.

### Figura 2: densidade do campo militar ao longo dos textos

**Nome do arquivo:** `densidade_militar_sia_pandora.png` e `.svg`.

**Tipo:** dois painéis empilhados verticalmente (SIA 1987 painel superior, Pandora 1999 painel inferior). Em cada painel, a curva de densidade do campo militar em janelas deslizantes de mil palavras ao longo do texto. Eixo X: posição no texto em palavras absolutas. Eixo Y: número de ocorrências do campo militar na janela.

**Por que só SIA e Pandora:** Lab Life tem densidade baixa (3,50/10k) e a curva ficaria praticamente plana, sem agregar leitura. SIA e Pandora são onde a distribuição importa para o argumento.

**Dados:** para cada obra, ler o `txt_norm`, identificar todas as posições onde ocorre um termo do campo militar (catálogo em `campos_lexicais/catalogo_termos.yaml`, grupo `militar`).

Para Pandora, **excluir** as ocorrências de war/wars classificadas como `descritivo` no `refinamento/war_pandora_classificacao.csv`. Para SIA, manter todas (a queda da desambiguação lá é de apenas 2,7\%, irrelevante para a curva).

**Janela:** mil palavras, passo de duzentas palavras (overlap de 80\%) para curva suave.

**Cor:** ambas as curvas em vermelho ferrugem (`#B22222`), com preenchimento abaixo da curva em vermelho muito claro semitransparente (`#B22222` com alpha 0,2). Isso enfatiza o campo militar como objeto único da figura.

**Anotações inline:** se você conseguir mapear, com confiança razoável, picos da curva de Pandora para capítulos específicos (o capítulo sobre Joliot, por exemplo, está aproximadamente entre as palavras 30.000-45.000), pode adicionar pequenas anotações textuais discretas, em cinza-escuro, com setas finas. Se não conseguir mapear com confiança, pule as anotações: melhor ausência do que erro.

**Eixos:**
- Eixo X: rótulo "Posição no texto (milhares de palavras)" (divida valores por mil para o eixo).
- Eixo Y: rótulo "Ocorrências do campo militar (janela de 1.000 palavras)".
- Cada painel pode ter um identificador no canto superior esquerdo em fonte pequena: "Science in Action, 1987" / "Pandora's Hope, 1999".

**Dimensões sugeridas:** 12x8 polegadas (dois painéis, 4 polegadas cada).

### Figura 3: rede de cocorrência entre campos figurativos em SIA 1987

**Nome do arquivo:** `rede_cocorrencia_sia.png` e `.svg`.

**Tipo:** grafo dos 17 campos figurativos como nós, com arestas representando cocorrência textual. A espessura da aresta proporcional ao número de cocorrências; o tamanho do nó proporcional à frequência absoluta do campo em SIA. Nó `militar` em destaque cromático (vermelho ferrugem `#B22222`); os demais em cinza médio (`#808080`).

**Layout:** `nx.spring_layout` com `seed=42` para reprodutibilidade. Idealmente o `militar` deve aparecer central ou periférico-dominante (não enterrado entre outros nós). Se o spring layout default produzir uma configuração ruim, você pode fixar `pos['militar'] = (0, 0)` e re-rodar o spring com `fixed=['militar']`.

**Filtro de arestas:** mostrar apenas arestas com pelo menos cinco cocorrências (limiar mínimo). Arestas em escala de cinza, com largura proporcional ao número de cocorrências.

**Dados:** ler `outputs/latour_1987_science_action_en/csv/cocorrencia.csv`. Confira primeiro o formato esperado (matriz quadrada? lista de arestas?). Se o formato não permitir leitura direta, recalcule com a mesma lógica do `scripts/05_cooccurrence.py`, usando janela de cem palavras.

**Rótulos:** todos os nós rotulados com o nome do campo, posicionados de modo a evitar sobreposição. Se houver sobreposição forte, considere `nx.draw_networkx_labels` com `bbox` (caixa branca semi-transparente) atrás de cada label.

**Eixos:** **sem eixos visíveis** (`plt.axis('off')`). Apenas a área de plotagem.

**Anotação inline:** no canto inferior direito, fora do grafo, texto pequeno: "Arestas: limiar mínimo de 5 cocorrências. Janela: 100 palavras."

**Dimensões sugeridas:** 12x10 polegadas.

## Estrutura sugerida do script

Crie `scripts/11_passo4_graficos.py` com a seguinte estrutura, mantendo o padrão do repositório:

```python
"""
Passo 4 do refinamento — gráficos comparativos para o capítulo 2 da tese.

Gera três gráficos que sustentam visualmente a subseção sobre figuração
militar nas três obras de Latour:

1. comparacao_frequencias_tres_obras.{png,svg}: densidade dos 17 campos
   figurativos nas três obras, barras agrupadas horizontais.
2. densidade_militar_sia_pandora.{png,svg}: densidade do campo militar
   ao longo dos textos de SIA 1987 e Pandora 1999, dois painéis.
3. rede_cocorrencia_sia.{png,svg}: grafo de cocorrências entre os 17
   campos em SIA 1987, com o militar como nó central destacado.

Saída em outputs/passo4/figuras/.
"""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import yaml

REPO = Path(__file__).resolve().parents[1]
OUT_DIR = REPO / "outputs" / "passo4" / "figuras"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Paleta
COR_MILITAR_1986 = "#E08570"
COR_MILITAR_1987 = "#B22222"
COR_MILITAR_1999 = "#7A1A1A"
COR_BASE_1986 = "#D4D4D4"
COR_BASE_1987 = "#808080"
COR_BASE_1999 = "#404040"


def estilo_matplotlib():
    plt.rcParams.update({
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.axis": "x",
        "grid.alpha": 0.3,
        "grid.linewidth": 0.5,
        "figure.dpi": 100,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "font.size": 10,
    })


def salvar(fig, nome):
    fig.savefig(OUT_DIR / f"{nome}.png", dpi=300, bbox_inches="tight")
    fig.savefig(OUT_DIR / f"{nome}.svg", bbox_inches="tight")
    plt.close(fig)


def figura_1_comparacao_frequencias():
    # implementação
    pass


def figura_2_densidade_militar():
    # implementação
    pass


def figura_3_rede_cocorrencia():
    # implementação
    pass


if __name__ == "__main__":
    estilo_matplotlib()
    figura_1_comparacao_frequencias()
    figura_2_densidade_militar()
    figura_3_rede_cocorrencia()
    print(f"Gráficos salvos em {OUT_DIR}")
```

## Dependências Python

O repositório já tem `matplotlib` e `pyyaml`. Adicione `networkx` se faltar:

```bash
pip install networkx --break-system-packages
```

Se houver `requirements.txt` ou `pyproject.toml`, atualize-os também com a dependência.

## Reprodução

Antes de commitar, rode o script:

```bash
python3 scripts/11_passo4_graficos.py
```

Confira visualmente que os três PNG saíram em `outputs/passo4/figuras/` e abra cada um:

- **Figura 1:** o campo `militar` aparece no topo do eixo Y, em vermelho, com três barras visivelmente desiguais (Lab Life curta, SIA muito longa, Pandora intermediária). Valores numéricos à direita das barras militares.
- **Figura 2:** dois painéis empilhados. Em SIA, curva espalhada com vários picos médios. Em Pandora, picos mais altos e isolados (sobretudo na primeira metade onde está o capítulo Joliot).
- **Figura 3:** grafo conexo com `militar` em posição visível. Arestas grossas saindo de `militar` para `black_box`, `network`, `inscription`, `translation`.

Se algum gráfico ficar mal posicionado ou visualmente confuso, ajuste antes de commitar. Esses gráficos vão para uma tese; vale o tempo de polir.

## Stagear, commitar e fazer push

```bash
git add scripts/11_passo4_graficos.py outputs/passo4/figuras/
git status
```

Conferir que apenas o script e os seis arquivos de figuras (três PNG + três SVG) estão staged. Se `kwic_ampliado.csv` ou `passagens_curadas.md` ou `sequencia_exercito_ciencia.md` aparecerem staged, **algo deu errado** com o `.gitignore` — pare e me avise.

Mensagem de commit:

```
git commit -m "Passo 4: gráficos comparativos para subseção sobre figuração militar

Três figuras geradas por scripts/11_passo4_graficos.py:

- comparacao_frequencias_tres_obras.{png,svg}: densidade dos 17 campos
  figurativos nas três obras de Latour, em barras agrupadas horizontais.
  Campo militar destacado em vermelho ferrugem, ordenação por densidade
  decrescente em Science in Action.

- densidade_militar_sia_pandora.{png,svg}: distribuição da densidade do
  campo militar ao longo dos textos de SIA 1987 e Pandora 1999, em
  janelas deslizantes de mil palavras. Em Pandora, ocorrências de
  war/wars classificadas como descritivo-históricas no passo 1 são
  excluídas antes da contagem.

- rede_cocorrencia_sia.{png,svg}: grafo de cocorrências entre os 17
  campos figurativos em Science in Action, calculado em janelas de
  cem palavras. Limiar mínimo de cinco cocorrências por aresta.
  Campo militar como nó central destacado.

As figuras vão para o repositório público (não reproduzem texto de
Latour, são representação visual derivada de contagens). Os artefatos
com reprodução textual (kwic_ampliado.csv, passagens_curadas.md,
sequencia_exercito_ciencia.md) permanecem locais conforme o passo 4."
```

E:

```bash
git push origin main
git log --oneline -3
```

Me mostre o resultado do push e do log.

## Em caso de problema

- Se `outputs/latour_1987_science_action_en/csv/cocorrencia.csv` não existir ou tiver formato inesperado, pare e me avise antes de tentar reconstituir.
- Se algum dado lido produzir gráficos manifestamente errados (campo militar com densidade zero em SIA, por exemplo), pare antes de commitar.
- Se a paleta sair fora do esperado (cores muito vibrantes, contraste insuficiente), ajuste antes de gerar a versão final.

## Depois do push

Os três gráficos estarão disponíveis em:
`https://github.com/julianehelanski/analise_figuracoes/tree/main/outputs/passo4/figuras`

Vou então, no meu Overleaf, descomentar os `\includegraphics` da subseção e baixar os PNG para a pasta `figuras/cap.2/lexicometria/` da tese.

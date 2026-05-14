# Contexto para Claude Code

Este arquivo é lido automaticamente por Claude Code a cada sessão e mantém memória do projeto.

---

## Sobre o projeto

Análise textual sistemática de figurações em Latour e Haraway, parte da tese de doutorado de Juliane Helanski (Unicamp, Ciências Sociais) sobre o C4AI-USP e o sistema Spira de inteligência artificial. A análise produz dado empírico para o capítulo 2 da tese, que argumenta a tensão figural entre o vocabulário militar-industrial latouriano e a figuração têxtil-feminista de Haraway.

## Sobre a pesquisadora

Juliane é doutoranda em ciências sociais com formação em STS/ANT. Trabalha em português brasileiro, com leitura em inglês e francês. Lê Latour, Haraway, Stengers, Ingold, Mol, Law, Strathern e Barad como interlocutoras próximas. O capítulo 1 da tese já está revisado e descreve método etnográfico não-inocente, em primeira pessoa do singular. O capítulo 2 está em revisão final, e este projeto produz material para reforçá-lo.

## Princípios de trabalho com Juliane

1. **Primeira pessoa do singular** em todos os textos produzidos para a tese (eu, minha pesquisa, meu campo, esta tese que escrevo). Evitar construções impessoais.

2. **Sem travessões `---`** em texto principal. Usar vírgulas, parênteses ou dois-pontos. Travessões duplos `--` para intervalos numéricos são aceitáveis.

3. **Sem fórmulas vedadas**: "não X, mas Y", "não apenas X, mas também Y", "menos X do que Y", "X, e não Y". Sempre reformular afirmativamente.

4. **Sem adjetivos avaliativos**: marcante, importante, relevante, significativo, central, principal, expressivo, irrealista, considerável, complexo (no sentido de elogiar), problemático. Substituir por descritores neutros.

5. **"capítulo" minúsculo** mesmo em referências cruzadas: "capítulo \ref{capitulo3}", nunca "Capítulo \ref{}".

6. **Aspas → `\enquote{}`**: nunca usar aspas inglesas ``...''`. Aspas internas com `\enquote*{}`.

7. **Tom etnográfico**: prosa densa, registro acadêmico, frases longas com conectores explícitos. Sem listas com marcadores em textos para a tese (listas técnicas em README e código são OK).

8. **Notas de rodapé argumentativas, não suplementares**: nota de rodapé desenvolve sub-argumento, não apenas adiciona referência. Estilo modelado pelo capítulo 3 da tese.

## Como os PDFs do corpus são acessados

**Os PDFs estão em uma pasta privada do Google Drive da Juliane**, sincronizada localmente via Google Drive for Desktop. O Claude Code lê os PDFs de um caminho local configurado em `.env` (na raiz do repositório).

**Antes de qualquer operação que dependa dos PDFs**, Claude Code deve:

1. Ler a variável `CORPUS_PDF_PATH` do `.env` usando `python-dotenv`.
2. Verificar se o caminho existe e é um diretório acessível.
3. Listar os PDFs presentes e cruzar com `corpus/README.md` (lista esperada).
4. Reportar à Juliane quais obras estão presentes e quais faltam, **antes** de prosseguir com extração ou análise.

**Em caso de falha** (caminho não existe, pasta vazia, permissão negada): parar, reportar o problema com mensagem clara, e aguardar instrução da Juliane. **Não** tentar baixar PDFs de outras fontes nem improvisar; o fluxo é Drive → sincronização local → leitura via `.env`.

Padrão de código para acesso aos PDFs:

```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
corpus_pdf_path = os.getenv("CORPUS_PDF_PATH")
if not corpus_pdf_path:
    raise ValueError("CORPUS_PDF_PATH não está definido no .env")

pdf_dir = Path(corpus_pdf_path)
if not pdf_dir.exists():
    raise FileNotFoundError(
        f"A pasta {pdf_dir} não existe. "
        "Verifique se o Google Drive está sincronizado e se o caminho "
        "em .env aponta para a pasta correta."
    )
if not pdf_dir.is_dir():
    raise NotADirectoryError(f"{pdf_dir} não é um diretório.")

# Listar PDFs
pdfs = list(pdf_dir.glob("*.pdf")) + list(pdf_dir.glob("*.PDF"))
print(f"Encontrados {len(pdfs)} PDFs em {pdf_dir}")
```

# Substituir as linhas 73-83 do CLAUDE.md por este bloco:

## Estado atual do projeto

**Etapa em andamento:** Refinamento sobre as Etapas 1 e 3, em sessão iniciada em 14 de maio de 2026. Cinco passos planejados, executados em sequência:

1. Desambiguação de `war`/`wars` no campo militar das três obras de Latour. **Concluído em 14/05/2026**. Resultado documentado em `docs/decisoes_metodologicas.md` (adendo ao final). Artefatos em `outputs/refinamento/`.
2. Validação amostral semântica dos campos figurativos (20 ocorrências por campo por obra, lidas por Juliane). Pendente.
3. Reformatação dos blocos interpretativos do relatório de trajetória para os critérios de estilo da tese (primeira pessoa, sem travessões, sem fórmulas vedadas, capítulo minúsculo). Pendente.
4. KWIC ampliado para janela de ±50 palavras sobre o campo militar nas três obras, com curadoria de 10 a 15 passagens citáveis. Pendente.
5. Início da contrapartida Haraway (corpus, catálogo têxtil-feminista, primeira lexicometria). Pendente.

**Decisões já tomadas e fixadas:**

- Corpus da Etapa 1: três obras de Latour em inglês original (Laboratory Life 1986 ed. Princeton, Science in Action 1987, Pandora's Hope 1999). Justificativa em `docs/decisoes_metodologicas.md` seção 1.
- Idioma de trabalho: inglês na Etapa 1 (originais de publicação). Francês e português entram em Etapa 3 plena, com lematização spaCy.
- Janela KWIC: ±10 palavras como padrão para detecção e contagem; ±50 palavras a ser adotada para curadoria de passagens citáveis (passo 4 do refinamento atual).
- Catálogo de termos: arquivo único em `campos_lexicais/catalogo_termos.yaml`, com 17 campos figurativos para Latour (16 da Etapa 1 mais o campo `militar` adicionado na Etapa 3).
- Campo `militar`: contagem registrada em duas versões a partir de 14/05/2026, bruta e refinada por desambiguação de `war`/`wars` (descritivo-histórico vs figurativo-latouriano). Aplicação simétrica nas três obras.

**Pendências:**

- Portar a lógica de desambiguação automática de `war`/`wars` para um script versionado em `scripts/`, com nome sugerido `09_desambiguar_war.py`. A camada manual fica em CSV auditável fora do script.
- Atualizar a tabela LaTeX `outputs/latex/trajetoria_latour_1986_1999.tex` ou adicionar a tabela complementar `outputs/refinamento/tabela_militar_refinada.tex` ao master da tese.
- Ajustar a seção 4.3.a do relatório `outputs/trajetoria_latour_1986_1999.md`: a frase sobre a manutenção do vocabulário militar em 1999 precisa ser reformulada à luz da queda de 26,4% pela desambiguação.
- Passos 2 a 5 do refinamento atual.

## Como Claude Code deve operar

1. **Não avançar entre etapas sem confirmação explícita da Juliane**.

2. **Documentar decisões em `docs/decisoes_metodologicas.md`** a cada decisão tomada.

3. **Marcar inferências em relatórios qualitativos** com `[INFERÊNCIA]` quando a afirmação não tiver citação direta como base.

4. **Seeds aleatórios fixos** em qualquer amostragem ou processo estocástico (`seed=42` por padrão).

5. **Scripts em Python 3.11+**, com type hints e docstrings em português.

6. **Estilo de código**: PEP 8 com linhas de até 100 caracteres. Usar `black` para formatação automática.

7. **Outputs sempre em duas versões**:
   - Arquivo aberto (CSV, Markdown) na pasta `outputs/`.
   - Quando aplicável, versão em LaTeX pronta para incorporar à tese, em `outputs/latex/`.

8. **Quando houver ambiguidade metodológica**, parar e perguntar à Juliane.

9. **Sobre traduções**: trabalhar com originais sempre que possível. Quando comparar versões (Latour francês vs. inglês vs. português), explicitar como camada de mediação.

10. **Sobre o capítulo 2 da tese**: o resultado desta análise alimenta o capítulo 2, mas não substitui a redação. Juliane escreve a interpretação final; Claude Code produz o material organizado e validado.

## Fontes de erro conhecidas a evitar

- **Pasta Drive não sincronizada**: ao iniciar uma sessão, verificar se `CORPUS_PDF_PATH` aponta para pasta existente e populada. Se o Drive estiver pausado, o sync não roda; alertar a Juliane.
- **Caminho com espaços (especialmente macOS)**: o caminho do Drive em macOS contém espaços (`My Drive`, `CloudStorage`). Usar `Path` do `pathlib` e citar caminhos entre aspas em scripts shell.
- **Extração de PDFs**: notas de rodapé podem se misturar ao corpo. Verificar amostralmente após `pdftotext -layout`.
- **Lemmatização**: spaCy às vezes erra em formas verbais (especialmente em francês). Validar amostralmente.
- **Alucinação em interpretação**: na Etapa 7 (leitura interpretativa), nunca afirmar sem citação direta. Marcar inferências com `[INFERÊNCIA]`.

## Comandos úteis

```bash
# verificar se o Drive está sincronizado
ls "$CORPUS_PDF_PATH"

# extrair texto de um PDF do Drive sincronizado
pdftotext -layout "$CORPUS_PDF_PATH/livro.pdf" corpus/txt/livro.txt

# rodar análise KWIC
python scripts/02_kwic.py \
    --texto corpus/txt/latour_1987.txt \
    --campo campos_lexicais/latour_militar_en.txt \
    --janela 50 \
    --saida outputs/csv/etapa1/latour_1987_militar.csv
```

## Referências cruzadas com a tese

- Capítulo 1: método etnográfico, situated knowledges, não-inocência haraway.
- Capítulo 2, bloco 2 da abertura: tensão figural Latour vs. Haraway vs. Stengers (este projeto sustenta empiricamente esse bloco).
- Capítulo 2, seção 2.6: bibliometria do campo brasileiro (este projeto segue lógica metodológica análoga, em escala diferente).
- Capítulo 3: genealogia IBM/Hollerith (não diretamente afetado, mas dialoga com o argumento sobre racionalidades sedimentadas).
- Capítulo 4: rede do Spira (não diretamente afetado).

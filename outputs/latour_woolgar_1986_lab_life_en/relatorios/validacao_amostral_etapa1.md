# Amostra estratificada de validação: latour_woolgar_1986_lab_life_en

Seed = 42. Estratos = inicio_capitulo, corpo, notas_fim, paratexto, qualidade_baixa. N por estrato = 3.

Use este documento como guia de leitura ao percorrer o PDF. Codifique cada página no CSV `amostra_validacao.csv`:

- `estrato_correto`: o estrato atribuído pelo algoritmo é correto? (sim/nao/parcial)
- `classe_correta`: a classe específica predita é correta? (sim/nao/parcial)
- `erro_extracao`: caracteres corrompidos, palavras coladas, linhas misturadas?
- `decisao_metodologica`: qualquer observação a registrar.

Se a taxa de erro em um estrato passar de 20%, ajustar a heurística correspondente em `scripts/01_extract_text.py` e reprocessar.

## Estrato: `inicio_capitulo`

### Página 236

- classe_predita: `inicio_capitulo`, qualidade_predita: `boa`, n_palavras: 226

**Início da página:**

> Chapter 6 THE CREATION OF ORDER OUT OF DISORDER In examining the construction of facts in a laboratory, we have presented the general organisation of the setting as constituted by someone unfamiliar with science (Chapter 2); we showed how the history of some of the laboratory's a...

**Meio:**

> ed, looking especially at the paradox of the term fact (Chapter 4); we then turned to the individuals in the laboratory in an attempt to make sense both of their careers and the solidity of their production (Chapter 5 ). In each of these chapters we defined terms which were often...

**Fim:**

> eceding chapters in an attempt more systematically to link the different concepts used. At the same time, we shall review some of the methodological problems encountered so far. It will not have escaped the reader's notice, for example, that a major problem arises from our conten...

### Página 16

- classe_predita: `inicio_capitulo`, qualidade_predita: `boa`, n_palavras: 290

**Início da página:**

> Chapter 1 FROM ORDER TO DISORDER 5 mins. John enters and goes into his office. He says something very quickly about having made a bad mistake. He had sent the review of a paper. . . . The rest of the sentence is inaudible. 5 mins. 30 secs. Barbara enters. She asks Spencer what ki...

**Meio:**

> rently writing at his desk, answers from his office. Jane leaves. 6 mins. 15 secs. Wilson enters and looks into a number of offices, trying to gather people together for a staff meeting. He receives vague promises. "It's a question of four thousand bucks which has to be resolved ...

**Fim:**

> abel. He leaves the room. Long silence. The library is empty. Some write in their offices, some work by windows in the brighly lit bench space. The staccato noise of typewriting can be heard from the lobby. 9 mins. Julius comes in eating an apple and perusing a copy of Nature. 9 ...

### Página 244

- classe_predita: `inicio_capitulo`, qualidade_predita: `boa`, n_palavras: 446

**Início da página:**

> The Creation of Order Out of Disorder 243 in other laboratories. This is the nature of the market defined in Chapter 5. No matter whether this taken-for-granted peptidic structure takes the form of a nonproblematic argument or of a white powder sample, the only important question...

**Meio:**

> hat it was more difficult for Watson to doubt it or simply to object that the keto form was equally probable. The cost-benefit analysis will vary according to the prevailing circumstances, so no general rules can be established. The style of an article can make it more difficult ...

**Fim:**

> and the set of productive forces, which makes construction possible. Every time a statement stabilises, it is reintroduced into the laboratory (in the guise of a machine, inscription device, skill, routine, prejudice, deduction, programme, and so on), and it is used to increase t...

## Estrato: `corpo`

### Página 248

- classe_predita: `corpo`, qualidade_predita: `boa`, n_palavras: 450

**Início da página:**

> The Creation of Order Out of Disorder 247 curves. One particular curve is selected, cleaned up, put on a slide and shown around in conjunction with the statement: "Stress simultaneously releases ACTH and Beta Endorphine." This statement stands out of and for the mass of figures. ...

**Meio:**

> haotic: statements have to be pushed, forced into the light, defended against attack, oblivion, and neglect. Very few statements are seized upon by everyone in the field because their use entails an enormous economy in the manipulation of data or statements (Brillouin, 1962: Ch. ...

**Fim:**

> ther than disorder. This basic philosophical assumption has recently been challenged, and our intention in the next part of this chapter is to show what light is shed on laboratory activity if such an assumption is modified. To do this in full would entail going beyond the usual ...

### Página 111

- classe_predita: `corpo`, qualidade_predita: `boa`, n_palavras: 450

**Início da página:**

> 110 LABORATORY LIFE of one or two of a certain set of eight papers. Within this network, then, TRH is accepted as a fact in the sense that it is sufficient to know that "TRH regulates the release by the pituitary of TSH," that "its chemical formula is Pyro-Glu-His-Pro-NH 2 " and ...

**Meio:**

> ource of noise, for the researcher. For a still smaller group, comprising a few score individuals and half a dozen laboratories, TRH is not merely a tool. For them, TRH represents and entire subfield. Indeed, for a few of the individuals in our study, it represented a lifetime's ...

**Fim:**

> nt as a nonproblematic substance is confined to a few hundred new investigators. Outside these networks TRH simply does not exist(see Chapter 4). In the hands of outsiders and once devoid of its label, TRH would be merely thought of as "some kind of white powder." It would only b...

### Página 85

- classe_predita: `corpo`, qualidade_predita: `boa`, n_palavras: 433

**Início da página:**

> 84 LABORATORY LIFE external object or objective condition of which the statements were taken to be indicators. Sources of "subjectivity" thus disappeared in the face of more than one statement, and the initial statement could be taken at face value and without qualification (cf.,...

**Meio:**

> atus of the statement. In the laboratory, "objects" were accomplished by the superimposition of several documents obtained from inscription devices within the laboratory or from papers by investigators outside the laboratory (cf., Chapter 4). No statement could be made except on ...

**Fim:**

> us, although the author had presented his statement as a type 2 or 3, the referee recast it in terms of type 1. Consider also the following: "The authors used a Polytron which is a much more vigorous means of tissue disruption. To my knowledge, there are no reports in the literat...

## Estrato: `notas_fim`

### Página 102

- classe_predita: `notas_fim`, qualidade_predita: `boa`, n_palavras: 4

**Início da página:**

> Image Not Available 1O1

**Meio:**

> Image Not Available 1O1

**Fim:**

> Image Not Available 1O1

### Página 96

- classe_predita: `notas_fim`, qualidade_predita: `boa`, n_palavras: 4

**Início da página:**

> Image Not Available 95

**Meio:**

> Image Not Available 95

**Fim:**

> Image Not Available 95

### Página 94

- classe_predita: `notas_fim`, qualidade_predita: `boa`, n_palavras: 4

**Início da página:**

> Image Not Available 93

**Meio:**

> Image Not Available 93

**Fim:**

> Image Not Available 93

## Estrato: `paratexto`

### Página 293

- classe_predita: `paratexto`, qualidade_predita: `boa`, n_palavras: 429

**Início da página:**

> 292 LABORATORY L FE Demand, for credible information, 201-208 Historicity, 239 Derrida, J., 88, 261 History of science, 106-107 Description, constraints on the, 38, 44, 254 Hoagland, J , 230 n 5 Dietrich (pseudonym) his career, 194-198 Horton, R., 42 Discovery, 129, 173, 185 Hoyl...

**Meio:**

> and artefact, Jutisz, P , 129 174 ff Falsification, 156 Kant, E , 175 Fetishism 259 n 10 Kawabata, Y , 247 Feyerabend, K., 251 Knorr, K., 54, 150, 152, 173, 175, 184, Fiction, 257, 261 230, 232, 236, 239, 251 Field (informant), 212 ff , 232 Kuhn, T , 24 Flower, 154 Folkers, K., 1...

**Fim:**

> man, T , 175 Habermas, J., 239 Lyotard, J. F., 150, 237 Hagstrom, W O , 52, 203 ff Hard and soft, as a consequence of instru- Machlup, F , 258 ments, 66 ff ; Harder and softer, 142, Marx, K , 179, 231, 259 their difference, 257 Mass spectrometer, 150; its role, 242, 259 Harris, G...

### Página 284

- classe_predita: `paratexto`, qualidade_predita: `boa`, n_palavras: 469

**Início da página:**

> PostScript 283 gation-namely the ways in which descriptions and reports of observations are variously presented (and received) as "good enough," "inadequate," "distorted," "real," "accurate" and so on. A more reflexive appreciation of laboratory studies is less dismissive of what...

**Meio:**

> need to explore forms of literary expressive whereby the monster can be simultaneously kept at bay and allowed a position at the heart of our enterprise. 8 Of course, one interesting aspect of the exploration of reflexivity is that our writing is conventionally constrained by the...

**Fim:**

> is at face value, and go away happy that he is better informed about the character of laboratory roofs (and views therefrom). For such readers we are naturally pleased to increase their sum of knowledge about the world. But, unfortunately, much would have been lost. We hoped that...

### Página 7

- classe_predita: `paratexto`, qualidade_predita: `boa`, n_palavras: 202

**Início da página:**

> 6 LABORATORY LIFE The Elimination of Concurrent Efforts by New Investments 119 The Construction of a New Object 124 The Peptidic Nature of TRF 129 Narrowing Down the Possibilities 142 TRF Moves into Other Networks 148 Notes 149 4 THE MICROPROCESSING OF FACTS

**Meio:**

> e Form of Credibility to Another 198 The Demand for Credible Information 201 Strategies, Positions and Career Trajectories Curriculum Vitae 208 Positions 211 Trajectories 214 Group Structure 216 Group Dynamics 223 Notes

**Fim:**

> 277 The Place of Philosophy 279 The Demise of the "Social" 281 Reflexivity 282 Conclusion 284 Notes 285 Additional References 287 Index 291

## Estrato: `qualidade_baixa`

### Página 296

- classe_predita: `qualidade_baixa`, qualidade_predita: `baixa`, n_palavras: 0

**Início da página:**

> 

**Meio:**

> 

**Fim:**

> 

### Página 222

- classe_predita: `qualidade_baixa`, qualidade_predita: `baixa`, n_palavras: 1

**Início da página:**

> 221

**Meio:**

> 221

**Fim:**

> 221

### Página 1

- classe_predita: `qualidade_baixa`, qualidade_predita: `baixa`, n_palavras: 0

**Início da página:**

> 

**Meio:**

> 

**Fim:**

> 

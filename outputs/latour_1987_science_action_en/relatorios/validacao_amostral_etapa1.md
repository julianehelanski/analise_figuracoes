# Amostra estratificada de validação: latour_1987_science_action_en

Seed = 42. Estratos = inicio_capitulo, corpo, notas_fim, paratexto, qualidade_baixa. N por estrato = 3.

Use este documento como guia de leitura ao percorrer o PDF. Codifique cada página no CSV `amostra_validacao.csv`:

- `estrato_correto`: o estrato atribuído pelo algoritmo é correto? (sim/nao/parcial)
- `classe_correta`: a classe específica predita é correta? (sim/nao/parcial)
- `erro_extracao`: caracteres corrompidos, palavras coladas, linhas misturadas?
- `decisao_metodologica`: qualquer observação a registrar.

Se a taxa de erro em um estrato passar de 20%, ajustar a heurística correspondente em `scripts/01_extract_text.py` e reprocessar.

## Estrato: `inicio_capitulo`

### Página 5

- classe_predita: `inicio_capitulo`, qualidade_predita: `boa`, n_palavras: 185

**Início da página:**

> Part A: The trials of rationality. Part B: Sociologics. Part C: Who needs hard facts? Chapter 6 Centres of calculation 215 Prologue: The domestication of the savage mind. Part A: Action at a distance. Part B: Centres of calculation. Part C: Metrologies Appendix 1 Rules of Method ...

**Meio:**

> Rules of Method 258 Appendix 2 Principles 259 Notes 260 References 266 Index 271 ((viii)) Acknowledgements Not being a native English speaker I had to rely heavily on my friends to revise successive drafts of this manuscript. John Law and Penelope Dulling have been most patient i...

**Fim:**

> ve been most patient in revising the earlier drafts. Steven Shapin, Harry Collins, Don MacKenzie, Ron W estrum and Leigh Star suffered each on one different chapter. I have been most fortunate in having Geoffrey Bowker edit the whole book, 'debug' it and suggest many useful chang...

### Página 286

- classe_predita: `inicio_capitulo`, qualidade_predita: `boa`, n_palavras: 185

**Início da página:**

> Chapter 4 1 I follow here Roy Porter's account (1982). See also his (1977) book on the formation of the new discipline of geology. 2 See D. Kevles (1978) as an excellent example of the historical study of a scientific profession. 3 This example is a collage. 4 Although all the el...

**Meio:**

> ample is a collage. 4 Although all the elements are accurate, this is an ideal-type and not a real example. 5 See T. Kidder (1981). 6 Most of the figures used in this part come from the National Science Foundation's Science Indicators published in Washington every two years. 7 Se...

**Fim:**

> ors published in Washington every two years. 7 See OECD (1984). 8 Number of doctorates in the US: total: 360,000; in research: 100,000; in development: 18,000 (Science Indicators, 1983, p. 254). 9 Number of scientists and engineers engaged in R & D by type of occupation and emplo...

### Página 148

- classe_predita: `inicio_capitulo`, qualidade_predita: `boa`, n_palavras: 487

**Início da página:**

> Part C. The model of diffusion "versus the model of translation The task of the fact-builders is now clearly outlined: there is a set of strategies to enlist and interest the human actors, and a second set to enlist and interest the non-human actors so as to hold the first. When ...

**Meio:**

> their own inner strength. In the end, if everything goes really well, it seems as if there are facts and machines spreading through minds, factories and households, slowed down only in a handful of farflung countries and by a few dimwits. Success in building black boxes has the s...

**Fim:**

> ain of people who borrowed claims varied from time to time because of the many elements the claims were tied to. If people wished to open the boxes, to renegotiate the facts, to appropriate them, masses of allies arrayed in tiers would come to the rescue of the claims and force t...

## Estrato: `corpo`

### Página 127

- classe_predita: `corpo`, qualidade_predita: `boa`, n_palavras: 527

**Início da página:**

> make my gyrocompass a real thing; wait a little, come my way, and after a while your ships will make full use of their terrifying powers again and my gyrocompasses will spread in ships and planes in the form of well-closed black boxes.' This community of interests is the result o...

**Meio:**

> his is what occurred with Diesel. MAN was ready to wait for a few years, to lend engineers, with the idea that they would soon resume their usual business of manufacturing engines but on a larger scale. If the return is delayed, the management may feel cheated, as if they were pe...

**Fim:**

> accepted standard for measuring detours because the 'acceptable' length of the detour is a result of negotiation. MAN, for instance, became worried after only a few years, but the private medical foundations that invested in Lawrence's huge accelerators at Berkeley did not, even ...

### Página 267

- classe_predita: `corpo`, qualidade_predita: `boa`, n_palavras: 517

**Início da página:**

> smallest change in the geometry of projection might have enormous consequences since the flow of forms coming from all over the planet and back to all the navigators will be altered. The tiny projection system is an obligatory passage point for the immense network of geography. T...

**Meio:**

> how to reconcile their readings when they are so far apart that it takes time for the observer of one clock to send the information to another observer, he is not in an abstract world, he is deep down at the centre of all exchanges of information, attentive to the most material a...

**Fim:**

> n general, `proximity', `association', the more central their work will become since it will concentrate still further what is going on in the centres of calculation. The sheer accumulation of nth order paper forms makes any nth+1 form that can at the same time maintain the featu...

### Página 19

- classe_predita: `corpo`, qualidade_predita: `boa`, n_palavras: 509

**Início da página:**

> like model, suddenly brings a new strength to his emerging new model. Not only are the pairs superimposable, but Chargaff laws can be made a consequence of his model. Another feature came to strengthen the model: it suggests a way for a gene to split into two parts and then for e...

**Meio:**

> e Wilkins and Rosalind Franklin, the only ones with X-rays pictures of the DNA, have? Will they see the model as the only form able to give, by projection, the shape visible on Rosalind's photographs? They'd like to know fast but dread the danger of the final showdown with people...

**Fim:**

> overwhelmed and then pledging complete support to it. Bragg is convinced although still worried that no one more serious than Jim and Francis had checked the helix. Now for the big game, the encounter between the model and those who for years had captured its projected image. 'Ma...

## Estrato: `notas_fim`

### Página 283

- classe_predita: `notas_fim`, qualidade_predita: `boa`, n_palavras: 334

**Início da página:**

> factor from a human pancreatic tumor that caused acromegaly', Science, vol. 218, pp. 585-7. 10 The article commented on here is by C. Packer, 'Reciprocal altruism in papio P.', Nature 1977 Vol. 265, no. 5593, pp. 441-443. Although this transformation of the literature is a sure t...

**Meio:**

> l Chemistry, vol. 256, no. 9 pp. 4219-27. On this and many other borderline cases, see W. Broad and N. Wade (1982). 12 For a general presentation see M. Callon, J. Law and A. Rip (eds) (1986). 13 On the somatostatin episode see Wade (1981, chapter 13). 14 For a good introduction ...

**Fim:**

> ing here the work of Mary Jo Nye (1980, 1986). 4 On this see N. Wade (1981, Chapter 13). 5 I am following here the empirical example studied by H. Collins (1985), although his description of the ways of settling controversies is rather different and will be analysed in Part II of...

### Página 284

- classe_predita: `notas_fim`, qualidade_predita: `boa`, n_palavras: 264

**Início da página:**

> 9 I am using here D. MacKenzie's (1978) article. See also his (1981) book on the larger setting of the same controversy. 10 On this episode of the discovery of somatostatin see N. Wade (1981 chapter 13). 11 This excerpt is taken from E. Duclaux's Traité de biochimie (1896), vol. ...

**Meio:**

> echblende', Comptes Rendus de l'Académie des Sciences, vol. 127, pp. 175-8. 13 For the definition of these words and of all the concepts of semiotics see A. Greimas and J. Courtès (1979/1983). For a presentation of semiotics in English see F. Bastide (1985). 14 See J. W. Dauben (...

**Fim:**

> ativism has been nicely summed up in many articles by Harry Collins. See in particular his latest book (1985). Chapter 3 1 For a presentation of laboratory studies see K. Knorr (1981), K. Knorr and M. Mulkay (eds) (1983) and M. Lynch (1985). 2 I am following in this introduction ...

### Página 285

- classe_predita: `notas_fim`, qualidade_predita: `boa`, n_palavras: 326

**Início da página:**

> 6 I follow here T.P. Hughes (1971). 7 On this see D. Kevles (1978), on the many different strategies to interest a society in the development of a profession. 8 This knowledge seems excessive to many sociologists of science (see S. Woolgar (1981), M. Callon and J. Law (1982), B. ...

**Meio:**

> this chapter. 14 This example is taken from L. Tolstoy's masterpiece (1869). 15 This expression has been proposed by J. Law (1986) in correlation with his notion of 'heterogeneous engineering'. 16 On this, see the notion of 'reverse salient' proposed by T. Hughes (1983). 17 I am ...

**Fim:**

> he necessary symmetry. On this see M. Callon (1986). 21 On Newcomen's engine see B. Gille (1978) 22 For a reader, a bibliography and an introduction to these many strategies, see D. MacKenzie and J. Wajcman (1985). 23 For a critical introduction to the notion of discovery, see A....

## Estrato: `paratexto`

### Página 294

- classe_predita: `paratexto`, qualidade_predita: `boa`, n_palavras: 224

**Início da página:**

> --- (1953) and Dubos, J. The White Plague: Tuberculosis, Man, and Society, Boston, Little Brown and Co. Dauben, J. W. (1979). Georges Cantor: His Mathematics and Philosophy of the Infinite. Cambridge, Mass., Harvard University Press. Desmond, Adrian (1975). The Hot-Blooded Dinosa...

**Meio:**

> ality, Tradition andRevolution. Ann Arbor, University of Michigan Press. --- (1978). Galileo at Work: His Scientific Biography. Chicago, Chicago University Press. Duclaux, Emile (1896). Pasteur: Histoire d'un Esprit. Sceaux, Charaire. Easlea, Brian (1980). Witch-Hunting, Magic an...

**Fim:**

> 986). 'The ultracentrifuge: interpretive flexibility and the development of a technological artefact'. Social studies of science (forthcoming) Evans-Pritchard, E.E. (1937/1972). Witchcraft, Oracles and Magic Among the Azande (translated from the French). Oxford Clarendon Press. F...

### Página 301

- classe_predita: `paratexto`, qualidade_predita: `boa`, n_palavras: 89

**Início da página:**

> Bill 72, 74, 83 black box, definition 2, borrowing them, 81-82, new definition 131, and machines 253 Blondlot 75, 78, 100 Bloor D. 184 Boas 109 Bodin 191-192 book of nature 244, 254 bootlegging 113, 114 botany 229 Brazeau P. 86-88 breaching 207 Bulmer R. 199-202, 210-213 bureaucr...

**Meio:**

> chemistry 235-236

**Fim:**

> Bill 72, 74, 83 black box, definition 2, borrowing them, 81-82, new definition 131, and machines 253 Blondlot 75, 78, 100 Bloor D. 184 Boas 109 Bodin 191-192 book of nature 244, 254 bootlegging 113, 114 botany 229 Brazeau P. 86-88 breaching 207 Bulmer R. 199-202, 210-213 bureaucr...

### Página 305

- classe_predita: `paratexto`, qualidade_predita: `boa`, n_palavras: 145

**Início da página:**

> Gray E. 187, 189, 197 great divide 211, 216, 221, 228, 232 growth hormone releasing hormone 23 et seq., 36, 108 Guillemin R. 27 et seq., 36 et seq., 45 et seq., 80 et seq., 86, 92, 95 hard facts 206 et seq., 252 health systems 172 hero, in the text 53-54, in the laboratory 88-91 ...

**Meio:**

> q., 36 et seq., 45 et seq., 80 et seq., 86, 92, 95 hard facts 206 et seq., 252 health systems 172 hero, in the text 53-54, in the laboratory 88-91 hidden agenda, of the text 55 Hutchins E. 187-188, 210 hygiene movement 115, 142 idea 135 immutable mobiles 227 et seq., 236-237 indu...

**Fim:**

> oratory 88-91 hidden agenda, of the text 55 Hutchins E. 187-188, 210 hygiene movement 115, 142 idea 135 immutable mobiles 227 et seq., 236-237 induction 51 industry 165, 170 inertia 132 et seq., 137, 250 information, definition 243 innovation 107 inscription 218 inscription devic...

## Estrato: `qualidade_baixa`

### Página 72

- classe_predita: `qualidade_baixa`, qualidade_predita: `baixa`, n_palavras: 26

**Início da página:**

> 2. kolonne: A.C M-(A.C) M+(A.C) H(A.C) Frontline 3. kolonne: A.D M-(A.D) Frontline 4. kolonne E.D M-(E.D) M+(E.D) H(E.D) Frontline 5. kolonne: E.F M-(E.F) M+(E.F) H(E.F) E.F

**Meio:**

> . kolonne: A.C M-(A.C) M+(A.C) H(A.C) Frontline 3. kolonne: A.D M-(A.D) Frontline 4. kolonne E.D M-(E.D) M+(E.D) H(E.D) Frontline 5. kolonne: E.F M-(E.F) M+(E.F) H(E.F) E.F

**Fim:**

> 2. kolonne: A.C M-(A.C) M+(A.C) H(A.C) Frontline 3. kolonne: A.D M-(A.D) Frontline 4. kolonne E.D M-(E.D) M+(E.D) H(E.D) Frontline 5. kolonne: E.F M-(E.F) M+(E.F) H(E.F) E.F

### Página 314

- classe_predita: `qualidade_baixa`, qualidade_predita: `baixa`, n_palavras: 0

**Início da página:**

> 

**Meio:**

> 

**Fim:**

> 

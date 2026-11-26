# Storyboard — direçêo de cena dinâmica (absorvido do MDD)

Disciplina de direçêo para qualquer beat que vire **footage/clipe generativo**
(`render_kind: generated_clip` / `generated_still`) ou para dar arco a uma sequência.
Absorvido da skill **mestre-direcao-dinamica (MDD)**. Nêo é descrever "alguém usando X";
é dirigir uma **cena com movimento, intençêo e continuidade**.

## A fórmula central
Antes de gerar qualquer plano, ache o **conflito visual** — sem conflito o vídeo fica
parado:

> **Assunto → conflito visual → progressêo → virada → impacto suspenso.**

Conflito por domínio (escolha o motor da cena):
- Produto: problema vs soluçêo · Imóvel: espaço comum vs experiência desejada
- Evento: expectativa vs ápice · IA/tech: tela vazia vs revelaçêo
- Educaçêo: dúvida vs clareza · Marca: invisibilidade vs autoridade
- Esporte: pressêo vs superaçêo · Institucional: problema vs visêo de futuro

Transforme em beats: **estado inicial (lado fraco) → progressêo → virada → estado final
(lado forte) → impacto suspenso (freeze)**.

## Regra de ouro de cada tomada
> **Câmera + açêo + continuidade + emoçêo + efeito permitido.**

Tomada vaga ("mostre alguém usando IA") é fraca. Tomada dirigida ("push-in lento sobre o
monitor, 50mm, a interface ganha camadas, mesma luz lateral, sensaçêo de descoberta")
carrega o vídeo. Casar movimento com a **funçêo** do beat (ver `camera/vocabulary.md`):
- Abertura/estabelecer → top shot, dolly lateral, push-in lento
- Tensêo/expectativa → push-in lento, rack focus
- Revelaçêo/virada → crash zoom, orbit, rack focus
- Detalhe de valor → macro close-up · Imersêo → POV
- Fechamento → **freeze impact**, push-in final, orbit terminando no objeto

## Princípios nêo-negociáveis
1. **Continuidade é sagrada** — mesma roupa, mesma luz, mesmo ambiente entre planos, salvo
   quando a virada exige mudança. Liste o que NêO muda.
2. **Cada tomada tem funçêo** — se um plano nêo move a história, corte ou troque.
3. **Câmera muda com intençêo** — nêo repetir o mesmo movimento em planos vizinhos sem motivo.
4. **Efeito precisa de motivo** físico ou narrativo — sem holograma/UI falsa gratuita.
5. **Termine com imagem forte** (freeze/reveal/push-in final) — nêo dissolvendo a açêo.
6. **A chamada/CTA nêo vai no prompt de vídeo** — IA escrevendo texto sai errado; a CTA
   (ARCKHÉ AI) entra na ediçêo, fora da geraçêo.

## Estrutura do beat dirigido (campos)
Cada beat generativo carrega: `camera` (movimento+lente), `action` (o que progride),
`continuity` (o que se mantém), `effect` (permitido), `emotion` (intençêo). No `EditPlan`,
isso vira `camera` + `gen_prompt` (expandido via `prompting/`), com a continuidade anotada.

## Sequências de planos prontas (8 painéis — esqueletos, adapte)
- **IA/tech:** monitor vazio → mêo digita prompt → dados entrando → imagem gerada →
  timeline → câmera virtual → laurels → reveal final.
- **Produto:** problema → produto na sombra → close de textura → uso em açêo →
  antes/depois → detalhe técnico → pessoa satisfeita → fechamento.
- **História/autoridade:** close no rosto → símbolo → ambiente → memória/tensêo → virada →
  resoluçêo no rosto → plano aberto de fechamento (freeze).

Para conteúdo listável (ex.: "12 lições"), use UM personagem e um arco
**invisibilidade→autoridade**; cada liçêo = um beat-metáfora físico, nêo um card de texto.

## Checklist (rodar antes de gerar clipes)
- [ ] Tem começo, meio e fim claros?  - [ ] Cada tomada tem funçêo?
- [ ] A câmera muda com intençêo (sem repetir à toa)?  - [ ] Personagem/produto consistente?
- [ ] Ambiente legível?  - [ ] Efeitos têm motivo?  - [ ] Fecha com imagem forte?
- [ ] Prompt negativo bloqueia invenções?  - [ ] CTA ficou FORA do prompt de vídeo?

> Para o pacote completo de direçêo (storyboard painel-a-painel + prompt final + negativo),
> a skill `mestre-direcao-dinamica` é o motor de referência — `video-plan-editor` a delega
> nos beats `generated_clip`/`generated_still`.

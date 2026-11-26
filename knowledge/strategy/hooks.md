# Strategy — Ganchos e retençêo

## A regra dos 3 segundos
Nenhum vídeo de sucesso começa devagar. Nos primeiros frames: **movimento**, **pergunta
provocativa** ou **imagem inesperada/chocante**. O gancho deve fazer uma de três coisas:
- ser **visualmente inesperado** (quebra de padrêo visual);
- fazer uma **pergunta provocativa**;
- prometer uma **recompensa clara**.

Fórmula matadora: **"Como [resultado desejado] sem [dor principal]"**.

## 3 tipos de gancho (gerar sempre as 3 opções)
A skill propõe 3 variações de gancho para os primeiros 3s:
1. **Curiosidade** — abre um loop ("O segredo que ninguém te conta sobre X…").
2. **Contraste / choque** — quebra expectativa ("Você está fazendo X totalmente errado").
3. **Benefício direto** — promessa clara ("Como dobrar Y em Z dias").

## Pattern Interrupt (quebra de padrêo)
Mudar **cenário, ângulo de câmera ou elemento na tela a cada 3–5s** para manter o cérebro
engajado e evitar monotonia. Em motion graphics isso = trocar archetype/câmera/cor a cada
beat (ver `camera/vocabulary.md`).

## Loops narrativos
Abrir uma curiosidade no início que só é respondida no fim ("no final eu te mostro o
erro nº1"). Mantém o espectador até o fim. Pode haver micro-loops a cada seçêo.

## Compartilhamento (por que as pessoas compartilham)
- **Sinalizaçêo de identidade** — compartilham o que reflete quem elas sêo.
- **Emoçêo de alta excitaçêo** — humor, admiraçêo, raiva, inspiraçêo. (Emoções de baixa
  excitaçêo, como tristeza calma, compartilham menos.)

## Como vira plano
`EditPlan.intent.hook_variants[]` recebe as 3 opções. O beat de abertura usa a escolhida.
`pacing` define a cadência de pattern interrupt (ver `pacing.md`). Loops viram anotações
nos beats (`open_loop` / `close_loop`).

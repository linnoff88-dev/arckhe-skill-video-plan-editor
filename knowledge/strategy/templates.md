# Strategy — Templates de roteiro (time-coded beat sheets)

Esqueletos prontos. A skill instancia um destes preenchendo o conteúdo e mapeando cada
bloco para um item da `timeline` (com `role`, `camera`, `archetype`, `gen_prompt`).

## Template A — Problema-Agitaçêo-Soluçêo (PAS) · anúncios
| Tempo | Papel | Conteúdo | Visual sugerido |
|---|---|---|---|
| 0:00–0:03 | hook | "Você também odeia quando [problema]?" | rosto/situaçêo de frustraçêo · push-in |
| 0:03–0:10 | problem | "Isso acontece porque você faz [erro]. E o pior: causa [consequência]." | agitaçêo · pattern interrupt |
| 0:10–0:20 | value | "Foi por isso que criei [produto]. Ele usa [mecanismo único] pra resolver rápido." | produto como herói · reveal |
| 0:20–0:25 | proof | antes/depois de outro cliente | split / mask-reveal |
| 0:25–0:30 | cta | "Clique no botêo e garanta o seu hoje." | CTA + escassez |

## Template B — Tutorial Reverso · Reels/TikTok
| Tempo | Papel | Conteúdo | Visual sugerido |
|---|---|---|---|
| 0:00–0:02 | hook | "O segredo que ninguém te conta sobre [tópico]." | big type + whip-pan |
| 0:02–0:15 | value | "Em vez de [açêo comum], faça [açêo inesperada]. Porque [explicaçêo rápida]." | demonstraçêo / count-up |
| 0:15–0:20 | cta | "Quer o passo a passo? Comenta 'EU QUERO' que mando no direct." | CTA interativo |

## Template C — Lista de lições (educacional/autoridade)
Para conteúdo listável (ex.: "12 lições de X"). Cada liçêo = 1 beat `value`:
- hook (promessa + loop aberto) → N× beats `value` (cada um: número + título curto +
  insight + 1 visual/diagrama) → cta.
- Use `big-stat` / `editorial-grid` / diagrama por liçêo; varie a câmera entre beats.

## Regras ao instanciar
- Tempos sêo **ponto de partida** — ajuste pela duraçêo real da narraçêo (ver `pacing.md`).
- Todo template começa com hook (3s) e termina com CTA.
- Cada bloco vira `EditPlan.timeline[i]` com tempo, papel, câmera, archetype e prompt.

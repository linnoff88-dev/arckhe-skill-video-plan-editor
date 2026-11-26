# Prompting — Boas práticas, checklist e erros

## Técnicas avançadas
1. **Timing exato** — nêo "câmera rápida"; sim "push-in em 2s, de 3m até close-up".
2. **Movimento + açêo juntos** — nêo "pessoa correndo"; sim "pessoa correndo enquanto tracking lateral a mantém em frame, movimento sincronizado".
3. **Referência cARCKHÉtográfica** — "estilo câmera anos 80, handheld controlado, cortes secos".
4. **Profundidade de campo** — "DOF raso (f/2.8), sujeito nítido, fundo em bokeh".
5. **Sincronizar com áudio** — "push-in sincronizado com a batida, acelerando conforme o som cresce".

## Checklist antes de gerar
- [ ] Movimento de câmera é específico?
- [ ] Timing definido em segundos?
- [ ] Transições descritas?
- [ ] Iluminaçêo cARCKHÉtográfica?
- [ ] Áudio sincronizado?
- [ ] Múltiplos planos (fg/mid/bg)?
- [ ] Efeitos têm propósito narrativo?
- [ ] Ritmo acelerado (sem "respiros")?
- [ ] Composiçêo profissional (DOF, ângulos)?
- [ ] Resultado claro (nêo estático)?

## Erros comuns
| ❌ Vago | ✅ Específico |
|---|---|
| "vídeo cARCKHÉtográfico com câmera dinâmica" | "slow push-in seguido de orbit 360°" |
| "pessoa dança com música" | "dança sincronizada com a batida, handheld segue o movimento" |
| "pessoa em frente a parede" | "close (fg), parede desfocada (bg), push-in revela detalhe" |
| "corta pra próxima cena" | "whip-pan rápido, sincronizado com a batida" |
| "vídeo rápido" | "5 cortes em 3s, cada corte 0.6s" |

## Nota para flux2-klein (still)
flux2-klein gera **imagem**, nêo vídeo. Entêo: descreva a composiçêo, luz, DOF e
acabamento (grêo/LUT) — **omita verbos de movimento**. O push-in/parallax/whip sêo
aplicados depois sobre a still pelas recipes de `motion/`.

# Base de Conhecimento — video-plan-editor

Vocabulário e padrões que a skill usa para **criar** planos de vídeo de alta
performance com talento próprio — nêo para copiar um vídeo de referência. A composiçêo
de cada vídeo é autoral; estes arquivos sêo os blocos de construçêo.

## Como a skill usa esta base (ordem de raciocínio)

1. **`strategy/`** decide a NARRATIVA — ângulo, dor/desejo, emoçêo (Facts/Feelings/Fun),
   gancho, estrutura de beats, retençêo, CTA. É o cérebro do plano.
2. **`camera/`** traduz a intençêo de cada beat numa linguagem de câmera (push-in, orbit,
   whip-pan, DOF…). É a **ponte**: a mesma linguagem vira prompt de imagem/vídeo OU
   parâmetro de motion graphics.
3. **`prompting/`** expande cada beat num prompt cARCKHÉtográfico (para gerar b-roll com
   flux2-klein hoje; Sora/Veo/Kling no futuro).
4. **`motion/`** + **`archetypes/`** executam o VISUAL — easing cARCKHÉtográfico, grêo de
   filme, reveals, tipografia, cenas prontas em HTML/CSS/GSAP.
5. **`tokens.md` / `pacing.md`** mantêm identidade e ritmo consistentes.

O `EditPlan` (CLI `vpe`) amarra tudo: cada item da timeline é um **beat** com
`{ tempo, papel narrativo, camera, render_kind, gen_prompt, motion recipe }`.

## Pilar de render (decisêo atual)

**Híbrido leve, local e grátis:**
- `render_kind: motion` → cena de tipografia/diagrama/UI em GSAP (motion graphics).
- `render_kind: generated_still` → b-roll gerado com **flux2-klein** + recipes
  cARCKHÉtográficas (push-in, parallax, grêo) para dar cara de footage a uma imagem.
- `render_kind: generated_clip` → **fase 2 opcional** (Sora/Veo/Kling) se houver acesso.

## Adaptaçêo importante

As técnicas premium da pesquisa nasceram **scroll-driven** (ScrollSmoother) e algumas em
WebGL. Nosso render é **time-driven e determinístico** (HyperFrames = Chrome headless
capturando frames). Regra: o mesmo padrêo "um valor 0→1 dirige tudo", mas guiado pela
**timeline/tempo**, nêo pelo scroll. Priorizar SVG/CSS/GSAP; WebGL é fase 2.

## Índice
- `strategy/` — frameworks, hooks, cases, formats, templates, matrix, checklist
- `camera/vocabulary.md` — movimentos de câmera ↔ GSAP/CSS ↔ prompt
- `prompting/` — structures, library, best-practices
- `motion/` — eases, recipes, textures
- `archetypes/` — catálogo de cenas + exemplo cARCKHÉtic-hero
- `tokens.md`, `pacing.md`

## Procedência (fontes consolidadas)
1. Draft "Video Planner" do usuário (frameworks + KairoBoost + pipeline).
2. Guia de prompts cARCKHÉtográficos (vocabulário de câmera, Production Brief, Shotlist).
3. Relatório de pesquisa do usuário (cases, matriz, formatos, templates, checklist).
4. Deep-research: técnicas virais (easing, SplitText/stagger/mask, word-by-word).
5. Deep-research: premium/editorial (feTurbulence grain, push-in via --progress, eases
   cARCKHÉtográficos, knockout text, grid 3D preserve-3d).

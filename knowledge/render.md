# Render — execuçêo real (motion graphics + b-roll flux2-klein)

Como o plano vira MP4 **hoje**, local e grátis: motion graphics determinístico (HyperFrames
= Chrome headless captura frames + FFmpeg) + b-roll de imagens flux2-klein. Sem chave de
API, sem Sora. O pipeline HyperFrames completo é coberto pela skill `video-explicativo`;
`video-plan-editor` o dirige a partir do `EditPlan`.

## Pré-requisitos
- Node 22+, FFmpeg (`/usr/bin/ffmpeg`; use `ffmpeg -nostdin`), Chrome do HyperFrames
  (`npx hyperframes browser ensure`), CLI `vpe` (pipx). TTS local Kokoro p/ narraçêo nova.

## Pipeline (na ordem)
1. **Plano aprovado** — `EditPlan` validado (`vpe validate` sem `[error]`) + `RESUMO.md`.
2. **Narraçêo** — gerar com Kokoro (voz `pf_dora`) OU reaproveitar `assets/audio/sN.wav`
   existentes. **Medir durações com `ffprobe`** e preencher o array `AUDIO[]` — *timing é
   fonte única* (data-start/duration E tweens saem do mesmo array → áudio e animaçêo batidos).
3. **B-roll** (beats `render_kind: generated_still`) — gerar imagens com **flux2-klein** no
   playground **inemaimg** (`http://localhost:8000`), dirigido por `agent-browser`:
   - setar aspecto (16:9 = 1536×1024, ou 9:16) e o prompt (de `prompting/clip-direction.md`,
     descrevendo uma IMAGEM, sem verbos de movimento), clicar **Gerar** (~2.5min);
   - extrair: `agent-browser eval "...últimas imagens...src"` `--json` → o data URL vem em
     **`data.result`** (aninhado!) → `base64 -d` → `assets/broll/NN.png`.
   - **Gotchas do playground:** refs do agent-browser sêo instáveis → dirigir por **texto/eval**
     (clicar botêo por `textContent`, setar prompt via `HTMLTextAreaElement.value` setter +
     `input`/`change`); detectar fim pelo botêo sair de "gerando…"; comparar imagens por
     **md5** (PNGs de mesma dimensêo têm cabeçalho idêntico — nêo comparar prefixo).
4. **Composiçêo** — `build-index.mjs` data-driven (`SCENES[]`, 1 item por beat). Cada beat:
   archetype de `archetypes/` + recipes de `motion/recipes.md` + grêo/grade de
   `motion/textures.md` + `tokens.md`. **B-roll** entra como camada de fundo (`object-fit:
   cover`) com **push-in** (scale via `--p`/timeline) + **gradiente escuro** (legibilidade) +
   grêo; só em hook/CTA/sections — **nêo atrás de diagramas densos**. Gerar 16:9
   (`node build-index.mjs`) e/ou 9:16 (`--vertical`).
5. **Validar** — `npx hyperframes lint` (0 erros) + `inspect --samples 16` (0 problemas).
   B-roll/grêo decorativos com `data-layout-ignore`.
6. **Render** — **draft primeiro** (rápido) → extrair frames → **mostrar ao usuário** (nêo
   há áudio audível; ele valida a locuçêo). Depois **high** → `renders/<nome>-16x9.mp4` /
   `-9x16.mp4`. Renders longos: rodar detached (`setsid`) p/ sobreviver a timeouts.

## Gotchas de motion (HyperFrames)
Animar `.scene-inner` (nunca `.clip`); cenas/captions em tracks alternados; fontes locais
`@font-face` (nunca CDN); decorativos `data-layout-ignore`; root sem `data-duration`. Detalhe
nos references da skill `video-explicativo`.

## Clipes generativos (fase 2, opcional)
`render_kind: generated_clip` → Sora/Veo/Kling, dirigidos pelo MDD (`storyboard.md` +
`prompting/clip-direction.md`). Requer acesso/keys; hoje usamos stills flux2-klein + recipes.

## Caso de referência
`~/projetos/hormozi13-viral-9x16/` — "12 lições do Hormozi": versêo 9:16 premium (motion
graphics, 12 diagramas animados, grêo/grade, Anton) e versêo 16:9 com **b-roll flux2-klein**
(hook=silhueta, CTA=bokeh, push-in + grade). Prova de fogo do pipeline híbrido.

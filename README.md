# skill-video-plan-editor

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


Skill (Claude Code) + pacote Python que transforma um **assunto** ou um **link**
(pÃ¡gina/vÃ­deo) num **plano profissional de ediÃ§Ã£o de vÃ­deo** â€” dado estruturado,
renderer-agnÃ³stico â€” e, opcionalmente, renderiza o vÃ­deo.

> VocÃª passa um assunto/link â†’ a skill **detecta o tipo de input**, **analisa a melhor
> aÃ§Ã£o de ediÃ§Ã£o**, escolhe um **preset de estilo** e emite `plano-edicao.json` +
> `RESUMO.md`. O render Ã© opcional e **jÃ¡ funciona**: motion graphics (HyperFrames) +
> b-roll gerado no **flux2-klein** â€” local, determinÃ­stico, sem chave de API.

---

## Por que

A ediÃ§Ã£o programÃ¡tica de vÃ­deo Ã© fragmentada: FFmpeg (CLI bruto), Auto-Editor (corte por
anÃ¡lise), MoviePy (Python), Remotion (React), HyperFrames (HTMLâ†’MP4). Falta a camada que,
a partir de **linguagem natural**, **decide o que fazer** e emite um plano de ediÃ§Ã£o limpo
e portÃ¡vel. Ã‰ isso que esta skill faz â€” e o plano, sendo JSON renderer-agnÃ³stico, pode ser
consumido por qualquer um desses backends ou por outros sistemas.

## InstalaÃ§Ã£o

Requer Python â‰¥ 3.11.

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
```

Isso expÃµe o console script **`vpe`**.

## InÃ­cio rÃ¡pido

```bash
# 1. Gerar o esqueleto do plano a partir do input + preset
vpe scaffold "como fazer pÃ£o caseiro" --preset viral > plano-edicao.json

# 2. (a skill preenche a timeline criativa â€” veja examples/)

# 3. Validar os guardrails antes de qualquer render
vpe validate plano-edicao.json

# 4. Gerar o resumo legÃ­vel para aprovaÃ§Ã£o
vpe resumo plano-edicao.json > RESUMO.md
```

## Como funciona

```
input (assunto | link de pÃ¡gina | link de vÃ­deo)
   â”‚
   â–¼
 detect â”€â†’ ingest+analyze â”€â†’ best action â”€â†’ preset de estilo â”€â†’ PLANO (json + resumo)
                                                                      â”‚
                                                          (opcional)  â–¼
                                                                   render â†’ MP4
```

- **Detect** (`vpe`/`detect.py`): classifica o input em `topic`, `page` ou `video` (por
  URL, extensÃ£o e domÃ­nio).
- **Analyze / best action**: a skill (via `SKILL.md`) decide o modo â€” vÃ­deo gerado para
  assunto/pÃ¡gina, corte de footage real para vÃ­deo â€” e registra o porquÃª em
  `intent.best_action_rationale`.
- **Preset de estilo**: `acao | suave | promo | vendas | viral` (perfis de parÃ¢metro).
- **Plano**: JSON abstrato (`EditPlan`, pydantic) + `RESUMO.md` legÃ­vel.
- **Render (opcional, jÃ¡ funcional)**: motion graphics via HyperFrames + b-roll flux2-klein
  (ver seÃ§Ã£o **Render** abaixo). Ingest de footage real (Auto-Editor) e clipes generativos
  (Sora/Veo) ficam pro roadmap.

## CLI â€” exemplos reais

### `vpe scaffold` â€” detecta o input e aplica o preset

```bash
$ vpe scaffold "https://youtu.be/dQw4w9WgXcQ" --preset viral --title "Corte Viral"
```
```jsonc
{
  "version": "1.0",
  "meta": { "title": "Corte Viral", "language": "pt-BR" },
  "source": { "kind": "video", "ref": "https://youtu.be/dQw4w9WgXcQ", "media": null },
  "intent": {
    "goal": "viral",
    "best_action_rationale": "Input classificado como 'video'; preset 'viral' sugere objetivo 'viral'. ..."
  },
  "style": {
    "preset": "viral",
    "pacing": { "avg_cut_seconds": 1.1, "energy": 0.95 },
    "transitions": ["cut", "zoom"],
    "music": { "energy": 0.95 },
    "captions": { "enabled": true, "style": "karaoke", "position": null },
    "color": { "look": "punchy" }
  },
  "output": { "aspect": "9:16", "duration_target_seconds": 30.0, "platform": "generic" },
  "timeline": [],
  "render": { "engine_hint": "auto" }
}
```
> O input do YouTube foi classificado como `video` e o preset `viral` jÃ¡ aplicou corte
> ~1.1s, legenda karaoke e aspect 9:16. A `timeline` nasce vazia â€” Ã© preenchida pela skill.

### `vpe validate` â€” guardrails antes do render

```bash
$ vpe validate examples/exemplo-viral-pao.json
$ echo $?
0
```
Plano com problemas reporta os itens (e retorna cÃ³digo 1 se houver `[error]`):
```text
[error] empty_timeline: timeline tem 0 itens
[warning] no_hook: plano sem cena de hook
```

### `vpe resumo` â€” documento legÃ­vel para aprovaÃ§Ã£o

```bash
$ vpe resumo examples/exemplo-viral-pao.json
```
```markdown
# PÃ£o caseiro em 20s

- **Fonte:** topic â€” como fazer pÃ£o caseiro rÃ¡pido
- **Objetivo:** viral
- **Por que essa aÃ§Ã£o:** Assunto curto, visual e com payoff imediato â€” ideal para vÃ­deo gerado vertical com cortes rÃ¡pidos.
- **Preset:** viral (corte ~1.1s, energia 0.95)
- **SaÃ­da:** 9:16, alvo 20.0s, tiktok

## Timeline
1. **hook** (`s1`)
   - Headline: PÃ£o em 20 segundos?!
   - NarraÃ§Ã£o: Olha sÃ³ que rÃ¡pido.
   - Legenda [0.0-1.5]: PÃ£o em 20s?!
2. **point** (`s2`)
   - Headline: 3 ingredientes
   - NarraÃ§Ã£o: Farinha, Ã¡gua e fermento.
   - Legenda [1.5-4.0]: SÃ³ 3 ingredientes
3. **cta** (`s3`)
   - Headline: INEMA.CLUB
   - NarraÃ§Ã£o: Receita completa no inema ponto club.
   - Legenda [18.0-20.0]: inema.club
```

Veja o plano completo de exemplo em [`examples/exemplo-viral-pao.json`](examples/exemplo-viral-pao.json).

## Presets

| Preset | corte mÃ©dio | transiÃ§Ãµes | trilha | legenda | aspect | uso |
|---|---|---|---|---|---|---|
| **acao**   | 1â€“2s | whip/zoom | alta | karaoke | 9:16 | dinÃ¢mico |
| **suave**  | 4â€“6s | crossfade | baixa | minimal | 16:9 | institucional |
| **promo**  | 2â€“3s | cut+zoom | mÃ©dia-alta | block | 16:9 / 1:1 | clipe promocional |
| **vendas** | 2â€“4s | cut | mÃ©dia | block + CTA | 16:9 / 9:16 | VSL/oferta |
| **viral**  | 0.8â€“1.5s | jump cut | alta | karaoke | 9:16 | TikTok/Instagram |

Cada preset Ã© um perfil de parÃ¢metros sobre o **mesmo** schema â€” trocar o preset muda
ritmo/transiÃ§Ãµes/trilha/legenda/aspect sem reescrever o plano base.

## Schema do plano (`EditPlan`)

JSON serializÃ¡vel (pydantic 2). Campos principais:

| Bloco | ConteÃºdo |
|---|---|
| `meta` | `title`, `language` |
| `source` | `kind` (video/page/topic), `ref`, `media` (duration/fps/resolution) |
| `intent` | `goal` (highlights/supercut/promo/explainer/sales/viral), `best_action_rationale` |
| `style` | `preset`, `pacing{avg_cut_seconds,energy}`, `transitions[]`, `music{energy}`, `captions{style}`, `color{look}` |
| `output` | `aspect` (16:9/9:16/1:1), `duration_target_seconds`, `platform` |
| `timeline[]` | `id`, `role` (hook/intro/point/broll/cta), `source_in/out` (corte real) **ou** `content{headline,narration,broll_query}` (cena gerada), `captions[]`, `overlays[]`, `transition_out` |
| `render` | `engine_hint` (auto/ffmpeg/hyperframes) |

## Como a skill orquestra (`SKILL.md`)

1. `vpe scaffold "<input>" --preset <...>` â†’ esqueleto do plano.
2. Preenche a `timeline` (roteiro/cenas para assunto/pÃ¡gina; `source_in/out` para vÃ­deo).
3. `vpe validate` â†’ zera os `[error]`.
4. `vpe resumo` â†’ mostra ao usuÃ¡rio para aprovar.
5. Render (opcional) quando solicitado â€” motion graphics + b-roll flux2-klein (ver **Render**).

Identidade default PT-BR; CTA INEMA.CLUB como Ãºltima cena em vÃ­deos gerados (desligÃ¡vel).

## Base de conhecimento (`knowledge/`)

O que dÃ¡ "talento" Ã  skill â€” vocabulÃ¡rio e padrÃµes que ela usa para **criar** (nÃ£o copiar).
A composiÃ§Ã£o de cada vÃ­deo Ã© autoral; estes arquivos sÃ£o os blocos de construÃ§Ã£o.

| Pilar | ConteÃºdo |
|---|---|
| `strategy/` | NARRATIVA â€” Viral5, Save the Cat, Hero, Hook-Value-CTA, hooks 3s, cases, formatos (Reels/VSL/Autoridade), templates, matriz, checklist |
| `camera/vocabulary.md` | linguagem de cÃ¢mera (ponte: vira prompt **e** parÃ¢metro de motion) |
| `storyboard.md` | **direÃ§Ã£o de cena** â€” conflito visual, cÃ¢mera por funÃ§Ã£o, continuidade sagrada, freeze final (**absorvido do MDD**) |
| `prompting/` | expandir cada beat em prompt cinematogrÃ¡fico; `clip-direction.md` = prompt-final + negativo |
| `motion/` | eases cinematogrÃ¡ficos, recipes GSAP/CSS time-driven, texturas feTurbulence (grÃ£o/halaÃ§Ã£o sem assets) |
| `archetypes/` | cenas prontas (HTML+CSS+GSAP), ex.: `cinematic-hero` |
| `tokens.md` Â· `pacing.md` | identidade (paleta/fontes) e ritmo (word-by-word, pattern interrupt) |

**IntegraÃ§Ã£o com o MDD** ([`mestre-direcao-dinamica`](#)): para beats
`render_kind: generated_clip`/`generated_still`, a skill **delega a direÃ§Ã£o cinematogrÃ¡fica
ao MDD** â€” que devolve storyboard painel-a-painel + prompt final + prompt negativo de
qualidade de diretor. `video-plan-editor` Ã© o **orquestrador** (estratÃ©gia â†’ plano â†’
execuÃ§Ã£o); o MDD Ã© o **motor de direÃ§Ã£o** dos beats generativos. Os princÃ­pios do MDD
(conflito visual, continuidade, freeze, CTA fora do prompt) estÃ£o destilados em
`knowledge/storyboard.md` e `knowledge/prompting/clip-direction.md`.

## Render (execuÃ§Ã£o real)

Local, determinÃ­stico, **sem chave de API** (HyperFrames = Chrome headless + FFmpeg). Receita
completa em [`knowledge/render.md`](knowledge/render.md). Resumo:

1. Plano aprovado (`vpe validate` ok) + narraÃ§Ã£o (Kokoro local ou WAVs reaproveitados;
   duraÃ§Ãµes medidas com `ffprobe` â†’ timing Ã© fonte Ãºnica).
2. **B-roll** (beats `generated_still`): gerar imagens no **flux2-klein** (playground
   `inemaimg`, dirigido por `agent-browser`) â†’ `assets/broll/`.
3. **ComposiÃ§Ã£o** `build-index.mjs` (data-driven): cada beat = archetype + recipes de motion
   + grÃ£o/grade; b-roll de fundo com push-in + gradiente escuro (sÃ³ hook/CTA/sections, nunca
   atrÃ¡s de diagrama denso).
4. `hyperframes lint` (0) + `inspect` (0) â†’ render **draft** (QC com frames) â†’ **high**
   (`renders/<nome>-16x9.mp4` / `-9x16.mp4`).

Clipes generativos (Sora/Veo/Kling) sÃ£o fase 2 opcional, dirigidos pelo MDD.

**Caso de referÃªncia:** `~/projetos/hormozi13-viral-9x16/` â€” "12 liÃ§Ãµes do Hormozi" em 9:16
premium (12 diagramas animados, grÃ£o/grade, Anton) e 16:9 com **b-roll flux2-klein** (hook
= silhueta, CTA = bokeh, push-in + grade). Prova de fogo do pipeline hÃ­brido.

## Arquitetura

```
video_plan_editor/
â”œâ”€â”€ models.py     # schema EditPlan (pydantic) + enums
â”œâ”€â”€ presets.py    # PresetProfile, registry PRESETS, style_for()
â”œâ”€â”€ detect.py     # classify_input() -> SourceKind
â”œâ”€â”€ validate.py   # Issue, validate_plan(), is_valid()  (guardrails preflight)
â”œâ”€â”€ resumo.py     # render_resumo() plano -> markdown
â”œâ”€â”€ builder.py    # scaffold_plan() detect + preset -> EditPlan
â””â”€â”€ cli.py        # vpe scaffold | validate | resumo
```

A camada de guardrails/validaÃ§Ã£o Ã© inspirada no fork
[`inematds/mcp-video`](https://github.com/inematds/mcp-video) (Apache-2.0, de
KyaniteLabs/mcp-video), que envolve FFmpeg + HyperFrames.

## Desenvolvimento

```bash
. .venv/bin/activate
pytest -v          # 35 testes
vpe scaffold "teste" --preset acao
```

## Roadmap

- **NÃºcleo gerador de plano** â€” schema, presets, detect, validaÃ§Ã£o, resumo, CLI. âœ…
- **Base de conhecimento** â€” strategy/camera/storyboard/prompting/motion/archetypes (+ MDD). âœ…
- **Render motion graphics + b-roll flux2-klein** (HyperFrames) â€” funcional (ver Render). âœ…
- **Ingest de footage real** â€” yt-dlp + ffprobe + transcriÃ§Ã£o + corte por silÃªncio/cena
  (Auto-Editor) + auto-highlights (padrÃ£o LAVE). â³ prÃ³ximo.
- **Clipes generativos** â€” Sora/Veo/Kling dirigidos pelo MDD (precisa de acesso). â³
- **Render nativo Remotion** (plano â†’ Tracks/Items) usando os
  [**remotion-templates**](https://github.com/inematds/remotion-templates) (81 componentes) como biblioteca
  de archetypes por beat/`role` (`hook`â†’Intro/Title, `point`â†’Text/Charts, `broll`â†’Image/Cinematic, `cta`â†’End
  Card) + export **OTIO `.otio`** p/ NLEs. â³

## Documentos

- Spec de design: [`docs/superpowers/specs/2026-06-06-video-plan-editor-design.md`](docs/superpowers/specs/2026-06-06-video-plan-editor-design.md)
- Plano de implementaÃ§Ã£o (Fase 1): [`docs/superpowers/plans/2026-06-06-video-plan-editor-core.md`](docs/superpowers/plans/2026-06-06-video-plan-editor-core.md)
- Pesquisa profunda: [`PESQUISA-E-DESIGN.md`](PESQUISA-E-DESIGN.md)

## LicenÃ§a

A definir.

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>
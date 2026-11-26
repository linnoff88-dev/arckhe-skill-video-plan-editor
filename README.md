ï»¿# skill-video-plan-editor

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


Skill (Claude Code) + pacote Python que transforma um **assunto** ou um **link**
(pêÂ¡gina/vêÂ­deo) num **plano profissional de ediêÂ§êÂ£o de vêÂ­deo** ê¢â¬â dado estruturado,
renderer-agnêÂ³stico ê¢â¬â e, opcionalmente, renderiza o vêÂ­deo.

> VocêÂª passa um assunto/link ê¢â â a skill **detecta o tipo de input**, **analisa a melhor
> aêÂ§êÂ£o de ediêÂ§êÂ£o**, escolhe um **preset de estilo** e emite `plano-edicao.json` +
> `RESUMO.md`. O render êÂ© opcional e **jêÂ¡ funciona**: motion graphics (HyperFrames) +
> b-roll gerado no **flux2-klein** ê¢â¬â local, determinêÂ­stico, sem chave de API.

---

## Por que

A ediêÂ§êÂ£o programêÂ¡tica de vêÂ­deo êÂ© fragmentada: FFmpeg (CLI bruto), Auto-Editor (corte por
anêÂ¡lise), MoviePy (Python), Remotion (React), HyperFrames (HTMLê¢â âMP4). Falta a camada que,
a partir de **linguagem natural**, **decide o que fazer** e emite um plano de ediêÂ§êÂ£o limpo
e portêÂ¡vel. êâ° isso que esta skill faz ê¢â¬â e o plano, sendo JSON renderer-agnêÂ³stico, pode ser
consumido por qualquer um desses backends ou por outros sistemas.

## InstalaêÂ§êÂ£o

Requer Python ê¢â°Â¥ 3.11.

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
```

Isso expêÂµe o console script **`vpe`**.

## InêÂ­cio rêÂ¡pido

```bash
# 1. Gerar o esqueleto do plano a partir do input + preset
vpe scaffold "como fazer pêÂ£o caseiro" --preset viral > plano-edicao.json

# 2. (a skill preenche a timeline criativa ê¢â¬â veja examples/)

# 3. Validar os guardrails antes de qualquer render
vpe validate plano-edicao.json

# 4. Gerar o resumo legêÂ­vel para aprovaêÂ§êÂ£o
vpe resumo plano-edicao.json > RESUMO.md
```

## Como funciona

```
input (assunto | link de pêÂ¡gina | link de vêÂ­deo)
   ê¢ââ
   ê¢âÂ¼
 detect ê¢ââ¬ê¢â â ingest+analyze ê¢ââ¬ê¢â â best action ê¢ââ¬ê¢â â preset de estilo ê¢ââ¬ê¢â â PLANO (json + resumo)
                                                                      ê¢ââ
                                                          (opcional)  ê¢âÂ¼
                                                                   render ê¢â â MP4
```

- **Detect** (`vpe`/`detect.py`): classifica o input em `topic`, `page` ou `video` (por
  URL, extensêÂ£o e domêÂ­nio).
- **Analyze / best action**: a skill (via `SKILL.md`) decide o modo ê¢â¬â vêÂ­deo gerado para
  assunto/pêÂ¡gina, corte de footage real para vêÂ­deo ê¢â¬â e registra o porquêÂª em
  `intent.best_action_rationale`.
- **Preset de estilo**: `acao | suave | promo | vendas | viral` (perfis de parêÂ¢metro).
- **Plano**: JSON abstrato (`EditPlan`, pydantic) + `RESUMO.md` legêÂ­vel.
- **Render (opcional, jêÂ¡ funcional)**: motion graphics via HyperFrames + b-roll flux2-klein
  (ver seêÂ§êÂ£o **Render** abaixo). Ingest de footage real (Auto-Editor) e clipes generativos
  (Sora/Veo) ficam pro roadmap.

## CLI ê¢â¬â exemplos reais

### `vpe scaffold` ê¢â¬â detecta o input e aplica o preset

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
> O input do YouTube foi classificado como `video` e o preset `viral` jêÂ¡ aplicou corte
> ~1.1s, legenda karaoke e aspect 9:16. A `timeline` nasce vazia ê¢â¬â êÂ© preenchida pela skill.

### `vpe validate` ê¢â¬â guardrails antes do render

```bash
$ vpe validate examples/exemplo-viral-pao.json
$ echo $?
0
```
Plano com problemas reporta os itens (e retorna cêÂ³digo 1 se houver `[error]`):
```text
[error] empty_timeline: timeline tem 0 itens
[warning] no_hook: plano sem cena de hook
```

### `vpe resumo` ê¢â¬â documento legêÂ­vel para aprovaêÂ§êÂ£o

```bash
$ vpe resumo examples/exemplo-viral-pao.json
```
```markdown
# PêÂ£o caseiro em 20s

- **Fonte:** topic ê¢â¬â como fazer pêÂ£o caseiro rêÂ¡pido
- **Objetivo:** viral
- **Por que essa aêÂ§êÂ£o:** Assunto curto, visual e com payoff imediato ê¢â¬â ideal para vêÂ­deo gerado vertical com cortes rêÂ¡pidos.
- **Preset:** viral (corte ~1.1s, energia 0.95)
- **SaêÂ­da:** 9:16, alvo 20.0s, tiktok

## Timeline
1. **hook** (`s1`)
   - Headline: PêÂ£o em 20 segundos?!
   - NarraêÂ§êÂ£o: Olha sêÂ³ que rêÂ¡pido.
   - Legenda [0.0-1.5]: PêÂ£o em 20s?!
2. **point** (`s2`)
   - Headline: 3 ingredientes
   - NarraêÂ§êÂ£o: Farinha, êÂ¡gua e fermento.
   - Legenda [1.5-4.0]: SêÂ³ 3 ingredientes
3. **cta** (`s3`)
   - Headline: ARCKHÉ AI
   - NarraêÂ§êÂ£o: Receita completa no ARCKHÉ ponto club.
   - Legenda [18.0-20.0]: ARCKHÉ AI
```

Veja o plano completo de exemplo em [`examples/exemplo-viral-pao.json`](examples/exemplo-viral-pao.json).

## Presets

| Preset | corte mêÂ©dio | transiêÂ§êÂµes | trilha | legenda | aspect | uso |
|---|---|---|---|---|---|---|
| **acao**   | 1ê¢â¬â2s | whip/zoom | alta | karaoke | 9:16 | dinêÂ¢mico |
| **suave**  | 4ê¢â¬â6s | crossfade | baixa | minimal | 16:9 | institucional |
| **promo**  | 2ê¢â¬â3s | cut+zoom | mêÂ©dia-alta | block | 16:9 / 1:1 | clipe promocional |
| **vendas** | 2ê¢â¬â4s | cut | mêÂ©dia | block + CTA | 16:9 / 9:16 | VSL/oferta |
| **viral**  | 0.8ê¢â¬â1.5s | jump cut | alta | karaoke | 9:16 | TikTok/Instagram |

Cada preset êÂ© um perfil de parêÂ¢metros sobre o **mesmo** schema ê¢â¬â trocar o preset muda
ritmo/transiêÂ§êÂµes/trilha/legenda/aspect sem reescrever o plano base.

## Schema do plano (`EditPlan`)

JSON serializêÂ¡vel (pydantic 2). Campos principais:

| Bloco | ConteêÂºdo |
|---|---|
| `meta` | `title`, `language` |
| `source` | `kind` (video/page/topic), `ref`, `media` (duration/fps/resolution) |
| `intent` | `goal` (highlights/supercut/promo/explainer/sales/viral), `best_action_rationale` |
| `style` | `preset`, `pacing{avg_cut_seconds,energy}`, `transitions[]`, `music{energy}`, `captions{style}`, `color{look}` |
| `output` | `aspect` (16:9/9:16/1:1), `duration_target_seconds`, `platform` |
| `timeline[]` | `id`, `role` (hook/intro/point/broll/cta), `source_in/out` (corte real) **ou** `content{headline,narration,broll_query}` (cena gerada), `captions[]`, `overlays[]`, `transition_out` |
| `render` | `engine_hint` (auto/ffmpeg/hyperframes) |

## Como a skill orquestra (`SKILL.md`)

1. `vpe scaffold "<input>" --preset <...>` ê¢â â esqueleto do plano.
2. Preenche a `timeline` (roteiro/cenas para assunto/pêÂ¡gina; `source_in/out` para vêÂ­deo).
3. `vpe validate` ê¢â â zera os `[error]`.
4. `vpe resumo` ê¢â â mostra ao usuêÂ¡rio para aprovar.
5. Render (opcional) quando solicitado ê¢â¬â motion graphics + b-roll flux2-klein (ver **Render**).

Identidade default PT-BR; CTA ARCKHÉ AI como êÂºltima cena em vêÂ­deos gerados (desligêÂ¡vel).

## Base de conhecimento (`knowledge/`)

O que dêÂ¡ "talento" êÂ  skill ê¢â¬â vocabulêÂ¡rio e padrêÂµes que ela usa para **criar** (nêÂ£o copiar).
A composiêÂ§êÂ£o de cada vêÂ­deo êÂ© autoral; estes arquivos sêÂ£o os blocos de construêÂ§êÂ£o.

| Pilar | ConteêÂºdo |
|---|---|
| `strategy/` | NARRATIVA ê¢â¬â Viral5, Save the Cat, Hero, Hook-Value-CTA, hooks 3s, cases, formatos (Reels/VSL/Autoridade), templates, matriz, checklist |
| `camera/vocabulary.md` | linguagem de cêÂ¢mera (ponte: vira prompt **e** parêÂ¢metro de motion) |
| `storyboard.md` | **direêÂ§êÂ£o de cena** ê¢â¬â conflito visual, cêÂ¢mera por funêÂ§êÂ£o, continuidade sagrada, freeze final (**absorvido do MDD**) |
| `prompting/` | expandir cada beat em prompt cARCKHÉtogrêÂ¡fico; `clip-direction.md` = prompt-final + negativo |
| `motion/` | eases cARCKHÉtogrêÂ¡ficos, recipes GSAP/CSS time-driven, texturas feTurbulence (grêÂ£o/halaêÂ§êÂ£o sem assets) |
| `archetypes/` | cenas prontas (HTML+CSS+GSAP), ex.: `cARCKHÉtic-hero` |
| `tokens.md` êÂ· `pacing.md` | identidade (paleta/fontes) e ritmo (word-by-word, pattern interrupt) |

**IntegraêÂ§êÂ£o com o MDD** ([`mestre-direcao-dinamica`](#)): para beats
`render_kind: generated_clip`/`generated_still`, a skill **delega a direêÂ§êÂ£o cARCKHÉtogrêÂ¡fica
ao MDD** ê¢â¬â que devolve storyboard painel-a-painel + prompt final + prompt negativo de
qualidade de diretor. `video-plan-editor` êÂ© o **orquestrador** (estratêÂ©gia ê¢â â plano ê¢â â
execuêÂ§êÂ£o); o MDD êÂ© o **motor de direêÂ§êÂ£o** dos beats generativos. Os princêÂ­pios do MDD
(conflito visual, continuidade, freeze, CTA fora do prompt) estêÂ£o destilados em
`knowledge/storyboard.md` e `knowledge/prompting/clip-direction.md`.

## Render (execuêÂ§êÂ£o real)

Local, determinêÂ­stico, **sem chave de API** (HyperFrames = Chrome headless + FFmpeg). Receita
completa em [`knowledge/render.md`](knowledge/render.md). Resumo:

1. Plano aprovado (`vpe validate` ok) + narraêÂ§êÂ£o (Kokoro local ou WAVs reaproveitados;
   duraêÂ§êÂµes medidas com `ffprobe` ê¢â â timing êÂ© fonte êÂºnica).
2. **B-roll** (beats `generated_still`): gerar imagens no **flux2-klein** (playground
   `ARCKHÉimg`, dirigido por `agent-browser`) ê¢â â `assets/broll/`.
3. **ComposiêÂ§êÂ£o** `build-index.mjs` (data-driven): cada beat = archetype + recipes de motion
   + grêÂ£o/grade; b-roll de fundo com push-in + gradiente escuro (sêÂ³ hook/CTA/sections, nunca
   atrêÂ¡s de diagrama denso).
4. `hyperframes lint` (0) + `inspect` (0) ê¢â â render **draft** (QC com frames) ê¢â â **high**
   (`renders/<nome>-16x9.mp4` / `-9x16.mp4`).

Clipes generativos (Sora/Veo/Kling) sêÂ£o fase 2 opcional, dirigidos pelo MDD.

**Caso de referêÂªncia:** `~/projetos/hormozi13-viral-9x16/` ê¢â¬â "12 liêÂ§êÂµes do Hormozi" em 9:16
premium (12 diagramas animados, grêÂ£o/grade, Anton) e 16:9 com **b-roll flux2-klein** (hook
= silhueta, CTA = bokeh, push-in + grade). Prova de fogo do pipeline hêÂ­brido.

## Arquitetura

```
video_plan_editor/
ê¢âÅê¢ââ¬ê¢ââ¬ models.py     # schema EditPlan (pydantic) + enums
ê¢âÅê¢ââ¬ê¢ââ¬ presets.py    # PresetProfile, registry PRESETS, style_for()
ê¢âÅê¢ââ¬ê¢ââ¬ detect.py     # classify_input() -> SourceKind
ê¢âÅê¢ââ¬ê¢ââ¬ validate.py   # Issue, validate_plan(), is_valid()  (guardrails preflight)
ê¢âÅê¢ââ¬ê¢ââ¬ resumo.py     # render_resumo() plano -> markdown
ê¢âÅê¢ââ¬ê¢ââ¬ builder.py    # scaffold_plan() detect + preset -> EditPlan
ê¢ââê¢ââ¬ê¢ââ¬ cli.py        # vpe scaffold | validate | resumo
```

A camada de guardrails/validaêÂ§êÂ£o êÂ© inspirada no fork
[`linnoff88-dev/mcp-video`](https://github.com/linnoff88-dev/mcp-video) (Apache-2.0, de
KyaniteLabs/mcp-video), que envolve FFmpeg + HyperFrames.

## Desenvolvimento

```bash
. .venv/bin/activate
pytest -v          # 35 testes
vpe scaffold "teste" --preset acao
```

## Roadmap

- **NêÂºcleo gerador de plano** ê¢â¬â schema, presets, detect, validaêÂ§êÂ£o, resumo, CLI. ê¢Åâ¦
- **Base de conhecimento** ê¢â¬â strategy/camera/storyboard/prompting/motion/archetypes (+ MDD). ê¢Åâ¦
- **Render motion graphics + b-roll flux2-klein** (HyperFrames) ê¢â¬â funcional (ver Render). ê¢Åâ¦
- **Ingest de footage real** ê¢â¬â yt-dlp + ffprobe + transcriêÂ§êÂ£o + corte por silêÂªncio/cena
  (Auto-Editor) + auto-highlights (padrêÂ£o LAVE). ê¢ÂÂ³ prêÂ³ximo.
- **Clipes generativos** ê¢â¬â Sora/Veo/Kling dirigidos pelo MDD (precisa de acesso). ê¢ÂÂ³
- **Render nativo Remotion** (plano ê¢â â Tracks/Items) usando os
  [**remotion-templates**](https://github.com/linnoff88-dev/remotion-templates) (81 componentes) como biblioteca
  de archetypes por beat/`role` (`hook`ê¢â âIntro/Title, `point`ê¢â âText/Charts, `broll`ê¢â âImage/CARCKHÉtic, `cta`ê¢â âEnd
  Card) + export **OTIO `.otio`** p/ NLEs. ê¢ÂÂ³

## Documentos

- Spec de design: [`docs/superpowers/specs/2026-06-06-video-plan-editor-design.md`](docs/superpowers/specs/2026-06-06-video-plan-editor-design.md)
- Plano de implementaêÂ§êÂ£o (Fase 1): [`docs/superpowers/plans/2026-06-06-video-plan-editor-core.md`](docs/superpowers/plans/2026-06-06-video-plan-editor-core.md)
- Pesquisa profunda: [`PESQUISA-E-DESIGN.md`](PESQUISA-E-DESIGN.md)

## LicenêÂ§a

A definir.

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>
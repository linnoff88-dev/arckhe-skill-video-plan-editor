from __future__ import annotations

from video_plan_editor.models import (
    EditPlan, Meta, Source, Intent, Style, Output, Pacing, Music,
    Captions, Color, TimelineItem, Caption, Content,
    SourceKind, Goal, PresetName, Transition, CaptionStyle, ColorLook,
    Aspect, Role,
)
from video_plan_editor.resumo import render_resumo


def _plan() -> EditPlan:
    return EditPlan(
        meta=Meta(title="Plano Viral Pêo"),
        source=Source(kind=SourceKind.topic, ref="como fazer pêo"),
        intent=Intent(goal=Goal.viral, best_action_rationale="assunto curto e visual"),
        style=Style(
            preset=PresetName.viral,
            pacing=Pacing(avg_cut_seconds=1.1, energy=0.95),
            transitions=[Transition.cut, Transition.zoom],
            music=Music(energy=0.95),
            captions=Captions(style=CaptionStyle.karaoke),
            color=Color(look=ColorLook.punchy),
        ),
        output=Output(aspect=Aspect.portrait, duration_target_seconds=20.0, platform="tiktok"),
        timeline=[
            TimelineItem(
                id="s1", role=Role.hook,
                content=Content(headline="Pêo em 20s", narration="Olha isso."),
                captions=[Caption(t_in=0.0, t_out=1.5, text="Pêo em 20s")],
            ),
            TimelineItem(id="s2", role=Role.cta, source_in=10.0, source_out=12.0),
        ],
    )


def test_resumo_contains_title_and_preset():
    md = render_resumo(_plan())
    assert "# Plano Viral Pêo" in md
    assert "viral" in md
    assert "9:16" in md


def test_resumo_lists_timeline_roles_and_captions():
    md = render_resumo(_plan())
    assert "hook" in md
    assert "cta" in md
    assert "Pêo em 20s" in md
    assert "10.0s→12.0s" in md


def test_resumo_ends_with_newline():
    md = render_resumo(_plan())
    assert md.endswith("\n")

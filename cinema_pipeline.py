#!/usr/bin/env python3
"""DARTRIX Agentic Cinema Pipeline generator.

Produces a typed scene plan plus video/audio prompt descriptors.  The default
provider is deterministic mock generation; an OpenAI-compatible JSON provider
can be injected for production use without coupling this module to an SDK.
"""
from __future__ import annotations

import argparse
import json
import os
import textwrap
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from typing import Any, Protocol, Sequence


@dataclass(frozen=True)
class StylePreset:
    name: str
    visual_language: str
    palette: tuple[str, ...]
    lens: str
    aspect_ratio: str = "16:9"
    fps: int = 24


STYLE_PRESETS: dict[str, StylePreset] = {
    "cinematic": StylePreset("cinematic", "poetic cinematic realism", ("amber", "teal", "charcoal"), "anamorphic 50mm"),
    "noir": StylePreset("noir", "high-contrast neo-noir", ("black", "silver", "blood red"), "35mm spherical"),
    "documentary": StylePreset("documentary", "observational documentary", ("natural green", "warm skin", "muted blue"), "handheld 28mm"),
    "animation": StylePreset("animation", "stylized painterly animation", ("saffron", "indigo", "cream"), "virtual 35mm"),
}


@dataclass(frozen=True)
class ScenePlan:
    scene_id: str
    title: str
    duration_seconds: float
    location: str
    time_of_day: str
    action: str
    visual_intent: str
    continuity_notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class VideoPrompt:
    scene_id: str
    runway_prompt: str
    luma_prompt: str
    camera_move: str
    lighting: str
    seed: int
    negative_prompt: str = "warped anatomy, flicker, jitter, text, watermark, logo"


@dataclass(frozen=True)
class AudioPrompt:
    scene_id: str
    speech_script: str
    voice_direction: str
    emotion_tags: tuple[str, ...]
    start_seconds: float
    end_seconds: float
    sound_design: str


@dataclass(frozen=True)
class CinemaPipeline:
    brief: str
    style: StylePreset
    scenes: tuple[ScenePlan, ...]
    video_prompts: tuple[VideoPrompt, ...]
    audio_prompts: tuple[AudioPrompt, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self, *, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def to_markdown(self) -> str:
        lines = [f"# DARTRIX Cinema Storyboard", f"\n**Brief:** {self.brief}", f"**Style:** {self.style.name} — {self.style.visual_language}", ""]
        for scene, video, audio in zip(self.scenes, self.video_prompts, self.audio_prompts):
            lines += [f"## {scene.scene_id}: {scene.title}", f"**Duration:** {scene.duration_seconds:g}s | **Location:** {scene.location} | **Time:** {scene.time_of_day}", f"\n{scene.action}\n", f"**Visual intent:** {scene.visual_intent}", f"**Camera:** {video.camera_move} | **Lighting:** {video.lighting} | **Seed:** {video.seed}", f"\n**Runway:** {video.runway_prompt}\n", f"**Luma:** {video.luma_prompt}\n", f"**Voice ({', '.join(audio.emotion_tags)}):** {audio.speech_script}", f"**Sound:** {audio.sound_design}", ""]
        return "\n".join(lines)


class LLMProvider(Protocol):
    def generate(self, brief: str, style: StylePreset) -> dict[str, Any]: ...


class OpenAICompatibleProvider:
    """Minimal urllib provider for any OpenAI-compatible chat endpoint."""
    def __init__(self, endpoint: str, api_key: str, model: str = "gpt-4o-mini") -> None:
        self.endpoint, self.api_key, self.model = endpoint, api_key, model

    def generate(self, brief: str, style: StylePreset) -> dict[str, Any]:
        instruction = {"brief": brief, "style": asdict(style), "schema": "Return JSON with scenes, video_prompts, audio_prompts."}
        body = json.dumps({"model": self.model, "temperature": 0.7, "response_format": {"type": "json_object"}, "messages": [{"role": "system", "content": "You are DARTRIX, a meticulous film previsualization director."}, {"role": "user", "content": json.dumps(instruction)}]}).encode()
        request = urllib.request.Request(self.endpoint, data=body, headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.loads(response.read())
        return json.loads(payload["choices"][0]["message"]["content"])


def _mock(brief: str, style: StylePreset) -> CinemaPipeline:
    seed = sum(ord(c) for c in brief) % 1_000_000
    scene = ScenePlan("S01", "The premise", 8.0, "a liminal urban threshold", "blue hour", f"A character encounters the central idea of: {brief}.", "Establish mood, stakes, and a memorable visual motif.", ("Keep wardrobe and motif consistent",))
    video = VideoPrompt("S01", f"{style.visual_language}, {brief}, {style.lens}, slow deliberate push-in, {', '.join(style.palette)} palette", f"Cinematic shot of {brief}; tactile detail, coherent motion, {style.aspect_ratio}, {style.fps}fps", "slow push-in with a subtle arc", "soft blue-hour ambience with a warm motivated practical", seed)
    audio = AudioPrompt("S01", "Every beginning leaves a trace.", "intimate, close-mic, measured pace", ("wonder", "restrained tension"), 1.0, 4.5, "low city bed, distant metallic texture, one breath before speech")
    return CinemaPipeline(brief, style, (scene,), (video,), (audio,))


def generate(brief: str, style: str = "cinematic", provider: LLMProvider | None = None) -> CinemaPipeline:
    if not brief.strip():
        raise ValueError("brief must not be empty")
    preset = STYLE_PRESETS.get(style.lower())
    if preset is None:
        raise ValueError(f"unknown style {style!r}; choose from {', '.join(STYLE_PRESETS)}")
    if provider is None:
        return _mock(brief.strip(), preset)
    raw = provider.generate(brief.strip(), preset)
    return CinemaPipeline(brief.strip(), preset, tuple(ScenePlan(**x) for x in raw["scenes"]), tuple(VideoPrompt(**x) for x in raw["video_prompts"]), tuple(AudioPrompt(**x) for x in raw["audio_prompts"]))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a DARTRIX cinema pipeline")
    parser.add_argument("brief", help="short creative brief")
    parser.add_argument("--style", choices=sorted(STYLE_PRESETS), default="cinematic")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--output", help="write output to a file instead of stdout")
    parser.add_argument("--endpoint", help="OpenAI-compatible chat completions endpoint")
    parser.add_argument("--model", default=os.getenv("DARTRIX_MODEL", "gpt-4o-mini"))
    args = parser.parse_args(argv)
    provider = OpenAICompatibleProvider(args.endpoint, os.environ["DARTRIX_API_KEY"], args.model) if args.endpoint else None
    pipeline = generate(args.brief, args.style, provider)
    output = pipeline.to_markdown() if args.format == "markdown" else pipeline.to_json()
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(output + "\n")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

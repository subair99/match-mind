#!/usr/bin/env python3
"""Scaffold the MatchMind project (uv workspace) in the current folder.

Usage (from inside the match-mind folder):
    python scaffold.py              # create anything that is missing
    python scaffold.py --dry-run    # show what would be created
    python scaffold.py --force      # also overwrite files that already exist

Existing files are never overwritten unless --force is given. The root
pyproject.toml is only extended with a [tool.uv.workspace] table if it lacks one.
"""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path
from textwrap import dedent

YEAR = dt.date.today().year


def member_pyproject(name: str, description: str, deps: list[str], uses_kit: bool = False) -> str:
    dep_lines = "\n".join(f'    "{d}",' for d in deps)
    sources = '\n[tool.uv.sources]\nevent-timeline-kit = { workspace = true }\n' if uses_kit else ""
    return dedent(f"""\
        [project]
        name = "{name}"
        version = "0.1.0"
        description = "{description}"
        requires-python = ">=3.12"
        dependencies = [
        {dep_lines}
        ]

        [build-system]
        requires = ["hatchling"]
        build-backend = "hatchling.build"
        """) + sources


ROOT_WORKSPACE_TABLE = dedent("""\

    [tool.uv.workspace]
    members = ["packages/*", "services/*", "infra"]
    """)

ROOT_PYPROJECT = dedent("""\
    [project]
    name = "matchmind"
    version = "0.1.0"
    description = "MatchMind: every match deserves a broadcast"
    requires-python = ">=3.12"
    dependencies = []

    [dependency-groups]
    dev = ["pytest", "ruff", "httpx"]
    """) + ROOT_WORKSPACE_TABLE

FILES: dict[str, str] = {
    # ---------------------------------------------------------------- root
    ".python-version": "3.12\n",
    ".gitignore": dedent("""\
        # Python / uv
        .venv/
        __pycache__/
        *.pyc
        .pytest_cache/
        .ruff_cache/
        dist/

        # Node / Vega
        node_modules/
        apps/tv/build/

        # AWS CDK
        cdk.out/

        # NEVER commit footage or consent forms to the public repo
        footage/
        *.mp4
        *.mov
        consent/
        .env
        """),
    "LICENSE": dedent(f"""\
        MIT License

        Copyright (c) {YEAR} MatchMind contributors

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE.
        """),
    "README.md": dedent("""\
        # MatchMind

        Every match deserves a broadcast. MatchMind turns phone footage of amateur
        football into a broadcast you can ask questions on Fire TV.

        ## Tech Implementation
        ## Design
        ## Potential Impact
        ## Quality of the Idea

        ## Setup
        ```bash
        uv sync --all-packages
        uv run pytest
        ```
        """),
    "FRICTION_LOG.md": dedent("""\
        # Friction log

        Log real problems on the day they happen. Never invent entries.

        ## Template
        - **Task attempted:**
        - **Steps taken:**
        - **Expected:**
        - **What actually happened:**
        - **Severity:** Critical / High / Medium / Low
        - **Workaround used:**
        - **Actionable suggestion:**
        """),
    # ---------------------------------------------------------------- docs
    "docs/architecture.md": "# Architecture\n\nIngest once per match; one MCP server answers the TV, phone and Alexa+.\n",
    "docs/product-feedback.md": dedent("""\
        # Product feedback

        For each tool: what you used it for, what worked, what needs work,
        onboarding (zero to hello world), and whether you would build with it again.
        """),
    "docs/feature-requests.md": "# Feature requests\n\nRate each: Critical / Important / Nice-to-have.\n",
    # ---------------------------------------------------------------- data
    "data/sample/hero_match_events.json": dedent("""\
        {
          "match_id": "hero-match",
          "title": "Saturday amateur league",
          "video_uri": "s3://REPLACE-ME/hero-match.mp4",
          "events": [
            {
              "event_id": "e1",
              "t_start": 2040.0,
              "t_end": 2052.0,
              "type": "goal",
              "player": 7,
              "importance": 0.95,
              "what": "Goal, 34'",
              "why": "Opens the scoring after a run down the left.",
              "next": ["watch_build_up", "follow_player"],
              "confidence": "high"
            },
            {
              "event_id": "e2",
              "t_start": 2710.0,
              "t_end": 2718.0,
              "type": "shot",
              "player": 7,
              "importance": 0.6,
              "what": "Shot saved, 45'",
              "why": "Second chance for number 7 in ten minutes.",
              "next": ["follow_player"],
              "confidence": "medium"
            }
          ]
        }
        """),
    # ---------------------------------------------------------------- open-source kit
    "packages/event-timeline-kit/pyproject.toml": member_pyproject(
        "event-timeline-kit", "Schema, SDK and agent tools for timestamped video events", ["pydantic"]
    ),
    "packages/event-timeline-kit/README.md": "# event-timeline-kit\n\nOpen schema, SDKs and agent tools for timestamped video events. MIT licensed.\n",
    "packages/event-timeline-kit/schema/event-timeline.schema.json": dedent("""\
        {
          "$schema": "https://json-schema.org/draft/2020-12/schema",
          "title": "EventTimeline",
          "type": "object",
          "required": ["match_id", "events"],
          "properties": {
            "match_id": {"type": "string"},
            "video_uri": {"type": "string"},
            "events": {
              "type": "array",
              "items": {
                "type": "object",
                "required": ["event_id", "t_start", "t_end", "type", "importance"],
                "properties": {
                  "event_id": {"type": "string"},
                  "t_start": {"type": "number", "minimum": 0},
                  "t_end": {"type": "number", "minimum": 0},
                  "type": {"type": "string"},
                  "player": {"type": ["integer", "null"]},
                  "importance": {"type": "number", "minimum": 0, "maximum": 1},
                  "what": {"type": "string"},
                  "why": {"type": "string"},
                  "next": {"type": "array", "items": {"type": "string"}},
                  "confidence": {"enum": ["low", "medium", "high"]}
                }
              }
            }
          }
        }
        """),
    "packages/event-timeline-kit/src/event_timeline_kit/__init__.py": dedent("""\
        from .models import Event, EventTimeline
        from .tools import find_moments, player_timeline

        __all__ = ["Event", "EventTimeline", "find_moments", "player_timeline"]
        """),
    "packages/event-timeline-kit/src/event_timeline_kit/models.py": dedent("""\
        from __future__ import annotations

        from typing import Literal

        from pydantic import BaseModel, Field, model_validator


        class Event(BaseModel):
            event_id: str
            t_start: float = Field(ge=0)
            t_end: float = Field(ge=0)
            type: str
            player: int | None = None
            importance: float = Field(ge=0, le=1)
            what: str = ""
            why: str = ""
            next: list[str] = []
            confidence: Literal["low", "medium", "high"] = "medium"

            @model_validator(mode="after")
            def _check_range(self) -> "Event":
                if self.t_end < self.t_start:
                    raise ValueError("t_end must be >= t_start")
                return self


        class EventTimeline(BaseModel):
            match_id: str
            title: str = ""
            video_uri: str = ""
            events: list[Event]
        """),
    "packages/event-timeline-kit/src/event_timeline_kit/schema.py": dedent("""\
        import json
        from pathlib import Path

        from .models import EventTimeline


        def load(path: str | Path) -> EventTimeline:
            return EventTimeline.model_validate(json.loads(Path(path).read_text()))


        def dump(timeline: EventTimeline, path: str | Path) -> None:
            Path(path).write_text(timeline.model_dump_json(indent=2))
        """),
    "packages/event-timeline-kit/src/event_timeline_kit/tools.py": dedent("""\
        from .models import Event, EventTimeline


        def find_moments(tl: EventTimeline, after: float = 0.0, limit: int = 3) -> list[Event]:
            \"\"\"Most important events after a playback position (\\"What did I miss?\\").\"\"\"
            later = [e for e in tl.events if e.t_start >= after]
            return sorted(later, key=lambda e: e.importance, reverse=True)[:limit]


        def player_timeline(tl: EventTimeline, player: int) -> list[Event]:
            \"\"\"All events for one shirt number, in time order.\"\"\"
            return sorted((e for e in tl.events if e.player == player), key=lambda e: e.t_start)
        """),
    "packages/event-timeline-kit/examples/football_match.json": '{"match_id": "example", "events": []}\n',
    "packages/event-timeline-kit/examples/doorbell_camera.json": '{"match_id": "front-door-2026-10-03", "events": []}\n',
    "packages/event-timeline-kit/js/README.md": "# JS half\n\nTypeScript SDK and the Vega `MomentTimeline` component (npm). Initialise with `npm init` when ready.\n",
    "packages/event-timeline-kit/tests/test_kit_smoke.py": dedent("""\
        from pathlib import Path

        from event_timeline_kit import find_moments, player_timeline
        from event_timeline_kit.schema import load

        SAMPLE = Path(__file__).parents[3] / "data" / "sample" / "hero_match_events.json"


        def test_sample_loads_and_ranks():
            tl = load(SAMPLE)
            assert find_moments(tl)[0].type == "goal"
            assert [e.event_id for e in player_timeline(tl, 7)] == ["e1", "e2"]
        """),
    # ---------------------------------------------------------------- MCP server
    "services/mcp_server/pyproject.toml": member_pyproject(
        "matchmind-server",
        "MatchMind MCP server and Strands agent (AgentCore Runtime)",
        # Check that the installed mcp version supports protocol 2025-11-25.
        ["mcp", "strands-agents", "strands-agents-tools", "bedrock-agentcore", "boto3", "event-timeline-kit"],
        uses_kit=True,
    ),
    "services/mcp_server/src/matchmind_server/__init__.py": "",
    "services/mcp_server/src/matchmind_server/app.py": dedent("""\
        \"\"\"MatchMind MCP server over Streamable HTTP.

        Run locally:  uv run --package matchmind-server python -m matchmind_server.app
        \"\"\"
        from mcp.server.fastmcp import FastMCP

        from . import tools

        mcp = FastMCP("matchmind")


        @mcp.tool()
        def find_moments(match_id: str, after_seconds: float = 0.0, limit: int = 3) -> list[dict]:
            \"\"\"Most important moments after a playback position.\"\"\"
            return tools.find_moments(match_id, after_seconds, limit)


        @mcp.tool()
        def player_timeline(match_id: str, player: int) -> list[dict]:
            \"\"\"All moments for one shirt number, in time order.\"\"\"
            return tools.player_timeline(match_id, player)


        # TODO: explain_moment, build_reel, request_share, get_viewer_state, save_viewer_state

        if __name__ == "__main__":
            mcp.run(transport="streamable-http")
        """),
    "services/mcp_server/src/matchmind_server/tools.py": dedent("""\
        \"\"\"Tool logic. Week 1 reads the hand-made sample; Phase 4 switches to DynamoDB.\"\"\"
        from pathlib import Path

        import event_timeline_kit as kit
        from event_timeline_kit.schema import load

        SAMPLE = Path(__file__).resolve().parents[4] / "data" / "sample" / "hero_match_events.json"


        def _timeline(match_id: str) -> kit.EventTimeline:
            return load(SAMPLE)  # TODO: read from index.py (DynamoDB)


        def find_moments(match_id: str, after: float, limit: int) -> list[dict]:
            return [e.model_dump() for e in kit.find_moments(_timeline(match_id), after, limit)]


        def player_timeline(match_id: str, player: int) -> list[dict]:
            return [e.model_dump() for e in kit.player_timeline(_timeline(match_id), player)]
        """),
    "services/mcp_server/src/matchmind_server/agent.py": '"""Strands agent loop: plan, call tools, check evidence, answer. (Phase 4)"""\n',
    "services/mcp_server/src/matchmind_server/index.py": '"""DynamoDB event index access. (Phase 4)"""\n',
    "services/mcp_server/src/matchmind_server/state.py": '"""Viewer state in AgentCore Memory: who you follow, where you stopped. (Phase 4)"""\n',
    "services/mcp_server/src/matchmind_server/ui/README.md": "MCP Apps (`ui://`) cards. Build only if the Alexa+ second track is confirmed.\n",
    "services/mcp_server/skills/match-analyst/SKILL.md": dedent("""\
        ---
        name: match-analyst
        description: Answer questions about an indexed amateur football match using MatchMind tools.
        ---

        # Match analyst

        Always ground answers in indexed events and say when evidence is thin.
        """),
    "services/mcp_server/tests/test_server_smoke.py": dedent("""\
        from matchmind_server import tools


        def test_find_moments_from_sample():
            assert tools.find_moments("hero-match", 0.0, 1)[0]["type"] == "goal"
        """),
    # ---------------------------------------------------------------- ingest
    "services/ingest/pyproject.toml": member_pyproject(
        "matchmind-ingest", "Ingest pipeline tasks for Step Functions", ["boto3", "numpy", "event-timeline-kit"], uses_kit=True
    ),
    "services/ingest/Dockerfile": dedent("""\
        # Lambda container image for ingest tasks.
        # TODO: base on public.ecr.aws/lambda/python:3.12 and add a static ffmpeg binary.
        """),
    "services/ingest/src/matchmind_ingest/__init__.py": "",
    "services/ingest/src/matchmind_ingest/audio_peaks.py": '"""Find whistle and cheer peaks in the match audio. (Phase 3)"""\n\n\ndef find_peaks(audio_path: str) -> list[float]:\n    raise NotImplementedError\n',
    "services/ingest/src/matchmind_ingest/keyframes.py": '"""Extract keyframes around each audio peak with ffmpeg. (Phase 3)"""\n\n\ndef extract(video_path: str, times: list[float]) -> list[str]:\n    raise NotImplementedError\n',
    "services/ingest/src/matchmind_ingest/label.py": '"""Label candidate moments with a Bedrock vision model. (Phase 3)"""\n\n\ndef label(keyframes: list[str]) -> list[dict]:\n    raise NotImplementedError\n',
    "services/ingest/src/matchmind_ingest/explain.py": '"""Write What / Why / What-next text for confirmed events. (Phase 3)"""\n\n\ndef explain(events: list[dict]) -> list[dict]:\n    raise NotImplementedError\n',
    "services/ingest/src/matchmind_ingest/publish.py": '"""Write confirmed events to the DynamoDB index. (Phase 3)"""\n\n\ndef publish(match_id: str, events: list[dict]) -> None:\n    raise NotImplementedError\n',
    "services/ingest/tests/test_ingest_smoke.py": "import matchmind_ingest  # noqa: F401\n\n\ndef test_imports():\n    assert True\n",
    # ---------------------------------------------------------------- tagger
    "services/tagger/pyproject.toml": member_pyproject(
        "matchmind-tagger", "Web tagger for confirming events", ["fastapi", "uvicorn", "jinja2", "boto3", "event-timeline-kit"], uses_kit=True
    ),
    "services/tagger/src/matchmind_tagger/__init__.py": "",
    "services/tagger/src/matchmind_tagger/app.py": dedent("""\
        \"\"\"Run: uv run --package matchmind-tagger uvicorn matchmind_tagger.app:app --reload --port 8001\"\"\"
        from fastapi import FastAPI

        app = FastAPI(title="MatchMind tagger")


        @app.get("/health")
        def health() -> dict:
            return {"ok": True}
        """),
    "services/tagger/src/matchmind_tagger/templates/.gitkeep": "",
    "services/tagger/tests/test_tagger_smoke.py": dedent("""\
        from fastapi.testclient import TestClient

        from matchmind_tagger.app import app


        def test_health():
            assert TestClient(app).get("/health").json() == {"ok": True}
        """),
    # ---------------------------------------------------------------- companion
    "services/companion/pyproject.toml": member_pyproject(
        "matchmind-companion", "Phone voice companion (MCP client)", ["fastapi", "uvicorn", "mcp"]
    ),
    "services/companion/src/matchmind_companion/__init__.py": "",
    "services/companion/src/matchmind_companion/app.py": dedent("""\
        \"\"\"Run: uv run --package matchmind-companion uvicorn matchmind_companion.app:app --reload --port 8002\"\"\"
        from pathlib import Path

        from fastapi import FastAPI
        from fastapi.responses import HTMLResponse

        app = FastAPI(title="MatchMind companion")
        INDEX = Path(__file__).parent / "static" / "index.html"


        @app.get("/", response_class=HTMLResponse)
        def index() -> str:
            return INDEX.read_text()
        """),
    "services/companion/src/matchmind_companion/mcp_client.py": '"""Forward voice questions to the MatchMind MCP server. (Phase 5)"""\n',
    "services/companion/src/matchmind_companion/static/index.html": dedent("""\
        <!doctype html>
        <html lang="en">
        <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>MatchMind</title></head>
        <body>
          <h1>MatchMind</h1>
          <button id="talk">Hold to ask</button>
          <!-- TODO (Phase 5): browser speech input, send question to the server -->
        </body>
        </html>
        """),
    # ---------------------------------------------------------------- infra
    "infra/pyproject.toml": member_pyproject("matchmind-infra", "AWS CDK app", ["aws-cdk-lib", "constructs"]),
    "infra/src/matchmind_infra/__init__.py": "",
    "infra/app.py": dedent("""\
        \"\"\"CDK entry point. Run with: cd infra && npx cdk synth --app "uv run python app.py\\"\"\"\"
        import aws_cdk as cdk

        from matchmind_infra.stacks.storage import StorageStack

        app = cdk.App()
        StorageStack(app, "MatchMindStorage")
        # TODO: IngestStack, ApiStack, ObservabilityStack
        app.synth()
        """),
    "infra/src/matchmind_infra/stacks/__init__.py": "",
    "infra/src/matchmind_infra/stacks/storage.py": dedent("""\
        from aws_cdk import RemovalPolicy, Stack
        from aws_cdk import aws_dynamodb as ddb
        from aws_cdk import aws_s3 as s3
        from constructs import Construct


        class StorageStack(Stack):
            def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
                super().__init__(scope, construct_id, **kwargs)
                s3.Bucket(self, "Footage", removal_policy=RemovalPolicy.RETAIN)
                ddb.Table(
                    self,
                    "EventIndex",
                    partition_key=ddb.Attribute(name="match_id", type=ddb.AttributeType.STRING),
                    sort_key=ddb.Attribute(name="event_id", type=ddb.AttributeType.STRING),
                    billing_mode=ddb.BillingMode.PAY_PER_REQUEST,
                )
        """),
    "infra/src/matchmind_infra/stacks/ingest.py": '"""Step Functions + Lambda ingest stack. (Phase 3)"""\n',
    "infra/src/matchmind_infra/stacks/api.py": '"""Endpoint for the TV app. (Phase 4)"""\n',
    "infra/src/matchmind_infra/stacks/observability.py": '"""CloudWatch dashboards and the $50 billing alarm. (Phase 3)"""\n',
    # ---------------------------------------------------------------- TV app (npm, not uv)
    "apps/tv/README.md": dedent("""\
        # MatchMind TV app (Vega, React Native)

        Not managed by uv. Create it from the Vega SDK / `vega-sports-app` sample,
        then move its files into this folder. Planned layout:

        - src/screens/     Home, Match, PlayerLens, Reel
        - src/components/  MomentCard, EvidenceCard, MomentTimeline
        - src/api/         calls to the MatchMind backend
        """),
    "apps/tv/src/screens/.gitkeep": "",
    "apps/tv/src/components/.gitkeep": "",
    "apps/tv/src/api/.gitkeep": "",
    # ---------------------------------------------------------------- scripts
    "scripts/upload_match.py": '"""Upload match footage to S3 and start the ingest state machine. (Phase 3)"""\n',
    "scripts/seed_sample_events.py": '"""Load data/sample/hero_match_events.json into DynamoDB. (Phase 4)"""\n',
}


def ensure_workspace_table(root: Path, dry_run: bool) -> str:
    """Create the root pyproject, or append the workspace table if it is missing."""
    path = root / "pyproject.toml"
    if not path.exists():
        if not dry_run:
            path.write_text(ROOT_PYPROJECT)
        return "created  pyproject.toml (workspace root)"
    text = path.read_text()
    if "[tool.uv.workspace]" in text:
        return "kept     pyproject.toml (workspace table already present)"
    if not dry_run:
        path.write_text(text.rstrip() + "\n" + ROOT_WORKSPACE_TABLE)
    return "updated  pyproject.toml (added [tool.uv.workspace])"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default=".", help="project folder (default: current folder)")
    parser.add_argument("--force", action="store_true", help="overwrite existing files")
    parser.add_argument("--dry-run", action="store_true", help="print actions without writing")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    created = skipped = 0
    print(f"Scaffolding MatchMind in {root}{' (dry run)' if args.dry_run else ''}\n")
    print(ensure_workspace_table(root, args.dry_run))

    for rel, content in FILES.items():
        path = root / rel
        if path.exists() and not args.force:
            skipped += 1
            print(f"skipped  {rel} (exists)")
            continue
        if not args.dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        created += 1
        print(f"created  {rel}")

    print(f"\nDone: {created} written, {skipped} skipped.")
    print("Next: uv add --dev pytest ruff httpx   (skip if already added)")
    print("      uv sync --all-packages && uv run pytest")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate matched dark and light SVG diagrams for the profile and workflow docs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape

ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"

FONT_SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
FONT_MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"


@dataclass(frozen=True)
class Theme:
    name: str
    canvas_bg: str
    canvas_border: str
    lane_bg: str
    lane_border: str
    card_bg: str
    card_border: str
    text_primary: str
    text_secondary: str
    text_muted: str
    arrow_neutral: str
    slate_fill: str
    slate_stroke: str
    slate_pill: str
    slate_text: str
    blue_fill: str
    blue_stroke: str
    blue_pill: str
    blue_text: str
    green_fill: str
    green_stroke: str
    green_pill: str
    green_text: str
    amber_fill: str
    amber_stroke: str
    amber_pill: str
    amber_text: str
    purple_fill: str
    purple_stroke: str
    purple_pill: str
    purple_text: str
    red_fill: str
    red_stroke: str
    red_pill: str
    red_text: str


DARK = Theme(
    name="dark",
    canvas_bg="#0d1117",
    canvas_border="#30363d",
    lane_bg="#161b22",
    lane_border="#30363d",
    card_bg="#1c2128",
    card_border="#30363d",
    text_primary="#e6edf3",
    text_secondary="#9da7b3",
    text_muted="#7d8590",
    arrow_neutral="#8b949e",
    slate_fill="#1b2028",
    slate_stroke="#6e7681",
    slate_pill="#262c36",
    slate_text="#c9d1d9",
    blue_fill="#13233a",
    blue_stroke="#388bfd",
    blue_pill="#1f3a5f",
    blue_text="#79c0ff",
    green_fill="#12261e",
    green_stroke="#3fb950",
    green_pill="#1a3c29",
    green_text="#56d364",
    amber_fill="#2b2111",
    amber_stroke="#d29922",
    amber_pill="#423113",
    amber_text="#e3b341",
    purple_fill="#211936",
    purple_stroke="#a371f7",
    purple_pill="#322452",
    purple_text="#d2a8ff",
    red_fill="#2d1619",
    red_stroke="#f85149",
    red_pill="#491f24",
    red_text="#ff7b72",
)

LIGHT = Theme(
    name="light",
    canvas_bg="#ffffff",
    canvas_border="#d0d7de",
    lane_bg="#f6f8fa",
    lane_border="#d0d7de",
    card_bg="#ffffff",
    card_border="#d0d7de",
    text_primary="#1f2328",
    text_secondary="#59636e",
    text_muted="#6e7781",
    arrow_neutral="#59636e",
    slate_fill="#f3f4f6",
    slate_stroke="#6e7781",
    slate_pill="#e5e7eb",
    slate_text="#374151",
    blue_fill="#ddf4ff",
    blue_stroke="#0969da",
    blue_pill="#b6e3ff",
    blue_text="#0550ae",
    green_fill="#dafbe1",
    green_stroke="#1a7f37",
    green_pill="#aceebb",
    green_text="#116329",
    amber_fill="#fff8c5",
    amber_stroke="#9a6700",
    amber_pill="#fae17d",
    amber_text="#7d4e00",
    purple_fill="#fbefff",
    purple_stroke="#8250df",
    purple_pill="#ecd8ff",
    purple_text="#6639ba",
    red_fill="#ffebe9",
    red_stroke="#cf222e",
    red_pill="#ffcecb",
    red_text="#a40e26",
)


def role_colors(theme: Theme, role: str) -> tuple[str, str, str, str]:
    mapping = {
        "neutral": (theme.card_bg, theme.card_border, theme.lane_bg, theme.text_secondary),
        "slate": (theme.slate_fill, theme.slate_stroke, theme.slate_pill, theme.slate_text),
        "blue": (theme.blue_fill, theme.blue_stroke, theme.blue_pill, theme.blue_text),
        "green": (theme.green_fill, theme.green_stroke, theme.green_pill, theme.green_text),
        "amber": (theme.amber_fill, theme.amber_stroke, theme.amber_pill, theme.amber_text),
        "purple": (theme.purple_fill, theme.purple_stroke, theme.purple_pill, theme.purple_text),
        "red": (theme.red_fill, theme.red_stroke, theme.red_pill, theme.red_text),
    }
    return mapping[role]


def svg_header(width: int, height: int, theme: Theme, title: str) -> list[str]:
    markers = []
    for name, color in (
        ("neutral", theme.arrow_neutral),
        ("slate", theme.slate_stroke),
        ("blue", theme.blue_stroke),
        ("green", theme.green_stroke),
        ("amber", theme.amber_stroke),
        ("purple", theme.purple_stroke),
        ("red", theme.red_stroke),
    ):
        markers.append(
            f'    <marker id="arrow-{name}" viewBox="0 0 10 10" refX="8.5" refY="5" '
            f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">\n'
            f'      <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="{color}"/>\n'
            f"    </marker>"
        )

    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="100%" role="img" aria-label="{escape(title)}">',
        "  <defs>",
        *markers,
        "  </defs>",
        f'  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="14" '
        f'fill="{theme.canvas_bg}" stroke="{theme.canvas_border}" stroke-width="1.5"/>',
    ]


def add_text(
    lines: list[str],
    x: float,
    y: float,
    content: str,
    *,
    fill: str,
    size: float = 12,
    weight: str = "400",
    anchor: str = "start",
    mono: bool = False,
) -> None:
    family = FONT_MONO if mono else FONT_SANS
    lines.append(
        f'  <text x="{x}" y="{y}" fill="{fill}" font-family="{family}" '
        f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">'
        f"{escape(content)}</text>"
    )


def add_rect(
    lines: list[str],
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    fill: str,
    stroke: str,
    rx: float = 8,
    stroke_width: float = 1.25,
    dashed: bool = False,
) -> None:
    dash_attr = ' stroke-dasharray="5 4"' if dashed else ""
    lines.append(
        f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"{dash_attr}/>'
    )


def add_pill(
    lines: list[str],
    x: float,
    y: float,
    w: float,
    h: float,
    label: str,
    *,
    fill: str,
    stroke: str,
    text_fill: str,
    dot_fill: str | None = None,
    size: float = 11,
    mono: bool = False,
) -> None:
    add_rect(lines, x, y, w, h, fill=fill, stroke=stroke, rx=h / 2, stroke_width=1)
    if dot_fill:
        lines.append(
            f'  <circle cx="{x + 11}" cy="{y + h / 2}" r="3.4" fill="{dot_fill}"/>'
        )
        add_text(
            lines,
            x + 19,
            y + h / 2 + 3.8,
            label,
            fill=text_fill,
            size=size,
            weight="600",
            anchor="start",
            mono=mono,
        )
    else:
        add_text(
            lines,
            x + w / 2,
            y + h / 2 + 3.8,
            label,
            fill=text_fill,
            size=size,
            weight="600",
            anchor="middle",
            mono=mono,
        )


def add_arrow(
    lines: list[str],
    d: str,
    *,
    theme: Theme,
    role: str = "neutral",
    width: float = 1.6,
    dashed: bool = False,
) -> None:
    color = theme.arrow_neutral if role == "neutral" else role_colors(theme, role)[1]
    dash_attr = ' stroke-dasharray="5 4"' if dashed else ""
    lines.append(
        f'  <path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
        f'stroke-linecap="round" stroke-linejoin="round"{dash_attr} '
        f'marker-end="url(#arrow-{role})"/>'
    )


def add_legend(lines: list[str], theme: Theme, right_x: float, y: float) -> None:
    items = [
        ("External", "slate", 86),
        ("Doc Repo", "purple", 92),
        ("Autonomous", "green", 104),
        ("HITL Gate", "amber", 98),
        ("Fix Loop", "red", 90),
    ]
    gap = 8
    total_w = sum(w for _, _, w in items) + gap * (len(items) - 1)
    cx = right_x - total_w
    for label, role, w in items:
        fill, stroke, _, text_fill = role_colors(theme, role)
        add_pill(
            lines,
            cx,
            y,
            w,
            23,
            label,
            fill=fill,
            stroke=stroke,
            text_fill=text_fill,
            dot_fill=stroke,
            size=10.5,
        )
        cx += w + gap


def draw_header_card(
    lines: list[str],
    theme: Theme,
    x: float,
    y: float,
    w: float,
    h: float,
    title: str,
    badge: str,
    role: str,
    rows: list[tuple[str, bool]],
    footer: str | None = None,
) -> None:
    fill, stroke, pill_bg, accent = role_colors(theme, role)
    add_rect(lines, x, y, w, h, fill=theme.card_bg, stroke=stroke, rx=9, stroke_width=1.35)
    add_rect(lines, x, y, w, 30, fill=fill, stroke=stroke, rx=9, stroke_width=1.0)
    lines.append(f'  <rect x="{x + 1}" y="{y + 20}" width="{w - 2}" height="11" fill="{fill}"/>')
    lines.append(f'  <line x1="{x}" y1="{y + 30}" x2="{x + w}" y2="{y + 30}" stroke="{stroke}" stroke-width="1"/>')
    add_text(lines, x + 11, y + 20, title, fill=theme.text_primary, size=11.5, weight="700")
    bw = max(44, len(badge) * 6.5 + 14)
    add_pill(lines, x + w - bw - 8, y + 5.5, bw, 19, badge, fill=pill_bg, stroke=stroke, text_fill=accent, size=9)

    by = y + 48
    for txt, is_mono in rows:
        add_text(lines, x + 11, by, txt, fill=theme.text_secondary, size=10.5, mono=is_mono)
        by += 17

    if footer:
        lines.append(
            f'  <line x1="{x + 10}" y1="{y + h - 25}" x2="{x + w - 10}" y2="{y + h - 25}" '
            f'stroke="{theme.card_border}" stroke-width="1"/>'
        )
        add_text(lines, x + 11, y + h - 9, footer, fill=accent, size=10, weight="600")


def build_workflow_overview(theme: Theme) -> str:
    w, h = 1180, 728
    lines = svg_header(w, h, theme, "CLI-First Multi-Agent, Continuous Intake & HITL Architecture")

    # Header
    add_text(
        lines,
        28,
        40,
        "CLI-First Multi-Agent, Intake & HITL Delivery Architecture",
        fill=theme.text_primary,
        size=18.5,
        weight="700",
    )
    add_text(
        lines,
        28,
        60,
        "External sources & doc repos -> daily-briefing -> Herdr 4-tier agents -> PR/comment/CI/Discord closed loop",
        fill=theme.text_secondary,
        size=12,
    )
    add_legend(lines, theme, right_x=1152, y=26)

    # Band 1: External Sources, Doc Repos, Session Memory & Continuous Intake
    add_text(
        lines,
        28,
        84,
        "OUTSIDE-THE-LOOP SOURCES, DOC REPOS & CONTINUOUS INTAKE",
        fill=theme.text_secondary,
        size=10.5,
        weight="700",
    )
    band1_cards = [
        ("External Systems", "EXT", "slate", [
            ("Company JIRA (CBRD issues)", False),
            ("GitHub (PRs, comments, CI)", False),
            ("Discord (operator alerts)", False),
        ], "Upstream state & human feed"),
        ("Doc & Rule Repos", "REPOS", "purple", [
            ("my-cubrid-docs · jira", True),
            ("my-cubrid-schedule", True),
            ("my-cubrid-workflow (rules)", True),
        ], "Markdown drafts & specs"),
        ("Session Memory", "STATE", "blue", [
            ("work-tracker (pwd WAL)", True),
            ("Like claude-mem for tasks", False),
            ("startup | clear | compact", True),
        ], "Source of truth per cwd"),
        ("Continuous Intake", "INTAKE", "green", [
            ("daily-briefing (poller)", True),
            ("JIRA + GitHub + ledger", False),
            ("confirmed-issue-flow", True),
        ], "Feeds Herdr Commander"),
    ]
    bx = 24
    bw = 266
    bgap = 22
    by = 94
    bh = 122
    for idx, (title, badge, role, rows, footer) in enumerate(band1_cards):
        draw_header_card(lines, theme, bx, by, bw, bh, title, badge, role, rows, footer)
        if idx < len(band1_cards) - 1:
            ax1 = bx + bw + 3
            ax2 = bx + bw + bgap - 3
            add_arrow(lines, f"M {ax1} {by + bh / 2} L {ax2} {by + bh / 2}", theme=theme, role="neutral", width=1.5)
        bx += bw + bgap

    # Connectors from Band 1 down into Band 2 (Herdr Commander at x=165, Space Leaders at x=440)
    green_stroke = role_colors(theme, "green")[1]
    blue_stroke = role_colors(theme, "blue")[1]
    # Corridor y=216..256: pills sit around y=222, green route runs cleanly below at y=246
    lines.append(f'  <path d="M 1021 216 L 1021 246 L 165 246" fill="none" stroke="{green_stroke}" stroke-width="1.6"/>')
    add_arrow(lines, "M 165 246 L 165 256", theme=theme, role="green", width=1.6)
    add_pill(
        lines,
        800,
        220,
        196,
        20,
        "daily-briefing -> hcmd intake",
        fill=role_colors(theme, "green")[0],
        stroke=green_stroke,
        text_fill=role_colors(theme, "green")[3],
        size=9.5,
    )
    add_arrow(lines, "M 731 216 L 731 256", theme=theme, role="blue", width=1.5, dashed=True)
    add_pill(
        lines,
        494,
        220,
        224,
        20,
        "pwd brief (survives /clear, /compact)",
        fill=role_colors(theme, "blue")[0],
        stroke=blue_stroke,
        text_fill=role_colors(theme, "blue")[3],
        size=9.5,
    )

    # Band 2: Herdr 4-Tier Hierarchy + cubrid-workenv
    blue_fill, blue_stroke, blue_pill, blue_text = role_colors(theme, "blue")
    add_rect(lines, 24, 258, 1132, 146, fill=theme.lane_bg, stroke=blue_stroke, rx=10, stroke_width=1.25)
    add_pill(
        lines,
        40,
        269,
        250,
        22,
        "HERDR 4-TIER AGENT HIERARCHY",
        fill=blue_pill,
        stroke=blue_stroke,
        text_fill=blue_text,
        size=10,
    )
    add_text(
        lines,
        1138,
        284,
        "Single-host multi-env isolation via cubrid-workenv",
        fill=theme.text_muted,
        size=11,
        anchor="end",
    )

    herdr_cards = [
        ("Herdr Commander", "hcmd · work-tracker", "Spawns & routes Space Leaders"),
        ("Space Leaders", "tabs[0], panes[0]", "1 Space + worktree per ticket"),
        ("Tab Leaders", "tabs[1..8], panes[0]", "Scoped: build, test, review"),
        ("Pane Workers", "panes[1..3] (2x2)", "Noisy builds, testkits & logs"),
    ]
    hx = 40
    hcw = 250
    hgap = 30
    for idx, (title, sub1, sub2) in enumerate(herdr_cards):
        add_rect(lines, hx, 300, hcw, 72, fill=blue_fill, stroke=blue_stroke, rx=8, stroke_width=1.2)
        add_text(lines, hx + 14, 322, title, fill=theme.text_primary, size=13, weight="700")
        add_text(lines, hx + 14, 341, sub1, fill=blue_text, size=11, weight="600", mono=True)
        add_text(lines, hx + 14, 359, sub2, fill=theme.text_secondary, size=11)
        if idx < len(herdr_cards) - 1:
            ax1 = hx + hcw + 3
            ax2 = hx + hcw + hgap - 3
            add_arrow(lines, f"M {ax1} 336 L {ax2} 336", theme=theme, role="blue", width=1.6)
        hx += hcw + hgap

    add_text(
        lines,
        590,
        392,
        "cubrid-workenv (1 server, N envs): auto-allocates & reclaims TCP ports + SysV SHM per worktree  ·  Socket waits (no sleep)  ·  4 AI/space, 10/session",
        fill=theme.text_secondary,
        size=10.5,
        anchor="middle",
    )

    # Band 3: Closed-Loop PR, Comments, CI, Issue Escalation & Merge
    add_text(
        lines,
        28,
        423,
        "CLOSED-LOOP PR, COMMENT-FIX, CI, ISSUE ESCALATION & MERGE WORKFLOW",
        fill=theme.text_secondary,
        size=10.5,
        weight="700",
    )

    flow_cards = [
        ("1. Intake & Workenv", "SETUP", "purple", [
            ("cubrid-worktree", True),
            ("cubrid-workenv (ports/SHM)", True),
            ("work-tracker pwd brief", False),
        ], "Isolated Space on 1 host"),
        ("2. Build & Draft PR", "HITL", "amber", [
            ("cubrid-build · testkit", True),
            ("cubrid-pr-create", True),
            ("Local lint + my-cubrid-docs", False),
        ], "Gate: confirm --draft push"),
        ("3. Comments & CI", "AUTO", "green", [
            ("cubrid-pr-flow · ci-watch", True),
            ("gh-pr-comments-fetch", True),
            ("cubrid-ci · tcc · tcr", True),
        ], "Comments, CI & new-bug triage"),
        ("4. Hermes Notify", "AUTO", "green", [
            ("hermes-notify daemon", True),
            ("SQLite outbox + dedupe", False),
            ("Discord status cards", False),
        ], "Logs to work-tracker"),
        ("5. Merge & Reclaim", "HITL", "HITL" if False else "amber", [
            ("cubrid-pr-merge", True),
            ("TCs -> Gate -> Engine PR", False),
            ("cub-workenv reset", True),
        ], "Gate: --yes + reclaim SHM"),
    ]

    fx = 24
    fw = 204
    fgap = 28
    fy = 433
    fh = 122
    for idx, (title, badge, role, rows, footer) in enumerate(flow_cards):
        draw_header_card(lines, theme, fx, fy, fw, fh, title, badge, role, rows, footer)
        if idx < len(flow_cards) - 1:
            ax1 = fx + fw + 3
            ax2 = fx + fw + fgap - 3
            add_arrow(lines, f"M {ax1} {fy + fh / 2} L {ax2} {fy + fh / 2}", theme=theme, role="neutral", width=1.6)
        fx += fw + fgap

    # Feedback & Escalation paths below the 5 cards (y=555..628)
    green_fill, green_stroke, _, green_text = role_colors(theme, "green")
    red_fill, red_stroke, _, red_text = role_colors(theme, "red")
    amber_fill, amber_stroke, _, amber_text = role_colors(theme, "amber")
    purple_fill, purple_stroke, _, purple_text = role_colors(theme, "purple")

    # Green self-loop on Card 3 (known flake: 1x rerun)
    add_arrow(lines, "M 616 555 L 616 579 L 558 579 L 558 557", theme=theme, role="green", width=1.5)
    add_pill(
        lines,
        518,
        568,
        138,
        21,
        "known flake: 1x rerun",
        fill=green_fill,
        stroke=green_stroke,
        text_fill=green_text,
        size=9.5,
    )

    # Red return loop: Card 3 (x=506) -> Card 2 (x=358) for PR comments or defect
    add_arrow(lines, "M 506 555 L 506 610 L 358 610 L 358 557", theme=theme, role="red", width=1.6, dashed=True)
    add_pill(
        lines,
        286,
        599,
        244,
        22,
        "PR comments / defect -> fix in Tab 1",
        fill=red_fill,
        stroke=red_stroke,
        text_fill=red_text,
        size=9.5,
    )

    # Purple/Amber issue escalation callout from Card 3 right-bottom (x=672) into pill top (599)
    add_arrow(lines, "M 672 555 L 672 597", theme=theme, role="purple", width=1.5, dashed=True)
    add_pill(
        lines,
        554,
        599,
        250,
        22,
        "New bug? HITL: File? -> Company JIRA",
        fill=purple_fill,
        stroke=purple_stroke,
        text_fill=purple_text,
        size=9.5,
    )

    # Amber human decision arrow: Card 4 (822) -> Card 5 (1054)
    add_arrow(lines, "M 822 555 L 822 592 L 1054 592 L 1054 557", theme=theme, role="amber", width=1.6)
    add_pill(
        lines,
        838,
        581,
        200,
        22,
        "Discord alert -> Human gate",
        fill=amber_fill,
        stroke=amber_stroke,
        text_fill=amber_text,
        size=9.5,
    )

    # Band 4: my-cubrid-workflow foundation
    add_rect(lines, 24, 634, 1132, 74, fill=theme.lane_bg, stroke=purple_stroke, rx=10, stroke_width=1.25)
    add_pill(
        lines,
        40,
        644,
        344,
        20,
        "my-cubrid-workflow  ·  RULE-DRIVEN AUTOMATION",
        fill=purple_pill_bg(theme),
        stroke=purple_stroke,
        text_fill=purple_text,
        size=10,
    )

    steps = [
        (40, 180, "rules/*.md (work habits)"),
        (244, 206, "sync-lock.toml (just drift)"),
        (474, 224, "check · test · run · sync"),
    ]
    for idx, (sx, sw, slabel) in enumerate(steps):
        add_rect(lines, sx, 672, sw, 25, fill=purple_fill, stroke=purple_stroke, rx=6, stroke_width=1)
        add_text(lines, sx + sw / 2, 688.5, slabel, fill=theme.text_primary, size=10.5, weight="600", anchor="middle", mono=True)
        if idx < len(steps) - 1:
            next_x = steps[idx + 1][0]
            add_arrow(lines, f"M {sx + sw + 3} 684.5 L {next_x - 3} 684.5", theme=theme, role="purple", width=1.4)

    add_rect(lines, 724, 644, 414, 54, fill=theme.card_bg, stroke=theme.card_border, rx=8, stroke_width=1)
    add_text(lines, 738, 664, "Tiered Git Integration Policy", fill=theme.text_primary, size=11.5, weight="700")
    add_text(
        lines,
        738,
        684,
        "Tier 1: solo repos (auto ff-merge)   ·   Tier 2: CUBRID/* (HITL gate)",
        fill=theme.text_secondary,
        size=10.5,
    )

    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def purple_pill_bg(theme: Theme) -> str:
    return theme.purple_pill


def build_intake_and_layers(theme: Theme) -> str:
    w, h = 1180, 578
    lines = svg_header(w, h, theme, "System Layers and Continuous Intake Architecture")

    add_text(
        lines,
        28,
        40,
        "System Layers & Continuous Intake Architecture",
        fill=theme.text_primary,
        size=18.5,
        weight="700",
    )
    add_text(
        lines,
        28,
        60,
        "Separating external systems, document repos, local feature CLIs, and background daemons",
        fill=theme.text_secondary,
        size=12,
    )

    cols = [
        (24, "EXTERNAL SYSTEMS", "slate"),
        (310, "DOC & RULE REPOS", "purple"),
        (596, "FEATURE CLIs & STATE", "blue"),
        (882, "BACKGROUND DAEMONS", "green"),
    ]
    cw = 274
    cy = 78
    ch = 376

    for cx, label, role in cols:
        fill, stroke, pill_bg, accent = role_colors(theme, role)
        add_rect(lines, cx, cy, cw, ch, fill=theme.lane_bg, stroke=stroke, rx=10, stroke_width=1.25)
        add_pill(lines, cx + 14, cy + 12, cw - 28, 22, label, fill=pill_bg, stroke=stroke, text_fill=accent, size=10)

    # Col 1 cards (External Systems)
    col1_cards = [
        ("Company JIRA", ["Assigned Confirmed / Develop", "Triage & transition gates", "New bug filings (after HITL)"]),
        ("GitHub", ["Pull requests & draft carriers", "Inline & top-level comments", "gha-ci Actions & Merge Gate"]),
        ("Discord", ["Early failure & pass/fail cards", "Review & merge-ready notices", "Direct Actions Run URLs"]),
    ]
    y = 124
    for title, bullets in col1_cards:
        add_rect(lines, 38, y, cw - 28, 98, fill=theme.card_bg, stroke=theme.card_border, rx=8, stroke_width=1.15)
        add_text(lines, 52, y + 23, title, fill=theme.text_primary, size=12.5, weight="700")
        by = y + 44
        for b in bullets:
            add_text(lines, 52, by, b, fill=theme.text_secondary, size=10.5)
            by += 17
        y += 110

    # Col 2 cards (Doc & Rule Repos)
    col2_cards = [
        ("my-cubrid-docs", "PR bodies, CI reports, ADRs"),
        ("my-cubrid-jira", "Markdown issues pushed before JIRA"),
        ("my-cubrid-schedule", "Daily & weekly planning sheets"),
        ("my-cubrid-workflow", "rules/*.md + sync-lock.toml"),
    ]
    y = 124
    for title, desc in col2_cards:
        add_rect(lines, 324, y, cw - 28, 72, fill=theme.card_bg, stroke=role_colors(theme, "purple")[1], rx=8, stroke_width=1.15)
        add_text(lines, 338, y + 25, title, fill=role_colors(theme, "purple")[3], size=12, weight="700", mono=True)
        add_text(lines, 338, y + 48, desc, fill=theme.text_secondary, size=10.5)
        y += 82

    # Col 3 cards (Feature CLIs & Local State)
    blue_fill, blue_stroke, _, blue_text = role_colors(theme, "blue")
    add_rect(lines, 610, 124, cw - 28, 108, fill=blue_fill, stroke=blue_stroke, rx=8, stroke_width=1.45)
    add_text(lines, 624, 146, "work-tracker", fill=theme.text_primary, size=12.5, weight="700", mono=True)
    add_text(lines, 624, 165, "pwd-scoped SQLite WAL memory", fill=blue_text, size=10.5, weight="600")
    add_text(lines, 624, 183, "Like claude-mem: brief & hook", fill=theme.text_secondary, size=10.5)
    add_text(lines, 624, 200, "Survives startup | clear | compact", fill=theme.text_secondary, size=10.5)
    add_text(lines, 624, 217, "Source of truth per workdir", fill=blue_text, size=10, mono=True)

    add_rect(lines, 610, 242, cw - 28, 108, fill=blue_fill, stroke=blue_stroke, rx=8, stroke_width=1.45)
    add_text(lines, 624, 264, "cubrid-workenv", fill=theme.text_primary, size=12.5, weight="700", mono=True)
    add_text(lines, 624, 283, "N isolated CUBRID envs on 1 host", fill=blue_text, size=10.5, weight="600")
    add_text(lines, 624, 301, "Auto-allocates & reclaims TCP", fill=theme.text_secondary, size=10.5)
    add_text(lines, 624, 318, "ports, SysV SHM keys & sockets", fill=theme.text_secondary, size=10.5)
    add_text(lines, 624, 335, "Separate DBs & install prefixes", fill=blue_text, size=10, mono=True)

    add_rect(lines, 610, 360, cw - 28, 80, fill=theme.card_bg, stroke=theme.card_border, rx=8, stroke_width=1.15)
    add_text(lines, 624, 382, "Domain CLIs", fill=theme.text_primary, size=12, weight="700")
    add_text(lines, 624, 401, "worktree · jira · dup · xref", fill=theme.text_secondary, size=10.5, mono=True)
    add_text(lines, 624, 419, "cubrid-ci · tcc · tcr · comments", fill=theme.text_secondary, size=10.5, mono=True)

    # Col 4 cards (Background Daemons)
    col4_cards = [
        ("daily-briefing", "Pulls JIRA + GitHub + ledger + hcmd"),
        ("cubrid-pr-flow", "Parallel review, comments & CI gate"),
        ("cubrid-ci-watch", "Read-only SQLite gha-ci event ledger"),
        ("hermes-notify", "Outbox + dedupe -> Discord + tracker"),
    ]
    y = 124
    green_stroke = role_colors(theme, "green")[1]
    green_text = role_colors(theme, "green")[3]
    for title, desc in col4_cards:
        add_rect(lines, 896, y, cw - 28, 72, fill=theme.card_bg, stroke=green_stroke, rx=8, stroke_width=1.15)
        add_text(lines, 910, y + 25, title, fill=green_text, size=12, weight="700", mono=True)
        add_text(lines, 910, y + 48, desc, fill=theme.text_secondary, size=10.5)
        y += 82

    # Bottom Continuous Intake Ribbon
    add_rect(lines, 24, 472, 1132, 84, fill=theme.lane_bg, stroke=blue_stroke, rx=10, stroke_width=1.25)
    add_pill(
        lines,
        40,
        482,
        290,
        20,
        "CONTINUOUS INTAKE & SESSION HANDOFF",
        fill=role_colors(theme, "blue")[2],
        stroke=blue_stroke,
        text_fill=blue_text,
        size=9.5,
    )

    ribbon = [
        (40, 214, "JIRA + GitHub + tracker"),
        (276, 198, "daily-briefing (sync)"),
        (496, 198, "confirmed-issue-flow"),
        (716, 198, "Herdr Commander (hcmd)"),
        (936, 204, "Space Leader (tabs[0])"),
    ]
    for idx, (rx, rw, rlabel) in enumerate(ribbon):
        rfill = blue_fill if idx >= 3 else theme.card_bg
        rstroke = blue_stroke if idx >= 2 else theme.card_border
        add_rect(lines, rx, 512, rw, 30, fill=rfill, stroke=rstroke, rx=7, stroke_width=1.15)
        add_text(lines, rx + rw / 2, 531, rlabel, fill=theme.text_primary, size=10.5, weight="600", anchor="middle")
        if idx < len(ribbon) - 1:
            nx = ribbon[idx + 1][0]
            add_arrow(lines, f"M {rx + rw + 2} 527 L {nx - 2} 527", theme=theme, role="blue", width=1.5)

    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def build_herdr_hierarchy(theme: Theme) -> str:
    w, h = 1120, 602
    lines = svg_header(w, h, theme, "Herdr 4-Tier Agent Hierarchy")

    add_text(lines, 28, 40, "Herdr 4-Tier Agent Hierarchy", fill=theme.text_primary, size=18.5, weight="700")
    add_text(
        lines,
        28,
        60,
        "Continuous intake feeds isolated Spaces while keeping orchestrator context lean",
        fill=theme.text_secondary,
        size=12,
    )

    blue_fill, blue_stroke, blue_pill, blue_text = role_colors(theme, "blue")
    purple_fill, purple_stroke, _, purple_text = role_colors(theme, "purple")
    green_fill, green_stroke, _, green_text = role_colors(theme, "green")

    # Top Intake Ribbon feeding Tier 0
    add_rect(lines, 28, 76, 768, 52, fill=theme.lane_bg, stroke=green_stroke, rx=8, stroke_width=1.2)
    add_pill(lines, 40, 91, 96, 22, "INTAKE", fill=role_colors(theme, "green")[2], stroke=green_stroke, text_fill=green_text, size=9.5)
    add_text(
        lines,
        148,
        99,
        "daily-briefing pulls Company JIRA + GitHub + work-tracker (in_herdr check)",
        fill=theme.text_primary,
        size=11,
        weight="600",
    )
    add_text(
        lines,
        148,
        117,
        "confirmed-issue-flow hands ready CBRD tickets to Herdr Commander -> spawns Space Leader",
        fill=theme.text_secondary,
        size=10.5,
    )
    add_arrow(lines, "M 412 128 L 412 148", theme=theme, role="green", width=1.6)

    # Tree orthogonal connectors (shifted +68px vertically)
    lines.append(f'  <path d="M 412 220 L 412 238 M 140 238 L 684 238" fill="none" stroke="{blue_stroke}" stroke-width="1.5"/>')
    for cx in (140, 412, 684):
        add_arrow(lines, f"M {cx} 238 L {cx} 254", theme=theme, role="blue", width=1.5)

    lines.append(f'  <path d="M 412 332 L 412 350 M 140 350 L 684 350" fill="none" stroke="{blue_stroke}" stroke-width="1.5"/>')
    for cx in (140, 412, 684):
        add_arrow(lines, f"M {cx} 350 L {cx} 366", theme=theme, role="blue", width=1.5)

    lines.append(f'  <path d="M 412 444 L 412 462 M 140 462 L 684 462" fill="none" stroke="{purple_stroke}" stroke-width="1.5"/>')
    for cx in (140, 412, 684):
        add_arrow(lines, f"M {cx} 462 L {cx} 478", theme=theme, role="purple", width=1.5)

    # Tier 0: Herdr Commander
    add_rect(lines, 166, 150, 492, 70, fill=blue_fill, stroke=blue_stroke, rx=9, stroke_width=1.6)
    add_pill(lines, 180, 161, 56, 19, "TIER 0", fill=blue_pill, stroke=blue_stroke, text_fill=blue_text, size=9.5)
    add_text(lines, 246, 175, "Herdr Commander (hcmd)", fill=theme.text_primary, size=13.5, weight="700")
    add_text(
        lines,
        180,
        195,
        "Spawns & routes Space Leaders  ·  hcmd status / find / peek / wait",
        fill=theme.text_secondary,
        size=11,
    )
    add_text(
        lines,
        180,
        211,
        "Reads work-tracker pwd memory & correlates open ticket state",
        fill=blue_text,
        size=10.5,
        mono=True,
    )

    # Tier 1: Spaces
    spaces = [
        (28, 224, False, "Space A: Feature", "tabs[0], panes[0]", "workenv: ports & SHM A"),
        (280, 264, True, "Space B: Ticket", "tabs[0], panes[0]", "workenv B · work-tracker pwd"),
        (572, 224, False, "Space C: PR Review", "tabs[0], panes[0]", "Review checkout · read-only"),
    ]
    for sx, sw, active, title, loc, desc in spaces:
        fill = blue_fill if active else theme.card_bg
        stroke = blue_stroke if active else theme.card_border
        swidth = 1.8 if active else 1.2
        add_rect(lines, sx, 256, sw, 76, fill=fill, stroke=stroke, rx=8, stroke_width=swidth)
        add_pill(lines, sx + 12, 266, 52, 18, "TIER 1", fill=blue_pill if active else theme.lane_bg, stroke=stroke, text_fill=blue_text if active else theme.text_muted, size=9)
        if active:
            add_pill(lines, sx + sw - 64, 266, 52, 18, "ACTIVE", fill=green_fill, stroke=green_stroke, text_fill=green_text, size=9)
        add_text(lines, sx + 72, 279, title, fill=theme.text_primary, size=12.5, weight="700")
        add_text(lines, sx + 12, 301, loc, fill=blue_text, size=11, weight="600", mono=True)
        add_text(lines, sx + 12, 319, desc, fill=theme.text_secondary, size=10.5)

    # Tier 2: Tabs under Space B
    tabs = [
        (28, 224, False, "Tab 1: fix / review", "panes[0] · Tab Leader", "Handles fix_in_herdr & comments"),
        (280, 264, True, "Tab 2: test", "panes[0] · Tab Leader", "Splits up to 3 worker panes"),
        (572, 224, False, "Tab 3: build", "--launcher shell", "Unrestricted compile & logs"),
    ]
    for tx, tw, active, title, loc, desc in tabs:
        fill = blue_fill if active else theme.card_bg
        stroke = blue_stroke if active else theme.card_border
        swidth = 1.8 if active else 1.2
        add_rect(lines, tx, 368, tw, 76, fill=fill, stroke=stroke, rx=8, stroke_width=swidth)
        add_pill(lines, tx + 12, 378, 52, 18, "TIER 2", fill=blue_pill if active else theme.lane_bg, stroke=stroke, text_fill=blue_text if active else theme.text_muted, size=9)
        if active:
            add_pill(lines, tx + tw - 64, 378, 52, 18, "ACTIVE", fill=green_fill, stroke=green_stroke, text_fill=green_text, size=9)
        add_text(lines, tx + 72, 391, title, fill=theme.text_primary, size=12, weight="700")
        add_text(lines, tx + 12, 413, loc, fill=blue_text, size=11, weight="600", mono=True)
        add_text(lines, tx + 12, 431, desc, fill=theme.text_secondary, size=10.5)

    # Tier 3: Leaf Worker Panes under Tab 2
    panes = [
        (28, 224, "Pane 1 (panes[1])", "Focused testkit run"),
        (280, 264, "Pane 2 (panes[2])", "Log & core-dump triage"),
        (572, 224, "Pane 3 (panes[3])", "Isolated repro / tail"),
    ]
    for px, pw, title, desc in panes:
        add_rect(lines, px, 480, pw, 68, fill=purple_fill, stroke=purple_stroke, rx=8, stroke_width=1.2)
        add_pill(lines, px + 12, 490, 52, 18, "TIER 3", fill=theme.card_bg, stroke=purple_stroke, text_fill=purple_text, size=9)
        add_text(lines, px + 72, 503, title, fill=theme.text_primary, size=12, weight="700")
        add_text(lines, px + 12, 529, desc, fill=theme.text_secondary, size=11)

    add_text(
        lines,
        412,
        573,
        "Leaf Workers (panes[1..3], 2x2 grid) execute assigned commands only — never create tabs or split panes.",
        fill=theme.text_muted,
        size=11,
        anchor="middle",
    )

    # Right Guardrails Panel
    add_rect(lines, 820, 76, 276, 500, fill=theme.lane_bg, stroke=theme.lane_border, rx=10, stroke_width=1.25)
    add_text(lines, 836, 102, "Operating Guardrails", fill=theme.text_primary, size=14, weight="700")
    add_text(lines, 836, 119, "Isolation & continuity guarantees", fill=theme.text_muted, size=11)

    guardrails = [
        ("Session Memory (pwd)", "blue", "work-tracker brief survives", "fresh starts, /clear & /compact."),
        ("Single-Host Isolation", "purple", "cubrid-workenv assigns & reclaims", "TCP ports + SysV SHM per Space."),
        ("Quota Caps", "amber", "Max 8 sub-tabs/space ·", "4 worker AIs/space · 10 total."),
        ("Event-Driven Waits", "green", "Socket waits (hcmd wait),", "never sleep polling loops."),
        ("Single Writer", "red", "1 mutating agent per worktree;", "respect AGENT_BLOCKED."),
        ("Clean Teardown", "neutral", "Close worker tabs; reclaim env", "resources on worktree delete."),
    ]
    gy = 132
    for title, role, line1, line2 in guardrails:
        _, stroke, _, accent = role_colors(theme, role)
        add_rect(lines, 834, gy, 248, 64, fill=theme.card_bg, stroke=theme.card_border, rx=8, stroke_width=1.1)
        lines.append(
            f'  <rect x="834" y="{gy + 8}" width="4" height="48" rx="2" fill="{stroke}"/>'
        )
        add_text(lines, 848, gy + 21, title, fill=accent if role != "neutral" else theme.text_primary, size=11.5, weight="700")
        add_text(lines, 848, gy + 38, line1, fill=theme.text_secondary, size=10.5)
        add_text(lines, 848, gy + 53, line2, fill=theme.text_secondary, size=10.5)
        gy += 73

    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def draw_swimlane_card(
    lines: list[str],
    theme: Theme,
    x: float,
    y: float,
    w: float,
    h: float,
    code: str,
    title: str,
    role: str,
    body: list[str],
) -> None:
    fill, stroke, pill_bg, accent = role_colors(theme, role)
    add_rect(lines, x, y, w, h, fill=theme.card_bg, stroke=stroke, rx=8, stroke_width=1.35)
    add_rect(lines, x, y, w, 28, fill=fill, stroke=stroke, rx=8, stroke_width=1.0)
    lines.append(f'  <rect x="{x + 1}" y="{y + 18}" width="{w - 2}" height="11" fill="{fill}"/>')
    lines.append(f'  <line x1="{x}" y1="{y + 28}" x2="{x + w}" y2="{y + 28}" stroke="{stroke}" stroke-width="1"/>')
    add_pill(lines, x + 8, y + 5, 26, 18, code, fill=pill_bg, stroke=stroke, text_fill=accent, size=9, mono=True)
    add_text(lines, x + 40, y + 18, title, fill=theme.text_primary, size=11, weight="700")
    by = y + 46
    for row in body:
        add_text(lines, x + 10, by, row, fill=theme.text_secondary, size=10.2)
        by += 17


def build_pr_ci_hitl_loop(theme: Theme) -> str:
    w, h = 1200, 738
    lines = svg_header(w, h, theme, "Closed-Loop Delivery: Intake, PR Comments, CI, Issue Escalation, Discord, and HITL")

    add_text(
        lines,
        28,
        40,
        "Closed-Loop Delivery: Intake, Comment-Fix, CI, Issue Escalation & HITL",
        fill=theme.text_primary,
        size=18.5,
        weight="700",
    )
    add_text(
        lines,
        28,
        60,
        "External JIRA/GitHub/Discord feeds paired with autonomous triage and explicit human gates",
        fill=theme.text_secondary,
        size=12,
    )
    add_legend(lines, theme, right_x=1172, y=26)

    slate_fill, slate_stroke, slate_pill, slate_text = role_colors(theme, "slate")
    amber_fill, amber_stroke, amber_pill, amber_text = role_colors(theme, "amber")
    green_fill, green_stroke, green_pill, green_text = role_colors(theme, "green")
    blue_fill, blue_stroke, blue_pill, blue_text = role_colors(theme, "blue")
    purple_fill, purple_stroke, _, purple_text = role_colors(theme, "purple")
    red_fill, red_stroke, _, red_text = role_colors(theme, "red")

    # External Strip (y=76..132)
    ext_boxes = [
        (42, 366, "Company JIRA", "Assigned Confirmed/Develop · Issue filing · Resolved"),
        (432, 348, "GitHub (CUBRID)", "Draft/Open PRs · Review comments · gha-ci + Gate"),
        (800, 348, "Discord (via Hermes)", "CI alerts · Comment notices · Merge-ready cards"),
    ]
    for ex, ew, etitle, esub in ext_boxes:
        add_rect(lines, ex, 76, ew, 56, fill=slate_fill, stroke=slate_stroke, rx=9, stroke_width=1.25)
        add_pill(lines, ex + 12, 85, 68, 17, "EXTERNAL", fill=slate_pill, stroke=slate_stroke, text_fill=slate_text, size=8.5)
        add_text(lines, ex + 88, 98, etitle, fill=theme.text_primary, size=12, weight="700")
        add_text(lines, ex + 12, 119, esub, fill=theme.text_secondary, size=10.5)

    # Swimlane 1: HITL Gates (y=152..300)
    add_rect(lines, 24, 152, 1152, 148, fill=theme.lane_bg, stroke=amber_stroke, rx=10, stroke_width=1.2)
    add_pill(lines, 64, 161, 174, 20, "HUMAN-IN-THE-LOOP GATES", fill=amber_pill, stroke=amber_stroke, text_fill=amber_text, size=9)

    # Swimlane 2: Autonomous Daemons (y=316..518)
    add_rect(lines, 24, 316, 1152, 202, fill=theme.lane_bg, stroke=green_stroke, rx=10, stroke_width=1.2)
    add_pill(lines, 64, 326, 228, 20, "AUTONOMOUS DAEMONS · systemd --user", fill=green_pill, stroke=green_stroke, text_fill=green_text, size=9)

    # Swimlane 3: Herdr Space & Local Skills (y=534..714)
    add_rect(lines, 24, 534, 1152, 180, fill=theme.lane_bg, stroke=blue_stroke, rx=10, stroke_width=1.2)
    add_pill(lines, 64, 544, 238, 20, "HERDR SPACE & CLIs · my-cubrid-skills", fill=blue_pill, stroke=blue_stroke, text_fill=blue_text, size=9)

    # 6 Columns starting at x=64 (leaving x=42 as clean vertical intake corridor):
    # C1=64 (64..228), C2=248 (248..412, mid 330), C3=432 (432..596, mid 514),
    # C4=616 (616..780, mid 698), C5=800 (800..964, mid 882), C6=984 (984..1148, mid 1066)
    cols = [64, 248, 432, 616, 800, 984]
    cw = 164

    # Lane 1 cards (y=194, h=90)
    draw_swimlane_card(
        lines, theme, cols[1], 194, cw, 90, "H1", "Confirm Draft PR", "amber",
        ["Review draft & lint", "Approve remote push", "Open --draft PR"],
    )
    draw_swimlane_card(
        lines, theme, cols[3], 194, cw, 90, "H2", "File Issue? (HITL)", "purple",
        ["New bug? Ask human", "cubrid-jira-dup check", "my-cubrid-jira -> JIRA"],
    )
    draw_swimlane_card(
        lines, theme, cols[4], 194, cw, 90, "H3", "Discord Triage", "amber",
        ["Inspect alert & URL", "Evaluate review notes", "Steer fix or merge"],
    )
    draw_swimlane_card(
        lines, theme, cols[5], 194, cw, 90, "H4", "Approve Merge", "amber",
        ["Run cubrid-pr-merge", "Check plan & msg lint", "Confirm --yes execute"],
    )

    # Lane 2 cards (y=366, h=100)
    draw_swimlane_card(
        lines, theme, cols[2], 366, cw, 100, "D1", "cubrid-pr-flow", "green",
        ["Parallel review + CI", "Watch PR comments", "AND-Join state gate"],
    )
    draw_swimlane_card(
        lines, theme, cols[3], 366, cw, 100, "D2", "ci-watch + Triage", "green",
        ["SQLite run ledger", "cubrid-ci · tcc · tcr", "Flake, fix, or new bug"],
    )
    draw_swimlane_card(
        lines, theme, cols[4], 366, cw, 100, "D3", "hermes-notify", "green",
        ["SQLite outbox + dedupe", "Discord kind routing", "Logs to work-tracker"],
    )
    draw_swimlane_card(
        lines, theme, cols[5], 366, cw, 100, "D4", "merge-handoff", "green",
        ["Ownership + threads", "Dual approval + lint", "TCs -> Gate -> Engine"],
    )

    # Lane 3 cards (y=582, h=106)
    draw_swimlane_card(
        lines, theme, cols[0], 582, cw, 106, "S1", "Intake & Workenv", "purple",
        ["daily-briefing -> hcmd", "worktree + workenv", "ports/SHM + tracker pwd"],
    )
    draw_swimlane_card(
        lines, theme, cols[1], 582, cw, 106, "S2", "Build & Draft", "blue",
        ["Neovim + AI agents", "build · testkit-run", "cubrid-pr-create"],
    )
    draw_swimlane_card(
        lines, theme, cols[3], 582, cw, 106, "S3", "Comment/Fix Loop", "red",
        ["gh-pr-comments-fetch", "Review, patch & test", "Reply, resolve, push"],
    )
    draw_swimlane_card(
        lines, theme, cols[5], 582, cw, 106, "S4", "Cleanup & Reclaim", "purple",
        ["cleanup --apply", "Close work-tracker", "Reclaim SHM/ports + JIRA"],
    )

    # Connectors (100% non-overlapping)
    # Company JIRA -> S1 intake along left corridor x=44
    add_arrow(lines, "M 44 132 L 44 635 L 62 635", theme=theme, role="slate", width=1.6)

    # GitHub -> D1 / D2 along gutter x=606 (between C3=596 and C4=616)
    lines.append(f'  <path d="M 606 132 L 606 350" fill="none" stroke="{slate_stroke}" stroke-width="1.4" stroke-dasharray="4 3"/>')
    add_arrow(lines, "M 606 350 L 566 350 L 566 364", theme=theme, role="slate", width=1.4)
    add_arrow(lines, "M 606 350 L 636 350 L 636 364", theme=theme, role="slate", width=1.4)

    # S1 -> S2
    add_arrow(lines, f"M {cols[0] + cw} 635 L {cols[1] - 2} 635", theme=theme, role="purple", width=1.6)

    # S2 -> H1 (straight UP at c2_mid=330, clears L2 pill<=292 and L3 pill<=302)
    c2_mid = cols[1] + cw / 2
    add_arrow(lines, f"M {c2_mid} 582 L {c2_mid} 286", theme=theme, role="amber", width=1.7)
    add_pill(lines, c2_mid - 54, 404, 108, 21, "local draft ready", fill=amber_fill, stroke=amber_stroke, text_fill=amber_text, size=9.5)

    # H1 -> D1
    c3_mid = cols[2] + cw / 2
    add_arrow(lines, f"M {cols[1] + cw} 239 L {c3_mid} 239 L {c3_mid} 364", theme=theme, role="green", width=1.7)
    add_pill(lines, c3_mid - 46, 228, 92, 21, "draft PR out", fill=green_fill, stroke=green_stroke, text_fill=green_text, size=9.5)

    # D1 -> D2 -> D3
    add_arrow(lines, f"M {cols[2] + cw} 416 L {cols[3] - 2} 416", theme=theme, role="green", width=1.6)
    add_arrow(lines, f"M {cols[3] + cw} 416 L {cols[4] - 2} 416", theme=theme, role="green", width=1.6)

    # D2 self-loop on top-right (1x rerun), spaced cleanly from D2 -> H2 at x=650
    add_arrow(lines, "M 762 366 L 762 338 L 722 338 L 722 364", theme=theme, role="green", width=1.5)
    add_pill(lines, 698, 320, 90, 20, "1x flake rerun", fill=green_fill, stroke=green_stroke, text_fill=green_text, size=9)

    # D2 -> H2 (Issue escalation: new bug? -> ask human -> Company JIRA)
    add_arrow(lines, "M 650 366 L 650 286", theme=theme, role="purple", width=1.6, dashed=True)
    add_pill(lines, 613, 319, 76, 20, "new bug?", fill=purple_fill, stroke=purple_stroke, text_fill=purple_text, size=9)
    c4_mid = cols[3] + cw / 2
    add_arrow(lines, f"M {c4_mid} 194 L {c4_mid} 165 L 284 165 L 284 134", theme=theme, role="purple", width=1.6)
    add_pill(lines, 424, 155, 138, 20, "publish to Company JIRA", fill=purple_fill, stroke=purple_stroke, text_fill=purple_text, size=9)

    # D2 -> S3 (Comment/defect fix loop)
    add_arrow(lines, f"M {c4_mid} 466 L {c4_mid} 580", theme=theme, role="red", width=1.7, dashed=True)
    add_pill(lines, c4_mid - 64, 482, 128, 21, "comments / PR defect", fill=red_fill, stroke=red_stroke, text_fill=red_text, size=9.5)

    # S3 -> S2 (new HEAD -> re-verify)
    add_arrow(lines, f"M {cols[3]} 635 L {cols[1] + cw + 2} 635", theme=theme, role="red", width=1.7, dashed=True)
    add_pill(lines, c3_mid - 64, 624, 128, 21, "new HEAD -> re-verify", fill=red_fill, stroke=red_stroke, text_fill=red_text, size=9.5)

    # D3 -> H3 via Discord
    c5_mid = cols[4] + cw / 2
    add_arrow(lines, f"M {c5_mid} 366 L {c5_mid} 286", theme=theme, role="amber", width=1.7)
    add_pill(lines, c5_mid - 48, 322, 96, 20, "via Discord", fill=amber_fill, stroke=amber_stroke, text_fill=amber_text, size=9.5)
    add_arrow(lines, f"M {c5_mid} 194 L {c5_mid} 134", theme=theme, role="slate", width=1.4, dashed=True)

    # H3 -> H4 -> D4 -> S4
    add_arrow(lines, f"M {cols[4] + cw} 239 L {cols[5] - 2} 239", theme=theme, role="amber", width=1.7)
    c6_mid = cols[5] + cw / 2
    add_arrow(lines, f"M {c6_mid} 284 L {c6_mid} 364", theme=theme, role="green", width=1.7)
    add_arrow(lines, f"M {c6_mid} 466 L {c6_mid} 580", theme=theme, role="purple", width=1.7)

    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        "workflow-overview": build_workflow_overview,
        "intake-and-layers": build_intake_and_layers,
        "herdr-hierarchy": build_herdr_hierarchy,
        "pr-ci-hitl-loop": build_pr_ci_hitl_loop,
    }
    for stem, builder in outputs.items():
        for theme in (DARK, LIGHT):
            target = ASSETS_DIR / f"{stem}-{theme.name}.svg"
            target.write_text(builder(theme), encoding="utf-8")
            print(f"Wrote {target}")


if __name__ == "__main__":
    main()

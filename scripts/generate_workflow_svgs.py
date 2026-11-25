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
            f'  <circle cx="{x + 12}" cy="{y + h / 2}" r="3.5" fill="{dot_fill}"/>'
        )
        add_text(
            lines,
            x + 21,
            y + h / 2 + 4,
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
        ("Autonomous", "green", 108),
        ("HITL Gate", "amber", 102),
        ("Fix Loop", "red", 94),
    ]
    gap = 10
    total_w = sum(w for _, _, w in items) + gap * (len(items) - 1)
    cx = right_x - total_w
    for label, role, w in items:
        fill, stroke, _, text_fill = role_colors(theme, role)
        add_pill(
            lines,
            cx,
            y,
            w,
            24,
            label,
            fill=fill,
            stroke=stroke,
            text_fill=text_fill,
            dot_fill=stroke,
            size=11,
        )
        cx += w + gap


def build_workflow_overview(theme: Theme) -> str:
    w, h = 1120, 586
    lines = svg_header(w, h, theme, "CLI-First Multi-Agent & HITL Delivery Architecture")

    # Header
    add_text(
        lines,
        28,
        42,
        "CLI-First Multi-Agent & HITL Delivery Architecture",
        fill=theme.text_primary,
        size=19,
        weight="700",
    )
    add_text(
        lines,
        28,
        62,
        "Herdr orchestration  ·  CUBRID skills & daemons  ·  Hermes -> Discord feedback loop",
        fill=theme.text_secondary,
        size=12.5,
    )
    add_legend(lines, theme, right_x=1092, y=28)

    # Top Band: Herdr 4-Tier Hierarchy
    blue_fill, blue_stroke, blue_pill, blue_text = role_colors(theme, "blue")
    add_rect(lines, 24, 78, 1072, 152, fill=theme.lane_bg, stroke=blue_stroke, rx=10, stroke_width=1.25)
    add_pill(
        lines,
        40,
        90,
        244,
        22,
        "HERDR 4-TIER AGENT HIERARCHY",
        fill=blue_pill,
        stroke=blue_stroke,
        text_fill=blue_text,
        size=10.5,
    )
    add_text(
        lines,
        1076,
        105,
        "Context isolation per ticket & worktree",
        fill=theme.text_muted,
        size=11,
        anchor="end",
    )

    herdr_cards = [
        ("Herdr Commander", "hcmd · work-tracker", "Cross-space routing & state"),
        ("Space Leaders", "tabs[0], panes[0]", "1 Space per ticket / worktree"),
        ("Tab Leaders", "tabs[1..8], panes[0]", "Scoped: build, test, review"),
        ("Pane Workers", "panes[1..3] (2x2)", "Noisy builds, tests & logs"),
    ]
    hx = 40
    card_w = 236
    gap = 29
    for idx, (title, sub1, sub2) in enumerate(herdr_cards):
        add_rect(lines, hx, 122, card_w, 74, fill=blue_fill, stroke=blue_stroke, rx=8, stroke_width=1.2)
        add_text(lines, hx + 14, 145, title, fill=theme.text_primary, size=13, weight="700")
        add_text(lines, hx + 14, 165, sub1, fill=blue_text, size=11, weight="600", mono=True)
        add_text(lines, hx + 14, 183, sub2, fill=theme.text_secondary, size=11)
        if idx < len(herdr_cards) - 1:
            ax1 = hx + card_w + 3
            ax2 = hx + card_w + gap - 3
            add_arrow(lines, f"M {ax1} 159 L {ax2} 159", theme=theme, role="blue", width=1.6)
        hx += card_w + gap

    add_text(
        lines,
        560,
        217,
        "Lean leader context   ·   Socket event waits (no sleep)   ·   Caps: 4 AI/space, 10/session   ·   1 writer/worktree",
        fill=theme.text_secondary,
        size=11,
        anchor="middle",
    )

    # Middle Band: Closed-Loop PR, Review, CI & Notification
    add_text(
        lines,
        28,
        254,
        "CLOSED-LOOP PR, REVIEW, CI & DISCORD WORKFLOW",
        fill=theme.text_secondary,
        size=11,
        weight="700",
    )

    flow_cards = [
        ("1. Ticket & Space", "SETUP", "purple", ["cubrid-jira · xref", "cubrid-worktree", "cubrid-workenv"], "Isolated DB + Space"),
        ("2. Draft PR", "HITL", "amber", ["cubrid-build · testkit", "cubrid-pr-create", "Local lint & body check"], "Gate: confirm push"),
        ("3. Review + CI", "AUTO", "green", ["cubrid-pr-flow", "cubrid-ci-watch", "Parallel AND-Join"], "cubrid-ci · tcc · tcr"),
        ("4. Hermes Notify", "AUTO", "green", ["hermes-notify daemon", "SQLite outbox + dedupe", "Discord status cards"], "Logs to work-tracker"),
        ("5. Merge & Cleanup", "HITL", "amber", ["cubrid-pr-merge", "final-merge-handoff", "Dual approval + lint"], "Gate: --yes + cleanup"),
    ]

    fx = 24
    fw = 192
    fgap = 28
    fy = 266
    fh = 128
    for idx, (title, badge, role, bullets, footer) in enumerate(flow_cards):
        fill, stroke, pill_bg, accent = role_colors(theme, role)
        add_rect(lines, fx, fy, fw, fh, fill=theme.card_bg, stroke=stroke, rx=9, stroke_width=1.35)
        add_rect(lines, fx, fy, fw, 32, fill=fill, stroke=stroke, rx=9, stroke_width=1.0)
        # Cover bottom corners of header strip so only top corners look rounded
        lines.append(
            f'  <rect x="{fx + 1}" y="{fy + 22}" width="{fw - 2}" height="11" fill="{fill}"/>'
        )
        lines.append(
            f'  <line x1="{fx}" y1="{fy + 32}" x2="{fx + fw}" y2="{fy + 32}" stroke="{stroke}" stroke-width="1"/>'
        )
        add_text(lines, fx + 11, fy + 21, title, fill=theme.text_primary, size=11.5, weight="700")
        add_pill(lines, fx + fw - 52, fy + 6.5, 42, 19, badge, fill=pill_bg, stroke=stroke, text_fill=accent, size=9)

        by = fy + 52
        for line_txt in bullets:
            add_text(lines, fx + 12, by, line_txt, fill=theme.text_secondary, size=11)
            by += 18

        lines.append(
            f'  <line x1="{fx + 10}" y1="{fy + fh - 26}" x2="{fx + fw - 10}" y2="{fy + fh - 26}" '
            f'stroke="{theme.card_border}" stroke-width="1"/>'
        )
        add_text(lines, fx + 12, fy + fh - 9, footer, fill=accent, size=10.5, weight="600")

        if idx < len(flow_cards) - 1:
            ax1 = fx + fw + 3
            ax2 = fx + fw + fgap - 3
            add_arrow(lines, f"M {ax1} {fy + fh / 2} L {ax2} {fy + fh / 2}", theme=theme, role="neutral", width=1.6)
        fx += fw + fgap

    # Feedback paths below the 5 cards (y=394..476)
    # Card 2 center = 244 + 96 = 340
    # Card 3 center = 464 + 96 = 560
    # Card 4 center = 684 + 96 = 780
    # Card 5 center = 904 + 96 = 1000
    green_fill, green_stroke, _, green_text = role_colors(theme, "green")
    red_fill, red_stroke, _, red_text = role_colors(theme, "red")
    amber_fill, amber_stroke, _, amber_text = role_colors(theme, "amber")

    # Green self-loop on Card 3 (known flake: 1x rerun)
    add_arrow(
        lines,
        "M 596 394 L 596 420 L 538 420 L 538 397",
        theme=theme,
        role="green",
        width=1.5,
    )
    add_pill(
        lines,
        494,
        409,
        146,
        22,
        "known flake: 1x rerun",
        fill=green_fill,
        stroke=green_stroke,
        text_fill=green_text,
        size=10,
    )

    # Red return arrow from Card 3 left-bottom to Card 2 bottom
    add_arrow(
        lines,
        "M 484 394 L 484 458 L 340 458 L 340 397",
        theme=theme,
        role="red",
        width=1.6,
        dashed=True,
    )
    add_pill(
        lines,
        282,
        446,
        220,
        22,
        "PR defect -> fix_in_herdr (Tab 1)",
        fill=red_fill,
        stroke=red_stroke,
        text_fill=red_text,
        size=10,
    )

    # Amber human decision arrow from Card 4 to Card 5
    add_arrow(
        lines,
        "M 780 394 L 780 438 L 1000 438 L 1000 397",
        theme=theme,
        role="amber",
        width=1.6,
    )
    add_pill(
        lines,
        792,
        426,
        196,
        22,
        "Discord alert -> Human decision",
        fill=amber_fill,
        stroke=amber_stroke,
        text_fill=amber_text,
        size=10,
    )

    # Bottom Foundation Band: my-cubrid-workflow
    purple_fill, purple_stroke, purple_pill, purple_text = role_colors(theme, "purple")
    add_rect(lines, 24, 484, 1072, 78, fill=theme.lane_bg, stroke=purple_stroke, rx=10, stroke_width=1.25)
    add_pill(
        lines,
        40,
        495,
        340,
        21,
        "my-cubrid-workflow  ·  RULE-DRIVEN AUTOMATION",
        fill=purple_pill,
        stroke=purple_stroke,
        text_fill=purple_text,
        size=10.5,
    )

    # Left 3 steps
    steps = [
        (40, 174, "rules/*.md (work habits)"),
        (238, 198, "sync-lock.toml (just drift)"),
        (460, 212, "check · test · run · sync"),
    ]
    for idx, (sx, sw, slabel) in enumerate(steps):
        add_rect(lines, sx, 524, sw, 26, fill=purple_fill, stroke=purple_stroke, rx=6, stroke_width=1)
        add_text(lines, sx + sw / 2, 541, slabel, fill=theme.text_primary, size=10.5, weight="600", anchor="middle", mono=True)
        if idx < len(steps) - 1:
            next_x = steps[idx + 1][0]
            add_arrow(lines, f"M {sx + sw + 3} 537 L {next_x - 3} 537", theme=theme, role="purple", width=1.4)

    # Right Tiered Git Policy callout
    add_rect(lines, 696, 495, 384, 56, fill=theme.card_bg, stroke=theme.card_border, rx=8, stroke_width=1)
    add_text(lines, 710, 515, "Tiered Git Integration Policy", fill=theme.text_primary, size=11.5, weight="700")
    add_text(
        lines,
        710,
        536,
        "Tier 1: solo repos (auto ff-merge)   ·   Tier 2: CUBRID/* (HITL)",
        fill=theme.text_secondary,
        size=10.5,
    )

    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def build_herdr_hierarchy(theme: Theme) -> str:
    w, h = 1120, 534
    lines = svg_header(w, h, theme, "Herdr 4-Tier Agent Hierarchy")

    add_text(lines, 28, 42, "Herdr 4-Tier Agent Hierarchy", fill=theme.text_primary, size=19, weight="700")
    add_text(
        lines,
        28,
        62,
        "Isolating noisy execution so orchestrators keep lean context windows",
        fill=theme.text_secondary,
        size=12.5,
    )

    blue_fill, blue_stroke, blue_pill, blue_text = role_colors(theme, "blue")
    purple_fill, purple_stroke, _, purple_text = role_colors(theme, "purple")
    green_fill, green_stroke, _, green_text = role_colors(theme, "green")
    amber_fill, amber_stroke, _, amber_text = role_colors(theme, "amber")

    # Tree orthogonal connectors (drawn behind cards)
    # Tier 0 center (412, 152) -> Tier 1 centers (140, 412, 684) at y=188
    lines.append(f'  <path d="M 412 152 L 412 170 M 140 170 L 684 170" fill="none" stroke="{blue_stroke}" stroke-width="1.5"/>')
    for cx in (140, 412, 684):
        add_arrow(lines, f"M {cx} 170 L {cx} 186", theme=theme, role="blue", width=1.5)

    # Space B center (412, 264) -> Tier 2 centers (140, 412, 684) at y=300
    lines.append(f'  <path d="M 412 264 L 412 282 M 140 282 L 684 282" fill="none" stroke="{blue_stroke}" stroke-width="1.5"/>')
    for cx in (140, 412, 684):
        add_arrow(lines, f"M {cx} 282 L {cx} 298", theme=theme, role="blue", width=1.5)

    # Tab 2 center (412, 376) -> Tier 3 centers (140, 412, 684) at y=412
    lines.append(f'  <path d="M 412 376 L 412 394 M 140 394 L 684 394" fill="none" stroke="{purple_stroke}" stroke-width="1.5"/>')
    for cx in (140, 412, 684):
        add_arrow(lines, f"M {cx} 394 L {cx} 410", theme=theme, role="purple", width=1.5)

    # Tier 0: Herdr Commander
    add_rect(lines, 180, 82, 464, 70, fill=blue_fill, stroke=blue_stroke, rx=9, stroke_width=1.6)
    add_pill(lines, 194, 93, 56, 19, "TIER 0", fill=blue_pill, stroke=blue_stroke, text_fill=blue_text, size=9.5)
    add_text(lines, 260, 107, "Herdr Commander (hcmd)", fill=theme.text_primary, size=13.5, weight="700")
    add_text(
        lines,
        194,
        127,
        "Inspects tabs[0] across spaces  ·  hcmd status / find / peek / wait",
        fill=theme.text_secondary,
        size=11,
    )
    add_text(
        lines,
        194,
        143,
        "Correlates open work-tracker items by cwd & ticket token",
        fill=blue_text,
        size=10.5,
        mono=True,
    )

    # Tier 1: Spaces
    spaces = [
        (28, 224, False, "Space A: Feature", "tabs[0], panes[0]", "Space Leader · own worktree"),
        (280, 264, True, "Space B: Ticket", "tabs[0], panes[0]", "Space Leader · max 8 sub-tabs"),
        (572, 224, False, "Space C: PR Review", "tabs[0], panes[0]", "Space Leader · review checkout"),
    ]
    for sx, sw, active, title, loc, desc in spaces:
        fill = blue_fill if active else theme.card_bg
        stroke = blue_stroke if active else theme.card_border
        swidth = 1.8 if active else 1.2
        add_rect(lines, sx, 188, sw, 76, fill=fill, stroke=stroke, rx=8, stroke_width=swidth)
        add_pill(lines, sx + 12, 198, 52, 18, "TIER 1", fill=blue_pill if active else theme.lane_bg, stroke=stroke, text_fill=blue_text if active else theme.text_muted, size=9)
        if active:
            add_pill(lines, sx + sw - 64, 198, 52, 18, "ACTIVE", fill=green_fill, stroke=green_stroke, text_fill=green_text, size=9)
        add_text(lines, sx + 72, 211, title, fill=theme.text_primary, size=12.5, weight="700")
        add_text(lines, sx + 12, 233, loc, fill=blue_text, size=11, weight="600", mono=True)
        add_text(lines, sx + 12, 251, desc, fill=theme.text_secondary, size=11)

    # Tier 2: Tabs under Space B
    tabs = [
        (28, 224, False, "Tab 1: review", "panes[0] · Tab Leader", "AI read-only code audit"),
        (280, 264, True, "Tab 2: test", "panes[0] · Tab Leader", "Splits up to 3 worker panes"),
        (572, 224, False, "Tab 3: build", "--launcher shell", "Unrestricted compile & logs"),
    ]
    for tx, tw, active, title, loc, desc in tabs:
        fill = blue_fill if active else theme.card_bg
        stroke = blue_stroke if active else theme.card_border
        swidth = 1.8 if active else 1.2
        add_rect(lines, tx, 300, tw, 76, fill=fill, stroke=stroke, rx=8, stroke_width=swidth)
        add_pill(lines, tx + 12, 310, 52, 18, "TIER 2", fill=blue_pill if active else theme.lane_bg, stroke=stroke, text_fill=blue_text if active else theme.text_muted, size=9)
        if active:
            add_pill(lines, tx + tw - 64, 310, 52, 18, "ACTIVE", fill=green_fill, stroke=green_stroke, text_fill=green_text, size=9)
        add_text(lines, tx + 72, 323, title, fill=theme.text_primary, size=12.5, weight="700")
        add_text(lines, tx + 12, 345, loc, fill=blue_text, size=11, weight="600", mono=True)
        add_text(lines, tx + 12, 363, desc, fill=theme.text_secondary, size=11)

    # Tier 3: Leaf Worker Panes under Tab 2
    panes = [
        (28, 224, "Pane 1 (panes[1])", "Focused testkit run"),
        (280, 264, "Pane 2 (panes[2])", "Log & core-dump triage"),
        (572, 224, "Pane 3 (panes[3])", "Isolated repro / tail"),
    ]
    for px, pw, title, desc in panes:
        add_rect(lines, px, 412, pw, 68, fill=purple_fill, stroke=purple_stroke, rx=8, stroke_width=1.2)
        add_pill(lines, px + 12, 422, 52, 18, "TIER 3", fill=theme.card_bg, stroke=purple_stroke, text_fill=purple_text, size=9)
        add_text(lines, px + 72, 435, title, fill=theme.text_primary, size=12, weight="700")
        add_text(lines, px + 12, 461, desc, fill=theme.text_secondary, size=11)

    add_text(
        lines,
        412,
        504,
        "Leaf Workers (panes[1..3], 2x2 grid) execute assigned commands only — never create tabs or split panes.",
        fill=theme.text_muted,
        size=11,
        anchor="middle",
    )

    # Right Guardrails Panel
    add_rect(lines, 820, 82, 276, 426, fill=theme.lane_bg, stroke=theme.lane_border, rx=10, stroke_width=1.25)
    add_text(lines, 836, 108, "Operating Guardrails", fill=theme.text_primary, size=14, weight="700")
    add_text(lines, 836, 125, "Hard limits enforced by rules & hcmd", fill=theme.text_muted, size=11)

    guardrails = [
        ("Context Separation", "blue", "Leaders plan & synthesize;", "workers absorb noisy output."),
        ("Quota Caps", "amber", "Max 8 sub-tabs/space ·", "4 worker AIs/space · 10 total."),
        ("Event-Driven Waits", "green", "Socket waits (hcmd wait),", "never sleep polling loops."),
        ("Single Writer", "red", "1 mutating agent per worktree;", "respect AGENT_BLOCKED."),
        ("Clean Teardown", "purple", "Close finished worker tabs;", "keep tabs[0] & panes[0]."),
    ]
    gy = 140
    for title, role, line1, line2 in guardrails:
        _, stroke, _, accent = role_colors(theme, role)
        add_rect(lines, 834, gy, 248, 64, fill=theme.card_bg, stroke=theme.card_border, rx=8, stroke_width=1.1)
        lines.append(
            f'  <rect x="834" y="{gy + 8}" width="4" height="48" rx="2" fill="{stroke}"/>'
        )
        add_text(lines, 848, gy + 21, title, fill=accent, size=11.5, weight="700")
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
        add_text(lines, x + 10, by, row, fill=theme.text_secondary, size=10.5)
        by += 17


def build_pr_ci_hitl_loop(theme: Theme) -> str:
    w, h = 1180, 646
    lines = svg_header(w, h, theme, "Closed-Loop Delivery: PR -> Review -> CI -> Hermes -> Discord -> HITL")

    add_text(
        lines,
        28,
        42,
        "Closed-Loop Delivery: PR -> Review -> CI -> Hermes -> Discord -> HITL",
        fill=theme.text_primary,
        size=18.5,
        weight="700",
    )
    add_text(
        lines,
        28,
        62,
        "Autonomous triage and notifications paired with explicit human decision gates",
        fill=theme.text_secondary,
        size=12.5,
    )
    add_legend(lines, theme, right_x=1152, y=28)

    amber_fill, amber_stroke, amber_pill, amber_text = role_colors(theme, "amber")
    green_fill, green_stroke, green_pill, green_text = role_colors(theme, "green")
    blue_fill, blue_stroke, blue_pill, blue_text = role_colors(theme, "blue")
    red_fill, red_stroke, _, red_text = role_colors(theme, "red")

    # 3 Swimlanes (keep header pills <= x=214 so C2 vertical arrow at x=311 never touches them)
    # Lane 1 (HITL)
    add_rect(lines, 24, 80, 1132, 138, fill=theme.lane_bg, stroke=amber_stroke, rx=10, stroke_width=1.2)
    add_pill(
        lines,
        40,
        90,
        172,
        21,
        "HUMAN-IN-THE-LOOP GATES",
        fill=amber_pill,
        stroke=amber_stroke,
        text_fill=amber_text,
        size=9.5,
    )

    # Lane 2 (Autonomous Daemons)
    add_rect(lines, 24, 234, 1132, 198, fill=theme.lane_bg, stroke=green_stroke, rx=10, stroke_width=1.2)
    add_pill(
        lines,
        40,
        244,
        244,
        21,
        "AUTONOMOUS DAEMONS · systemd --user",
        fill=green_pill,
        stroke=green_stroke,
        text_fill=green_text,
        size=9.5,
    )

    # Lane 3 (Herdr Space & Local Skills)
    add_rect(lines, 24, 448, 1132, 174, fill=theme.lane_bg, stroke=blue_stroke, rx=10, stroke_width=1.2)
    add_pill(
        lines,
        40,
        458,
        256,
        21,
        "HERDR SPACE · my-cubrid-skills",
        fill=blue_pill,
        stroke=blue_stroke,
        text_fill=blue_text,
        size=9.5,
    )

    # 6 Columns: C1..C6, width=166, gap=20
    cols = [42, 228, 414, 600, 786, 972]
    cw = 166

    # Lane 1 cards (y=120, h=86)
    draw_swimlane_card(
        lines, theme, cols[1], 120, cw, 86, "H1", "Confirm Draft PR", "amber",
        ["Review draft & lint", "Approve remote push", "Open --draft PR"],
    )
    draw_swimlane_card(
        lines, theme, cols[4], 120, cw, 86, "H2", "Discord Triage", "amber",
        ["Inspect alert card", "Open Actions Run URL", "Approve merge or fix"],
    )
    draw_swimlane_card(
        lines, theme, cols[5], 120, cw, 86, "H3", "Approve Merge", "amber",
        ["Run cubrid-pr-merge", "Check plan & msg lint", "Confirm --yes execute"],
    )

    # Lane 2 cards (y=282, h=100)
    draw_swimlane_card(
        lines, theme, cols[2], 282, cw, 100, "D1", "cubrid-pr-flow", "green",
        ["Parallel review + CI", "TC reviewer precheck", "AND-Join state flow"],
    )
    draw_swimlane_card(
        lines, theme, cols[3], 282, cw, 100, "D2", "ci-watch + Triage", "green",
        ["SQLite run ledger", "cubrid-ci · tcc · tcr", "Flake vs PR defect"],
    )
    draw_swimlane_card(
        lines, theme, cols[4], 282, cw, 100, "D3", "hermes-notify", "green",
        ["SQLite outbox + dedupe", "Discord kind routing", "Update work-tracker"],
    )
    draw_swimlane_card(
        lines, theme, cols[5], 282, cw, 100, "D4", "merge-handoff", "green",
        ["Ownership + threads", "Dual approval + lint", "TCs -> Gate -> Engine"],
    )

    # Lane 3 cards (y=492, h=102)
    draw_swimlane_card(
        lines, theme, cols[0], 492, cw, 102, "S1", "Ticket & Space", "purple",
        ["cubrid-jira · xref", "cubrid-worktree", "cubrid-workenv"],
    )
    draw_swimlane_card(
        lines, theme, cols[1], 492, cw, 102, "S2", "Build & Draft", "blue",
        ["Neovim + AI agents", "build · testkit-run", "cubrid-pr-create"],
    )
    draw_swimlane_card(
        lines, theme, cols[3], 492, cw, 102, "S3", "Fix in Herdr", "red",
        ["fix_in_herdr -> Tab 1", "Patch & verify locally", "Push updated HEAD"],
    )
    draw_swimlane_card(
        lines, theme, cols[5], 492, cw, 102, "S4", "Cleanup", "purple",
        ["cleanup --apply", "Close work-tracker", "Worktree + JIRA"],
    )

    # Arrows (all non-crossing!)
    # S1 -> S2
    add_arrow(lines, f"M {cols[0] + cw} 543 L {cols[1] - 2} 543", theme=theme, role="purple", width=1.6)
    # S2 -> H1 (straight up through empty C2 of Lane 2)
    c2_mid = cols[1] + cw / 2
    add_arrow(lines, f"M {c2_mid} 492 L {c2_mid} 208", theme=theme, role="amber", width=1.7)
    add_pill(
        lines,
        c2_mid - 58,
        322,
        116,
        22,
        "local draft ready",
        fill=amber_fill,
        stroke=amber_stroke,
        text_fill=amber_text,
        size=10,
    )

    # H1 -> D1 (right to C3 mid, then down into D1)
    c3_mid = cols[2] + cw / 2
    add_arrow(lines, f"M {cols[1] + cw} 163 L {c3_mid} 163 L {c3_mid} 280", theme=theme, role="green", width=1.7)
    add_pill(
        lines,
        c3_mid - 46,
        152,
        92,
        22,
        "draft PR out",
        fill=green_fill,
        stroke=green_stroke,
        text_fill=green_text,
        size=10,
    )

    # D1 -> D2 -> D3
    add_arrow(lines, f"M {cols[2] + cw} 332 L {cols[3] - 2} 332", theme=theme, role="green", width=1.6)
    add_arrow(lines, f"M {cols[3] + cw} 332 L {cols[4] - 2} 332", theme=theme, role="green", width=1.6)

    # D2 self-loop on top (1x auto-rerun) inside Lane 2 upper space
    c4_mid = cols[3] + cw / 2
    add_arrow(
        lines,
        f"M {c4_mid + 26} 282 L {c4_mid + 26} 254 L {c4_mid - 26} 254 L {c4_mid - 26} 280",
        theme=theme,
        role="green",
        width=1.5,
    )
    add_pill(
        lines,
        c4_mid - 64,
        243,
        128,
        20,
        "flake: 1x auto-rerun",
        fill=green_fill,
        stroke=green_stroke,
        text_fill=green_text,
        size=9.5,
    )

    # D2 -> S3 (red arrow straight down)
    add_arrow(lines, f"M {c4_mid} 382 L {c4_mid} 490", theme=theme, role="red", width=1.7, dashed=True)
    add_pill(
        lines,
        c4_mid - 68,
        396,
        136,
        22,
        "defect -> fix_in_herdr",
        fill=red_fill,
        stroke=red_stroke,
        text_fill=red_text,
        size=9.5,
    )

    # S3 -> S2 (red arrow straight left across empty C3 of Lane 3)
    add_arrow(lines, f"M {cols[3]} 543 L {cols[1] + cw + 2} 543", theme=theme, role="red", width=1.7, dashed=True)
    add_pill(
        lines,
        c3_mid - 64,
        532,
        128,
        22,
        "new HEAD -> re-verify",
        fill=red_fill,
        stroke=red_stroke,
        text_fill=red_text,
        size=9.5,
    )

    # D3 -> H2 (straight up at C5)
    c5_mid = cols[4] + cw / 2
    add_arrow(lines, f"M {c5_mid} 282 L {c5_mid} 208", theme=theme, role="amber", width=1.7)
    add_pill(
        lines,
        c5_mid - 50,
        234,
        100,
        21,
        "Discord card",
        fill=amber_fill,
        stroke=amber_stroke,
        text_fill=amber_text,
        size=10,
    )

    # H2 -> H3 (horizontal)
    add_arrow(lines, f"M {cols[4] + cw} 163 L {cols[5] - 2} 163", theme=theme, role="amber", width=1.7)

    # H3 -> D4 (straight down at C6)
    c6_mid = cols[5] + cw / 2
    add_arrow(lines, f"M {c6_mid} 206 L {c6_mid} 280", theme=theme, role="green", width=1.7)

    # D4 -> S4 (straight down at C6)
    add_arrow(lines, f"M {c6_mid} 382 L {c6_mid} 490", theme=theme, role="purple", width=1.7)

    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        "workflow-overview": build_workflow_overview,
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

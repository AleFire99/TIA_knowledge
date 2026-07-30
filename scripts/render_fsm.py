"""Render *.fsm.yaml (schema/fsm.schema.json) into draft markdown for the
Diagramma di stato / Timer / Azioni di ingresso doc sections.

Output is an English draft skeleton, not final Italian prose: it renders the
deterministic parts (mermaid structure, table shape, state/transition/guard/
timer identifiers) faithfully from the yaml, and carries the yaml's English
free text into table cells / edge labels as-is. A human or a Claude Code doc
pass then localizes that draft into the final IT + EN wording for index.md.

Usage:
    uv run python scripts/render_fsm.py <device-doc-dir-or-file.fsm.yaml>
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


def load_fbs(target: Path) -> list[dict]:
    if target.is_dir():
        paths = sorted(target.glob("*.fsm.yaml"))
        if not paths:
            raise SystemExit(f"no *.fsm.yaml files found in {target}")
    else:
        paths = [target]
    return [yaml.safe_load(p.read_text(encoding="utf-8")) for p in paths]


def _iter_states(states: list[dict], prefix: str = ""):
    """Yield (path, node) for every state node at any depth."""
    for node in states:
        path = f"{prefix}.{node['id']}" if prefix else node["id"]
        yield path, node
        if node.get("children"):
            yield from _iter_states(node["children"], path)


def _parent_scope(path: str) -> str:
    """Dotted parent path of a state path; "" for a top-level state."""
    return path.rsplit(".", 1)[0] if "." in path else ""


def _bare_name(path: str, scope: str) -> str:
    if path == "[*]":
        return path
    return path[len(scope) + 1 :] if scope else path


def _edge_scope(frm: str, to: str) -> str:
    scope_from = None if frm == "[*]" else _parent_scope(frm)
    scope_to = None if to == "[*]" else _parent_scope(to)
    if scope_from is None and scope_to is None:
        return ""
    if scope_from is None:
        return scope_to
    if scope_to is None:
        return scope_from
    if scope_from == scope_to:
        return scope_from
    # Cross-scope edge (not seen in current devices) -> fall back to the
    # longest common dotted-path prefix, or root.
    a, b = scope_from.split("."), scope_to.split(".")
    common = []
    for x, y in zip(a, b):
        if x != y:
            break
        common.append(x)
    return ".".join(common)


def render_mermaid(fb: dict) -> str:
    edges_by_scope: dict[str, list[str]] = {}
    for t in fb["transitions"]:
        scope = _edge_scope(t["from"], t["to"])
        frm = _bare_name(t["from"], scope)
        to = _bare_name(t["to"], scope)
        line = f"{frm} --> {to}"
        if t.get("guard"):
            line += f" : {t['guard']}"
        edges_by_scope.setdefault(scope, []).append(line)

    def render_scope(scope_path: str, level_states: list[dict], depth: int) -> list[str]:
        indent = "    " * depth
        lines = [indent + e for e in edges_by_scope.get(scope_path, [])]
        for node in level_states:
            if not node.get("children"):
                continue
            child_path = f"{scope_path}.{node['id']}" if scope_path else node["id"]
            if lines:
                lines.append("")
            lines.append(f"{indent}state {node['id']} {{")
            lines.extend(render_scope(child_path, node["children"], depth + 1))
            lines.append(f"{indent}}}")
        return lines

    body = render_scope("", fb["states"], 1)
    out = ["stateDiagram-v2", f"state {fb['label']}{{"]
    out.extend(body)
    out.append("}")
    return "```mermaid\n" + "\n".join(out) + "\n```"


def render_guard_formulas(fb: dict) -> str | None:
    formulas = fb.get("guard_formulas")
    if not formulas:
        return None
    lines = [f"{g['name']} := {g['expression']};" for g in formulas]
    return "```Pascal\n" + "\n".join(lines) + "\n```"


def render_state_table(fb: dict) -> str:
    rows = [
        (path, node)
        for path, node in _iter_states(fb["states"])
        if "outputs" in node or "description" in node
    ]
    output_cols: list[str] = []
    for _, node in rows:
        for key in node.get("outputs", {}):
            if key not in output_cols:
                output_cols.append(key)

    header = ["State"] + output_cols + ["Description"]
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    for path, node in rows:
        outputs = node.get("outputs", {})
        cells = [path]
        for col in output_cols:
            if col in outputs:
                val = outputs[col]
                cells.append(str(val).lower() if isinstance(val, bool) else str(val))
            else:
                cells.append("")
        cells.append(node.get("description", ""))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def render_value_table(fb: dict) -> str | None:
    rows = [(path, node["value"]) for path, node in _iter_states(fb["states"]) if "value" in node]
    if not rows:
        return None
    lines = ["| State | Int value |", "|---|---|"]
    for path, value in rows:
        lines.append(f"| {path} | {value} |")
    return "\n".join(lines)


def render_timer_table(fb: dict) -> str | None:
    timers = fb.get("timers")
    if not timers:
        return None
    lines = [
        "| Timer | Active state(s) | Threshold (parameter) |",
        "|---|---|---|",
    ]
    for t in timers:
        active = " or ".join(t["active_states"])
        lines.append(f"| {t['name']} | {active} | {t['param']} |")
    notes = [f"*{t['name']} raises: {t['raises']}*" for t in timers if t.get("raises")]
    return "\n".join(lines + ([""] + notes if notes else []))


def render_entry_actions_table(fb: dict) -> str | None:
    actions = fb.get("entry_actions")
    if not actions:
        return None
    lines = [
        "| State reached | Entry action |",
        "|---|---|",
    ]
    for a in actions:
        lines.append(f"| {a['state']} | {'; '.join(a['actions'])} |")
    shadows = [f"*{a['state']} entry gated by shadow var `{a['shadow_var']}`*" for a in actions if a.get("shadow_var")]
    return "\n".join(lines + ([""] + shadows if shadows else []))


def render_fb_section(fb: dict) -> str:
    parts = [f"<!-- fb: {fb['fb']} (udt: {fb['udt']}, source: {fb['source']}) -->"]

    delegates = fb.get("delegates") or {}
    fsm_delegate = delegates.get("fsm")
    timer_delegate = delegates.get("timer")

    if fsm_delegate:
        parts.append(
            f"State diagram and Timer: delegated to child instance `{fsm_delegate}` — "
            "omit both sections, cross-reference that instance's page instead."
        )
    else:
        parts.append("**State diagram** (draft — localize before pasting into \"Diagramma di stato\")")
        parts.append(render_mermaid(fb))
        guard_block = render_guard_formulas(fb)
        if guard_block:
            parts.append(guard_block)
        parts.append(render_state_table(fb))
        value_table = render_value_table(fb)
        if value_table:
            parts.append("**Int values** (draft — append under \"Diagramma di stato\", after the state table)")
            parts.append(value_table)

        if timer_delegate:
            parts.append(
                f"**Timer**: delegated to child instance(s) {', '.join(f'`{t}`' for t in timer_delegate)} "
                "— omit Timer section, cross-reference accordingly."
            )
        else:
            timer_table = render_timer_table(fb)
            if timer_table:
                parts.append("**Timer** (draft — localize before pasting into \"Timer\")")
                parts.append(timer_table)

        entry_table = render_entry_actions_table(fb)
        if entry_table:
            parts.append("**Azioni di ingresso** (draft — localize before pasting into \"Azioni di ingresso\")")
            parts.append(entry_table)

    if fb.get("notes"):
        parts.append("**Notes** (draft — fold into Funzionamento prose)")
        parts.append("\n".join(f"- {n}" for n in fb["notes"]))

    return "\n\n".join(parts)


def render_device(fbs: list[dict]) -> str:
    if len(fbs) == 1:
        return render_fb_section(fbs[0])
    sections = [f"#### {fb['fb']}\n\n{render_fb_section(fb)}" for fb in fbs]
    return "\n\n".join(sections)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="device doc directory or a single *.fsm.yaml file")
    args = parser.parse_args()
    if not args.target.exists():
        raise SystemExit(f"not found: {args.target}")
    sys.stdout.reconfigure(encoding="utf-8")
    print(render_device(load_fbs(args.target)))


if __name__ == "__main__":
    sys.exit(main())

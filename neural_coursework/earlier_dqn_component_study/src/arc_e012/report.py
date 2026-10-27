from __future__ import annotations

import json
from .tournament import ROOT, load_cfg


def fmt(x, digits=3):
    return "NA" if x is None else f"{float(x):.{digits}f}"


def comp_line(label: str, c: dict) -> str:
    p = c["progress_by_600"]
    cap = c["completion_cap"]
    return (
        f"- **{label}**: p600 {p['mean']:+.4f} [{p['ci95'][0]:+.4f}, {p['ci95'][1]:+.4f}]; "
        f"completion-cap {cap['mean']:+.4f} [{cap['ci95'][0]:+.4f}, {cap['ci95'][1]:+.4f}]."
    )


def main():
    cfg = load_cfg()
    lock = json.loads((ROOT / "results/LOCK_IN.json").read_text())
    lines = [
        "# E012 Final DQN Consolidation",
        "",
        "## Question",
        "",
        "Does the final evidence-backed DQN stack retain its advantage when D14 exploration and Dueling value architecture are removed one at a time?",
        "",
        "## Frozen stack entering E012",
        "",
        "- E004 representation: `E-onehotcnn__T-stack2__A-vector__U-effect`.",
        "- E008 backbone: Dueling Double-DQN family, one-step uniform replay, no C51.",
        "- E009 exploration: full D14 structured policy only on the epsilon-exploration branch.",
        "- E010 mechanics adapter excluded: improved mechanics prediction but no behavioral uplift.",
        "- E011 mechanics persistence excluded: tied the E009 behavioral control on fresh holdout seeds.",
        "",
        "## Three-seed matched ablation",
        "",
        "| rank | system | p250 | p600 | completion-cap | reward | first progress | D14/epsilon |",
        "|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for s in lock["summaries"]:
        lines.append(
            f"| {s['rank']} | `{s['id']}` | {fmt(s['progress_by_250'])} | {fmt(s['progress_by_600'])} | "
            f"{fmt(s['completion_cap'],4)} | {fmt(s['reward_total'])} | {fmt(s['first_progress_when_seen'],1)} | "
            f"{fmt(s['d14_fraction_of_epsilon'])} |"
        )

    lines += ["", "## Full-stack ablation effects", ""]
    names = {
        "E12_A_no_d14": "FULL - no-D14",
        "E12_A_no_dueling": "FULL - no-Dueling",
        "E12_A_plain_ddqn": "FULL - plain-DDQN anchor",
    }
    for sid, c in lock["comparisons_full_minus_ablation"].items():
        lines.append(comp_line(names.get(sid, f"FULL - {sid}"), c))

    lines += [
        "",
        "## Decision",
        "",
        f"`{lock['decision']}`",
        "",
        f"Selected/frozen DQN: `{lock['selected']['id']}`",
        "",
        "## Interpretation",
        "",
        "- E012 is a consolidation/ablation, not another broad architecture search.",
        "- Exact behavioral ties retain the full stack because D14 and Dueling already entered with prior experimental evidence.",
        "- If an ablation is behaviorally better, E012 flags component review instead of automatically claiming a new architecture.",
        "- This is the DQN baseline to freeze before building the official-style local evaluator and advanced specialist architectures.",
        "- Public games are development-exposed and sparse p600 is not the official Kaggle score.",
        "",
    ]
    text = "\n".join(lines)
    (ROOT / "results/REPORT.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()

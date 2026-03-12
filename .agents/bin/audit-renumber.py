#!/usr/bin/env python3
"""Compare current content/ files against pre-renumbering commit to find content loss."""
import subprocess
import sys
from path import Path

REPO = Path(__file__).parent.parent.parent
CONTENT = REPO / "presentation" / "content"
PRE_COMMIT = "932dbbb"  # last commit before renumbering

# Old → New filename mapping
MAPPING = [
    ("01-title.md", "00-title.md"),
    ("02-backstory-magic.md", "01-backstory-magic.md"),
    ("03-do-i-need-one.md", "02-do-i-need-one.md"),
    ("04-trouble-comes-knocking.md", "03-trouble-comes-knocking.md"),
    ("04.1-what-do-we-know.md", "04-what-do-we-know.md"),
    ("05-the-mighty-fine-team.md", "05-the-mighty-fine-team.md"),
    ("06-newest-party-member.md", "06-newest-party-member.md"),
    ("08-how-do-you-want-to-do-this.md", "07-how-do-you-want-to-do-this.md"),
    ("09-join-the-fray.md", "08-join-the-fray.md"),
    ("10-skills-in-action.md", "09-skills-in-action.md"),
    ("11-loot-the-room.md", "10-loot-the-room.md"),
    ("11.5-eventual-consistency.md", "11-eventual-consistency.md"),
    ("12-more-work.md", "12-more-work.md"),
    ("13-its-a-trap.md", "13-its-a-trap.md"),
    ("14-jetpacks.md", "14-jetpacks.md"),
    ("14.5-playbook.md", "15-playbook.md"),
    ("15-closing.md", "16-closing.md"),
    ("16-questions.md", "17-questions.md"),
]


def git_show(commit, filepath):
    """Get file content from a git commit."""
    try:
        result = subprocess.run(
            ["git", "show", f"{commit}:{filepath}"],
            capture_output=True, text=True, cwd=REPO,
        )
        return result.stdout if result.returncode == 0 else None
    except Exception:
        return None


def main():
    problems = []
    print(f"Comparing current content/ against {PRE_COMMIT}\n")
    print(f"{'Old file':<45} {'Old':>4} → {'New file':<45} {'Now':>4}  Status")
    print("-" * 120)

    for old_name, new_name in MAPPING:
        old_content = git_show(PRE_COMMIT, f"presentation/content/{old_name}")
        new_path = CONTENT / new_name
        new_content = new_path.read_text() if new_path.exists() else None

        old_lines = len(old_content.splitlines()) if old_content else 0
        new_lines = len(new_content.splitlines()) if new_content else 0

        if new_content is None:
            status = "MISSING!"
            problems.append((old_name, new_name, "file missing"))
        elif new_lines == 0:
            status = "EMPTY!"
            problems.append((old_name, new_name, "file is empty (0 lines)"))
        elif old_content and new_content.strip() == old_content.strip():
            status = "ok (identical)"
        elif abs(old_lines - new_lines) > 3:
            diff = new_lines - old_lines
            sign = "+" if diff > 0 else ""
            status = f"CHANGED ({sign}{diff} lines)"
            if new_lines < old_lines - 5:
                problems.append((old_name, new_name, f"lost {-diff} lines"))
        else:
            status = "ok (minor diff)"

        print(f"{old_name:<45} {old_lines:>4} → {new_name:<45} {new_lines:>4}  {status}")

    print()
    if problems:
        print(f"PROBLEMS FOUND ({len(problems)}):")
        for old, new, issue in problems:
            print(f"  {old} → {new}: {issue}")

        print("\nTo restore a file from the old commit:")
        print(f"  git show {PRE_COMMIT}:presentation/content/<old-name> > presentation/content/<new-name>")
    else:
        print("No problems found — all content preserved.")

    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

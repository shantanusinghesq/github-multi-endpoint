"""Read-only checks for this small Markdown skill package; standard library only."""
import re
import sys
from pathlib import Path


def validate(root):
    errors = []
    entry = root / "SKILL.md"
    if not entry.is_file():
        return ["Missing SKILL.md"]
    text = entry.read_text(encoding="utf-8-sig")
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        errors.append("Missing YAML frontmatter")
    else:
        fields = dict(re.findall(r"^([a-z]+):[ \t]*(.+)$", parts[1], re.M))
        if fields.get("name") != "github-multi-endpoint":
            errors.append("Unexpected skill name")
        if not fields.get("description", "").strip():
            errors.append("Missing description")
    for path in root.rglob("*.md"):
        body = path.read_text(encoding="utf-8-sig")
        if re.search(r"\b(?:TODO|TBD)\b|\[INSERT", body):
            errors.append(f"Unfinished scaffold: {path.name}")
        for target in re.findall(r"\]\(([^)]+)\)", body):
            if "://" in target or target.startswith("#"):
                continue
            dest = (path.parent / target.split("#", 1)[0]).resolve()
            if not dest.is_relative_to(root.resolve()) or not dest.is_file():
                errors.append(f"Invalid internal reference: {target}")
    if not (root / "references" / "checklist.md").is_file():
        errors.append("Missing checklist")
    return errors


if __name__ == "__main__":
    package = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "skills" / "github-multi-endpoint"
    findings = validate(package)
    print("\n".join(findings) if findings else "Skill package checks passed")
    sys.exit(bool(findings))

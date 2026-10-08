from pathlib import Path
import json


def test_latest_audit_file():
    project_root = Path(__file__).resolve().parent.parent
    audit_dir = project_root / "company" / "data" / "audit"

    audit_files = sorted(
        audit_dir.glob("*.json"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )

    if not audit_files:
        raise FileNotFoundError(
            f"No audit files were found in {audit_dir}."
        )

    latest_file = audit_files[0]

    report = json.loads(
        latest_file.read_text(encoding="utf-8")
    )

    print("Latest audit file:")
    print(latest_file)

    print("\nAudit report:")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    test_latest_audit_file()
"""Build the static RADIO archive from the PDFs in reports/."""

from collections.abc import Iterable
from html import escape
from pathlib import Path
import re
import shutil
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "_site"
REPORT_TYPES = {
    "prelabs": "Prelab",
    "lab-reports": "Lab report",
}


def natural_order(name: str) -> list[int | str]:
    """Keep Lab 2 ahead of Lab 10."""
    return [
        int(part) if index % 2 else part
        for index, part in enumerate(re.split(r"([0-9]+)", name.casefold()))
    ]


def report_files() -> Iterable[tuple[str, Path]]:
    for folder in REPORT_TYPES:
        for path in (ROOT / "reports" / folder).iterdir():
            if path.is_file() and not path.is_symlink() and path.suffix.lower() == ".pdf":
                yield folder, path


def report_row(folder: str, path: Path) -> str:
    relative_path = path.relative_to(ROOT)
    destination = OUTPUT / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, destination)

    title = escape(" ".join(path.stem.replace("_", " ").split()) or path.stem)
    url = escape(quote(relative_path.as_posix()))
    return f"""      <li class="report" data-kind="{folder}">
        <div class="report-main">
          <span class="file-icon" aria-hidden="true">PDF</span>
          <div>
            <h3 dir="auto">{title}</h3>
            <span class="report-type">{REPORT_TYPES[folder]}</span>
          </div>
        </div>
        <div class="report-actions">
          <a class="open-pdf" href="{url}" target="_blank" rel="noopener"
             aria-label="Open {title} (new tab)">Open PDF</a>
          <a class="download-pdf" href="{url}" download
             aria-label="Download {title}">Download</a>
        </div>
      </li>"""


def main() -> None:
    reports = sorted(report_files(), key=lambda report: (
        natural_order(report[1].stem), report[0], report[1].name
    ))

    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    shutil.copytree(ROOT / "site" / "assets", OUTPUT / "assets")
    rows = "\n".join(report_row(folder, path) for folder, path in reports)
    template = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
    count = len(reports)
    label = "document" if count == 1 else "documents"
    page = (
        template.replace("<!--INITIAL_COUNT-->", f"{count} {label}")
        .replace("<!--EMPTY_STATE_ATTRIBUTE-->", "hidden" if reports else "")
        .replace("<!--REPORT_ROWS-->", rows)
    )
    (OUTPUT / "index.html").write_text(page, encoding="utf-8")
    print(f"Built {OUTPUT} with {count} {label}.")


if __name__ == "__main__":
    main()

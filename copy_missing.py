#!/usr/bin/env python3
"""
copy_missing.py
Copy only folders/files that exist in folderB (source) but are missing from
folderA (destination). Existing files in folderA are NEVER overwritten.

Examples ( Sao chép tệp tuyển tập thư viện cho Altium Library):
    python copy_missing.py "E:\ALL_PROJECTS\GIT_REPOSITORY\HARDWARE_LIBRARY\Sample\altium-library-master\footprints" "E:\ALL_PROJECTS\GIT_REPOSITORY\HARDWARE_LIBRARY\Altium_Library\footprints"

    python copy_missing.py "E:\ALL_PROJECTS\GIT_REPOSITORY\HARDWARE_LIBRARY\Sample\altium-library-master\symbols"    "E:\ALL_PROJECTS\GIT_REPOSITORY\HARDWARE_LIBRARY\Altium_Library\symbols"
    
    python copy_missing.py "E:\ALL_PROJECTS\GIT_REPOSITORY\HARDWARE_LIBRARY\Sample\altium-library-master\STEP"       "E:\ALL_PROJECTS\GIT_REPOSITORY\HARDWARE_LIBRARY\Altium_Library\STEP"

Preview only (kiểm tra những gì sẽ được sao chép mà không thay đổi bất cứ thứ gì):
    python copy_missing.py "E:\ALL_PROJECTS\GIT_REPOSITORY\HARDWARE_LIBRARY\Sample\altium-library-master\STEP" "E:\ALL_PROJECTS\GIT_REPOSITORY\HARDWARE_LIBRARY\Altium_Library\STEP" --dry-run

Filter extensions (giới hạn các tệp được sao chép theo phần mở rộng):
    python copy_missing.py "E:\ALL_PROJECTS\GIT_REPOSITORY\HARDWARE_LIBRARY\Sample\altium-library-master\STEP" "E:\ALL_PROJECTS\GIT_REPOSITORY\HARDWARE_LIBRARY\Altium_Library\STEP" --ext .step .stp
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


def human_size(num_bytes: int) -> str:
    units = ("B", "KB", "MB", "GB", "TB")
    size = float(num_bytes)
    for unit in units:
        if size < 1024.0 or unit == units[-1]:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{num_bytes} B"


def normalize_extensions(exts: list[str] | None) -> set[str] | None:
    if not exts:
        return None
    result = set()
    for ext in exts:
        ext = ext.strip().lower()
        if not ext.startswith("."):
            ext = "." + ext
        result.add(ext)
    return result


def copy_missing(
    source: Path,
    destination: Path,
    *,
    dry_run: bool = False,
    extensions: set[str] | None = None,
    verbose: bool = True,
) -> tuple[int, int, int, int]:
    """
    Returns:
        (files_copied, dirs_created, files_skipped, total_bytes)
    """
    files_copied = 0
    dirs_created = 0
    files_skipped = 0
    total_bytes = 0

    source = source.resolve()
    destination = destination.resolve()

    if not source.exists():
        raise FileNotFoundError(f"Source folder does not exist: {source}")
    if not source.is_dir():
        raise NotADirectoryError(f"Source is not a folder: {source}")

    # Create root destination if needed.
    if not destination.exists():
        if verbose:
            print(f"[DIR ] {destination}")
        if not dry_run:
            destination.mkdir(parents=True, exist_ok=True)
        dirs_created += 1

    # os.walk is efficient and does not load the whole tree into memory.
    for current_root, dirnames, filenames in os.walk(source):
        current_root_path = Path(current_root)
        relative_root = current_root_path.relative_to(source)
        destination_root = destination / relative_root

        # Recreate subdirectories, including empty ones.
        for dirname in dirnames:
            src_dir = current_root_path / dirname
            rel_dir = src_dir.relative_to(source)
            dst_dir = destination / rel_dir

            if not dst_dir.exists():
                if verbose:
                    print(f"[DIR ] {rel_dir}")
                if not dry_run:
                    dst_dir.mkdir(parents=True, exist_ok=True)
                dirs_created += 1

        for filename in filenames:
            src_file = current_root_path / filename

            # Optional extension filter.
            if extensions is not None and src_file.suffix.lower() not in extensions:
                continue

            rel_file = src_file.relative_to(source)
            dst_file = destination / rel_file

            # Core rule: existing destination files are left untouched.
            if dst_file.exists():
                files_skipped += 1
                continue

            try:
                file_size = src_file.stat().st_size
            except OSError:
                file_size = 0

            if verbose:
                print(f"[COPY] {rel_file}  ({human_size(file_size)})")

            if not dry_run:
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                # copy2 preserves timestamps and metadata where supported.
                shutil.copy2(src_file, dst_file)

            files_copied += 1
            total_bytes += file_size

    return files_copied, dirs_created, files_skipped, total_bytes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Copy only files/folders missing from folderA. "
            "Existing files are never overwritten."
        )
    )
    parser.add_argument(
        "folderB",
        type=Path,
        help="Source folder containing the more complete library",
    )
    parser.add_argument(
        "folderA",
        type=Path,
        help="Destination folder to receive missing files",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be copied without changing anything",
    )
    parser.add_argument(
        "--ext",
        nargs="+",
        default=None,
        help="Optional extensions to copy, e.g. --ext .SchLib .PcbLib .step .stp",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Do not print every copied file; only show the summary",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    extensions = normalize_extensions(args.ext)

    print(f"Source (folderB):      {args.folderB}")
    print(f"Destination (folderA): {args.folderA}")
    print(f"Mode:                  {'DRY RUN' if args.dry_run else 'COPY'}")
    if extensions:
        print(f"Extensions:            {', '.join(sorted(extensions))}")
    else:
        print("Extensions:            ALL")
    print("-" * 72)

    try:
        copied, dirs, skipped, total_bytes = copy_missing(
            args.folderB,
            args.folderA,
            dry_run=args.dry_run,
            extensions=extensions,
            verbose=not args.quiet,
        )
    except (OSError, ValueError) as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        return 1

    print("-" * 72)
    print("SUMMARY")
    print(f"New folders : {dirs}")
    print(f"New files   : {copied}")
    print(f"Skipped     : {skipped} existing files")
    print(f"Data copied : {human_size(total_bytes)}")
    if args.dry_run:
        print("\nNo files were changed because --dry-run was used.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

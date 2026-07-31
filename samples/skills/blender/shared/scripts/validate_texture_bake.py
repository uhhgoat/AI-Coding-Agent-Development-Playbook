"""Validate saved texture-bake artifacts against their manifest."""

import argparse
import hashlib
import json
import math
import struct
import sys
from pathlib import Path


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
REQUIRED_PRIMARY_MAPS = {
    "base_color",
    "roughness",
    "metallic",
    "normal",
    "ao",
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else None
    return parser.parse_args(argv)


def file_sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def png_header(path):
    with path.open("rb") as source:
        signature = source.read(8)
        length = struct.unpack(">I", source.read(4))[0]
        chunk_type = source.read(4)
        payload = source.read(length)
    if signature != PNG_SIGNATURE or chunk_type != b"IHDR" or length != 13:
        raise ValueError("not a supported PNG")
    width, height, bit_depth, color_type, _, _, _ = struct.unpack(
        ">IIBBBBB",
        payload,
    )
    return {
        "dimensions": [width, height],
        "bit_depth": bit_depth,
        "color_type": color_type,
    }


def add_check(checks, name, status, evidence):
    checks.append({"name": name, "status": status, "evidence": evidence})


def validate_fingerprint(checks, name, record):
    path = Path(record["path"])
    exists = path.is_file() and path.stat().st_size > 0
    actual_hash = file_sha256(path) if exists else None
    expected_hash = record.get("sha256")
    passed = exists and (expected_hash is None or actual_hash == expected_hash)
    add_check(
        checks,
        name,
        "pass" if passed else "fail",
        {
            "path": str(path),
            "exists": exists,
            "expected_sha256": expected_hash,
            "actual_sha256": actual_hash,
        },
    )


def main():
    args = parse_args()
    manifest_path = args.manifest.resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    checks = []

    validate_fingerprint(checks, "source-stage", manifest["source"])
    validate_fingerprint(
        checks,
        "source-material-manifest",
        manifest["source_material_manifest"],
    )
    validate_fingerprint(
        checks,
        "baked-preview-stage",
        manifest["output_preview_stage"],
    )

    seen_semantics = set()
    map_evidence = []
    for record in manifest.get("maps", []):
        semantic = record["semantic"]
        seen_semantics.add(semantic)
        path = Path(record["path"])
        evidence = {
            "semantic": semantic,
            "path": str(path),
            "exists": path.is_file(),
        }
        passed = path.is_file() and path.stat().st_size > 0
        if passed:
            evidence["actual_sha256"] = file_sha256(path)
            evidence["expected_sha256"] = record.get("sha256")
            passed = evidence["actual_sha256"] == evidence["expected_sha256"]
            try:
                header = png_header(path)
                evidence["png"] = header
                passed = passed and header["dimensions"] == record["dimensions"]
                passed = passed and header["bit_depth"] == record["bit_depth"]
            except (OSError, ValueError, struct.error) as error:
                evidence["png_error"] = str(error)
                passed = False
        statistics = record.get("statistics", {})
        numeric = [
            statistics.get("minimum"),
            statistics.get("maximum"),
            statistics.get("mean"),
            statistics.get("standard_deviation"),
        ]
        finite = all(
            isinstance(value, (int, float)) and math.isfinite(value)
            for value in numeric
        )
        passed = passed and finite and statistics.get("finite") is True
        if semantic in REQUIRED_PRIMARY_MAPS:
            passed = passed and statistics.get("non_flat") is True
        evidence["statistics"] = statistics
        evidence["status"] = "pass" if passed else "fail"
        map_evidence.append(evidence)
    add_check(
        checks,
        "saved-maps",
        "pass"
        if map_evidence
        and all(record["status"] == "pass" for record in map_evidence)
        else "fail",
        map_evidence,
    )
    add_check(
        checks,
        "required-primary-semantics",
        "pass" if REQUIRED_PRIMARY_MAPS <= seen_semantics else "fail",
        {
            "required": sorted(REQUIRED_PRIMARY_MAPS),
            "present": sorted(seen_semantics),
            "missing": sorted(REQUIRED_PRIMARY_MAPS - seen_semantics),
        },
    )

    coverage = manifest.get("coverage", {})
    overlap = {
        semantic: record.get("overlap_pixels")
        for semantic, record in coverage.items()
    }
    add_check(
        checks,
        "atlas-coverage-overlap",
        "pass"
        if overlap and all(value == 0 for value in overlap.values())
        else "fail",
        overlap,
    )

    preview = manifest.get("preview", {})
    preview_dir = Path(preview.get("directory", ""))
    required_previews = [
        preview_dir / filename for filename in preview.get("required", [])
    ]
    missing_previews = [
        str(path)
        for path in required_previews
        if not path.is_file() or path.stat().st_size == 0
    ]
    add_check(
        checks,
        "baked-preview-evidence",
        "pass" if required_previews and not missing_previews else "fail",
        {
            "directory": str(preview_dir),
            "required": [str(path) for path in required_previews],
            "missing_or_empty": missing_previews,
        },
    )

    failures = [
        check["name"] for check in checks if check["status"] == "fail"
    ]
    warnings = list(manifest.get("validation", {}).get("warnings", []))
    report = {
        "manifest": str(manifest_path),
        "manifest_sha256": file_sha256(manifest_path),
        "status": "fail" if failures else ("warn" if warnings else "pass"),
        "checks": checks,
        "failures": failures,
        "warnings": warnings,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"TEXTURE_BAKE_VALIDATION={args.output.resolve()}")
    print(f"TEXTURE_BAKE_STATUS={report['status']}")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

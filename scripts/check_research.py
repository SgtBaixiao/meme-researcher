#!/usr/bin/env python3
"""Check installed dependencies and evidence contracts without network access."""
import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit

REQUIRED = ["SKILL.md", "scripts/bili_search.py", "scripts/bili_video.py",
            "scripts/bili_comments.py", "scripts/bili_memes.py",
            "scripts/tieba_search.py", "scripts/make_report.py"]
STATES = {"confirmed", "community-research", "rumor", "unverified"}

def doctor(directory):
    root = Path(directory).expanduser().resolve()
    missing = [name for name in REQUIRED if not (root / name).is_file()]
    return {"ok": not missing, "root": str(root), "missing": missing,
            "scope": "file availability only; platform access is not probed"}

def validate(document):
    problems = []
    if not isinstance(document, dict) or not isinstance(document.get("sources"), list) or not isinstance(document.get("claims"), list):
        return {"ok": False, "problems": ["sources and claims must be arrays"]}
    sources = {}
    for source in document["sources"]:
        if not isinstance(source, dict) or not isinstance(source.get("id"), str) or not source["id"].strip():
            problems.append("source needs a nonempty id")
            continue
        source_id = source["id"]
        if source_id in sources:
            problems.append(f"duplicate source: {source_id}")
        sources[source_id] = source
        url = source.get("url")
        try:
            parsed = urlsplit(url) if isinstance(url, str) else None
            valid_url = parsed and parsed.scheme in ("http", "https") and parsed.hostname and not parsed.username and not parsed.password and not any(char.isspace() for char in url)
            if parsed:
                parsed.port  # reject malformed and out-of-range ports
        except ValueError:
            valid_url = False
        if not valid_url:
            problems.append(f"source {source_id}: URL must be HTTP(S) without credentials")
        if not isinstance(source.get("origin_chain"), str) or not source["origin_chain"].strip():
            problems.append(f"source {source_id}: origin_chain is required")
    seen = set()
    for claim in document["claims"]:
        if not isinstance(claim, dict) or not isinstance(claim.get("id"), str) or not claim["id"].strip():
            problems.append("claim needs a nonempty id")
            continue
        claim_id = claim["id"]
        if claim_id in seen:
            problems.append(f"duplicate claim: {claim_id}")
        seen.add(claim_id)
        refs = claim.get("source_ids")
        if not isinstance(refs, list) or any(not isinstance(ref, str) for ref in refs):
            problems.append(f"claim {claim_id}: source_ids must be strings")
            continue
        if not isinstance(claim.get("status"), str) or claim["status"] not in STATES:
            problems.append(f"claim {claim_id}: invalid status")
        if not isinstance(claim.get("text"), str) or not claim["text"].strip():
            problems.append(f"claim {claim_id}: text is required")
        for ref in refs:
            if ref not in sources:
                problems.append(f"claim {claim_id}: missing source {ref}")
        chains = {sources[ref].get("origin_chain") for ref in refs if ref in sources and isinstance(sources[ref].get("origin_chain"), str) and sources[ref]["origin_chain"].strip()}
        if claim.get("status") == "confirmed" and len(chains) < 2:
            problems.append(f"claim {claim_id}: confirmed needs two independent origin chains")
    return {"ok": not problems, "problems": problems,
            "scope": "structure and declared provenance only; factual review is required"}

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    dependencies = commands.add_parser("doctor")
    dependencies.add_argument("--meme-digger", required=True)
    evidence = commands.add_parser("validate")
    evidence.add_argument("file", type=Path)
    args = parser.parse_args(argv)
    try:
        result = doctor(args.meme_digger) if args.command == "doctor" else validate(json.loads(args.file.read_text(encoding="utf8")))
    except (OSError, ValueError) as error:
        result = {"ok": False, "problems": [str(error)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1

if __name__ == "__main__":
    raise SystemExit(main())

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check_research.py"
spec = importlib.util.spec_from_file_location("research_checks", SCRIPT)
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)

class EvidenceTests(unittest.TestCase):
    def document(self):
        return {"sources": [
            {"id":"a", "url":"https://example.org/a", "origin_chain":"original"},
            {"id":"b", "url":"https://example.net/b", "origin_chain":"independent"}],
            "claims":[{"id":"claim", "text":"Research claim", "status":"confirmed", "source_ids":["a","b"]}]}

    def test_confirmed_claim_accepts_two_declared_independent_chains(self):
        self.assertTrue(checks.validate(self.document())["ok"])

    def test_reposts_and_duplicate_references_do_not_confirm_a_claim(self):
        data = self.document()
        data["sources"][1]["origin_chain"] = "original"
        self.assertFalse(checks.validate(data)["ok"])
        data["claims"][0]["source_ids"] = ["a", "a"]
        self.assertFalse(checks.validate(data)["ok"])

    def test_missing_references_invalid_urls_and_duplicates_fail(self):
        data = self.document()
        data["sources"][0]["url"] = "javascript:alert(1)"
        data["claims"][0]["source_ids"].append("missing")
        data["sources"].append(data["sources"][0])
        result = checks.validate(data)
        self.assertFalse(result["ok"])
        self.assertTrue(any("duplicate source" in item for item in result["problems"]))
        self.assertTrue(any("URL" in item for item in result["problems"]))
        self.assertTrue(any("missing source missing" in item for item in result["problems"]))

    def test_malformed_field_types_and_urls_return_validation_errors(self):
        data = self.document()
        data["claims"][0]["status"] = []
        self.assertFalse(checks.validate(data)["ok"])
        for url in ["https://user:secret@example.org", "https://example.org:99999", "https://exa\nmple.org", "http://[invalid"]:
            data = self.document()
            data["sources"][0]["url"] = url
            self.assertFalse(checks.validate(data)["ok"])

    def test_unverified_claim_can_preserve_an_unresolved_question(self):
        data = self.document()
        data["claims"][0].update(status="unverified", source_ids=[])
        self.assertTrue(checks.validate(data)["ok"])

    def test_dependency_check_and_cli_error_contract(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.assertFalse(checks.doctor(root)["ok"])
            for name in checks.REQUIRED:
                file = root / name
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text("fixture")
            self.assertTrue(checks.doctor(root)["ok"])
            malformed = root / "bad.json"
            malformed.write_text("not json")
            result = subprocess.run([sys.executable, str(SCRIPT), "validate", str(malformed)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertFalse(json.loads(result.stdout)["ok"])

if __name__ == "__main__":
    unittest.main()

"""Exercise the catalog CLI against real temporary files."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENTRY = '''
[[kits]]
id = "example"
name = "Example"
description = "A useful example workflow."
repository = "example/kit"
publisher = "Example Org"
categories = ["science", "verification"]
status = "community"
'''


class CatalogCLI(unittest.TestCase):
    def run_catalog(self, registry, readme=None, *args):
        with tempfile.TemporaryDirectory() as directory:
            registry_path = Path(directory) / "registry.toml"
            registry_path.write_text(registry, encoding="utf-8")
            command = [sys.executable, str(ROOT / "scripts/catalog.py"),
                       "--registry", str(registry_path)]
            readme_path = Path(directory) / "README.md"
            if readme is not None:
                readme_path.write_text(readme, encoding="utf-8")
                command += ["--readme", str(readme_path)]
            result = subprocess.run(command + list(args), capture_output=True, text=True)
            content = readme_path.read_text(encoding="utf-8") if readme_path.exists() else None
            return result, content

    def test_accepts_valid_registry(self):
        result, _ = self.run_catalog('registry_version = "1"\n' + ENTRY)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_duplicate_ids_across_kits_and_tools(self):
        tool = ENTRY.replace("[[kits]]", "[[related_tools]]").replace('status = "community"\n', '')
        result, _ = self.run_catalog('registry_version = "1"\n' + ENTRY + tool)
        self.assertEqual(result.returncode, 1)
        self.assertIn("duplicate id", result.stderr.lower())

    def test_rejects_case_variant_repository_duplicates(self):
        duplicate = ENTRY.replace('id = "example"', 'id = "other"').replace('example/kit', 'Example/Kit')
        result, _ = self.run_catalog('registry_version = "1"\n' + ENTRY + duplicate)
        self.assertEqual(result.returncode, 1)
        self.assertIn("duplicate repository", result.stderr.lower())

    def test_rejects_invalid_metadata(self):
        mutations = [
            ('status = "community"', 'status = "trusted"'),
            ('["science", "verification"]', '["unknown"]'),
            ('["science", "verification"]', '["science", "software-product-development"]'),
            ('publisher = "Example Org"', 'publisher = ""'),
            ('repository = "example/kit"', 'repository = "https://github.com/example/kit"'),
            ('id = "example"', 'id = "example"\nunknown = true'),
            ('id = "example"', 'id = "example\\n"'),
            ('repository = "example/kit"', 'repository = "example/kit\\n"'),
            ('["science", "verification"]', '["science", "verification\\n"]'),
            ('status = "community"', 'status = "community"\nkit = "example\\n"'),
        ]
        for before, after in mutations:
            with self.subTest(after=after):
                result, _ = self.run_catalog('registry_version = "1"\n' + ENTRY.replace(before, after))
                self.assertEqual(result.returncode, 1)
                self.assertNotIn("Traceback", result.stderr)

    def test_related_tools_cannot_claim_a_kit_selector(self):
        tool = ENTRY.replace("[[kits]]", "[[related_tools]]").replace('status = "community"', 'kit = "example"')
        result, _ = self.run_catalog('registry_version = "1"\n' + ENTRY + tool.replace('id = "example"', 'id = "tool"'))
        self.assertEqual(result.returncode, 1)

    def test_reports_malformed_toml(self):
        result, _ = self.run_catalog('registry_version = "1"\n[[kits]\n')
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("Traceback", result.stderr)

    def test_generates_catalog_without_changing_surrounding_content(self):
        readme = "Intro\n<!-- BEGIN CATALOG -->\nstale\n<!-- END CATALOG -->\nFooter\n"
        result, content = self.run_catalog('registry_version = "1"\n' + ENTRY, readme, "--write")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(content.startswith("Intro\n<!-- BEGIN CATALOG -->\n"))
        self.assertTrue(content.endswith("<!-- END CATALOG -->\nFooter\n"))
        self.assertIn("[**Example**](https://github.com/example/kit)", content)
        self.assertIn("[`example/kit`](https://github.com/example/kit)", content)
        self.assertNotIn("**[Example Org]**", content)
        self.assertIn("## Science", content)
        self.assertNotIn("stale", content)
        checked, _ = self.run_catalog('registry_version = "1"\n' + ENTRY, content, "--check")
        self.assertEqual(checked.returncode, 0, checked.stderr)

    def test_detects_readme_drift_without_writing(self):
        readme = "<!-- BEGIN CATALOG -->\nstale\n<!-- END CATALOG -->\n"
        result, content = self.run_catalog('registry_version = "1"\n' + ENTRY, readme, "--check")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(content, readme)
        self.assertIn("--write", result.stderr)

    def test_refuses_missing_markers(self):
        result, content = self.run_catalog('registry_version = "1"\n' + ENTRY, "Handwritten README\n", "--write")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(content, "Handwritten README\n")
        self.assertNotIn("Traceback", result.stderr)

    def test_invalid_registry_never_rewrites_readme(self):
        readme = "<!-- BEGIN CATALOG -->\nstale\n<!-- END CATALOG -->\n"
        registry = 'registry_version = "1"\n' + ENTRY.replace('status = "community"', 'status = "invalid"')
        result, content = self.run_catalog(registry, readme, "--write")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(content, readme)

    def test_treats_description_metadata_as_plain_text(self):
        registry = 'registry_version = "1"\n' + ENTRY.replace('description = "A useful example workflow."', 'description = "<script>Bad</script> [link](https://bad.example)"')
        readme = "<!-- BEGIN CATALOG -->\n<!-- END CATALOG -->\n"
        result, content = self.run_catalog(registry, readme, "--write")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("<script>", content)
        self.assertIn(r"\[link\]", content)

    def test_lists_multikit_and_related_tool_without_install_sections(self):
        registry = 'registry_version = "1"\n' + ENTRY + 'kit = "compete"\n'
        tool = ENTRY.replace("[[kits]]", "[[related_tools]]").replace('status = "community"\n', '').replace('id = "example"', 'id = "tool"').replace('example/kit', 'example/tool')
        registry += tool
        readme = "<!-- BEGIN CATALOG -->\n<!-- END CATALOG -->\n"
        result, content = self.run_catalog(registry, readme, "--write")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[`example/kit`](https://github.com/example/kit)", content)
        self.assertIn("**Related tool**", content)
        self.assertNotIn("cfs kit install", content)
        self.assertNotIn("<details>", content)


if __name__ == "__main__":
    unittest.main()

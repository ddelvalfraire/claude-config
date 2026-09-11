import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("generator", ROOT / "scripts/generate-agents-md.py")
GENERATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GENERATOR)


class GeneratorTests(unittest.TestCase):
    def test_frontmatter_valid_document_preserves_body(self):
        self.assertEqual(GENERATOR.strip_frontmatter('---\nname: test\n---\n\n# Body\n'), '# Body\n')

    def test_frontmatter_unclosed_document_preserves_text(self):
        text = '---\nThis is an ordinary Markdown divider.\n'
        try:
            result = GENERATOR.strip_frontmatter(text)
        except IndexError:
            self.fail("Unclosed frontmatter must be preserved, not crash generation")
        self.assertEqual(result, text)

    def test_frontmatter_separator_in_metadata_preserves_body(self):
        text = '---\ndescription: text ending ---\nname: test\n---\n# Body\n'
        self.assertEqual(GENERATOR.strip_frontmatter(text), '# Body\n')


if __name__ == "__main__":
    unittest.main()

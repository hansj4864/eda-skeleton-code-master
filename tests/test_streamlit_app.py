from __future__ import annotations

import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


class StreamlitInteractionTests(unittest.TestCase):
    def setUp(self) -> None:
        app_path = Path(__file__).resolve().parents[1] / "app.py"
        self.app = AppTest.from_file(str(app_path), default_timeout=20).run()
        self.assertFalse(self.app.exception)

    def test_mcq_submission_reveals_solution(self) -> None:
        self.app.radio[0].set_value(1)
        self.app.button[0].click().run()
        self.assertFalse(self.app.exception)
        self.assertEqual(1, len(self.app.success))
        self.assertGreaterEqual(len(self.app.code), 1)
        self.assertGreaterEqual(len(self.app.expander), 1)

    def test_medium_code_submission_and_filtering(self) -> None:
        self.app.selectbox[0].set_value("결측치").run()
        self.app.selectbox[1].set_value("중급").run()
        self.assertFalse(self.app.exception)
        self.assertEqual(1, len(self.app.text_input))
        self.app.text_input[0].set_value('df["age"].fillna(df["age"].median())')
        self.app.button[0].click().run()
        self.assertFalse(self.app.exception)
        self.assertEqual(1, len(self.app.success))


if __name__ == "__main__":
    unittest.main()

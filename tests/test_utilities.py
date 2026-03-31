import unittest
import json
import os
from src.name_of_the_machine.utilities import (
    plato_text_to_cmj,
    plato_text_to_muj,
    plato_text_to_mpuj,
    cmj_to_plato_text,
    new_plato_text
)


class TestTransformations(unittest.TestCase):
    def setUp(self):
        # Paths to example files
        base_dir = os.path.dirname(__file__) + '/data'
        with open(os.path.join(base_dir, 'plato_example.txt'), 'r', encoding='utf-8') as f:
            self.plato_txt = f.read()
        
        with open(os.path.join(base_dir, 'cmj_example.json'), 'r', encoding='utf-8') as f:
            self.cmj_json = json.load(f)
            
        with open(os.path.join(base_dir, 'mpuj_example.json'), 'r', encoding='utf-8') as f:
            self.mpuj_json = json.load(f)
            
        with open(os.path.join(base_dir, 'muj_example.json'), 'r', encoding='utf-8') as f:
            self.muj_json = json.load(f)
            
        self.machine_name = "Thinking-Machine"
        self.maxDiff = None

    def test_plato_text_to_muj(self):
        result = plato_text_to_muj(self.plato_txt, self.machine_name)
        self.assertEqual(result, self.muj_json)

    def test_plato_text_to_mpuj(self):
        result = plato_text_to_mpuj(self.plato_txt, self.machine_name)
        self.assertEqual(result, self.mpuj_json)

    def test_plato_text_to_cmj(self):
        result = plato_text_to_cmj(self.plato_txt, self.machine_name)
        self.assertEqual(result, self.cmj_json)

    def test_cmj_to_plato_text(self):
        result = cmj_to_plato_text(self.cmj_json)
        self.assertEqual(result.strip(), self.plato_txt.strip())

    def test_new_plato_text(self):
        thoughts = "This is a thought.\n\nIt spans multiple paragraphs."
        text = "This is the final text.\n\nIt also has paragraphs."

        expected = (
            "Thinking-Machine: (thinking) This is a thought.\n\tIt spans multiple paragraphs.\n\n"
            "Thinking-Machine: This is the final text.\n\tIt also has paragraphs.\n\n"
        )
        result = new_plato_text(thoughts, text, self.machine_name)
        self.assertEqual(result, expected)

        expected_no_thoughts = "Thinking-Machine: This is the final text.\n\tIt also has paragraphs.\n\n"
        result2 = new_plato_text("", text, self.machine_name)
        self.assertEqual(result2, expected_no_thoughts)

        expected_no_text = "Thinking-Machine: (thinking) This is a thought.\n\tIt spans multiple paragraphs.\n\n"
        result3 = new_plato_text(thoughts, "", self.machine_name)
        self.assertEqual(result3, expected_no_text)


if __name__ == '__main__':
    unittest.main()

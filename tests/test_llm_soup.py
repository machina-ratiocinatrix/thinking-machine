import unittest
from src.name_of_the_machine.utilities import llm_soup_to_text


class TestLLMSoupToText(unittest.TestCase):
    def test_basic_text(self):
        self.assertEqual(llm_soup_to_text("Hello world"), "Hello world")

    def test_bold_italic(self):
        self.assertEqual(llm_soup_to_text("This is **bold** and __bold__."), "This is bold and bold.")
        self.assertEqual(llm_soup_to_text("This is *italic* and _italic_."), "This is italic and italic.")
        self.assertEqual(llm_soup_to_text("Combined ***bold italic***!"), "Combined bold italic!")

    def test_inline_code(self):
        self.assertEqual(llm_soup_to_text("Here is some `inline code`."), "Here is some inline code.")

    def test_fenced_code_blocks(self):
        text = "Before code\n```python\ndef foo():\n    pass\n```\nAfter code"
        self.assertEqual(llm_soup_to_text(text), "Before code\n\tAfter code")
        
        text2 = "Before code\n~~~javascript\nconsole.log(1);\n~~~\nAfter code"
        self.assertEqual(llm_soup_to_text(text2), "Before code\n\tAfter code")

    def test_headers(self):
        text = "# Header 1\nSome text\n## Header 2\nMore text"
        self.assertEqual(llm_soup_to_text(text), "Header 1\nSome text\nHeader 2\nMore text")
        
        text2 = "Setext Header\n=============\nSome text"
        self.assertEqual(llm_soup_to_text(text2), "Setext Header\nSome text")

    def test_links_and_images(self):
        self.assertEqual(llm_soup_to_text("Click [here](https://url.com) now."), "Click here now.")
        self.assertEqual(llm_soup_to_text("An image ![alt text](img.png) here."), "An image here.")

    def test_blockquotes(self):
        text = "> This is a quote\n> It continues"
        self.assertEqual(llm_soup_to_text(text), "This is a quote\nIt continues")

    def test_lists(self):
        text = "- Item 1\n* Item 2\n+ Item 3"
        self.assertEqual(llm_soup_to_text(text), "Item 1\nItem 2\nItem 3")
        
        text2 = "1. First\n2. Second\n10. Tenth"
        self.assertEqual(llm_soup_to_text(text2), "First\nSecond\nTenth")

    def test_html_tags(self):
        self.assertEqual(llm_soup_to_text("<p>Hello <b>world</b>!</p>"), "Hello world!")
        self.assertEqual(llm_soup_to_text("<div>Text <br/> More text</div>"), "Text\nMore text")

    def test_html_comments(self):
        self.assertEqual(llm_soup_to_text("Visible <!-- hidden --> visible"), "Visible visible")

    def test_html_entities(self):
        self.assertEqual(llm_soup_to_text("Tom &amp; Jerry"), "Tom & Jerry")
        self.assertEqual(llm_soup_to_text("It&#39;s mine"), "It's mine")

    def test_horizontal_rules(self):
        text = "Above\n---\nBelow\n***\nEnd"
        self.assertEqual(llm_soup_to_text(text), "Above\n\tBelow\n\tEnd")

    def test_whitespace_and_paragraphs(self):
        # Multiple spaces and tabs
        self.assertEqual(llm_soup_to_text("Too   many \t spaces"), "Too many spaces")
        # Paragraphs consolidated
        self.assertEqual(llm_soup_to_text("Para 1\n\n\n\nPara 2"), "Para 1\n\tPara 2")
        # Leading and trailing
        self.assertEqual(llm_soup_to_text(" \n  \t Trim me \n \t  "), "Trim me")


if __name__ == '__main__':
    unittest.main()

import unittest

from extractmarkdown import extract_markdown_images, extract_markdown_links, extract_title


class TestTextNode(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_multiple_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extraction = extract_markdown_images(text)
        self.assertEqual(
            extraction,
            [
              ("rick roll", "https://i.imgur.com/aKaOqIh.gif"), 
              ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")  
            ]
        )

    def test_extract_both(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extraction = extract_markdown_images(text)
        self.assertEqual(
            extraction,
            [
              ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ]
        )

    def test_extract_heading(self):
        text = "# This is the heading\n it should only return that first line"
        extraction = extract_title(text)
        self.assertEqual(extraction, "This is the heading")

    def test_extract_heading(self):
        text = "## This is the heading\n it should only return an error"
        with self.assertRaises(Exception):
            extraction = extract_title(text)
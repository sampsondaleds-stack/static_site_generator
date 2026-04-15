import unittest

from block import BlockType, block_to_block_type, markdown_to_html_node
from htmlnode import ParentNode, HTMLNode, LeafNode

class TestTextNode(unittest.TestCase):
    def test_heading_block(self):
        block = "### Heading"
        results = block_to_block_type(block)
        self.assertEqual(results, BlockType.HEADING)

    def test_paragraph_block(self):
        block = "This is a Paragraph\nit has more than one line\nwhich is what a paragraph needs"
        results = block_to_block_type(block)
        self.assertEqual(results, BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```\nthis is a code block\nwith multiple lines\n```"
        results = block_to_block_type(block)
        self.assertEqual(results, BlockType.CODE)
    
    def test_quote_block(self):
        block = "> this is a quote\n>the second line has no space"
        results = block_to_block_type(block)
        self.assertEqual(results, BlockType.QUOTE)
    
    def test_ulist_block(self):
        block = "- this is a list\n- with two lines"
        results = block_to_block_type(block)
        self.assertEqual(results, BlockType.ULIST)

    def test_olist_block(self):
        block = "1. this is an ordered list\n2. the second line\n3. the third line"
        results = block_to_block_type(block)
        self.assertEqual(results, BlockType.OLIST)
    
    def test_olist_block_failure(self):
        block = "1. this is an ordered list\n the second line\n3. the third line"
        results = block_to_block_type(block)
        self.assertEqual(results, BlockType.PARAGRAPH)
    
    def test_quote_block_failure(self):
        block = "> this is a quote\n the second line fails"
        results = block_to_block_type(block)
        self.assertEqual(results, BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
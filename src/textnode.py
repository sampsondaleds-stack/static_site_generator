from enum import Enum
import htmlnode

class TextType(Enum):
	TEXT = "text"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"

class TextNode:
	def __init__(self, text, text_type, url = None):
		self.text = text
		self.text_type = text_type
		self.url = url
	
	def __eq__(self, other):
		return (
			self.text == other.text and
			self.text_type == other.text_type and
			self.url == other.url
		)

	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
	if text_node.text_type not in TextType:
		raise Exception("invalid text type")
	if text_node.text_type == TextType.TEXT:
		return htmlnode.LeafNode(None, text_node.text)
	if text_node.text_type == TextType.BOLD:
		return htmlnode.LeafNode("b", text_node.text)
	if text_node.text_type == TextType.ITALIC:
		return htmlnode.LeafNode("i", text_node.text)
	if text_node.text_type == TextType.CODE:
		return htmlnode.LeafNode("code", text_node.text)
	if text_node.text_type == TextType.LINK:
		return htmlnode.LeafNode("a", text_node.text, {"href": text_node.url})
	if text_node.text_type == TextType.IMAGE:
		return htmlnode.LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
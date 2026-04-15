from enum import Enum
from splitdelimiter import markdown_to_blocks, text_to_textnodes
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextType, TextNode, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ","## ","### ","#### ","##### ","###### ")):
        return BlockType.HEADING
    if lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith((">","> ")):
        for line in lines:
            if not line.startswith((">","> ")):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        for index, line in enumerate(lines):
            if not line.startswith(f"{index +1}. "):
                return BlockType.PARAGRAPH
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_to_html_node(block, block_type)
        html_nodes.append(html_node)
    parent_node = ParentNode("div", html_nodes)
    return parent_node


def block_to_html_node(block, block_type):
    if block_type == BlockType.HEADING:
        return heading_block_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_block_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_block_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_block_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_block_to_html_node(block)
    return ParentNode("p", text_to_children(block.replace("\n", " ")))

def heading_block_to_html_node(block):
    count, text = block.split(" ", 1)
    return ParentNode(f"h{len(count)}", text_to_children(text))

def code_block_to_html_node(block):
    lines = block.split("\n")
    lines = lines[1:-1]
    text = "\n".join(lines) + "\n"
    text_node = TextNode(text, TextType.TEXT)
    html_node = text_node_to_html_node(text_node)
    html_code_node = ParentNode("code", [html_node])
    html_pre_node = ParentNode("pre", [html_code_node])
    return html_pre_node

def quote_block_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        line = line.lstrip(">")
        line = line.lstrip(" ")
        new_lines.append(line)
    text = "\n".join(new_lines)
    return ParentNode("blockquote", text_to_children(text))

def ulist_block_to_html_node(block):
    lines = block.split("\n")
    html_nodes = []
    for line in lines:
        line = line.split(" ", 1)[1]
        html_nodes.append(ParentNode("li", text_to_children(line)))
    return ParentNode("ul", html_nodes)

def olist_block_to_html_node(block):
    lines = block.split("\n")
    html_nodes = []
    for line in lines:
        line = line.split(" ", 1)[1]
        html_nodes.append(ParentNode("li", text_to_children(line)))
    return ParentNode("ol", html_nodes)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)
    return html_nodes
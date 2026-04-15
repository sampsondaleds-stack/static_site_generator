import re

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_title(text):
    try:
        result = re.findall(r"(?<!#)#(?!#)(.*)", text)[0].strip()
    except IndexError:
        raise Exception("No h1 header found")
    return result


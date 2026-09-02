from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    plain_text = 'text'
    bold_text = 'bold'
    italic_text = 'italic'
    code_text = 'code'
    link = 'link'
    image = 'image'

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url


    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return False
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    textstyle = text_node.text_type
        
    if textstyle == TextType.plain_text:
        return LeafNode(None, text_node.text)
    if textstyle == TextType.bold_text:
        return LeafNode("b", text_node.text)
    if textstyle == TextType.italic_text:
        return LeafNode("i", text_node.text)
    if textstyle == TextType.code_text:
        return LeafNode("code", text_node.text)
    if textstyle == TextType.link:
        if text_node.url is None:
            raise ValueError("No URL/invalid URL")
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if textstyle == TextType.image:
        if text_node.url is None:
            raise ValueError("No URL/invalid URL")
        return LeafNode("img","",{"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"{textstyle} is not a valid option!")


def __repr__(self) -> str:
    return f"TextNode({self.text}, {self.text_type}, {self.url})"

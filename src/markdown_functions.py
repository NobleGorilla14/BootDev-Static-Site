from textnode import *
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type.plain_text:
            new_nodes.append(node)
            continue
        split_nodes = []
        delmatch = node.text.split(delimiter)
        if len(delmatch) % 2 == 0:
            raise ValueError(f'A matching closing {delimiter} was not found')
        for s in range(len(delmatch)):
            if delmatch[s] == "":
                continue
            if s % 2 == 0:
                split_nodes.append(TextNode(delmatch[s], TextType.plain_text))
            else:
                split_nodes.append(TextNode(delmatch[s], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str,str]]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str,str]]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.plain_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.plain_text))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.image,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.plain_text))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.plain_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.plain_text))
            new_nodes.append(TextNode(link[0], TextType.link, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.plain_text))
    return new_nodes

def text_to_textnodes(text) -> list[TextNode]:
    nodes = [TextNode(text,TextType.plain_text)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.bold_text)
    nodes = split_nodes_delimiter(nodes, "__", TextType.italic_text)
    nodes = split_nodes_delimiter(nodes, "`", TextType.code_text)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    cleaned = markdown.strip()
    split = cleaned.split('\n\n')
    final = []
    for x in split:
        stripped = x.strip()
        if stripped != "":
            final.append(stripped)
    return final

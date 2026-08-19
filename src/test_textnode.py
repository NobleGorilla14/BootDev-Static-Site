import unittest
from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.bold_text)
        node2 = TextNode("This is a text node", TextType.bold_text)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.plain_text)
        node2 = TextNode("This is a text node", TextType.bold_text)
        self.assertNotEqual(node, node2)

    def testaurl(self):
        node = TextNode("This is a text node", TextType.bold_text,"www.fakeurl.com")
        self.assertIsNotNone(node.url)

    def test_text(self):
        node = TextNode("This is a text node", TextType.plain_text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    
class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.plain_text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.image, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.bold_text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

class TestInLineMarkdown(unittest.TestCase):
    def text_outputformat(self):
        node = TextNode("This is text with a `code block` word", TextType.plain_text)
        new_nodes = split_nodes_delimiter([node], "`", TextType.code_text)
        self.assertListEqual(new_nodes,[
                TextNode("This is text with a ", TextType.plain_text),
                TextNode("code block", TextType.code_text),
                TextNode(" word", TextType.plain_text),
                                ]
                         )
       
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.plain_text)
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold_text)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.plain_text),
                TextNode("bolded", TextType.bold_text),
                TextNode(" word", TextType.plain_text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.plain_text
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold_text)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.plain_text),
                TextNode("bolded", TextType.bold_text),
                TextNode(" word and ", TextType.plain_text),
                TextNode("another", TextType.bold_text),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.plain_text
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold_text)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.plain_text),
                TextNode("bolded word", TextType.bold_text),
                TextNode(" and ", TextType.plain_text),
                TextNode("another", TextType.bold_text),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.plain_text)
        new_nodes = split_nodes_delimiter([node], "_", TextType.italic_text)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.plain_text),
                TextNode("italic", TextType.italic_text),
                TextNode(" word", TextType.plain_text),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.plain_text)
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold_text)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.italic_text)
        self.assertListEqual(
            [
                TextNode("bold", TextType.bold_text),
                TextNode(" and ", TextType.plain_text),
                TextNode("italic", TextType.italic_text),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.plain_text)
        new_nodes = split_nodes_delimiter([node], "`", TextType.code_text)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.plain_text),
                TextNode("code block", TextType.code_text),
                TextNode(" word", TextType.plain_text),
            ],
            new_nodes,
        )

def test_extract_markdown_images(self):
    matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

def test_extract_markdown_links(self):
    matches = extract_markdown_links("This is a bunch of garbage with a [link](https://fake.com) and [another](https://workingremote.org)")
    self.assertListEqual(
        [
            ("link","https://fake.com"),
            ("another","https://workingremote.org")
        ],
        matches
    )

if __name__ == "__main__":
    unittest.main()

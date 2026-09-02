import unittest
from textnode import *
from markdown_functions import *


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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.plain_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.plain_text),
                TextNode("image", TextType.image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.plain_text),
                TextNode("second image", TextType.image, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.plain_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.image, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.plain_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.plain_text),
                TextNode("image", TextType.image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.plain_text),
                TextNode(
                    "second image", TextType.image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://wikipedia.org) with text that follows",
            TextType.plain_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.plain_text),
                TextNode("link", TextType.link, "https://boot.dev"),
                TextNode(" and ", TextType.plain_text),
                TextNode("another link", TextType.link, "https://wikipedia.org"),
                TextNode(" with text that follows", TextType.plain_text),
            ],
            new_nodes,
        )    
    
    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.plain_text)
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold_text)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.italic_text)
        self.assertEqual(
            [
                TextNode("bold", TextType.bold_text),
                TextNode(" and ", TextType.plain_text),
                TextNode("italic", TextType.italic_text),
            ],
            new_nodes,
        )

#    def test_text_to_textnodes(self):
#        nodes = text_to_textnodes(
#            "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
#        )
#        self.assertListEqual(
#            [
#               TextNode("This is ", TextType.plain_text),
#               TextNode("text", TextType.bold_text),
#               TextNode(" with an ", TextType.plain_text),
#               TextNode("italic", TextType.italic_text),
#               TextNode(" word and a ", TextType.plain_text),
#               TextNode("code block", TextType.code_text),
#                TextNode(" and an ", TextType.plain_text),
#                TextNode("image", TextType.image, "https://i.imgur.com/zjjcJKZ.png"),
#                TextNode(" and a ", TextType.plain_text),
#                TextNode("link", TextType.link, "https://boot.dev"),
#            ],
#            nodes,
#        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks2(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
This is a list
That would have stuff
with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\nThis is a list\nThat would have stuff\nwith items"
            ],
        )

    def test_markdown_to_blocks3(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
This is a list

That would have stuff
with items

Such as this
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\nThis is a list","That would have stuff\nwith items","Such as this"
            ],
        )

if __name__ == "__main__":
    unittest.main()

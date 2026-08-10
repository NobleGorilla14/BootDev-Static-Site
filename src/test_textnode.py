import unittest
from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()

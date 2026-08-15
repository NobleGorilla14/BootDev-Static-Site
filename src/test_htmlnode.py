import unittest
from htmlnode import HTMLNODE
from leafnode import LeafNode
from parentnode import ParentNode

class HTMLNode(unittest.TestCase):
    def test_neq(self):
        node = HTMLNODE("HTMLNode","",[],{})
        node2 = HTMLNODE("HTMLNode2","",[],{})
        self.assertNotEqual(node,node2)

    def testprops(self):
        node = HTMLNODE("HTMLNode3","",[],{'href':"https://www.google.com",'target':"blank"})
        self.assertDictEqual(node.props,{'href':"https://www.google.com",'target':"blank"})

    def testnoprops(self):
        node = HTMLNODE("HTMLNode4","",[],{})
        self.assertDictEqual(node.props,{})

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
    )

    def test_to_html_no_children(self):
        child_node = LeafNode("","")
        parent_node = ParentNode("p",[child_node])
        self.assertNotEqual(parent_node.to_html(),"ValueError: invalid HTML: no value.  All leaf nodes must have a value!")

if __name__ == "__main__":
    unittest.main()

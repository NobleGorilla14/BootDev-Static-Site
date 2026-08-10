import unittest
from htmlnode import HTMLNODE


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

if __name__ == "__main__":
    unittest.main()

from textnode import *
from markdown_functions import *

#new_node = TextNode("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",TextType.plain_text,)
#print(split_nodes_link(new_node))

##new_node = split_nodes_image(split_nodes_link(text))
##print(new_node)
#Test= text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
#c = 0
#for node in Test:
#    c += 1
#    print(f'For Node {c}...{node.text},{node.text_type},{node.url}')

Test = markdown_to_blocks("""This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
""")
print(Test)

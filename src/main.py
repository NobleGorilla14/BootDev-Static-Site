from textnode import TextNode, TextType

def main() -> None:
    node = TextNode("This is some anchor text", TextType.link, "https://www.boot.dev")
    print(node.text)
    print(node.text_type)
    print(node.url)
          

main()

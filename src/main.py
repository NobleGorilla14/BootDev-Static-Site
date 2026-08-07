from textnode import TextNode, TextType

def main() -> None:
    node = TextNode("This is some anchor text", TextType.link, "https://www.boot.dev")
    print(node)

main()

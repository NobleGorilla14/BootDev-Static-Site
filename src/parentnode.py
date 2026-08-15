from htmlnode import HTMLNODE

class ParentNode(HTMLNODE):
    def __init__(self, tag: str, children: list, props: dict | None = None) -> None:
        super().__init__(tag, None, children, props)
    
    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("invalid tag: no value.  All parent nodes must have a tag!")
        if not self.children:
            raise ValueError("invalid children: no value.  All parent nodes must child nodes!")
        children_html = ""
        for child in self.children:
            children_html = children_html + child.to_html()
        return f'<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>'

    def __repr__(self):
         return f"ParentNode({self.tag}, {self.children}, {self.props})"

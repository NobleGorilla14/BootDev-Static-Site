class HTMLNODE:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list | None = None, props: dict | None = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        raise NotImplementedError("{self} is not implemented, there should be something here!")

    
    def props_to_html(self):
        if not self.props:
            return ""
        else:
            return " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())

    def __repr__(self):
        print(f'Node(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r}')

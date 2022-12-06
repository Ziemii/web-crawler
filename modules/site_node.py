class SiteNode:
    """
    Node structure with value: str and children: list[SiteNode] properties.
    """
    def __init__(self, value):
        self.value: str = value
        self.children: list[SiteNode] = []

    def add_child(self, site_node) -> None:
        """Adds node to children pool"""
        self.children.append(site_node)

    def children_count(self) -> int:
        """Returns number of child nodes"""
        return len(self.children)

    def __str__(self, level=0):
        node_string = "\t" * level + self.value + f" ({len(self.children)})" + "\n"
        for child in self.children:
            node_string += child.__str__(level + 1)
        return node_string

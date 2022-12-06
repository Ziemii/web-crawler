import unittest
from modules.site_node import SiteNode


class TestSiteNode(unittest.TestCase):
    def setUp(self):
        self.root_node = SiteNode("root")
        self.subroot_1 = SiteNode("subroot_1")
        self.subroot_1_1 = SiteNode("subroot_1_1")
        self.subroot_1_2 = SiteNode("subroot_1_2")
        self.subroot_1_2_1 = SiteNode("subroot_1_2_1")
        self.subroot_2 = SiteNode("subroot_2")

        self.root_node.add_child(self.subroot_1)
        self.root_node.add_child(self.subroot_2)
        self.subroot_1.add_child(self.subroot_1_1)
        self.subroot_1.add_child(self.subroot_1_2)
        self.subroot_1_2.add_child(self.subroot_1_2_1)

    def test_site_add_child(self):
        initial_root_children_count = len(self.root_node.children)
        new_node = SiteNode("subroot_3")
        self.root_node.add_child(new_node)
        root_children_count_after_add_child = len(self.root_node.children)

        self.assertTrue((new_node in self.root_node.children))
        self.assertEqual(
            root_children_count_after_add_child, initial_root_children_count + 1
        )

    def test_site_node_children_count(self):
        self.assertEqual(self.root_node.children_count(), len(self.root_node.children))

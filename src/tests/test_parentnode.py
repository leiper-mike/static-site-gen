import unittest

from src.parentnode import ParentNode
from src.leafnode import LeafNode

class TestParentNode(unittest.TestCase):
     leaves = [LeafNode("b","This is a props test",props={"href":"https://www.google.com"}), LeafNode("i","This is a test"), LeafNode("","This is a no tag test")]
     parents = [ParentNode("p", leaves), ParentNode("p", leaves,props={"href":"https://www.google.com"}), ParentNode("p", [leaves[2],leaves[0],leaves[1]])]

     def test_no_tag(self):
          parent = ParentNode("", self.leaves)
          with self.assertRaises(ValueError) as err:
               parent.to_html()
          self.assertEqual(err.exception.__str__(), "ParentNodes must have a tag initialized")
     def test_no_children(self):
          parent = ParentNode("p",[])
          with self.assertRaises(ValueError) as err:
               parent.to_html()
          self.assertEqual(err.exception.__str__(), "ParentNodes must have children")
          e = ValueError("ParentNodes must have children")
     def test_one_leaf(self):
          parent = ParentNode("p", [self.leaves[0]])
          str = parent.to_html()
          self.assertEqual(str,"<p><b href=\"https://www.google.com\">This is a props test</b></p>")
     def test_multiple_leaves(self):
          parent = ParentNode("p", self.leaves)
          str = parent.to_html()
          self.assertEqual(str,"<p><b href=\"https://www.google.com\">This is a props test</b><i>This is a test</i>This is a no tag test</p>")
     def test_one_parent(self):
          parent = ParentNode("h1", [self.parents[0]])
          str = parent.to_html()
          self.assertEqual(str, "<h1><p><b href=\"https://www.google.com\">This is a props test</b><i>This is a test</i>This is a no tag test</p></h1>")
     def test_multiple_parents(self):
          parent = ParentNode("h1", self.parents)
          str = parent.to_html()
          #I'm regretting using such long test variables...
          result = ("<h1><p><b href=\"https://www.google.com\">This is a props test</b><i>This is a test</i>This is a no tag test</p>"
                    "<p href=\"https://www.google.com\"><b href=\"https://www.google.com\">This is a props test</b><i>This is a test</i>This is a no tag test</p>"
                    "<p>This is a no tag test<b href=\"https://www.google.com\">This is a props test</b><i>This is a test</i></p></h1>")
          self.assertEqual(str,result)
     def test_nested_parents(self):
          parent = ParentNode("h1",[ParentNode("h2",[ParentNode("h3",[self.leaves[0]])])])
          str = parent.to_html()
          self.assertEqual(str, "<h1><h2><h3><b href=\"https://www.google.com\">This is a props test</b></h3></h2></h1>")
if __name__ == "__main__":
     unittest.main()
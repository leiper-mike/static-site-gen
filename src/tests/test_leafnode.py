import unittest

from src.leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
     def test_no_tag(self):
          leaf = LeafNode("", "test")
          str = leaf.to_html()
          self.assertEqual(str, "test")
     def test_no_props(self):
          leaf = LeafNode("p","test")
          str = leaf.to_html()
          self.assertEqual(str,"<p>test</p>")
     def test_bad_props(self):
          leaf = LeafNode("p","test",["href","https://www.google.com"])
          str = leaf.to_html()
          self.assertEqual(str,"<p>test</p>")
     def test_props(self):
          leaf = LeafNode("p","test",props={"href":"https://www.google.com"})
          str = leaf.to_html()
          self.assertEqual(str,"<p href=\"https://www.google.com\">test</p>")
          
if __name__ == "__main__":
     unittest.main()
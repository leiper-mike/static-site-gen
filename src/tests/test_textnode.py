import unittest

from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
     def test_eq(self):
          node = TextNode("This is a text node", TextType.BOLD)
          node2 = TextNode("This is a text node", TextType.BOLD)
          self.assertEqual(node, node2)
     def test_url_eq(self):
          node = TextNode("This is a text node", TextType.BOLD, url=None)
          node2 = TextNode("This is a text node", TextType.BOLD)
          self.assertEqual(node, node2)
     def test_url_neq(self):
          node = TextNode("This is a text node", TextType.BOLD, url="http://url.com")
          node2 = TextNode("This is a text node", TextType.BOLD)
          self.assertNotEqual(node, node2)
     def test_type_neq(self):
          node = TextNode("This is a text node", TextType.BOLD)
          node2 = TextNode("This is a text node", "bold")
          self.assertNotEqual(node, node2)
if __name__ == "__main__":
     unittest.main()
import unittest

from src.textnode import TextNode, TextType
from src.leafnode import LeafNode

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
     def test_to_html_node(self):
          node = TextNode("This is a text node", TextType.BOLD)
          node2 = TextNode("This is a text node", TextType.BOLD, url="https://www.google.com")
          leaf1 = node.to_html_node()
          leaf2 = node2.to_html_node()
          self.assertEqual(leaf1,leaf2)
          self.assertIsInstance(leaf1,LeafNode)
          with self.assertRaises(TypeError) as e:
               TextNode("test", "wrong").to_html_node()
          self.assertEqual(str(e.exception), "text_type must be a valid member of the TextType enum")
     def test_to_html_node_types(self):
          leaf1 = TextNode("This is a text node", TextType.TEXT).to_html_node()
          leaf2 = TextNode("This is a text node", TextType.BOLD).to_html_node()
          leaf3 = TextNode("This is a text node", TextType.ITALIC).to_html_node()
          leaf4 = TextNode("This is a text node", TextType.CODE).to_html_node()
          leaf5 = TextNode("This is a text node", TextType.LINK, url="https://www.google.com").to_html_node()
          leaf6 = TextNode("This is a text node", TextType.IMAGE, url="https://www.google.com").to_html_node()
          self.assertEqual(leaf1.tag,"")
          self.assertEqual(leaf2.tag,"b")
          self.assertEqual(leaf3.tag,"i")
          self.assertEqual(leaf4.tag,"code")
          self.assertEqual(leaf5.tag,"a")
          self.assertEqual(leaf5.props,{"href":"https://www.google.com"})
          self.assertEqual(leaf6.props,{'alt': 'This is a text node', 'src': 'https://www.google.com'})
     def test_to_html_node_no_url(self):
          with self.assertRaises(ValueError) as e:
               TextNode("test", TextType.LINK).to_html_node()
          self.assertEqual(str(e.exception), "url must be provided for text nodes with link text type")
          with self.assertRaises(ValueError) as ex:
               TextNode("test", TextType.IMAGE).to_html_node()
          self.assertEqual(str(ex.exception), "url must be provided for text nodes with img text type")      
if __name__ == "__main__":
     unittest.main()
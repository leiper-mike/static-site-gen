import unittest
from src.htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
     def test_props_to_html(self):
          node = HTMLNode("<p>","test",props={"href":"https://www.google.com", "target":"_blank"})
          str = node.props_to_html()
          self.assertEqual(str, " href=\"https://www.google.com\" target=\"_blank\"")
     def test_none_props_to_html(self):
          node = HTMLNode("<p>","test")
          with self.assertRaises(TypeError):
               node.props_to_html()
     def test_empty_props_to_html(self):
          node = HTMLNode("<p>","test", props={})
          str = node.props_to_html()
          self.assertEqual(str,"")
     def test_repr(self):
          node1 = HTMLNode()
          node2 = HTMLNode("<p>")
          node3 = HTMLNode("<p>","test",)
          node4 = HTMLNode("<p>","test",[node1])
          node5 = HTMLNode("<p>","test",[node1],props={'href':"https://www.google.com"})
          self.assertEqual(repr(node1), "HTMLNode(tag:None, value:None, children:None, props:None)")
          self.assertEqual(repr(node2), "HTMLNode(tag:<p>, value:None, children:None, props:None)")
          self.assertEqual(repr(node3), "HTMLNode(tag:<p>, value:test, children:None, props:None)")
          self.assertEqual(repr(node4), "HTMLNode(tag:<p>, value:test, children:[HTMLNode(tag:None, value:None, children:None, props:None)], props:None)")
          self.assertEqual(repr(node5), "HTMLNode(tag:<p>, value:test, children:[HTMLNode(tag:None, value:None, children:None, props:None)], props:{'href': 'https://www.google.com'})")

if __name__ == "__main__":
     unittest.main()
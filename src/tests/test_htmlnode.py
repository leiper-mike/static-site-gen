import unittest
from src.htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
     def test_props_to_html(self):
          node = HTMLNode("p","test",props={"href":"https://www.google.com", "target":"_blank"})
          str = node.props_to_html()
          self.assertEqual(str, " href=\"https://www.google.com\" target=\"_blank\"")
     def test_none_props_to_html(self):
          node = HTMLNode("p","test")
          with self.assertRaises(TypeError):
               node.props_to_html()
     def test_empty_props_to_html(self):
          node = HTMLNode("p","test", props={})
          str = node.props_to_html()
          self.assertEqual(str,"")
     def test_repr(self):
          node1 = HTMLNode()
          node2 = HTMLNode("p")
          node3 = HTMLNode("p","test",)
          node4 = HTMLNode("p","test",[node1])
          node5 = HTMLNode("p","test",[node1],props={'href':"https://www.google.com"})
          self.assertEqual(repr(node1), "HTMLNode(tag:None, value:None, children:None, props:None)")
          self.assertEqual(repr(node2), "HTMLNode(tag:p, value:None, children:None, props:None)")
          self.assertEqual(repr(node3), "HTMLNode(tag:p, value:test, children:None, props:None)")
          self.assertEqual(repr(node4), "HTMLNode(tag:p, value:test, children:[HTMLNode(tag:None, value:None, children:None, props:None)], props:None)")
          self.assertEqual(repr(node5), "HTMLNode(tag:p, value:test, children:[HTMLNode(tag:None, value:None, children:None, props:None)], props:{'href': 'https://www.google.com'})")
     def test_eq(self):
          
          node1 = HTMLNode("p","test")
          node2 = HTMLNode("p","test")
          self.assertEqual(node1,node2)
          node3 = HTMLNode("p","test1")
          node4 = HTMLNode("p","test")
          self.assertNotEqual(node3,node4)
          node5 = HTMLNode("p","test", props={'href':"https://www.google.com"})
          node6 = HTMLNode("p","test", props={'href':"https://www.google.com"})
          self.assertEqual(node5,node6)
          node7 = HTMLNode("p","test", props={'href':"https://www.google.com"})
          node8 = HTMLNode("p","test", props={'href':"https://www.youtube.com"})
          self.assertNotEqual(node7,node8)
          node9 = HTMLNode("p","test",[node1,node8])
          node10 = HTMLNode("p","test",[node1,node8])
          self.assertEqual(node9,node10)
          self.assertNotEqual(node1,node10)
          node11 = HTMLNode("p","test",[node10,node9])
          node12 = HTMLNode("p","test",[node10,node9])
          self.assertEqual(node11,node12)
          node13 = HTMLNode("p","test",[node3,node4])
          node14 = HTMLNode("p","test",[node4,node3])
          self.assertNotEqual(node13,node14)

if __name__ == "__main__":
     unittest.main()
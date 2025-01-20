import unittest

from src.textnode import TextNode, TextType
from src.utils import split_nodes_delimiter,extract_markdown_images,extract_markdown_links,split_nodes_link, split_nodes_image, text_to_textnodes

class TestUtils(unittest.TestCase):
     
     def test_split_nodes(self):
          inputs = [
                    (TextNode("test `code` test", TextType.TEXT), "`", TextType.CODE),
                    (TextNode("test *italics* test", TextType.TEXT), "*", TextType.ITALIC),
                    (TextNode("test **bold** test", TextType.TEXT), "**", TextType.BOLD),
                    (TextNode("code", TextType.CODE), "`", TextType.CODE),
                    (TextNode("test `code`", TextType.TEXT), "`", TextType.CODE),
                    (TextNode("`code`", TextType.TEXT), "`", TextType.CODE),
                    (TextNode("test `code` test *italics* test **bold** test", TextType.TEXT), "**", TextType.BOLD)
                    ]
          outputs = [
                    [TextNode("test ", TextType.TEXT),TextNode("code", TextType.CODE),TextNode(" test", TextType.TEXT)],
                    [TextNode("test ", TextType.TEXT),TextNode("italics", TextType.ITALIC),TextNode(" test", TextType.TEXT)],
                    [TextNode("test ", TextType.TEXT),TextNode("bold", TextType.BOLD),TextNode(" test", TextType.TEXT)],
                    [TextNode("code", TextType.CODE)],
                    [TextNode("test ", TextType.TEXT),TextNode("code", TextType.CODE)],
                    [TextNode("code", TextType.CODE)],
                    [TextNode("test `code` test *italics* test ", TextType.TEXT),TextNode("bold", TextType.BOLD),TextNode(" test", TextType.TEXT)]
                    ]
          for i in range(0,len(inputs)):
               input = inputs[i]
               out = split_nodes_delimiter([input[0]],input[1],input[2])
               self.assertListEqual(out,outputs[i],i)
     def test_bold_and_italics_split_nodes(self):
          nodes = split_nodes_delimiter([TextNode("*italics* and **bold**", TextType.TEXT)],"**",TextType.BOLD)
          final = split_nodes_delimiter(nodes,"*",TextType.ITALIC)
          self.assertListEqual(final,[TextNode("italics", TextType.ITALIC),TextNode(" and ", TextType.TEXT),TextNode("bold", TextType.BOLD)])
     def test_split_nodes_bad_delim(self):
          bad_nodes = [
                    TextNode("test `code test", TextType.TEXT),
                    TextNode("test code` test", TextType.TEXT),
               ]
          for node in bad_nodes:
               with self.assertRaises(ValueError) as e:
                    split_nodes_delimiter([node],"`",TextType.CODE)
               self.assertEqual(e.exception.__str__(), "Invalid markdown syntax, missing closing/starting delimiter")
     def test_empty_str_split_nodes(self):
          res = split_nodes_delimiter([TextNode("", TextType.TEXT)],"`",TextType.CODE)
          self.assertListEqual([],res)
     def test_no_delims_split_nodes(self):
          res = split_nodes_delimiter([TextNode("test code test", TextType.TEXT)],"`",TextType.CODE)
          self.assertListEqual(res, [TextNode("test code test", TextType.TEXT)])

class TestExtractMarkdown(unittest.TestCase):
     def test_extract_markdown_images(self):
          str = "this is a markdown image: ![image](https://www.image.com)"
          res = extract_markdown_images(str)
          self.assertEqual(res[0], ("image","https://www.image.com"))
     def test_extract_markdown_images_none(self):
          str = "this is not a markdown image: not an image"
          res = extract_markdown_images(str)
          self.assertListEqual(res,[])
     def test_extract_markdown_images_plaintext(self):
          str = "this is not a markdown image: https://www.image.com"
          res = extract_markdown_images(str)
          self.assertListEqual(res,[])
     def test_extract_markdown_images_wrong_format(self):
          str = "this is not a markdown image: [image](https://www.image.com), neither is this: ![link]https://www.link.com, nor this: link(https://www.link.com)"
          res = extract_markdown_images(str)
          self.assertListEqual(res,[])

     def test_extract_markdown_links(self):
          str = "this is a markdown link: [link](https://www.link.com)"
          res = extract_markdown_links(str)
          self.assertEqual(res[0], ("link","https://www.link.com"))
     def test_extract_markdown_links_multiple(self):
          str = "this is a markdown link: [link](https://www.link.com) test [link1](https://www.link1.com) "
          res = extract_markdown_links(str)
          self.assertListEqual(res, [("link","https://www.link.com"),("link1","https://www.link1.com")])

     def test_extract_markdown_links_none(self):
          str = "this is not a markdown link: not an link"
          res = extract_markdown_links(str)
          self.assertListEqual(res,[])
     def test_extract_markdown_links_plaintext(self):
          str = "this is not a markdown link: https://www.link.com"
          res = extract_markdown_links(str)
          self.assertListEqual(res,[])
     def test_extract_markdown_links_wrong_format(self):
          str = "this is not a markdown link: ![link](https://www.link.com), neither is this: [link]https://www.link.com, nor this: link(https://www.link.com)"
          res = extract_markdown_links(str)
          self.assertListEqual(res,[])

class TestSplitNodesImagesLinks(unittest.TestCase):
     def test_split_nodes_link(self):
          res = split_nodes_link([TextNode("link: [link](https://www.link.com)",TextType.TEXT)])
          correct = [TextNode("link: ",TextType.TEXT), TextNode("link",TextType.LINK, url="https://www.link.com")]
          self.assertListEqual(res, correct)
     def test_split_nodes_link_words_after_link(self):
          res = split_nodes_link([TextNode("link: [link](https://www.link.com) test",TextType.TEXT)])
          correct = [TextNode("link: ",TextType.TEXT), TextNode("link",TextType.LINK, url="https://www.link.com"),TextNode(" test",TextType.TEXT)]
          self.assertListEqual(res, correct)
     def test_split_nodes_link_multiple(self):
          res = split_nodes_link([TextNode("link: [link](https://www.link.com) other link: [link1](https://www.link1.com) other other link: [link2](https://www.link2.com)",TextType.TEXT)])
          correct = [TextNode("link: ",TextType.TEXT), TextNode("link",TextType.LINK, url="https://www.link.com"),
                     TextNode(" other link: ",TextType.TEXT), TextNode("link1",TextType.LINK, url="https://www.link1.com"),
                     TextNode(" other other link: ",TextType.TEXT), TextNode("link2",TextType.LINK, url="https://www.link2.com"),]
          self.assertListEqual(res, correct)
     def test_split_nodes_link_none(self):
          res = split_nodes_link([TextNode("no links :D",TextType.TEXT)])
          self.assertListEqual(res,[TextNode("no links :D",TextType.TEXT)])

     def test_split_nodes_image(self):
          res = split_nodes_image([TextNode("image: ![image](https://www.image.com)",TextType.TEXT)])
          correct = [TextNode("image: ",TextType.TEXT), TextNode("image",TextType.IMAGE, url="https://www.image.com")]
          self.assertListEqual(res, correct)
     def test_split_nodes_image_words_after_image(self):
          res = split_nodes_image([TextNode("image: ![image](https://www.image.com) test",TextType.TEXT)])
          correct = [TextNode("image: ",TextType.TEXT), TextNode("image",TextType.IMAGE, url="https://www.image.com"),TextNode(" test",TextType.TEXT)]
          self.assertListEqual(res, correct)
     def test_split_nodes_image_multiple(self):
          res = split_nodes_image([TextNode("image: ![image](https://www.image.com) other image: ![image1](https://www.image1.com) other other image: ![image2](https://www.image2.com)",TextType.TEXT)])
          correct = [TextNode("image: ",TextType.TEXT), TextNode("image",TextType.IMAGE, url="https://www.image.com"),
                     TextNode(" other image: ",TextType.TEXT), TextNode("image1",TextType.IMAGE, url="https://www.image1.com"),
                     TextNode(" other other image: ",TextType.TEXT), TextNode("image2",TextType.IMAGE, url="https://www.image2.com"),]
          self.assertListEqual(res, correct)
     def test_split_nodes_image_none(self):
          res = split_nodes_image([TextNode("no images :D",TextType.TEXT)])
          self.assertListEqual(res,[TextNode("no images :D",TextType.TEXT)])

class TestTextToTextnodes(unittest.TestCase):
     def test_all(self):
          text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
          res = text_to_textnodes(text)
          correct = [
               TextNode("This is ", TextType.TEXT),
               TextNode("text", TextType.BOLD),
               TextNode(" with an ", TextType.TEXT),
               TextNode("italic", TextType.ITALIC),
               TextNode(" word and a ", TextType.TEXT),
               TextNode("code block", TextType.CODE),
               TextNode(" and an ", TextType.TEXT),
               TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
               TextNode(" and a ", TextType.TEXT),
               TextNode("link", TextType.LINK, "https://boot.dev")
          ]
          self.assertListEqual(res,correct)
     def test_none(self):
          text = "This is text with an italic word and a code block and an obi wan image and a link"
          res = text_to_textnodes(text)
          correct = [
               TextNode("This is text with an italic word and a code block and an obi wan image and a link", TextType.TEXT)
          ]
          self.assertListEqual(res,correct)

     def test_italics_bold(self):
          text = "This is **text** with an *italic* word and a code block and an obi wan image and a link"
          res = text_to_textnodes(text)
          correct = [
               TextNode("This is ", TextType.TEXT),
               TextNode("text", TextType.BOLD),
               TextNode(" with an ", TextType.TEXT),
               TextNode("italic", TextType.ITALIC),
               TextNode(" word and a code block and an obi wan image and a link", TextType.TEXT)
          ]
          self.assertListEqual(res,correct)

     def test_image(self):
          text = "This is text with an italic word and a code block and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a link"
          res = text_to_textnodes(text)
          correct = [
               TextNode("This is text with an italic word and a code block and an ", TextType.TEXT),
               TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
               TextNode(" and a link", TextType.TEXT)
          ]
          self.assertListEqual(res,correct)
     def test_link(self):
          text = "This is text with an italic word and a code block and an obi wan image and a [link](https://boot.dev)"
          res = text_to_textnodes(text)
          correct = [
               TextNode("This is text with an italic word and a code block and an obi wan image and a ", TextType.TEXT),
               TextNode("link", TextType.LINK, "https://boot.dev")
          ]
          self.assertListEqual(res,correct)
     def test_code(self):
          text = "This is text with an italic word and a `code block` and an obi wan image and a link"
          res = text_to_textnodes(text)
          correct = [
               TextNode("This is text with an italic word and a ", TextType.TEXT),
               TextNode("code block", TextType.CODE),
               TextNode(" and an obi wan image and a link", TextType.TEXT)
          ]
          self.assertListEqual(res,correct)
     def test_delim_errs(self):
          text1 = "this has a *bad delimiter"
          with self.assertRaises(ValueError) as e:
               text_to_textnodes(text1)
          self.assertEqual(e.exception.__str__(), "Invalid markdown syntax, missing closing/starting delimiter")
          text1 = "this has a **bad delimiter"
          with self.assertRaises(ValueError) as e:
               text_to_textnodes(text1)
          self.assertEqual(e.exception.__str__(), "Invalid markdown syntax, missing closing/starting delimiter")
          text1 = "this has a `bad delimiter"
          with self.assertRaises(ValueError) as e:
               text_to_textnodes(text1)
          self.assertEqual(e.exception.__str__(), "Invalid markdown syntax, missing closing/starting delimiter")
if __name__ == "__main__":
     unittest.main()
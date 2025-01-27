import unittest

from src.textnode import TextNode, TextType
from src.utils import *

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

class TestMarkdownToBlocks(unittest.TestCase):
     def test(self):
          str = """# This is a heading

               This is a paragraph of text. It has some **bold** and *italic* words inside of it.

               * This is the first list item in a list block\n* This is a list item\n* This is another list item"""
          ret = markdown_to_blocks(str)
          correct = ["# This is a heading",
                    "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                    "* This is the first list item in a list block\n* This is a list item\n* This is another list item"]
          self.assertListEqual(ret,correct)
     def multiline_test(self):
          str = """# This is a really long \nheading

               This is a paragraph of text.\nIt has some **bold** and *italic* words inside of it.

               * This is the first list item in a list block\n* This is a list item\n* This is another list item"""
          ret = markdown_to_blocks(str)
          correct = ["# This is a heading",
                    "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                    "* This is the first list item in a list block\n* This is a list item\n* This is another list item"]
          self.assertListEqual(ret,correct)
     def test_trailing_new_lines(self):
          str = """# This is a really long \nheading\n\n\n\n\n\n

               This is a paragraph of text.\nIt has some **bold** and *italic* words inside of it.\n\n\n\n

               * This is the first list item in a list block\n* This is a list item\n* This is another list item\n\n\n\n\n"""
          ret = markdown_to_blocks(str)
          correct = ["# This is a really long \nheading",
                    "This is a paragraph of text.\nIt has some **bold** and *italic* words inside of it.",
                    "* This is the first list item in a list block\n* This is a list item\n* This is another list item"]
          self.assertListEqual(ret,correct)
     def test_leading_new_lines(self):
          str = """\n\n\n\n\n\n\n# This is a really long \nheading

               This is a paragraph of text.\nIt has some **bold** and *italic* words inside of it.\n\n\n\n

               * This is the first list item in a list block\n* This is a list item\n* This is another list item"""
          ret = markdown_to_blocks(str)
          correct = ["# This is a really long \nheading",
                    "This is a paragraph of text.\nIt has some **bold** and *italic* words inside of it.",
                    "* This is the first list item in a list block\n* This is a list item\n* This is another list item"]
          self.assertListEqual(ret,correct)
class TestBlockToBlockType(unittest.TestCase):
     def test_heading(self):
          block = "###### Heading"
          self.assertEqual(block_to_block_type(block),"heading")
     def test_code(self):
          block = "```code code code```"
          self.assertEqual(block_to_block_type(block),"code")
     def test_quote(self):
          block = "> don't believe everything you read on the internet \n>- abraham lincoln"
          self.assertEqual(block_to_block_type(block),"quote")
     def test_ulist(self):
          block = "* list thingy\n- other list thingy\n* yet another list thingy"
          self.assertEqual(block_to_block_type(block),"ulist")
     def test_olist(self):
          block = "1. list thingy\n2. other list thingy\n3. yet another list thingy"
          self.assertEqual(block_to_block_type(block),"olist")
     def test_paragraph(self):
          block = "paragraph paragraph"
          self.assertEqual(block_to_block_type(block),"paragraph")
     def test_paragraph_fallback(self):
          block = "#nospace\n``notenoughticks``\n>other things besides quotes\n* other things besides ulist\n1. other things besides olist"
          self.assertEqual(block_to_block_type(block),"paragraph")
     def test_out_of_order_olist(self):
          block = "1. list\n2. list\n5. 3 m'lord!"
          self.assertEqual(block_to_block_type(block),"paragraph")
     def test_quote_ulist_olist(self):
          block = "1. list\n> list\n- 3 m'lord!"
          self.assertEqual(block_to_block_type(block),"paragraph")

class TestMarkdownToHTML(unittest.TestCase):
     def test_one_header(self):
          markdown = "# This is a **header**, which has *children*"
          result = markdown_to_html(markdown)
          correct = ParentNode("div",[ParentNode("h1",[
               LeafNode("","This is a "),
               LeafNode("b","header"),
               LeafNode("",", which has "),
               LeafNode("i","children")])])
          self.assertEqual(result,correct)
     def test_multiple_header(self):
          markdown = "# This is a **header**, which has *children*\n\n### h3"
          result = markdown_to_html(markdown)
          correct = ParentNode("div",[
               ParentNode("h1",[
                    LeafNode("","This is a "),
                    LeafNode("b","header"),
                    LeafNode("",", which has "),
                    LeafNode("i","children")]),
               ParentNode("h3",[
                    LeafNode("","h3")])])
          self.assertEqual(result,correct)
     def test_multiline_header(self):
          markdown = "# This is a **header**, which has *children*\nand multiple lines"
          result = markdown_to_html(markdown)
          correct = ParentNode("div",[
               ParentNode("h1",[
                    LeafNode("","This is a "),
                    LeafNode("b","header"),
                    LeafNode("",", which has "),
                    LeafNode("i","children"),
                    LeafNode("br",""),
                    LeafNode("", "and multiple lines")])])
          self.assertEqual(result,correct)     
     def test_code(self):
          markdown = "```This is a **code block**, which has *children*```"
          result = markdown_to_html(markdown)
          correct = ParentNode("div",[
               ParentNode("code",[
                    LeafNode("","This is a "),
                    LeafNode("b","code block"),
                    LeafNode("",", which has "),
                    LeafNode("i","children")])])
          self.assertEqual(result,correct)
     def test_multiple_code(self):
          markdown = "```This is a **code block**, which has *children*```\n\n```This is a **code block**, which has *children*```"
          result = markdown_to_html(markdown)
          correct = ParentNode("div",[
               ParentNode("code",[
                    LeafNode("","This is a "),
                    LeafNode("b","code block"),
                    LeafNode("",", which has "),
                    LeafNode("i","children")]),
               ParentNode("code",[
                    LeafNode("","This is a "),
                    LeafNode("b","code block"),
                    LeafNode("",", which has "),
                    LeafNode("i","children")])])
          self.assertEqual(result,correct)
     def test_multiline_code(self):
          markdown = "```This is a **code block**, which has *children*\nprint('hello world')```"
          result = markdown_to_html(markdown)
          correct = ParentNode("div",[
               ParentNode("code",[
                    LeafNode("","This is a "),
                    LeafNode("b","code block"),
                    LeafNode("",", which has "),
                    LeafNode("i","children"),
                    LeafNode("br",""),
                    LeafNode("","print('hello world')")])])
          self.assertEqual(result,correct)
     def test_quote(self):
          markdown = "> This is a **block quote**, which has *children*"
          result = markdown_to_html(markdown)
          correct = ParentNode("div",[
               ParentNode("blockquote",[
                    LeafNode("","This is a "),
                    LeafNode("b","block quote"),
                    LeafNode("",", which has "),
                    LeafNode("i","children")])])
          self.assertEqual(result,correct)
     def test_multiline_quote(self):
          markdown = "> This is a **block quote**, which has *children*\n> - Abraham Lincoln"
          result = markdown_to_html(markdown)
          correct = ParentNode("div",[
               ParentNode("blockquote",[
                    LeafNode("","This is a "),
                    LeafNode("b","block quote"),
                    LeafNode("",", which has "),
                    LeafNode("i","children"),
                    LeafNode("br",""),
                    LeafNode("","- Abraham Lincoln")])])
          self.assertEqual(result,correct)
     def test_ulist(self):
          markdown = "* This is an **unordered list**, which has *children*\n- Abraham Lincoln"
          result = markdown_to_html(markdown)
          correct = ParentNode("div",[
               ParentNode("ul",[
                    ParentNode("li",[
                         LeafNode("","This is an "),
                         LeafNode("b","unordered list"),
                         LeafNode("",", which has "),
                         LeafNode("i","children")]),
                    ParentNode("li",[
                         LeafNode("","Abraham Lincoln")])])])
          self.assertEqual(result,correct)
     def test_olist(self):
          markdown = "1. This is an **ordered list**, which has *children*\n2. Abraham Lincoln"
          result = markdown_to_html(markdown)
          correct = ParentNode("div",[
               ParentNode("ol",[
                    ParentNode("li",[
                         LeafNode("","This is an "),
                         LeafNode("b","ordered list"),
                         LeafNode("",", which has "),
                         LeafNode("i","children")]),
                    ParentNode("li",[
                         LeafNode("","Abraham Lincoln")])])])
          self.assertEqual(result,correct)
     def test_paragraph(self):
          markdown = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
          result = markdown_to_html(markdown)
          correct = ParentNode("div",[
               ParentNode("p",[
                    LeafNode("","This is "),
                    LeafNode("b","text"),
                    LeafNode(""," with an "),
                    LeafNode("i","italic"),
                    LeafNode(""," word and a "),
                    LeafNode("code","code block"),
                    LeafNode(""," and an "),
                    LeafNode("img","", props={"src":"https://i.imgur.com/fJRm4Vk.jpeg", "alt":"obi wan image"}),
                    LeafNode(""," and a "),
                    LeafNode("a","link", props={"href":"https://boot.dev"}),
               ])])
          self.assertEqual(result,correct)
     def test_outer_tag(self):
          markdown = "test"
          result = markdown_to_html(markdown, parentTag="p")
          correct = ParentNode("p",[ParentNode("p",[LeafNode("","test")])])
          self.assertEqual(result,correct)
     
if __name__ == "__main__":
     unittest.main()
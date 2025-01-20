from src.textnode import TextNode, TextType
import re

def text_to_textnodes(text):
     init = TextNode(text,TextType.TEXT)
     return split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter(split_nodes_link(split_nodes_image([init])),"**",TextType.BOLD),"*",TextType.ITALIC),"`",TextType.CODE)




def split_nodes_delimiter(old_nodes, delimiter, text_type):
      new_nodes = []
      for node in old_nodes:
          if node.text_type != TextType.TEXT:
               new_nodes.append(node)
               continue
          nodes = node.text.split(delimiter)
          # nodes length should never be even, means we were missing a closing/starting delimiter
          if len(nodes) % 2 == 0:
               raise ValueError("Invalid markdown syntax, missing closing/starting delimiter")
          for i in range(0,len(nodes)):
               #every other string should be the type we're looking for
               if i % 2 != 0:
                    new_nodes.append(TextNode(nodes[i],text_type=text_type))
               #don't append empty strings as text nodes     
               elif nodes[i] != "":
                    new_nodes.append(TextNode(nodes[i],text_type=TextType.TEXT))
      return new_nodes

def extract_markdown_images(text):
     return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
     
def extract_markdown_links(text):
     return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def split_nodes_image(old_nodes):
     new_nodes = []
     for node in old_nodes:
          if node.text_type != TextType.TEXT:
               new_nodes.append(node)
               continue
          text = node.text
          while extract_markdown_images(text):
               image = extract_markdown_images(text)[0]
               nodes = text.split(f"![{image[0]}]({image[1]})",1)
               new_nodes.append(TextNode(nodes[0],TextType.TEXT))
               new_nodes.append(TextNode(image[0],TextType.IMAGE,url=image[1]))
               text = nodes[1]
          if text:
               new_nodes.append(TextNode(text,TextType.TEXT))
     return new_nodes

def split_nodes_link(old_nodes):
     new_nodes = []
     for node in old_nodes:
          if node.text_type != TextType.TEXT:
               new_nodes.append(node)
               continue
          text = node.text
          while extract_markdown_links(text):
               link = extract_markdown_links(text)[0]
               nodes = text.split(f"[{link[0]}]({link[1]})",1)
               new_nodes.append(TextNode(nodes[0],TextType.TEXT))
               new_nodes.append(TextNode(link[0],TextType.LINK,url=link[1]))
               text = nodes[1]
          if text:
               new_nodes.append(TextNode(text,TextType.TEXT))
     return new_nodes

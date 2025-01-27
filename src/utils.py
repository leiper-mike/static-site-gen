from src.textnode import TextNode, TextType
from src.leafnode import LeafNode
from src.parentnode import ParentNode
import os
import shutil
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
               raise ValueError(f"Invalid markdown syntax, missing closing/starting delimiter")
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

def markdown_to_blocks(markdown):
     #two newlines indicate a blank line
     init = markdown.split("\n\n")
     #strip each line of trailing/leading whitespace (includes new lines) 
     maplist = list(map(lambda str: str.strip(), init))
     #filter out empty strings
     filterlist = list(filter(lambda s: s, maplist))
     return filterlist

def block_to_block_type(block):
     if block[:3] == "```" and block[-3:] == "```":
          return "code"
     elif "# " in block[:7]:
          return "heading"
     isquote = False
     isulist = False
     isolist = False
     count = 1
     for line in block.split("\n"):
          if line[0] == ">" and not isolist and not isulist:
               isquote = True
          elif not isolist and not isquote and (line[0:2] == "* " or line[0:2] == "- "):
               isulist = True
          elif not isulist and not isquote and line[:3] == f"{count}. ":
               isolist = True
               count+=1
          else:
               isquote = False
               isulist = False
               isolist = False
               break
               
     if isquote:
          return "quote"
     elif isulist:
          return "ulist"
     elif isolist:
          return "olist"
     else:
          return "paragraph"

def markdown_to_html(markdown, parentTag = "div"):
     blocks = markdown_to_blocks(markdown)
     children = []
     for block in blocks:
          blocktype = block_to_block_type(block)
          #print(blocktype)
          children.append(block_to_html(block, blocktype))
     return ParentNode(parentTag,children)
          
def block_to_html(block, blocktype):
     if blocktype == "heading":
          hlevel = block.count("#")
          return ParentNode(f"h{hlevel}", block_to_html_with_br(block[hlevel+1:]))
     elif blocktype == "code":
          return ParentNode("code", block_to_html_with_br(block[3:-3]))
     elif blocktype == "quote":
          #remove leading >'s
          block = "\n".join(map(lambda b: b.lstrip("> "),block.split("\n")))
          return ParentNode("blockquote",block_to_html_with_br(block))
     elif blocktype == "ulist":
          items = block.split("\n")
          ret = []
          for item in items:
               item = item[2:]
               leaves = text_to_children(item)
               ret.append(ParentNode("li", leaves))
          return ParentNode("ul",ret)
     elif blocktype == "olist":
          items = block.split("\n")
          ret = []
          for item in items:
               leaves = text_to_children(item[item.find(". ") + 2:])
               ret.append(ParentNode("li", leaves))
          return ParentNode("ol",ret)
     elif blocktype == "paragraph":
          return ParentNode("p", block_to_html_with_br(block))

def text_to_children(text):
     return list(map(lambda t: t.to_html_node(), text_to_textnodes(text)))


#splits block into lines, inserts <br> between lines, converts each line into html
def block_to_html_with_br(block):
     leaves = []
     lines = block.split("\n")
     for i in range(0,len(lines)):
          leaves.extend(text_to_children(lines[i]))
          #add a new line between each line, except the last
          if i != len(lines)-1 and len(lines) > 1:
               leaves.append(LeafNode("br",""))
     return leaves

def clean_public():
     shutil.rmtree("./public")
     os.mkdir("./public")

def copy_static_public():
     clean_public()
     copy("./static")

def copy(path):
     paths = os.listdir(path)
     publicpath = path.replace("static","public",1)
     for p in paths:
          relPath = f"{path}/{p}"
          publicRelPath = f"{publicpath}/{p}"
          if os.path.isfile(relPath):
               print(f"Copying: {relPath} to {publicRelPath}")
               shutil.copy(f"{relPath}",f"{publicRelPath}")
          elif os.path.isdir(relPath):
               print(f"moving to dir: {relPath}")
               os.mkdir(publicRelPath)
               copy(f"{relPath}")

def extract_title(markdown):
     lines = markdown.split("\n")
     for line in lines:
          if line.count("#") == 1 and "# " in line:
               return line.strip("# ")
     raise ValueError("No title found in the markdown")

def generate_page(from_path, template_path, to_path):
     print(f"Generating page from {from_path} to {to_path}, using {template_path}")
     with open(from_path, "r") as content_file:
          content = content_file.read()
          with open(template_path, "r") as template_file:
               template = template_file.read()
               html = markdown_to_html(content)
               title = extract_title(content)
               template = template.replace(" {{ Title }} ", title)
               template = template.replace("{{ Content }}", html.to_html())
               # remove the last path which would be the file name
               to_folders = "/".join(to_path.split("/")[:-1])
               os.makedirs(to_folders, exist_ok=True)
               with open(to_path, "w") as to_file:
                    to_file.write(template)

def generate_pages_recursive(from_path_dir, template_path, to_path_dir):
     paths = os.listdir(from_path_dir)
     for path in paths:
          relPath = f"{from_path_dir}/{path}"
          path = path.replace(".md",".html")
          relToPath = f"{to_path_dir}/{path}"
          if os.path.isfile(relPath):
               generate_page(relPath,template_path,relToPath)
          else:
               generate_pages_recursive(relPath,template_path,relToPath)

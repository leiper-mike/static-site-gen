from enum import Enum

from src.leafnode import LeafNode
class TextType(Enum):
     TEXT = "text"
     BOLD = "bold"
     ITALIC = "italic"
     CODE = "code"
     LINK = "link"
     IMAGE = "image"
class TextNode():
     def __init__(self, text, text_type, url = None):
          self.text = text
          self.text_type = text_type
          self.url = url
     def __eq__(self, other):
          return self.text == other.text and self.text_type == other.text_type and self.url == other.url
     def __repr__(self):
          return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
     def to_html_node(self):
          if not self.text_type in TextType:
               raise TypeError("text_type must be a valid member of the TextType enum")
          match self.text_type:
               case TextType.TEXT:
                    return LeafNode("", self.text)
               case TextType.BOLD:
                    return LeafNode("b", self.text)
               case TextType.ITALIC:
                    return LeafNode("i", self.text)
               case TextType.CODE:
                    return LeafNode("code", self.text)
               case TextType.LINK:
                    if not self.url or not isinstance(self.url,str):
                         raise ValueError("url must be provided for text nodes with link text type")
                    return LeafNode("a", self.text, {"href":self.url})
               case TextType.IMAGE:
                    if not self.url or not isinstance(self.url,str):
                         raise ValueError("url must be provided for text nodes with img text type")
                    return LeafNode("img","",{"src":self.url,"alt":self.text})
               case _:
                    raise Exception("Could not match text_type to a member of TextType enum")

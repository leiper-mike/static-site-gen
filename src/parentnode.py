from src.htmlnode import HTMLNode

class ParentNode(HTMLNode):
     def __init__(self, tag, children, props=None):
          super().__init__(tag, children=children, props=props)

     def to_html(self):
          if not self.tag:
               raise ValueError("ParentNodes must have a tag initialized")
          if not self.children:
               raise ValueError("ParentNodes must have children")
          props = ""
          try:
               props = self.props_to_html()
          except:
               pass
          ret = f"<{self.tag}{props}>"
          for child in self.children:
               ret += child.to_html()
          ret+= f"</{self.tag}>"
          return ret
     
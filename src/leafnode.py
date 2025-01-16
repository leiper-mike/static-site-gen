from htmlnode import HTMLNode

class LeafNode(HTMLNode):
     def __init__(self,tag,value,props=None):
          super().__init__(tag,value,props=props)
     def to_html(self):
          if not self.value:
               raise ValueError("All leaf nodes must have a value")
          if not self.tag:
               return self.value
          props = ""
          try:
               if self.props:
                    props = self.props_to_html()
                    return f"<{self.tag}{props}>{self.value}</{self.tag}>"
               else:
                    return f"<{self.tag}>{self.value}</{self.tag}>"
          except TypeError as e:
               print(e)
               return f"<{self.tag}>{self.value}</{self.tag}>"
          
          
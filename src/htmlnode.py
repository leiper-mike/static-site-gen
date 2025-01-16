
class HTMLNode():
     def __init__(self, tag = None, value = None, children = None, props = None):
          self.tag = tag
          self.value = value
          self.children = children
          self.props = props
     def to_html(self):
          raise NotImplementedError()
     def props_to_html(self):
          str = ""
          if not isinstance(self.props, dict):
               raise TypeError("HTMLNode object does not have a valid props dictionary initialized")
          for key in self.props:
               str += f" {key}=\"{self.props[key]}\""
          return str
     def __repr__(self):
          return f"HTMLNode(tag:{self.tag}, value:{self.value}, children:{self.children}, props:{self.props})"
     
     
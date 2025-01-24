
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
     def __eq__(self, other):
          if other.children:
               if not self.children: 
                    return False
          if self.children:
               if other.children:
                    if not len(self.children) == len(other.children):
                         return False
                    for i in range(0,len(self.children)):
                         if not self.children[i] == other.children[i]:
                              return False
               else:
                    return False     
          return self.tag == other.tag and self.value == other.value and self.props == other.props 
     
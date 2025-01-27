from src.utils import copy_static_public, generate_pages_recursive

def main():
     copy_static_public()
     generate_pages_recursive("content","template.html","public")
main()
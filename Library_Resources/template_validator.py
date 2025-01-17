import os
import sys
import html5lib
from bs4 import BeautifulSoup

class TemplateValidator:
    def __init__(self, root_path):
        self.root_path = root_path
        self.errors = []

    def validate_html_structure(self, html_content):
        """Validate HTML5 structure"""
        try:
            parser = html5lib.HTMLParser(strict=True)
            parser.parse(html_content)
            return True
        except Exception as e:
            self.errors.append(f"HTML Structure Error: {str(e)}")
            return False

    def check_required_elements(self, soup):
        """Check for required HTML elements"""
        required_elements = {
            'title': soup.find('title'),
            'meta_description': soup.find('meta', attrs={'name': 'description'}),
            'main_content': soup.find('main'),
            'header': soup.find('header'),
            'footer': soup.find('footer')
        }

        for element, found in required_elements.items():
            if not found:
                self.errors.append(f"Missing required element: {element}")

    def validate_template(self, file_path):
        """Comprehensive template validation"""
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Reset errors
        self.errors = []

        # HTML5 structure validation
        if not self.validate_html_structure(html_content):
            return False

        # BeautifulSoup parsing for deeper checks
        soup = BeautifulSoup(html_content, 'html.parser')
        self.check_required_elements(soup)

        return len(self.errors) == 0

    def validate_all_templates(self):
        """Validate all index.html files"""
        valid_templates = 0
        total_templates = 0

        for folder in os.listdir(self.root_path):
            folder_path = os.path.join(self.root_path, folder)
            if os.path.isdir(folder_path):
                template_path = os.path.join(folder_path, 'index.html')
                if os.path.exists(template_path):
                    total_templates += 1
                    if self.validate_template(template_path):
                        valid_templates += 1
                    else:
                        print(f"Validation errors in {folder}/index.html:")
                        for error in self.errors:
                            print(f"  - {error}")

        print(f"\nTemplate Validation Summary:")
        print(f"Total Templates: {total_templates}")
        print(f"Valid Templates: {valid_templates}")
        print(f"Validation Rate: {(valid_templates/total_templates)*100:.2f}%")

def main():
    root_path = r'C:\Users\ihelp\Comprehensive_Resource_Library\Comprehensive_Resource_Library\Library_Resources'
    validator = TemplateValidator(root_path)
    validator.validate_all_templates()

if __name__ == "__main__":
    main()

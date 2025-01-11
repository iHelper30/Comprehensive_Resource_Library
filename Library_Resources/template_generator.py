import os
import json
import markdown2

class TemplateGenerator:
    def __init__(self, root_path):
        self.root_path = root_path
        self.template_path = os.path.join(root_path, '02_Purpose_of_Library', 'index.html')

    def generate_metadata(self, folder_name):
        """Generate metadata based on folder name and content"""
        return {
            "title": folder_name.split('_', 1)[1].replace('_', ' '),
            "subtitle": f"Comprehensive guide to {folder_name.split('_', 1)[1].lower()}",
            "meta_description": f"Resources and insights for {folder_name.split('_', 1)[1].lower()}",
            "keywords": folder_name.split('_', 1)[1].lower().split()
        }

    def read_readme(self, folder_path):
        """Read and convert README.md to HTML"""
        readme_path = os.path.join(folder_path, 'README.md')
        if os.path.exists(readme_path):
            with open(readme_path, 'r', encoding='utf-8') as f:
                return markdown2.markdown(f.read())
        return "<p>No content available</p>"

    def generate_index_html(self, folder_name):
        """Generate index.html for a given folder"""
        folder_path = os.path.join(self.root_path, folder_name)
        metadata = self.generate_metadata(folder_name)
        content = self.read_readme(folder_path)

        with open(self.template_path, 'r', encoding='utf-8') as template_file:
            template = template_file.read()

        # Simple template injection
        for key, value in metadata.items():
            template = template.replace(f"{{{{ {key} }}}}", str(value))
        
        template = template.replace("{{ content }}", content)
        template = template.replace("{{ key_takeaways }}", "<p>Key insights will be added soon.</p>")
        
        # Placeholder for navigation
        template = template.replace("{{ previous_page }}", "../")
        template = template.replace("{{ next_page }}", "../")

        return template

    def process_all_folders(self):
        """Process all folders and generate index.html"""
        for folder in os.listdir(self.root_path):
            if os.path.isdir(os.path.join(self.root_path, folder)):
                if not os.path.exists(os.path.join(self.root_path, folder, 'index.html')):
                    index_content = self.generate_index_html(folder)
                    with open(os.path.join(self.root_path, folder, 'index.html'), 'w', encoding='utf-8') as f:
                        f.write(index_content)
                    print(f"Generated index.html for {folder}")

def main():
    root_path = r'C:\Users\ihelp\Comprehensive_Resource_Library\Comprehensive_Resource_Library\Library_Resources'
    generator = TemplateGenerator(root_path)
    generator.process_all_folders()

if __name__ == "__main__":
    main()

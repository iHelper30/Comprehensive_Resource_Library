import os
import json
import unittest
import html5lib
from bs4 import BeautifulSoup

class ComprehensiveLibrarySystemTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root_path = r'C:\Users\ihelp\Comprehensive_Resource_Library\Comprehensive_Resource_Library\Library_Resources'
        cls.navigation_file = os.path.join(cls.root_path, 'navigation.json')
        cls.metadata_file = os.path.join(cls.root_path, 'library_metadata.json')

    def test_folder_structure(self):
        """Verify consistent folder naming and structure"""
        folders = [f for f in os.listdir(self.root_path) 
                   if os.path.isdir(os.path.join(self.root_path, f)) 
                   and f.startswith(tuple(str(i).zfill(2) for i in range(1, 50)))]
        
        self.assertTrue(folders, "No knowledge blocks found")
        
        for folder in folders:
            # Check folder name format
            self.assertTrue(folder.startswith(tuple(str(i).zfill(2) for i in range(1, 50))), 
                            f"Invalid folder name format: {folder}")
            
            # Verify index.html exists
            index_path = os.path.join(self.root_path, folder, 'index.html')
            self.assertTrue(os.path.exists(index_path), f"Missing index.html in {folder}")

    def test_navigation_integrity(self):
        """Validate navigation.json structure and links"""
        # Verify navigation file exists
        self.assertTrue(os.path.exists(self.navigation_file), "Navigation file missing")
        
        # Load navigation data
        with open(self.navigation_file, 'r', encoding='utf-8') as f:
            navigation_data = json.load(f)
        
        # Check navigation structure
        self.assertIsInstance(navigation_data, dict, "Invalid navigation data structure")
        
        # Verify first and last entries
        first_folder = min(navigation_data.keys())
        last_folder = max(navigation_data.keys())
        
        self.assertIsNone(navigation_data[first_folder]['previous'], 
                          f"First folder {first_folder} should have no previous page")
        self.assertIsNone(navigation_data[last_folder]['next'], 
                          f"Last folder {last_folder} should have no next page")

    def test_metadata_integrity(self):
        """Validate library metadata structure"""
        # Verify metadata file exists
        self.assertTrue(os.path.exists(self.metadata_file), "Metadata file missing")
        
        # Load metadata
        with open(self.metadata_file, 'r', encoding='utf-8') as f:
            library_metadata = json.load(f)
        
        # Check core metadata structure
        self.assertIn('total_knowledge_blocks', library_metadata)
        self.assertIn('categories', library_metadata)
        self.assertIn('knowledge_blocks', library_metadata)
        
        # Verify total knowledge blocks matches
        self.assertEqual(
            library_metadata['total_knowledge_blocks'], 
            len(library_metadata['knowledge_blocks']),
            "Mismatch in total knowledge blocks"
        )

    def test_html_template_consistency(self):
        """Verify HTML template consistency across all index.html files"""
        for folder in os.listdir(self.root_path):
            folder_path = os.path.join(self.root_path, folder)
            
            # Skip non-directories
            if not os.path.isdir(folder_path):
                continue
            
            index_path = os.path.join(folder_path, 'index.html')
            
            # Skip folders without index.html
            if not os.path.exists(index_path):
                continue
            
            # Read and parse HTML
            with open(index_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Validate HTML5 structure
            try:
                parser = html5lib.HTMLParser(strict=True)
                parser.parse(html_content)
            except Exception as e:
                self.fail(f"HTML5 parsing failed for {index_path}: {str(e)}")
            
            # Additional BeautifulSoup checks
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Check for required elements
            self.assertIsNotNone(soup.find('title'), f"Missing title in {index_path}")
            self.assertIsNotNone(soup.find('meta', attrs={'name': 'description'}), 
                                 f"Missing meta description in {index_path}")
            self.assertIsNotNone(soup.find('main'), f"Missing main content in {index_path}")

def main():
    unittest.main(verbosity=2)

if __name__ == "__main__":
    main()

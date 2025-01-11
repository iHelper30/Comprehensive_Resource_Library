import os
import json

class NavigationGenerator:
    def __init__(self, root_path):
        self.root_path = root_path
        self.folders = sorted([
            f for f in os.listdir(root_path) 
            if os.path.isdir(os.path.join(root_path, f)) 
            and f.startswith(tuple(str(i).zfill(2) for i in range(1, 50)))
        ])

    def generate_navigation_links(self):
        """Generate navigation links with previous and next page information"""
        navigation_data = {}
        
        for index, folder in enumerate(self.folders):
            # Previous page logic
            previous_page = self.folders[index - 1] if index > 0 else None
            
            # Next page logic
            next_page = self.folders[index + 1] if index < len(self.folders) - 1 else None
            
            navigation_data[folder] = {
                'previous': previous_page,
                'next': next_page
            }
        
        return navigation_data

    def update_index_files(self, navigation_data):
        """Update index.html files with navigation links"""
        for folder, nav_info in navigation_data.items():
            index_path = os.path.join(self.root_path, folder, 'index.html')
            
            if os.path.exists(index_path):
                with open(index_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace navigation placeholders
                content = content.replace(
                    "{{ previous_page }}", 
                    f"../{nav_info['previous']}" if nav_info['previous'] else "#"
                )
                content = content.replace(
                    "{{ next_page }}", 
                    f"../{nav_info['next']}" if nav_info['next'] else "#"
                )
                
                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(content)
        
        # Generate navigation JSON for potential future use
        with open(os.path.join(self.root_path, 'navigation.json'), 'w', encoding='utf-8') as f:
            json.dump(navigation_data, f, indent=2)

def main():
    root_path = r'C:\Users\ihelp\Comprehensive_Resource_Library\Comprehensive_Resource_Library\Library_Resources'
    nav_generator = NavigationGenerator(root_path)
    
    # Generate navigation links
    navigation_data = nav_generator.generate_navigation_links()
    
    # Update index files with navigation
    nav_generator.update_index_files(navigation_data)
    
    print("Navigation links generated and index files updated successfully.")

if __name__ == "__main__":
    main()

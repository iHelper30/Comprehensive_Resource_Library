import os
import json
import sys

class FinalSystemReview:
    def __init__(self, root_path):
        self.root_path = root_path
        self.review_results = {
            'critical_checks': {},
            'summary': {
                'total_checks': 0,
                'passed_checks': 0,
                'failed_checks': 0
            }
        }

    def check_critical_files(self):
        """Verify existence of critical project files"""
        critical_files = [
            'navigation.json',
            'library_metadata.json',
            'PROJECT_README.md',
            'template_generator.py',
            'navigation_generator.py',
            'metadata_enricher.py',
            'system_tests.py'
        ]

        for file in critical_files:
            file_path = os.path.join(self.root_path, file)
            exists = os.path.exists(file_path)
            self.review_results['critical_checks'][file] = exists
            self.review_results['summary']['total_checks'] += 1
            self.review_results['summary']['passed_checks'] += 1 if exists else 0

    def validate_knowledge_blocks(self):
        """Validate knowledge block structure"""
        folders = [f for f in os.listdir(self.root_path) 
                   if os.path.isdir(os.path.join(self.root_path, f)) 
                   and f.startswith(tuple(str(i).zfill(2) for i in range(1, 50)))]
        
        block_validation = {
            'total_blocks': len(folders),
            'blocks_with_readme': 0,
            'blocks_with_index': 0
        }

        for folder in folders:
            folder_path = os.path.join(self.root_path, folder)
            
            # Check README.md
            if os.path.exists(os.path.join(folder_path, 'README.md')):
                block_validation['blocks_with_readme'] += 1
            
            # Check index.html
            if os.path.exists(os.path.join(folder_path, 'index.html')):
                block_validation['blocks_with_index'] += 1

        self.review_results['knowledge_block_validation'] = block_validation
        
        # Update summary
        self.review_results['summary']['total_checks'] += 3
        self.review_results['summary']['passed_checks'] += (
            block_validation['total_blocks'] > 0 and
            block_validation['blocks_with_readme'] == block_validation['total_blocks'] and
            block_validation['blocks_with_index'] == block_validation['total_blocks']
        ) * 3

    def validate_metadata_integrity(self):
        """Check metadata file integrity"""
        metadata_path = os.path.join(self.root_path, 'library_metadata.json')
        
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            # Basic metadata structure checks
            checks = {
                'total_blocks_match': metadata.get('total_knowledge_blocks', 0) == len(metadata.get('knowledge_blocks', {})),
                'categories_exist': bool(metadata.get('categories')),
                'knowledge_blocks_exist': bool(metadata.get('knowledge_blocks'))
            }

            self.review_results['metadata_integrity'] = checks
            
            # Update summary
            self.review_results['summary']['total_checks'] += 3
            self.review_results['summary']['passed_checks'] += sum(checks.values())

        except (FileNotFoundError, json.JSONDecodeError):
            self.review_results['metadata_integrity'] = {
                'total_blocks_match': False,
                'categories_exist': False,
                'knowledge_blocks_exist': False
            }

    def generate_review_report(self):
        """Generate comprehensive review report"""
        # Calculate overall system health
        total_checks = self.review_results['summary']['total_checks']
        passed_checks = self.review_results['summary']['passed_checks']
        
        self.review_results['system_health'] = {
            'total_checks': total_checks,
            'passed_checks': passed_checks,
            'pass_percentage': (passed_checks / total_checks * 100) if total_checks > 0 else 0
        }

        # Write report to file
        report_path = os.path.join(self.root_path, 'SYSTEM_REVIEW_REPORT.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.review_results, f, indent=2)

        return self.review_results

def main():
    root_path = r'C:\Users\ihelp\Comprehensive_Resource_Library\Comprehensive_Resource_Library\Library_Resources'
    
    # Perform system review
    system_review = FinalSystemReview(root_path)
    system_review.check_critical_files()
    system_review.validate_knowledge_blocks()
    system_review.validate_metadata_integrity()
    review_results = system_review.generate_review_report()

    # Print system health
    print("Final System Review Results:")
    print(f"Total Checks: {review_results['system_health']['total_checks']}")
    print(f"Passed Checks: {review_results['system_health']['passed_checks']}")
    print(f"System Health: {review_results['system_health']['pass_percentage']:.2f}%")

    # Exit with appropriate status
    sys.exit(0 if review_results['system_health']['pass_percentage'] == 100 else 1)

if __name__ == "__main__":
    main()

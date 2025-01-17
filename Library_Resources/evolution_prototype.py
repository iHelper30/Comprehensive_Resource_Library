import os
import json
import re
from typing import List, Dict, Any

class KnowledgeEvolutionPrototype:
    def __init__(self, root_path: str):
        self.root_path = root_path
        self.metadata_path = os.path.join(root_path, 'library_metadata.json')
        self.usage_tracking_path = os.path.join(root_path, 'usage_tracking.json')

    def extract_keywords(self, text: str, top_n: int = 5) -> List[str]:
        """Extract top keywords from text"""
        # Simple keyword extraction (can be replaced with advanced NLP)
        words = re.findall(r'\b\w+\b', text.lower())
        word_freq = {}
        for word in words:
            if len(word) > 3:  # Ignore short words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        return sorted(word_freq, key=word_freq.get, reverse=True)[:top_n]

    def generate_content_correlations(self) -> Dict[str, List[str]]:
        """Generate basic content correlations"""
        with open(self.metadata_path, 'r') as f:
            metadata = json.load(f)
        
        correlations = {}
        for block, info in metadata['knowledge_blocks'].items():
            keywords = self.extract_keywords(info.get('summary', ''))
            correlations[block] = keywords
        
        return correlations

    def track_content_usage(self, block_id: str):
        """Track usage of knowledge blocks"""
        try:
            with open(self.usage_tracking_path, 'r') as f:
                usage_data = json.load(f)
        except FileNotFoundError:
            usage_data = {}
        
        usage_data[block_id] = usage_data.get(block_id, 0) + 1
        
        with open(self.usage_tracking_path, 'w') as f:
            json.dump(usage_data, f, indent=2)

def main():
    root_path = r'C:\Users\ihelp\Comprehensive_Resource_Library\Comprehensive_Resource_Library\Library_Resources'
    evolution_prototype = KnowledgeEvolutionPrototype(root_path)
    
    # Demonstrate keyword extraction
    print("Content Correlations:")
    correlations = evolution_prototype.generate_content_correlations()
    print(json.dumps(correlations, indent=2))
    
    # Simulate content usage tracking
    evolution_prototype.track_content_usage('01_Welcome_Message')
    evolution_prototype.track_content_usage('02_Purpose_of_Library')

if __name__ == "__main__":
    main()

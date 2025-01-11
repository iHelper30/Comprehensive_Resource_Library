import sqlite3
import json
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple

class MetricsAnalyzer:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.metrics_db = self.base_path / 'analytics_data/metrics.db'
        self.feedback_dir = self.base_path / 'feedback_data'
        
    def analyze_engagement(self, days: int = 30) -> Dict:
        """Analyze engagement metrics for the specified period"""
        conn = sqlite3.connect(self.metrics_db)
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Query metrics
        metrics = {}
        
        # Page views analysis
        df_views = pd.read_sql_query('''
            SELECT page_path, COUNT(*) as view_count
            FROM page_views
            WHERE timestamp >= ?
            GROUP BY page_path
            ORDER BY view_count DESC
        ''', conn, params=(start_date.isoformat(),))
        
        metrics['top_viewed_resources'] = df_views.head(10).to_dict('records')
        
        # Downloads analysis
        df_downloads = pd.read_sql_query('''
            SELECT resource_path, COUNT(*) as download_count
            FROM downloads
            WHERE timestamp >= ?
            GROUP BY resource_path
            ORDER BY download_count DESC
        ''', conn, params=(start_date.isoformat(),))
        
        metrics['most_downloaded'] = df_downloads.head(10).to_dict('records')
        
        # Time spent analysis
        df_time = pd.read_sql_query('''
            SELECT page_path, AVG(duration) as avg_time_spent
            FROM time_spent
            WHERE timestamp >= ?
            GROUP BY page_path
            ORDER BY avg_time_spent DESC
        ''', conn, params=(start_date.isoformat(),))
        
        metrics['highest_engagement'] = df_time.head(10).to_dict('records')
        
        conn.close()
        return metrics
    
    def analyze_feedback(self) -> Dict:
        """Analyze user feedback from collected forms"""
        feedback_metrics = {
            'satisfaction_scores': [],
            'most_valuable_resources': {},
            'improvement_suggestions': [],
            'recommendation_rate': {'Yes': 0, 'No': 0, 'Maybe': 0}
        }
        
        # Process each feedback file
        for feedback_file in self.feedback_dir.glob('*.json'):
            with open(feedback_file, 'r') as f:
                feedback = json.load(f)
                
                # Collect satisfaction scores
                feedback_metrics['satisfaction_scores'].append(
                    feedback['satisfaction_metrics']['overall_satisfaction']
                )
                
                # Track valuable resources
                valuable = feedback['feedback_sections']['most_useful']['options']
                for resource in valuable:
                    feedback_metrics['most_valuable_resources'][resource] = \
                        feedback_metrics['most_valuable_resources'].get(resource, 0) + 1
                
                # Collect improvement suggestions
                if feedback['feedback_sections']['improvements']['text_response']:
                    feedback_metrics['improvement_suggestions'].append(
                        feedback['feedback_sections']['improvements']['text_response']
                    )
                
                # Track recommendation rates
                would_recommend = feedback['satisfaction_metrics']['would_recommend']
                feedback_metrics['recommendation_rate'][would_recommend] += 1
        
        return feedback_metrics
    
    def generate_report(self, days: int = 30) -> str:
        """Generate a comprehensive analysis report"""
        engagement = self.analyze_engagement(days)
        feedback = self.analyze_feedback()
        
        report = f"""
# Resource Library Performance Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Period: Last {days} days

## Engagement Metrics

### Top Viewed Resources
{"".join(f"- {r['page_path']}: {r['view_count']} views\\n" for r in engagement['top_viewed_resources'])}

### Most Downloaded Resources
{"".join(f"- {r['resource_path']}: {r['download_count']} downloads\\n" for r in engagement['most_downloaded'])}

### Highest User Engagement (Time Spent)
{"".join(f"- {r['page_path']}: {r['avg_time_spent']:.2f} seconds avg\\n" for r in engagement['highest_engagement'])}

## User Feedback Analysis

### Overall Satisfaction
- Average Score: {sum(feedback['satisfaction_scores']) / len(feedback['satisfaction_scores']):.2f}/5
- Total Responses: {len(feedback['satisfaction_scores'])}

### Most Valuable Resources
{"".join(f"- {k}: {v} mentions\\n" for k, v in sorted(feedback['most_valuable_resources'].items(), key=lambda x: x[1], reverse=True))}

### Recommendation Rate
- Would Recommend: {feedback['recommendation_rate']['Yes']}
- Might Recommend: {feedback['recommendation_rate']['Maybe']}
- Would Not Recommend: {feedback['recommendation_rate']['No']}

### Top Improvement Suggestions
{"".join(f"- {suggestion}\\n" for suggestion in feedback['improvement_suggestions'][:5])}

## Recommendations
1. Focus on expanding high-engagement resources
2. Address common improvement suggestions
3. Enhance less-accessed resources
4. Consider user interface improvements based on feedback
"""
        
        # Save report
        report_path = self.base_path / 'reports' / f'performance_report_{datetime.now().strftime("%Y%m%d")}.md'
        report_path.parent.mkdir(exist_ok=True)
        with open(report_path, 'w') as f:
            f.write(report)
        
        return report

def main():
    analyzer = MetricsAnalyzer('c:/Users/ihelp/Comprehensive_Resource_Library')
    report = analyzer.generate_report()
    print("Report generated successfully!")
    print(report)

if __name__ == '__main__':
    main()

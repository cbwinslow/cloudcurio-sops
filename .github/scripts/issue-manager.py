#!/usr/bin/env python3
"""
Issue Manager - Automated issue triage and management
"""

import os
import json
import re
from typing import List, Dict, Set
from datetime import datetime

class IssueManager:
    """Manages automated issue triage and classification"""
    
    CATEGORY_KEYWORDS = {
        'infrastructure': [
            'network', 'compute', 'storage', 'monitoring', 'deployment',
            'server', 'cloud', 'kubernetes', 'docker', 'container'
        ],
        'systems': [
            'linux', 'ubuntu', 'desktop', 'laptop', 'windows',
            'os', 'operating system', 'systemd', 'cron'
        ],
        'software': [
            'code', 'programming', 'application', 'database', 'api',
            'development', 'bug', 'feature', 'software'
        ],
        'ai-automation': [
            'ai', 'agent', 'llm', 'machine learning', 'ml',
            'automation', 'ansible', 'crewai', 'model'
        ],
        'governance': [
            'compliance', 'audit', 'policy', 'governance',
            'regulation', 'legal', 'ethics', 'standards'
        ],
        'security': [
            'security', 'vulnerability', 'encryption', 'authentication',
            'authorization', 'hardening', 'exploit', 'cve'
        ],
        'documentation': [
            'docs', 'documentation', 'readme', 'guide',
            'tutorial', 'manual', 'wiki'
        ]
    }
    
    PRIORITY_KEYWORDS = {
        'high': [
            'urgent', 'critical', 'emergency', 'blocker',
            'production', 'outage', 'down', 'broken'
        ],
        'low': [
            'nice to have', 'enhancement', 'minor', 'trivial',
            'cosmetic', 'typo'
        ]
    }
    
    TYPE_KEYWORDS = {
        'bug': ['bug', 'error', 'issue', 'problem', 'broken', 'fail'],
        'enhancement': ['feature', 'enhancement', 'improvement', 'request'],
        'question': ['question', 'help', 'how to', 'documentation']
    }
    
    def __init__(self, issue_data: Dict):
        """Initialize with issue data from GitHub"""
        self.issue = issue_data
        self.title = issue_data.get('title', '').lower()
        self.body = (issue_data.get('body') or '').lower()
        self.labels: Set[str] = set()
    
    def analyze(self) -> Dict:
        """Analyze issue and return recommendations"""
        self._categorize()
        self._prioritize()
        self._type_classify()
        self._identify_standards()
        
        return {
            'labels': list(self.labels),
            'priority': self._get_priority(),
            'category': self._get_categories(),
            'standards': self._get_relevant_standards(),
            'recommendations': self._get_recommendations()
        }
    
    def _categorize(self):
        """Categorize issue based on keywords"""
        text = f"{self.title} {self.body}"
        
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                self.labels.add(f'category:{category}')
    
    def _prioritize(self):
        """Determine issue priority"""
        text = f"{self.title} {self.body}"
        
        # Check for high priority indicators
        if any(kw in text for kw in self.PRIORITY_KEYWORDS['high']):
            self.labels.add('priority:high')
        elif any(kw in text for kw in self.PRIORITY_KEYWORDS['low']):
            self.labels.add('priority:low')
        else:
            self.labels.add('priority:medium')
    
    def _type_classify(self):
        """Classify issue type"""
        text = f"{self.title} {self.body}"
        
        for issue_type, keywords in self.TYPE_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                self.labels.add(f'type:{issue_type}')
                break
    
    def _identify_standards(self):
        """Identify relevant standards directories"""
        standards_map = {
            'infrastructure': 'standards-and-procedures/01-infrastructure/',
            'systems': 'standards-and-procedures/02-systems/',
            'software': 'standards-and-procedures/03-software/',
            'ai-automation': 'standards-and-procedures/04-ai-and-automation/',
            'governance': 'standards-and-procedures/05-governance/'
        }
        
        self.relevant_standards = []
        for label in self.labels:
            if label.startswith('category:'):
                category = label.split(':')[1]
                if category in standards_map:
                    self.relevant_standards.append(standards_map[category])
    
    def _get_priority(self) -> str:
        """Get determined priority"""
        for label in self.labels:
            if label.startswith('priority:'):
                return label.split(':')[1]
        return 'medium'
    
    def _get_categories(self) -> List[str]:
        """Get all categories"""
        return [
            label.split(':')[1] 
            for label in self.labels 
            if label.startswith('category:')
        ]
    
    def _get_relevant_standards(self) -> List[str]:
        """Get relevant standards directories"""
        return self.relevant_standards
    
    def _get_recommendations(self) -> List[str]:
        """Generate recommendations for issue handling"""
        recommendations = []
        
        priority = self._get_priority()
        if priority == 'high':
            recommendations.append("🚨 High priority - assign immediately")
            recommendations.append("Consider creating hotfix branch if production-impacting")
        
        categories = self._get_categories()
        if 'security' in categories:
            recommendations.append("🔒 Security issue - review privately before public disclosure")
            recommendations.append("Check against security standards in governance/")
        
        if 'ai-automation' in categories:
            recommendations.append("🤖 AI/Automation - consider ethics and safety implications")
            recommendations.append("Review AI ethics standards in 04-ai-and-automation/01-agent-behavior/")
        
        if self.relevant_standards:
            recommendations.append(f"📚 Reference standards: {', '.join(self.relevant_standards)}")
        
        return recommendations

    def generate_comment(self) -> str:
        """Generate automated comment for the issue"""
        analysis = self.analyze()
        
        comment = f"""🤖 **Automated Issue Analysis**

**Priority:** {analysis['priority']}
**Categories:** {', '.join(analysis['category']) if analysis['category'] else 'Uncategorized'}
**Labels Applied:** {', '.join(analysis['labels'])}

"""
        
        if analysis['standards']:
            comment += "**Relevant Standards:**\n"
            for std in analysis['standards']:
                comment += f"- `{std}`\n"
            comment += "\n"
        
        if analysis['recommendations']:
            comment += "**Recommendations:**\n"
            for rec in analysis['recommendations']:
                comment += f"- {rec}\n"
            comment += "\n"
        
        comment += """**Next Steps:**
1. Review and adjust labels if needed
2. Assign to appropriate team member
3. Link to related issues or PRs
4. Consult relevant standards documentation
5. Update project board status

---
*This analysis was generated automatically. Please review and adjust as needed.*
"""
        
        return comment


def main():
    """Main entry point for GitHub Actions"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: issue-manager.py <issue_json_file>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r') as f:
        issue_data = json.load(f)
    
    manager = IssueManager(issue_data)
    analysis = manager.analyze()
    comment = manager.generate_comment()
    
    # Output for GitHub Actions
    print(json.dumps({
        'analysis': analysis,
        'comment': comment
    }, indent=2))


if __name__ == '__main__':
    main()

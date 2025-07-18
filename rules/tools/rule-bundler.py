#!/usr/bin/env python3
"""
Rule Bundler for Context-Aware Loading
Bundle rules intelligently based on context to minimize token usage.

Usage:
    python rule-bundler.py --task "review typescript code"
    python rule-bundler.py --language typescript --sections requirements,antipatterns
    python rule-bundler.py --bundle test-setup --output bundle.json
    python rule-bundler.py --create-bundle "typescript-testing" rule1.md rule2.md
"""

import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
import re


class RuleBundler:
    """Bundle rules for efficient LLM consumption."""
    
    def __init__(self):
        self.rules_dir = Path(__file__).parent.parent
        self.rules_index = self._load_rules_index()
        self.bundles_dir = self.rules_dir / 'bundles'
        self.bundles_dir.mkdir(exist_ok=True)
        
    def _load_rules_index(self) -> Dict:
        """Load the rules index."""
        index_path = self.rules_dir / 'rules-index.json'
        if index_path.exists():
            return json.loads(index_path.read_text())
        return {'rules': {}}
    
    def bundle_for_task(self, task_description: str) -> Dict:
        """Create an optimized bundle based on task description."""
        # Extract keywords and determine context
        context = self._analyze_task(task_description)
        
        # Select relevant rules
        selected_rules = self._select_rules_for_context(context)
        
        # Determine which sections to include
        sections = self._determine_sections_for_task(task_description)
        
        # Build the bundle
        bundle = self._build_bundle(selected_rules, sections)
        
        # Add metadata
        bundle['metadata'] = {
            'task': task_description,
            'context': context,
            'token_estimate': self._estimate_tokens(bundle),
            'rule_count': len(selected_rules)
        }
        
        return bundle
    
    def _analyze_task(self, task: str) -> Dict:
        """Analyze task to determine context."""
        task_lower = task.lower()
        
        context = {
            'action': 'unknown',
            'languages': [],
            'categories': [],
            'keywords': []
        }
        
        # Determine action
        if any(word in task_lower for word in ['review', 'check', 'validate', 'audit']):
            context['action'] = 'review'
        elif any(word in task_lower for word in ['generate', 'create', 'write', 'implement']):
            context['action'] = 'generate'
        elif any(word in task_lower for word in ['fix', 'repair', 'correct', 'update']):
            context['action'] = 'fix'
        elif any(word in task_lower for word in ['learn', 'understand', 'explain']):
            context['action'] = 'learn'
        
        # Detect languages
        language_patterns = {
            'typescript': ['typescript', 'ts', 'tsx'],
            'javascript': ['javascript', 'js', 'jsx'],
            'python': ['python', 'py'],
            'csharp': ['c#', 'csharp', 'dotnet', '.net'],
            'go': ['go', 'golang'],
            'java': ['java'],
            'ruby': ['ruby', 'rb']
        }
        
        for lang, patterns in language_patterns.items():
            if any(p in task_lower for p in patterns):
                context['languages'].append(lang)
        
        # Detect categories
        category_patterns = {
            'test-naming': ['test', 'testing', 'spec', 'unit test'],
            'code-quality': ['quality', 'clean code', 'refactor', 'code review'],
            'security': ['security', 'secure', 'vulnerability', 'owasp'],
            'git-workflow': ['git', 'commit', 'branch', 'pull request', 'pr']
        }
        
        for cat, patterns in category_patterns.items():
            if any(p in task_lower for p in patterns):
                context['categories'].append(cat)
        
        # Extract keywords
        keywords = re.findall(r'\b\w{4,}\b', task_lower)
        context['keywords'] = [k for k in keywords if k not in 
                              ['that', 'this', 'with', 'from', 'have']]
        
        return context
    
    def _select_rules_for_context(self, context: Dict) -> List[str]:
        """Select relevant rules based on context."""
        selected = set()
        
        for rule_id, rule in self.rules_index['rules'].items():
            score = 0
            
            # Language match
            if rule['language'] in context['languages']:
                score += 10
            elif rule['language'] == 'universal':
                score += 2
            
            # Category match
            if rule['category'] in context['categories']:
                score += 8
            
            # Keyword match in tags
            for keyword in context['keywords']:
                if keyword in ' '.join(rule.get('tags', [])).lower():
                    score += 3
            
            # Add rules with sufficient score
            if score >= 8:
                selected.add(rule_id)
        
        # Add prerequisites
        selected_with_deps = set(selected)
        for rule_id in selected:
            if rule_id in self.rules_index['rules']:
                prereqs = self.rules_index['rules'][rule_id].get('prerequisites', [])
                selected_with_deps.update(prereqs)
        
        return list(selected_with_deps)
    
    def _determine_sections_for_task(self, task: str) -> List[str]:
        """Determine which sections to include based on task."""
        task_lower = task.lower()
        
        # Default sections based on action
        if 'review' in task_lower or 'check' in task_lower:
            return ['RULE_SUMMARY', 'MUST_NOT_DO', 'antipatterns']
        elif 'generate' in task_lower or 'create' in task_lower:
            return ['RULE_SUMMARY', 'MUST_FOLLOW', 'requirements', 'good_examples']
        elif 'fix' in task_lower:
            return ['RULE_SUMMARY', 'antipatterns', 'good_examples']
        elif 'learn' in task_lower or 'explain' in task_lower:
            return ['RULE_SUMMARY', 'CONTEXT_AND_RATIONALE']
        else:
            # Include minimal sections for unknown tasks
            return ['RULE_SUMMARY', 'requirements', 'antipatterns']
    
    def _build_bundle(self, rule_ids: List[str], sections: List[str]) -> Dict:
        """Build bundle with selected rules and sections."""
        from extract_rule_section import RuleExtractor
        
        bundle = {
            'rules': {}
        }
        
        for rule_id in rule_ids:
            if rule_id not in self.rules_index['rules']:
                continue
            
            rule_info = self.rules_index['rules'][rule_id]
            rule_path = self.rules_dir / rule_info['file_path']
            
            if not rule_path.exists():
                continue
            
            extractor = RuleExtractor(rule_path)
            
            rule_data = {
                'metadata': {
                    'rule_id': rule_id,
                    'category': rule_info['category'],
                    'language': rule_info['language'],
                    'severity': rule_info['severity']
                },
                'sections': {}
            }
            
            # Extract requested sections
            for section in sections:
                if section == 'RULE_SUMMARY':
                    rule_data['sections']['summary'] = extractor.extract_section('RULE_SUMMARY')
                elif section == 'requirements' or section == 'MUST_FOLLOW':
                    rule_data['sections']['requirements'] = extractor.extract_requirements()
                elif section == 'antipatterns' or section == 'MUST_NOT_DO':
                    rule_data['sections']['antipatterns'] = extractor.extract_antipatterns()
                elif section == 'good_examples':
                    examples = extractor.extract_examples('good')
                    # Limit to first example to save tokens
                    rule_data['sections']['good_examples'] = examples[:1] if examples else []
                elif section == 'CONTEXT_AND_RATIONALE':
                    rule_data['sections']['context'] = extractor.extract_section('CONTEXT_AND_RATIONALE')
            
            bundle['rules'][rule_id] = rule_data
        
        return bundle
    
    def _estimate_tokens(self, bundle: Dict) -> int:
        """Estimate token count for bundle."""
        # Rough estimation: 1 token ≈ 4 characters
        text = json.dumps(bundle)
        return len(text) // 4
    
    def bundle_by_criteria(self, language: Optional[str] = None, 
                          categories: Optional[List[str]] = None,
                          sections: Optional[List[str]] = None) -> Dict:
        """Create bundle based on specific criteria."""
        # Select rules
        selected_rules = []
        
        for rule_id, rule in self.rules_index['rules'].items():
            if language and rule['language'] != language:
                continue
            if categories and rule['category'] not in categories:
                continue
            selected_rules.append(rule_id)
        
        # Use default sections if not specified
        if not sections:
            sections = ['RULE_SUMMARY', 'requirements', 'antipatterns']
        
        return self._build_bundle(selected_rules, sections)
    
    def create_named_bundle(self, name: str, rule_files: List[str], 
                           sections: Optional[List[str]] = None) -> Path:
        """Create a named bundle from specific rule files."""
        if not sections:
            sections = ['RULE_SUMMARY', 'requirements', 'antipatterns', 'good_examples']
        
        # Extract rule IDs from file paths
        rule_ids = []
        for rule_file in rule_files:
            rule_path = Path(rule_file)
            # Find in index by file path
            for rule_id, rule_info in self.rules_index['rules'].items():
                if rule_info['file_path'].endswith(rule_path.name):
                    rule_ids.append(rule_id)
                    break
        
        # Build bundle
        bundle = self._build_bundle(rule_ids, sections)
        bundle['metadata'] = {
            'name': name,
            'created': datetime.now().isoformat(),
            'rule_count': len(rule_ids),
            'sections': sections
        }
        
        # Save bundle
        bundle_path = self.bundles_dir / f"{name}.json"
        bundle_path.write_text(json.dumps(bundle, indent=2))
        
        return bundle_path
    
    def load_bundle(self, name: str) -> Dict:
        """Load a named bundle."""
        bundle_path = self.bundles_dir / f"{name}.json"
        if bundle_path.exists():
            return json.loads(bundle_path.read_text())
        raise FileNotFoundError(f"Bundle '{name}' not found")
    
    def optimize_bundle(self, bundle: Dict, max_tokens: int = 2000) -> Dict:
        """Optimize bundle to fit within token limit."""
        current_tokens = self._estimate_tokens(bundle)
        
        if current_tokens <= max_tokens:
            return bundle
        
        # Optimization strategies
        optimized = bundle.copy()
        
        # 1. Remove examples if present
        for rule_id in optimized['rules']:
            if 'good_examples' in optimized['rules'][rule_id]['sections']:
                del optimized['rules'][rule_id]['sections']['good_examples']
                current_tokens = self._estimate_tokens(optimized)
                if current_tokens <= max_tokens:
                    return optimized
        
        # 2. Remove context sections
        for rule_id in optimized['rules']:
            if 'context' in optimized['rules'][rule_id]['sections']:
                del optimized['rules'][rule_id]['sections']['context']
                current_tokens = self._estimate_tokens(optimized)
                if current_tokens <= max_tokens:
                    return optimized
        
        # 3. Keep only summaries and critical sections
        for rule_id in optimized['rules']:
            sections = optimized['rules'][rule_id]['sections']
            # Keep only summary and either requirements or antipatterns
            new_sections = {}
            if 'summary' in sections:
                new_sections['summary'] = sections['summary']
            if 'antipatterns' in sections and len(sections['antipatterns']) > 0:
                new_sections['antipatterns'] = sections['antipatterns'][:3]  # Top 3
            elif 'requirements' in sections:
                new_sections['requirements'] = sections['requirements'][:3]  # Top 3
            optimized['rules'][rule_id]['sections'] = new_sections
        
        return optimized
    
    def get_predefined_bundles(self) -> Dict[str, Dict]:
        """Get predefined bundle configurations."""
        return {
            'typescript-testing': {
                'description': 'TypeScript test writing bundle',
                'rules': ['typescript-test-naming', 'universal-test-naming'],
                'sections': ['RULE_SUMMARY', 'requirements', 'good_examples']
            },
            'code-review': {
                'description': 'Code review checklist',
                'categories': ['code-quality'],
                'sections': ['RULE_SUMMARY', 'antipatterns']
            },
            'security-audit': {
                'description': 'Security audit rules',
                'categories': ['security'],
                'sections': ['RULE_SUMMARY', 'requirements', 'antipatterns']
            },
            'git-workflow': {
                'description': 'Git workflow standards',
                'categories': ['git-workflow'],
                'sections': ['RULE_SUMMARY', 'requirements', 'good_examples']
            },
            'quick-reference': {
                'description': 'Minimal quick reference',
                'sections': ['RULE_SUMMARY'],
                'max_rules': 10
            }
        }


def format_bundle_summary(bundle: Dict) -> str:
    """Format bundle for human reading."""
    lines = []
    
    if 'metadata' in bundle:
        meta = bundle['metadata']
        lines.append(f"Bundle: {meta.get('name', 'Unnamed')}")
        lines.append(f"Rules: {meta.get('rule_count', len(bundle['rules']))}")
        lines.append(f"Estimated tokens: {meta.get('token_estimate', 'Unknown')}")
        lines.append("")
    
    lines.append("Included Rules:")
    for rule_id, rule_data in bundle['rules'].items():
        meta = rule_data['metadata']
        lines.append(f"  - {rule_id} ({meta['language']}/{meta['category']}) [{meta['severity']}]")
        sections = list(rule_data['sections'].keys())
        lines.append(f"    Sections: {', '.join(sections)}")
    
    return "\n".join(lines)


def main():
    """Command-line interface."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    bundler = RuleBundler()
    
    if sys.argv[1] == '--task':
        # Bundle for task
        task = ' '.join(sys.argv[2:])
        bundle = bundler.bundle_for_task(task)
        
        print(format_bundle_summary(bundle))
        print(f"\nOptimized bundle created for: {task}")
    
    elif sys.argv[1] == '--language':
        # Bundle by language
        language = sys.argv[2]
        sections = None
        
        if len(sys.argv) > 4 and sys.argv[3] == '--sections':
            sections = sys.argv[4].split(',')
        
        bundle = bundler.bundle_by_criteria(language=language, sections=sections)
        print(format_bundle_summary(bundle))
    
    elif sys.argv[1] == '--bundle':
        # Load predefined bundle
        bundle_name = sys.argv[2]
        
        predefined = bundler.get_predefined_bundles()
        if bundle_name in predefined:
            config = predefined[bundle_name]
            print(f"Creating bundle: {config['description']}")
            
            # Build based on config
            if 'rules' in config:
                bundle = bundler._build_bundle(config['rules'], config['sections'])
            elif 'categories' in config:
                bundle = bundler.bundle_by_criteria(
                    categories=config['categories'],
                    sections=config['sections']
                )
            
            if '--output' in sys.argv:
                output_idx = sys.argv.index('--output') + 1
                output_path = Path(sys.argv[output_idx])
                output_path.write_text(json.dumps(bundle, indent=2))
                print(f"Bundle saved to: {output_path}")
            else:
                print(json.dumps(bundle, indent=2))
        else:
            print(f"Unknown bundle: {bundle_name}")
            print(f"Available: {', '.join(predefined.keys())}")
    
    elif sys.argv[1] == '--create-bundle':
        # Create custom bundle
        name = sys.argv[2]
        rule_files = sys.argv[3:]
        
        bundle_path = bundler.create_named_bundle(name, rule_files)
        print(f"Bundle created: {bundle_path}")
    
    elif sys.argv[1] == '--optimize':
        # Optimize existing bundle
        bundle_file = Path(sys.argv[2])
        max_tokens = 2000
        
        if len(sys.argv) > 4 and sys.argv[3] == '--max-tokens':
            max_tokens = int(sys.argv[4])
        
        bundle = json.loads(bundle_file.read_text())
        optimized = bundler.optimize_bundle(bundle, max_tokens)
        
        print(f"Original tokens: {bundler._estimate_tokens(bundle)}")
        print(f"Optimized tokens: {bundler._estimate_tokens(optimized)}")
        
        if '--output' in sys.argv:
            output_idx = sys.argv.index('--output') + 1
            output_path = Path(sys.argv[output_idx])
            output_path.write_text(json.dumps(optimized, indent=2))
            print(f"Optimized bundle saved to: {output_path}")


if __name__ == '__main__':
    from datetime import datetime
    main()
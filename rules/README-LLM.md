# Workflow-Tools Rules - LLM Usage Guide

This guide explains how LLMs (Large Language Models) can efficiently use the workflow-tools rules.

## 🚀 Quick Start for LLMs

### Primary Index Files
1. **`rules-index.json`** - Machine-readable rule catalog
2. **`llm-quick-queries.yaml`** - Pre-built query patterns
3. **`LLM-QUERY-GUIDE.md`** - Detailed query instructions

### Rule File Structure
All rules follow a consistent pattern with:
- YAML front matter (metadata)
- CAPS_SECTION_NAMES (for extraction)
- Extraction markers (`<!-- EXTRACT:section:start -->`)
- Structured examples (GOOD_EXAMPLE_001, BAD_EXAMPLE_001)

## 📊 Optimized Query Patterns

### 1. Get Rule Summary
```
Load: rules-index.json
Query: rules.[rule-id].summary
Returns: One-line description
Context needed: ~50 tokens
```

### 2. Check Code Compliance
```
Load: Rule file, section MUST_NOT_DO
Pattern match: Against provided code
Returns: Violations with rule IDs (ANT001, etc.)
Context needed: ~200 tokens per rule
```

### 3. Generate Compliant Code
```
Load: GOOD_EXAMPLE_* + MUST_FOLLOW from relevant rule
Generate: Code matching patterns
Validate: Against MUST_NOT_DO patterns
Context needed: ~500 tokens
```

### 4. Quick Reference
```
Load: llm-quick-queries.yaml
Query: quick_queries.[topic].[query_name]
Returns: Specific answer
Context needed: ~100 tokens
```

## 🎯 Common Use Cases

### Use Case 1: "How should I name tests?"
```python
# Optimal query path:
1. Load rules-index.json
2. Find test-naming rules for target language
3. Load RULE_SUMMARY + first GOOD_EXAMPLE
4. Return formatted guidance

# Tokens used: ~300
```

### Use Case 2: "Review this code"
```python
# Optimal query path:
1. Identify language from code
2. Load relevant MUST_NOT_DO sections
3. Pattern match violations
4. Return specific feedback with rule IDs

# Tokens used: ~500
```

### Use Case 3: "Set up TypeScript project"
```python
# Optimal query path:
1. Query rules-index.json for typescript rules
2. Load checklist from llm-quick-queries.yaml
3. Include config file paths
4. Return step-by-step setup

# Tokens used: ~400
```

## 🔍 Extraction Patterns

### Extract Specific Sections
```markdown
<!-- EXTRACT:requirements:start -->
Content to extract
<!-- EXTRACT:requirements:end -->
```

Available sections:
- `requirements` - The MUST_FOLLOW rules
- `antipatterns` - The MUST_NOT_DO rules
- `patterns` - Pattern recognition rules
- `metrics` - How to measure compliance

### Section Markers
All major sections use CAPS_WITH_UNDERSCORES:
- `RULE_SUMMARY` - One-line description
- `MUST_FOLLOW` - Requirements (REQ001, REQ002...)
- `MUST_NOT_DO` - Anti-patterns (ANT001, ANT002...)
- `GOOD_EXAMPLE_001` - Positive examples
- `BAD_EXAMPLE_001` - Negative examples
- `AUTOMATED_CHECKS` - Tooling configuration
- `METRICS` - Measurement queries

## 📈 Performance Optimization

### 1. Use the Index First
Always start with `rules-index.json` to:
- Find relevant rules by language/tag
- Understand relationships
- Get summaries without loading full files

### 2. Load Minimal Context
For fastest responses, load only needed sections:
```yaml
# For code generation
Load: GOOD_EXAMPLE_* + MUST_FOLLOW
Skip: Rationale, migration guide, metrics

# For code review  
Load: MUST_NOT_DO + BAD_EXAMPLE_*
Skip: Good examples, automation details

# For explanations
Load: RULE_SUMMARY + CONTEXT_AND_RATIONALE
Skip: Examples, technical details
```

### 3. Cache Common Queries
Frequently needed data:
- `rules-index.json` (cache per session)
- Test naming patterns
- Commit type definitions
- Language-specific requirements

## 🤖 Integration Examples

### ChatGPT Custom Instructions
```
When querying workflow-tools rules:
1. Start with rules-index.json
2. Use extraction markers for specific sections
3. Load minimal context based on query type
4. Return structured responses with rule IDs
```

### Claude Project Knowledge
```
Key files for workflow-tools:
- /rules/rules-index.json (rule catalog)
- /rules/llm-quick-queries.yaml (quick lookups)
- /rules/[language]/[category]/*.md (specific rules)

Query pattern: Load index → Find rule → Extract section → Format response
```

### API Integration
```python
def get_rule_requirements(rule_id):
    # Load only requirements section
    rule_file = f"rules/{get_rule_path(rule_id)}"
    content = read_file(rule_file)
    return extract_section(content, "requirements")

def check_compliance(code, language):
    # Load only antipatterns for language
    rules = get_rules_by_language(language)
    violations = []
    for rule in rules:
        antipatterns = get_rule_section(rule, "MUST_NOT_DO")
        violations.extend(check_patterns(code, antipatterns))
    return violations
```

## 📚 Rule Metadata Structure

Each rule has YAML front matter:
```yaml
rule_id: unique-identifier
category: test-naming|code-quality|security|git-workflow
language: typescript|csharp|python|universal
severity: required|recommended|optional
tags: [searchable, tags, here]
prerequisites: [required-rules]
related_rules: [similar-rules]
```

This enables queries like:
- "All required rules for TypeScript"
- "Rules tagged with 'security'"
- "Prerequisites for rule X"

## 🎨 Response Formatting

### For Developers
```markdown
**Rule**: [Title]
**Summary**: [One line]

✅ Do:
- [Simplified requirement]

❌ Don't:
- [Simplified anti-pattern]

Example:
```code
[Minimal example]
```
```

### For Automation
```json
{
  "rule_id": "rule-name",
  "violations": ["ANT001", "ANT003"],
  "fixes": {
    "ANT001": "Remove 'should' from test name",
    "ANT003": "Use business language"
  }
}
```

## 🔧 Utility Queries

### List Rules by Property
```sql
SELECT rule_id, summary 
FROM rules 
WHERE language='typescript' 
  AND severity='required'
```

### Find Related Rules
```sql
SELECT related_rules 
FROM rules 
WHERE rule_id='typescript-test-naming'
```

### Get Quick Fix
```yaml
Query: quick_fixes.test_naming
For pattern: "should return X when Y"
Returns: "Y_returns_X"
```

---

**Remember**: Optimal LLM usage means loading minimum context for maximum value. Use the index, extract specific sections, and cache common queries!
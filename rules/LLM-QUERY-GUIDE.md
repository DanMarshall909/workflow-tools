# LLM Query Guide for Workflow-Tools Rules

This guide helps LLMs efficiently query and extract information from workflow-tools rules.

## Quick Extraction Queries

### 1. Get Specific Requirements
```
Extract MUST_FOLLOW requirements from rule: [rule-id]
Return only items marked REQ001-REQ999
```

### 2. Find Anti-patterns
```
Extract MUST_NOT_DO items from category: [category]
Return items marked ANT001-ANT999 with reasons
```

### 3. Get Examples by Quality
```
Show all GOOD_EXAMPLE_* from language: [language]
Include context and explanation
```

### 4. Rule Summary by Topic
```
Return RULE_SUMMARY for all rules tagged: [tag]
Format as bullet list with rule IDs
```

## Structured Query Patterns

### Query by Scenario
```json
{
  "query_type": "scenario",
  "scenario": "starting new TypeScript project",
  "need": ["test_naming", "code_quality", "linting"],
  "return_format": "checklist"
}
```

Expected Response:
```markdown
## TypeScript Project Setup Checklist
- [ ] Apply rule: typescript-test-naming (business-focused test names)
- [ ] Apply rule: typescript-code-quality (strict mode, no any)
- [ ] Install: eslint-config (run: cp rules/typescript/configs/eslint.config.js)
```

### Query by Compliance Check
```json
{
  "query_type": "compliance_check",
  "code_sample": "test('should return user data', () => {})",
  "check_against": "typescript-test-naming",
  "return_violations": true
}
```

Expected Response:
```json
{
  "compliant": false,
  "violations": [
    {
      "rule": "ANT001",
      "issue": "Uses 'should' in test name",
      "suggestion": "test('user_data_is_accessible', () => {})"
    }
  ]
}
```

### Query for Migration
```json
{
  "query_type": "migration",
  "from": "old_pattern",
  "to": "workflow_tools_standard",
  "scope": "test_naming",
  "return_steps": true
}
```

## Efficient Context Loading

### Minimal Context Patterns

1. **For Code Generation**
   ```
   Load only:
   - GOOD_EXAMPLE_* from relevant rule
   - MUST_FOLLOW requirements
   - Skip: rationale, migration guide
   ```

2. **For Code Review**
   ```
   Load only:
   - MUST_NOT_DO antipatterns
   - BAD_EXAMPLE_* with explanations
   - Skip: good examples, metrics
   ```

3. **For Learning**
   ```
   Load only:
   - RULE_SUMMARY
   - CONTEXT_AND_RATIONALE
   - Skip: examples, automation
   ```

## Query Optimization Tips

### 1. Use Extraction Markers
Rules contain `<!-- EXTRACT:section:start -->` markers:
- `requirements` - Just the requirements
- `antipatterns` - Just the anti-patterns
- `patterns` - Pattern recognition rules
- `metrics` - Measurement queries

### 2. Use Rule Index
Query `rules-index.json` for:
- Finding rules by language/framework
- Understanding prerequisites
- Getting rule relationships
- Finding related rules

### 3. Use Structured Sections
All rules use CAPS_SECTIONS for easy extraction:
- `RULE_SUMMARY` - One-line description
- `MUST_FOLLOW` - Requirements
- `MUST_NOT_DO` - Anti-patterns
- `GOOD_EXAMPLE_*` - Positive examples
- `BAD_EXAMPLE_*` - Negative examples

## Common LLM Tasks

### Generate Compliant Code
```
Task: Generate [component type] following [rule-id]
1. Load GOOD_EXAMPLE_* from rule
2. Load MUST_FOLLOW requirements
3. Generate code matching patterns
4. Validate against MUST_NOT_DO
```

### Review Code for Compliance
```
Task: Review [code] against [rule-id]
1. Load MUST_NOT_DO patterns
2. Load BAD_EXAMPLE_* patterns
3. Check for violations
4. Suggest corrections using GOOD_EXAMPLE_*
```

### Explain Rule to Developer
```
Task: Explain [rule-id] to developer
1. Load RULE_SUMMARY
2. Load CONTEXT_AND_RATIONALE
3. Load one GOOD_EXAMPLE and one BAD_EXAMPLE
4. Skip automation details
```

### Create Team Checklist
```
Task: Create checklist for [language] development
1. Query rules-index.json for language rules
2. Load RULE_SUMMARY for each
3. Extract key MUST_FOLLOW items
4. Format as actionable checklist
```

## Response Formatting

### For Developers
```markdown
## Rule: [Rule Title]
**Summary**: [RULE_SUMMARY]

### What to do:
- [REQ001 simplified]
- [REQ002 simplified]

### What to avoid:
- [ANT001 simplified]
- [ANT002 simplified]

### Example:
```[language]
[One good example]
```
```

### For Automated Tools
```json
{
  "rule_id": "typescript-test-naming",
  "compliance": {
    "requirements": ["REQ001", "REQ002"],
    "violations": ["ANT001"],
    "suggestions": ["Use pattern: user_can_*"]
  }
}
```

## Performance Tips

1. **Cache Rule Index**: Load `rules-index.json` once per session
2. **Lazy Load Examples**: Only load examples when needed
3. **Use Extraction Markers**: Extract specific sections instead of full files
4. **Batch Related Queries**: Get all rules for a language at once

## Query Examples

### "How should I name tests in TypeScript?"
```
1. Load rule: typescript-test-naming
2. Extract: RULE_SUMMARY + MUST_FOLLOW
3. Show: GOOD_EXAMPLE_001
4. Return: Formatted guidelines
```

### "Review my PR for code quality"
```
1. Identify languages in PR
2. Load relevant MUST_NOT_DO sections
3. Pattern match against changes
4. Return: Violations with fixes
```

### "Set up a new Python project"
```
1. Query rules-index.json for Python rules
2. Load RULE_SUMMARY for each
3. Load configuration files
4. Return: Setup checklist
```

---

Remember: Less context = Faster responses. Load only what you need!
# LLM API Examples for Rule Consumption

This document provides practical examples of how LLMs can consume workflow-tools rules through various APIs and integration patterns.

## OpenAI Function Calling Example

```python
import openai
import json
from pathlib import Path

# Define functions for OpenAI to call
functions = [
    {
        "name": "get_rule_requirements",
        "description": "Get requirements from a specific rule",
        "parameters": {
            "type": "object",
            "properties": {
                "rule_id": {
                    "type": "string",
                    "description": "The rule ID to query"
                },
                "section": {
                    "type": "string",
                    "enum": ["requirements", "antipatterns", "examples"],
                    "description": "Which section to extract"
                }
            },
            "required": ["rule_id", "section"]
        }
    }
]

def get_rule_requirements(rule_id: str, section: str):
    """Function that OpenAI can call to get rule data."""
    # Use the extraction tool
    from extract_rule_section import RuleExtractor
    
    rule_path = Path(f"rules/{rule_id}.md")
    if not rule_path.exists():
        return {"error": f"Rule {rule_id} not found"}
    
    extractor = RuleExtractor(rule_path)
    
    if section == "requirements":
        return extractor.extract_requirements()
    elif section == "antipatterns":
        return extractor.extract_antipatterns()
    elif section == "examples":
        return {
            "good": extractor.extract_examples("good"),
            "bad": extractor.extract_examples("bad")
        }

# Example usage
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Show me the test naming requirements for TypeScript"}
    ],
    functions=functions,
    function_call="auto"
)
```

## Claude Tool Use Example

```python
import anthropic

# Define tool for Claude
tools = [
    {
        "name": "check_code_compliance",
        "description": "Check if code follows workflow-tools rules",
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The code to check"
                },
                "language": {
                    "type": "string",
                    "description": "Programming language"
                },
                "rule_category": {
                    "type": "string",
                    "description": "Category of rules to check against"
                }
            },
            "required": ["code", "language", "rule_category"]
        }
    }
]

def check_code_compliance(code: str, language: str, rule_category: str):
    """Check code against workflow-tools rules."""
    # Load rules index
    with open("rules/rules-index.json") as f:
        rules_index = json.load(f)
    
    # Find applicable rules
    applicable_rules = [
        rule for rule_id, rule in rules_index["rules"].items()
        if rule["language"] == language and rule["category"] == rule_category
    ]
    
    violations = []
    
    for rule in applicable_rules:
        # Load antipatterns for this rule
        rule_file = Path(f"rules/{rule['file_path']}")
        extractor = RuleExtractor(rule_file)
        antipatterns = extractor.extract_antipatterns()
        
        # Check each antipattern
        for antipattern in antipatterns:
            if check_pattern(code, antipattern):
                violations.append({
                    "rule_id": rule["rule_id"],
                    "violation": antipattern["id"],
                    "message": antipattern["antipattern"],
                    "fix": antipattern["instead"]
                })
    
    return violations

# Example usage with Claude
client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1000,
    tools=tools,
    messages=[{
        "role": "user",
        "content": "Check this test: test('should return user data', () => {})"
    }]
)
```

## LangChain Integration Example

```python
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI

def query_workflow_rules(query: str) -> str:
    """Query workflow-tools rules based on natural language."""
    # Load the quick queries
    with open("rules/llm-quick-queries.yaml") as f:
        quick_queries = yaml.safe_load(f)
    
    # Simple keyword matching (in production, use embeddings)
    if "test naming" in query.lower():
        return json.dumps(quick_queries["quick_queries"]["test_naming"])
    elif "commit" in query.lower():
        return json.dumps(quick_queries["quick_queries"]["git"]["commit_types"])
    # ... more patterns
    
    return "No matching rules found"

# Create LangChain tool
rule_tool = Tool(
    name="WorkflowRules",
    func=query_workflow_rules,
    description="Query workflow-tools rules for coding standards"
)

# Create agent
llm = OpenAI(temperature=0)
agent = initialize_agent(
    [rule_tool],
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Use the agent
response = agent.run("How should I name my Jest tests?")
```

## REST API Example

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional

app = FastAPI()

class RuleQuery(BaseModel):
    rule_id: Optional[str] = None
    language: Optional[str] = None
    category: Optional[str] = None
    section: Optional[str] = None

class ComplianceCheck(BaseModel):
    code: str
    language: str
    rule_ids: Optional[List[str]] = None

@app.post("/api/rules/query")
async def query_rules(query: RuleQuery):
    """Query rules based on criteria."""
    with open("rules/rules-index.json") as f:
        rules_index = json.load(f)
    
    results = []
    
    for rule_id, rule in rules_index["rules"].items():
        # Filter by criteria
        if query.rule_id and rule_id != query.rule_id:
            continue
        if query.language and rule["language"] != query.language:
            continue
        if query.category and rule["category"] != query.category:
            continue
        
        # Extract requested section
        if query.section:
            rule_path = Path(f"rules/{rule['file_path']}")
            extractor = RuleExtractor(rule_path)
            
            if query.section == "summary":
                section_data = extractor.extract_section("RULE_SUMMARY")
            else:
                section_data = getattr(extractor, f"extract_{query.section}")()
            
            results.append({
                "rule_id": rule_id,
                "section": query.section,
                "data": section_data
            })
        else:
            results.append(rule)
    
    return {"rules": results}

@app.post("/api/rules/check")
async def check_compliance(check: ComplianceCheck):
    """Check code compliance against rules."""
    violations = []
    
    # Load applicable rules
    with open("rules/rules-index.json") as f:
        rules_index = json.load(f)
    
    for rule_id, rule in rules_index["rules"].items():
        if rule["language"] != check.language:
            continue
        
        if check.rule_ids and rule_id not in check.rule_ids:
            continue
        
        # Check against this rule
        rule_violations = check_rule_compliance(
            check.code,
            rule_id,
            rule["file_path"]
        )
        violations.extend(rule_violations)
    
    return {
        "compliant": len(violations) == 0,
        "violations": violations
    }

# Run with: uvicorn api:app --reload
```

## GraphQL API Example

```graphql
type Query {
  rule(id: String!): Rule
  rules(language: String, category: String, tags: [String]): [Rule]
  checkCompliance(code: String!, language: String!): ComplianceResult
}

type Rule {
  id: String!
  summary: String!
  category: String!
  language: String!
  severity: String!
  requirements: [Requirement]
  antipatterns: [Antipattern]
  examples(type: ExampleType): [Example]
}

type Requirement {
  id: String!
  description: String!
  rationale: String
  impact: String
}

type Antipattern {
  id: String!
  description: String!
  why: String
  instead: String
}

type Example {
  id: String!
  title: String!
  code: String!
  explanation: String!
  type: ExampleType!
}

enum ExampleType {
  GOOD
  BAD
}

type ComplianceResult {
  compliant: Boolean!
  violations: [Violation]
}

type Violation {
  ruleId: String!
  violationId: String!
  message: String!
  suggestion: String
  line: Int
  column: Int
}
```

## Embedding-Based Semantic Search

```python
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

class RuleSemanticSearch:
    """Semantic search for workflow-tools rules."""
    
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.rule_data = []
        
    def build_index(self):
        """Build FAISS index for all rules."""
        with open("rules/rules-index.json") as f:
            rules_index = json.load(f)
        
        # Collect all rule content
        texts = []
        for rule_id, rule in rules_index["rules"].items():
            # Combine relevant text
            text = f"{rule['summary']} {' '.join(rule['tags'])}"
            
            # Add requirements and antipatterns
            rule_path = Path(f"rules/{rule['file_path']}")
            if rule_path.exists():
                extractor = RuleExtractor(rule_path)
                reqs = extractor.extract_requirements()
                for req in reqs:
                    text += f" {req['requirement']}"
            
            texts.append(text)
            self.rule_data.append({
                "rule_id": rule_id,
                "summary": rule["summary"],
                "file_path": rule["file_path"]
            })
        
        # Create embeddings
        embeddings = self.model.encode(texts)
        
        # Build FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype('float32'))
    
    def search(self, query: str, k: int = 5):
        """Search for relevant rules."""
        # Encode query
        query_embedding = self.model.encode([query])
        
        # Search
        distances, indices = self.index.search(
            query_embedding.astype('float32'), 
            k
        )
        
        # Return results
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.rule_data):
                result = self.rule_data[idx].copy()
                result['relevance_score'] = float(1 / (1 + distance))
                results.append(result)
        
        return results

# Usage
searcher = RuleSemanticSearch()
searcher.build_index()

results = searcher.search("how to name tests in React")
for result in results:
    print(f"{result['rule_id']}: {result['summary']} (score: {result['relevance_score']:.3f})")
```

## Streaming Response Example

```python
async def stream_rule_analysis(code: str, language: str):
    """Stream rule analysis results as they're processed."""
    with open("rules/rules-index.json") as f:
        rules_index = json.load(f)
    
    # Find applicable rules
    applicable_rules = [
        (rule_id, rule) for rule_id, rule in rules_index["rules"].items()
        if rule["language"] == language
    ]
    
    for rule_id, rule in applicable_rules:
        # Process one rule at a time
        rule_path = Path(f"rules/{rule['file_path']}")
        extractor = RuleExtractor(rule_path)
        
        # Check antipatterns
        antipatterns = extractor.extract_antipatterns()
        for antipattern in antipatterns:
            if check_pattern(code, antipattern):
                yield {
                    "type": "violation",
                    "rule_id": rule_id,
                    "violation": antipattern["id"],
                    "message": antipattern["antipattern"],
                    "suggestion": antipattern["instead"]
                }
        
        # Also yield progress
        yield {
            "type": "progress",
            "rule_id": rule_id,
            "status": "completed"
        }

# FastAPI streaming endpoint
from fastapi.responses import StreamingResponse

@app.post("/api/rules/analyze-stream")
async def analyze_stream(code: str, language: str):
    async def generate():
        async for result in stream_rule_analysis(code, language):
            yield f"data: {json.dumps(result)}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )
```

## Caching Strategy

```python
from functools import lru_cache
import hashlib
import redis

# Redis cache for rule queries
cache = redis.Redis(host='localhost', port=6379, decode_responses=True)

def cache_key(rule_id: str, section: str) -> str:
    """Generate cache key for rule section."""
    return f"rule:{rule_id}:{section}"

@lru_cache(maxsize=100)
def get_rule_section_cached(rule_id: str, section: str):
    """Get rule section with caching."""
    # Check Redis cache first
    cached = cache.get(cache_key(rule_id, section))
    if cached:
        return json.loads(cached)
    
    # Load from file
    rule_path = Path(f"rules/{rule_id}.md")
    extractor = RuleExtractor(rule_path)
    
    if section == "requirements":
        data = extractor.extract_requirements()
    elif section == "antipatterns":
        data = extractor.extract_antipatterns()
    else:
        data = extractor.extract_section(section)
    
    # Cache for 1 hour
    cache.setex(
        cache_key(rule_id, section),
        3600,
        json.dumps(data)
    )
    
    return data
```

## Batch Processing Example

```python
async def batch_check_compliance(files: List[Dict[str, str]]):
    """Check multiple files for compliance in batch."""
    results = {}
    
    # Group files by language
    by_language = {}
    for file_info in files:
        lang = file_info['language']
        if lang not in by_language:
            by_language[lang] = []
        by_language[lang].append(file_info)
    
    # Process each language group
    for language, file_group in by_language.items():
        # Load rules once per language
        rules = load_rules_for_language(language)
        
        # Check each file
        for file_info in file_group:
            violations = []
            for rule in rules:
                rule_violations = check_file_against_rule(
                    file_info['content'],
                    rule
                )
                violations.extend(rule_violations)
            
            results[file_info['path']] = {
                'violations': violations,
                'compliant': len(violations) == 0
            }
    
    return results
```

## Integration Tips

1. **Minimize Context**: Use extraction tools to load only needed sections
2. **Cache Aggressively**: Rules don't change often, cache parsed results
3. **Batch Operations**: Process multiple files/rules together
4. **Use Indexes**: Pre-build indexes for fast lookups
5. **Stream Results**: For large operations, stream results as available
6. **Semantic Search**: Use embeddings for natural language queries
7. **Version Control**: Track rule versions for consistency
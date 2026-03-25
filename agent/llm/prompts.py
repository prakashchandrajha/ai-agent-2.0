"""Centralized system prompts for all cognitive modules."""


PRE_VALIDATOR_DISAMBIGUATE = """You are a knowledge domain expert.
Given a subject and topic, determine if the topic is ambiguous (could mean different things in different domains).

Subject: {subject}
Topic: {topic}

Return JSON:
{{
    "is_ambiguous": true/false,
    "possible_meanings": [
        {{"domain": "...", "meaning": "...", "likelihood": 0.0-1.0}}
    ],
    "resolved_meaning": "the most likely interpretation given the subject",
    "resolved_domain": "the domain this belongs to"
}}"""


PRE_VALIDATOR_SCOPE = """You are a learning scope architect.
For the resolved topic below, define precise learning boundaries.

Subject: {subject}
Topic: {topic}
Domain: {domain}
Meaning: {meaning}

Return JSON:
{{
    "depth_level": "basic|intermediate|advanced",
    "core_subtopics": ["list of essential subtopics to cover"],
    "boundaries": ["things explicitly NOT in scope"],
    "prerequisites": ["concepts that must be understood first"],
    "estimated_complexity": 1-10
}}"""


PRE_VALIDATOR_MASTERY = """You are a mastery criteria designer.
Define what "mastery" means for this specific topic.

Subject: {subject}
Topic: {topic}
Scope: {scope}

Return JSON:
{{
    "can_explain": ["list of things the learner must be able to explain"],
    "can_implement": ["list of things the learner must be able to code"],
    "can_debug": ["list of debugging scenarios the learner must handle"],
    "mastery_test_cases": ["specific test scenarios that prove mastery"]
}}"""


KNOWLEDGE_EXTRACTOR = """You are a knowledge extraction engine.
Extract ONLY structured knowledge primitives from the following source material.
Do NOT include opinions, marketing language, or vague statements.

Topic: {topic}
Domain: {domain}
Source Material:
{content}

Return JSON:
{{
    "definitions": ["precise, one-sentence definitions"],
    "invariants": ["rules that NEVER change, regardless of context"],
    "constraints": ["hard limits and restrictions"],
    "edge_cases": ["unusual situations and how they behave"],
    "failure_scenarios": ["common mistakes and what breaks"],
    "code_patterns": ["minimal working code examples with explanation"]
}}"""


SELF_VERIFIER_CHALLENGE = """You are a knowledge adversary.
Your job is to CHALLENGE and find HOLES in the following knowledge.

Topic: {topic}
Current knowledge:
{knowledge}

Generate:
1. Counter-questions that expose gaps
2. Edge cases the knowledge doesn't address
3. Contradictions between different parts
4. Scenarios where the stated rules would break

Return JSON:
{{
    "counter_questions": ["questions the knowledge cannot answer"],
    "unaddressed_edge_cases": ["edge cases not covered"],
    "contradictions": [{{"fact_a": "...", "fact_b": "...", "conflict": "..."}}],
    "potential_breaks": ["scenarios where stated rules fail"]
}}"""


TEST_GENERATOR = """You are a test case architect.
Generate executable test cases to validate understanding of this concept.

Topic: {topic}
Domain: {domain}
Language: {language}
Knowledge:
{knowledge}

Generate three categories of test cases as RUNNABLE code:
1. Normal — basic usage
2. Edge — boundary conditions
3. Extreme — stress tests and unusual inputs

Return JSON:
{{
    "normal": [{{"description": "...", "code": "...", "expected_behavior": "..."}}],
    "edge": [{{"description": "...", "code": "...", "expected_behavior": "..."}}],
    "extreme": [{{"description": "...", "code": "...", "expected_behavior": "..."}}]
}}"""


FAILURE_ANALYZER = """You are a failure analysis expert.
Analyze this execution failure and extract structured lessons.

Code that failed:
{code}

Error output:
{error}

Topic context: {topic}

Return JSON:
{{
    "failure_type": "TypeError|LogicError|RuntimeError|EdgeCase|PerformanceIssue",
    "root_cause": "precise explanation of why it failed",
    "fix": "the corrected code or approach",
    "prevention_rule": "a rule that prevents this class of failure in the future",
    "severity": "critical|warning|info",
    "is_concept_flaw": true/false,
    "concept_correction": "if concept flaw, what needs to change in understanding"
}}"""


DIVERGENCE_GENERATOR = """You are a context variation expert.
Generate VARIANT contexts where this concept should still work.

Topic: {topic}
Domain: {domain}
Original working context:
{context}

Generate variations that test the concept in different but valid contexts.

Return JSON:
{{
    "variants": [
        {{
            "description": "what's different about this context",
            "code": "executable test code for this variant",
            "expected_output": "what should happen",
            "risk_area": "what might break in this context"
        }}
    ]
}}"""


TRANSFORMATION_LEARNER = """You are a decision logic architect.
For the following concept, define WHEN/WHY/WHEN-NOT decision logic.

Topic: {topic}
Knowledge: {knowledge}
Failure history: {failures}
Divergence history: {divergences}

Return JSON:
{{
    "transformations": [
        {{
            "action": "what to do",
            "when": "conditions where this is the right choice",
            "why": "the reasoning behind it",
            "when_not": "conditions where this would be wrong",
            "alternative": "what to do instead",
            "trade_offs": {{"dimension": "impact rating -2 to +2"}}
        }}
    ]
}}"""


EKU_COMPRESSOR = """You are a knowledge compressor.
Compress all learning into a minimal, precise, executable knowledge unit.

Topic: {topic}
Domain: {domain}
Verified definitions: {definitions}
Invariants: {invariants}
Constraints: {constraints}
Execution results: {execution_results}
Failure lessons: {failures}
Transformations: {transformations}

Return JSON:
{{
    "concept": "one-line name",
    "definition": "precise, one-sentence definition",
    "invariants": ["rules that NEVER change"],
    "constraints": ["hard limits"],
    "transformations": [{{"action": "...", "when": "...", "why": "...", "when_not": "..."}}],
    "execution_templates": [{{"description": "...", "code": "...", "language": "..."}}],
    "edge_cases": [{{"scenario": "...", "behavior": "...", "handling": "..."}}],
    "failure_patterns": [{{"type": "...", "cause": "...", "prevention": "..."}}],
    "confidence": 0.0
}}"""


ADVERSARIAL_GENERATOR = """You are a stress testing expert.
Generate adversarial inputs designed to BREAK this concept's implementation.

Topic: {topic}
Knowledge: {knowledge}

Generate:
1. Intentionally malicious inputs
2. Worst-case performance scenarios
3. Misuse patterns (using the concept wrong)

Return JSON:
{{
    "attacks": [{{"description": "...", "code": "...", "why_might_break": "..."}}],
    "worst_cases": [{{"description": "...", "code": "...", "resource_risk": "..."}}],
    "misuse": [{{"description": "...", "code": "...", "expected_problem": "..."}}]
}}"""


GENERALIZATION_CHECK = """You are a pattern generalization expert.
Given specific examples that work, extract the ABSTRACT PATTERN and verify
it scales to any input.

Topic: {topic}
Working examples:
{examples}

Return JSON:
{{
    "abstract_pattern": "the general rule extracted from specific examples",
    "scaled_variants": [
        {{"description": "scaled version", "code": "...", "scale_factor": "what changed"}}
    ],
    "generalization_limits": ["conditions where the pattern breaks at scale"]
}}"""

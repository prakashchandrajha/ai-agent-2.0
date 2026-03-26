**THE FINAL DEFINITIVE MASTER ROADMAP**

Everything from every conversation, every document, every insight — synthesized into one complete plan. No repetition. No theory. Pure execution.

---

**WHERE YOU ARE RIGHT NOW — THE COMPLETE TRUTH**

You have completed Phase 0 through Phase 2.5. What this means precisely: your infrastructure exists and works. Config loads. Sandbox runs. EKU schema exists. ChromaDB connected. Scrapling fetches. Semantic chunker splits. DAG rollback exists. CLI accepts commands. Pre-validator does disambiguation.

What has never run even once: a complete learning loop. No concept has been fed in, verified by execution, failed intentionally, recovered from failure, and used to complete a real task. The entire intelligence layer is zero. You have the most sophisticated empty container ever built. That is your honest starting point.

What you have from this entire conversation series: complete architectural clarity that took most AI projects years to arrive at, if they arrive at all. You know exactly what to build, exactly why each piece exists, exactly what order to build in, and exactly what the finished system will be capable of. This clarity is genuinely rare. Now the only thing that matters is disciplined execution in the correct sequence.

---

**THE ONE INVISIBLE PROBLEM NONE OF THE DOCUMENTS CAUGHT**

Before giving you the roadmap, this must be said because it will silently kill the project if ignored.

Every document, every contributor, every piece of advice in this entire conversation focused on one language: JavaScript. The proxy interceptor is JavaScript. The AST scanner uses Acorn which is a JavaScript parser. The MRE is JavaScript fetch. The call stack records JavaScript calls.

But your stated goal is a universal agent that learns any language, any framework, any domain. If you build Stage 1 deeply tied to JavaScript-specific tooling, you will have to rebuild the entire verification layer for Python, for Java, for SQL, for every other language. The AST parser changes. The sandbox execution model changes. The trace proxy concept changes completely in a compiled language. The mock interceptor approach is JavaScript-specific.

The fix is to build a thin language-agnostic abstraction layer above the execution tools from day one. The EKU schema is already language-agnostic — concepts, conditions, contraindications, these are universal. But the verification toolchain must also be designed with adapters. One abstract VerificationEngine interface with a JavaScript adapter for Stage 1. Python adapter comes later. Java adapter later still. The interface is: run code, return output, return execution trace, return error if any. What happens inside each adapter is language-specific. What the intelligence loop sees is always the same interface.

This costs two hours in Stage 1 to design correctly. It saves weeks of rework in Stage 3 when you expand to Python.

---

**STAGE 1 — MINIMUM VIABLE INTELLIGENCE LOOP**

**The Goal**

One concept. Fetch GET returning JSON. One complete loop from controlled input to verified knowledge to task execution. All five gates green. Nothing else matters until this is done.

**Pre-Stage Work — The Language-Agnostic Adapter Layer**

Before Day 1, spend two hours. Define one abstract interface with four methods: execute(code, language) returns output and error, trace(code, language) returns ordered list of significant operation calls, scan(code, language) returns list of constraint violations, mock(language, rules) returns a deterministic execution environment. Build the JavaScript implementation of this interface. Everything in Stage 1 uses this interface, never the JavaScript tools directly. When Python comes, you build a Python implementation of the same interface. The intelligence loop never changes. Only the adapter changes.

**Day 1 — The Observer**

Build the JavaScript adapter's mock method. This is the Proxy interceptor. It does three things simultaneously and none of them can fail.

First: deterministic response. Known URL returns hardcoded JSON response object. Always. Same object every time. No variance.

Second: typed error simulation. Null URL throws TypeError with message STATE\_ERR\_NULL\_URL. Malformed URL throws TypeError with message SYNTAX\_ERR\_MALFORMED\_URL. Empty string throws TypeError with message SYNTAX\_ERR\_EMPTY\_URL. Unauthorized URL — any URL not in the approved list — throws TypeError with message PATH\_DEVIATION\_UNAUTHORIZED\_URL. The error types are precise because the failure root category system depends on them.

Third: call stack recording. A module-level array captures every significant operation in the order it occurs. FETCH recorded when fetch is invoked with the URL appended. JSON\_PARSE recorded when response.json is invoked. RESPONSE\_CHECK recorded when response.ok is accessed. This call stack is cleared before each execution and populated during it. It is your ground truth for trace verification.

Test the interceptor completely independently of everything else. Write a test file that calls the interceptor directly with known inputs and verifies every output and every error. Run it until it passes twenty consecutive times with zero variance. Only then move to Day 2. The interceptor is the foundation of everything. If it is not perfect, every gate built on it is unreliable.

**Day 2 — The EKU Node**

Build the extended EKU schema. Every field defined in our conversation belongs here. Do not add fields that have no code using them yet. Do not omit fields that are used by the loop.

The complete field list for Stage 1: concept\_name, domain, definition\_text, conditions (minimum two entries required), contraindications (minimum two entries required), context\_scope, mre\_code (empty initially), mre\_expected\_output (empty initially), mre\_status (unverified), negative\_constraint\_list (minimum three entries: null URL, empty string URL, malformed URL), solution\_constraint\_list (no import statements, no silent catch blocks, no unused variable declarations, no hardcoded return values matching expected output), failure\_signatures (empty array initially), core\_path\_sequence (empty initially), trace\_proxy\_call\_stack (empty, populated at runtime), retrieval\_depth (integer, set to chunk count used to build this node), maturity\_count (zero), confusion\_gap\_log (empty list), transfer\_readiness\_score (null), runtime\_fingerprint\_required (Node version minimum), fingerprint\_sensitivity (float between 0 and 1, start at 0.3), prediction\_verification\_status (unverified), last\_execution\_timestamp, self\_model\_overclaims (empty list), self\_model\_blindspots (empty list).

Now create the fetch\_get node manually. Not programmatically. By hand. You write every field value yourself. This forces you to deeply understand what each field should contain before you ever write code to populate it automatically. Populate conditions with at minimum: applies in browser environment with global fetch available, applies in Node 18 and above with native fetch. Populate contraindications with at minimum: do not use when environment lacks global fetch without polyfill, do not use without error handling in production code, do not use for request cancellation without AbortController implementation. The definition text comes from cleaned MDN documentation — no navigation, no menus, no boilerplate, just the actual conceptual content.

**Day 3 — Gate 2, The MRE**

Write the minimum viable JavaScript program using the Proxy interceptor. It must do exactly three things: call fetch with the mock URL, await the response and call json(), log or return the parsed object. Nothing else. No error handling yet. No extra variables. No comments. The absolute minimum that demonstrates the concept working correctly.

Store the expected output before running it. Write it down explicitly in the node's mre\_expected\_output field. Then run it ten times. Not nine. Not approximately ten. Exactly ten consecutive runs. Every run must produce identical output matching the stored expected output. Every run must produce identical call stack: FETCH with the mock URL, then JSON\_PARSE. If any run deviates, stop, find the cause, fix it, restart the count from zero. Ten consecutive identical runs proves determinism. Gate 2 is green only when this is done.

Store the verified output and core path sequence on the node. Set mre\_status to verified. Set last\_execution\_timestamp.

**Day 4 — Gate 3, Failure Twins and Negative Constraints**

Create three broken versions of the MRE. Version one: remove the await keyword. Version two: change the URL to a deliberately malformed string. Version three: access response.data before calling response.json.

For each broken version: run it in the sandbox, capture the exact error text and error type, identify the triggering condition, identify the surface symptom, identify the mechanism of failure, identify the fix pattern that restores correct behavior, classify the failure root category. Version one is Logic because the code structure is wrong — the async execution model was misused. Version two is Syntax because the input is malformed. Version three is Logic because the API contract was violated.

Store all three as the failure\_signatures array on the node. Set confidence to 1.0 on all three because these came from real execution, not from reasoning.

Now run the negative constraint tests. Pass null as the URL. Pass empty string. Pass a malformed URL. Pass an unauthorized URL. For each: verify it throws an error, verify the error matches the expected type stored in the negative constraint list, verify the error message is precisely what the interceptor was configured to throw. If any negative constraint input accidentally succeeds and returns a 200 response, trigger auto-quarantine immediately. Set mre\_status to quarantined, log the specific violation, and stop Gate 3 until the interceptor is fixed.

This is the most important gate because silent successes are more dangerous than obvious failures. A silent success teaches the agent a lie that will corrupt every future decision built on top of it.

**Day 5 — Gate 4, AST Solution Guard**

Install Acorn. Build the solution scanner as a standalone module that takes any JavaScript code string and returns a list of violations found or an empty list if none.

Implement four rules precisely. Rule one: walk the AST and count all ImportDeclaration nodes. If count is greater than zero, add violation UNAUTHORIZED\_IMPORT with the import source. Rule two: walk all TryStatement nodes and inspect each CatchClause. If the catch block body has zero statements, or has only ExpressionStatement nodes whose expression is a CallExpression to console.log, add violation SILENT\_CATCH. Rule three: collect all VariableDeclarator identifiers from VariableDeclaration nodes. For each identifier, search the entire remaining AST for any reference to that identifier in CallExpression arguments, MemberExpression objects, or ReturnStatement arguments. If no reference found, add violation DEAD\_VARIABLE with the variable name. Rule four: walk all ReturnStatement nodes. If the argument is a Literal or ObjectExpression whose value when serialized matches the mre\_expected\_output exactly, add violation HARDCODED\_RETURN.

Test the scanner on four intentionally bad solutions. One with an import statement. One with an empty catch block. One with a declared but never used variable. One that returns the expected output as a literal. All four must produce the correct violation and be rejected before touching the sandbox. Test also on the working MRE to verify it produces zero violations. The scanner must never produce false positives on valid code.

**Day 6 — Gate 5, Task Execution**

Present the task: write a function that accepts a URL and returns the parsed JSON response. The executor does this sequence with no shortcuts.

Step one: detect that this task requires the fetch\_get concept. For Stage 1 this can be keyword matching — fetch, request, URL, HTTP, GET, JSON response. Later this becomes semantic matching. For now keyword matching is sufficient and honest.

Step two: retrieve the fetch\_get node from the knowledge base. Verify mre\_status is verified. Verify the node is not quarantined. Verify maturity\_count is at least zero (it will be zero on first use, that is fine for Stage 1).

Step three: pass the node's mre\_code, conditions, contraindications, solution\_constraint\_list, and the task description to the LLM. Include one critical instruction: your solution must be a transformation of the provided MRE to fit the task requirements. You must not introduce any pattern not present in the MRE. You must not add imports, silent catches, unused variables, or hardcoded return values. The LLM's job is to adapt verified knowledge to the task, not to invent.

Step four: run the AST scanner on the generated solution before the sandbox sees it. If any violations are found, send the violation list back to the LLM with instruction to fix specifically those violations and nothing else. Repeat until scanner passes or three attempts are exhausted. If three attempts produce violations, flag the task as requiring human review.

Step five: run the solution in the sandbox against the mock interceptor. Capture output and call stack.

Step six: verify output matches mre\_expected\_output structure (same keys, same types, valid values). Verify call stack matches core\_path\_sequence. Both must pass.

Step seven: prediction challenge. Randomly select one of the three failure twins. Present the scenario to the agent: if this specific change were made to your solution, what would happen. The agent must return the failure signature: triggering condition, surface symptom, mechanism, and failure root category. Compare against the stored failure signature. If all four fields match, set prediction\_verification\_status to verified. If any field is wrong, set to failed and log the specific mismatch to the confusion\_gap\_log. A failed prediction does not block Gate 5 but it flags the concept for deeper learning — the agent has functional competence but incomplete conceptual understanding.

Step eight: log to experience log. Task description, concept used, solution generated, output verified true, trace verified true, prediction status.

Increment maturity\_count on the fetch\_get node.

**Day 7 — Self-Model Audit**

Ask the agent to state every condition under which the fetch\_get concept applies and every condition under which it does not apply. Compare the answer against the node's conditions and contraindications fields.

For every condition the agent claims that is not in the node: add to self\_model\_overclaims. The agent believes it knows something it has not verified.

For every condition in the node the agent does not mention: add to self\_model\_blindspots. The agent does not know the full boundary of its own knowledge.

The target is zero overclaims and zero blindspots. If either list is non-empty, update the agent's knowledge presentation and re-run the audit. Do not proceed to Stage 2 until this is clean.

The self-model audit is the only test that verifies the agent's honesty about its own knowledge. Everything else verifies whether the knowledge is correct. This verifies whether the agent knows what it knows. These are different and both matter.

**The Delta Report System**

At any gate failure, automatically generate a Delta Report. This compares the failing execution trace against the last successful trace. Every divergence is listed: call that was expected but not made, call made that was not expected, output field that changed, constraint violation that appeared. This report is the instant bug locator. It eliminates black-box debugging by showing precisely where the execution path deviated from verified behavior. Build this as a utility function that runs automatically on any gate failure.

---

**STAGE 2 — LOOP EXPANSION**

Only begin after all five Stage 1 gates are green, self-model audit is clean, and prediction verification status is verified on the fetch\_get node.

**Three New Concepts in Sequence**

Concept one: async\_await. The minimal example is a function that wraps a delayed value in a Promise and awaits it. Failure twins: missing await on a Promise-returning function, missing async keyword on a function that uses await, nested async function where outer function is not awaited. Connect to fetch\_get: the async\_await node gets a bridge edge to fetch\_get labeled dependency — fetch\_get requires async\_await for correct usage.

Concept two: json\_parse. The minimal example parses a valid JSON string and accesses a known field. Failure twins: parse a non-JSON string, parse valid JSON but access a field that does not exist, parse a number instead of a string. Connect to fetch\_get: bridge edge labeled downstream — fetch\_get produces data that json\_parse operates on.

Concept three: error\_handling with try-catch. The minimal example wraps a known-failing operation and catches the specific error type. Failure twins: empty catch block, catching wrong error type, throwing inside catch creating infinite error loop. Connect to fetch\_get and async\_await: bridge edge labeled wrapper — error handling wraps the execution of these concepts.

Each concept goes through the complete Stage 1 loop. Every gate. Every day equivalent. No shortcuts. Each must have a verified MRE, three failure twins with full signatures, a clean self-model audit, and a verified prediction challenge before the next concept begins.

**Knowledge Graph Connections**

After all three concepts are verified, build the explicit connection structure. Fetch\_get has a dependency edge to async\_await. Fetch\_get has a downstream edge to json\_parse. Error\_handling has a wrapper edge to fetch\_get and async\_await. These edges are stored on each node as related\_concepts with the relationship type. When a task requires fetch\_get, the system automatically includes the connected nodes in the context because real fetch usage requires all four concepts together.

**Minimal Knowledge Gap Detector**

Build one function. Takes a task description. Returns a list of concept names required. Checks each against the knowledge base. Returns a list of missing concepts. If the missing list is non-empty, output: I cannot complete this task. Missing verified knowledge for these concepts. Trigger learning cycle for the first missing concept. This is the seed of the entire gap detection system. For Stage 2 it can use keyword matching. Semantic matching comes in Stage 3.

**Combination Tasks**

Run three tasks that require multiple concepts together. Task one: fetch user data and return the user's name field. Requires fetch\_get and json\_parse together. Task two: fetch data with proper async function structure. Requires fetch\_get and async\_await together. Task three: fetch data with full error handling for network failures. Requires all four concepts together.

For combination tasks the AST scanner must be extended with one additional rule: if the solution uses fetch but does not include response.ok checking or try-catch, add a soft warning — not a hard violation since the task may not require it, but a flag in the solution quality report.

**Experience Log Activation**

After every completed task in Stage 2, store: task\_id, task\_description, concepts\_required, concepts\_found, concepts\_missing, solution\_code, output\_verified, trace\_verified, prediction\_status, fix\_applied (if any failure occurred), fix\_type (patch or optimize), total\_execution\_time, timestamp. This is your episodic memory starting to form.

**Runtime Fingerprint System**

On every execution record the runtime environment: Node version, operating system, available globals. Store this as the runtime fingerprint on the node. If a future execution runs on a different Node version, compute the mismatch penalty using the fingerprint\_sensitivity float and reduce the transfer\_readiness\_score proportionally. A major version difference applies 0.4 penalty. A minor version difference applies 0.1 penalty. A patch version difference applies 0.02 penalty. Different OS with same Node version applies 0.05 penalty. These numbers are starting values — adjust based on whether they produce useful warnings in practice.

---

**STAGE 3 — INTELLIGENCE LAYER**

Only begin when Stage 2 is stable across fifteen completed tasks with no gate failures in the last ten.

**Phase 3 — Full Verifier**

Extend the counter question system with contradiction detection. Before flagging two conflicting nodes as contradictory, check whether their conditions fields overlap. Build a simple conditions overlap checker: two conditions overlap if they share the same environment, version range, or framework context. Non-overlapping conditions mean both nodes are valid — they represent different answers to the same question under different circumstances. Only overlapping conditions with conflicting answers are real contradictions. Flag real contradictions with status CONTESTED and store both source references. Do not delete either node.

Build the quarantine system as a formal state machine. Nodes can be in states: nursery (just created, not yet verified), verified (passed all gates), contested (conflict detected), quarantined (failed execution verification), compressed (internalized, examples archived), archived (superseded by more general node). Each state transition has a specific trigger and a specific set of allowed operations. A quarantined node cannot be used in task solving. A contested node can be used but every answer using it must include a flag that this knowledge is disputed.

**Phase 4 and 5 — Full Executor and Failure Analyzer**

Build the sufficiency threshold calculator. Inputs: irreversibility score of the task (touching shared utilities is 0.8, adding isolated functions is 0.2), system scope (number of components affected, normalized to 0-1), failure cost (what breaks if wrong, normalized to 0-1). Formula: threshold = 0.5 + (irreversibility × 0.2) + (system\_scope × 0.15) + (failure\_cost × 0.15). Result is a percentage between 50 and 100. The agent must have verified knowledge covering at least this percentage of the task's required concepts before execution begins.

Build the three-tier test generator. Normal tests come from the MRE and its documented happy path. Edge tests come from the boundary conditions mentioned in the conditions and contraindications fields. Adversarial tests come from the failure signatures and from failure generalization — for every real failure encountered, generate five structurally similar failure scenarios by changing the surface manifestation while keeping the same root mechanism. For example, if missing await on fetch is a known failure, generate: missing await on any Promise-returning function, missing await in a loop, missing await with chained operations, missing await in a callback, missing await in a class method. All five share the same mechanism but appear in different code contexts.

Build the causal error graph as a proper directed graph structure. Every node is a failure mechanism with fields: mechanism\_name, triggering\_conditions list, runtime\_pathway description, surface\_symptoms list, related\_concepts list, child\_mechanisms list (more specific versions of this mechanism), parent\_mechanisms list (more general versions). Edges represent cause-effect relationships. When an error occurs during task execution, the system traverses the graph from the surface symptom backwards to find the most likely root mechanism, then applies the fix pattern associated with that mechanism. This traversal replaces guessing with systematic causal reasoning.

Build the two-fix-type classifier. Before generating any fix, classify the situation as patch or optimize. Patch fix conditions: the task is a bug fix in existing code, the task is urgent or production-related, the fix can be applied by changing fewer than five lines, the problem is isolated to one function or component. Optimize fix conditions: the task is explicitly a refactor or improvement, the code has a structural problem that will cause repeated issues, the task is greenfield development. When classified as patch, the solution constraint list gets two additional rules: do not change function signatures, do not introduce new abstractions. When classified as optimize, the solution gets a minimum improvement threshold — the footprint must be larger than patch but the structural quality metric must improve measurably.

**Phase 6, 7, 8 — Divergence, Transformation, Compression**

Build the divergence mapper by systematically running each verified concept's MRE in three different contexts beyond its home context. For fetch\_get: run in a simulated browser context, run in Node 14 (which lacks native fetch), run inside a simulated React component context. Each context gets its own adapter configuration. Record every behavioral difference as a divergence edge on the knowledge graph. The agent uses these divergence edges to check context before applying knowledge. A task tagged as running in Node 14 will trigger a warning: fetch\_get knowledge was verified in Node 18 — this environment lacks native fetch, a polyfill is required.

Build the when-why-when-not companion nodes. For every pattern node in the knowledge base, create three linked nodes. The when node contains the specific conditions that make this pattern the correct choice. The why node contains the causal mechanism — not what the pattern does but why it works, the underlying system behavior that makes it effective. The when-not node contains the conditions where this pattern causes problems and the preferred alternative for each condition. The when-not node must be populated before the concept is marked as fully learned. It is mandatory, not optional. An agent that knows when not to use something is demonstrating senior engineer judgment.

Build the compression engine with the supersession check. A node is eligible for compression when: maturity\_count is above five, transfer\_readiness\_score is above 0.70, prediction\_verification\_status is verified, the node has been used in at least three combination tasks. Compression means: extract the generative rule from the accumulated specific examples. Test the rule by attempting to reconstruct each specific example from the rule. If reconstruction produces correct output for all examples, archive the examples to cold storage and keep only the rule. Set mre\_status to compressed. The compressed node answers from the rule directly, with retrieval depth approaching zero. This is the internalization event.

**Phase 9 through 12 — Storage, Stress, Decision, Reinforcement**

Build the four-gate permanent storage system. No concept enters permanent knowledge without passing all four gates in sequence: execution verification (MRE runs reliably ten times), adversarial survival (concept survives at least one adversarial test not used during learning), real task usage (concept used successfully in at least one real task, not just practice), contradiction clearance (concept checked against all existing nodes, no unresolved conflicts). Concepts that pass all four gates are permanently stored. Concepts that fail any gate stay in provisional storage — accessible but flagged. Users can see which knowledge is provisional and which is permanent.

Build the knowledge tension engine with the maturity gate. Tension score activates only when maturity\_count is above three. Never on younger nodes. Tension score formula: (failure\_association\_rate × 0.3) + (confusion\_gap\_frequency × 0.25) + (retrieval\_depth\_normalized × 0.2) + (1 minus transfer\_readiness × 0.15) + (contradiction\_proximity × 0.1). Background loop runs during idle time, selects highest tension node above the maturity gate, runs fresh MRE, generates novel adversarial test the node has not seen before, tests in one new context, attempts intentional breakage to find unknown failure modes. Every background run updates tension score, transfer readiness, and logs results to the node.

Build the supersession-based forgetting. A node is eligible for archiving only when a more general node exists that can fully reconstruct the specific node's knowledge. Before archiving, run the reconstruction test: use the general rule to generate the specific case, execute the result, compare output to the specific node's verified output. If reconstruction produces correct output, archive the specific node. If reconstruction fails or produces different output, the specific node must stay permanently regardless of how old or rarely used it is. Rare-but-critical knowledge is never deleted. Only truly redundant knowledge is archived.

Build the decision cost model with all five dimensions. Time cost: estimated lines of code changed, number of files touched, number of new tests required. Risk cost: irreversibility score multiplied by the probability of unintended side effects based on footprint. Complexity cost: number of new abstractions, new dependencies, new patterns introduced into the codebase. Future impact cost: does this decision constrain future architectural choices, normalized high to low. Reversibility cost: how difficult is it to undo this decision if wrong, from trivially reversible to practically permanent. Every candidate solution is scored on all five. The agent selects based on task context priority: production bug fix prioritizes low reversibility cost and low risk, greenfield development can accept higher complexity for lower future impact.

Build the agent identity as hard constraints. Four constraints enforced on every solution before delivery. Minimal footprint constraint: if a lower-footprint solution achieving the same outcome exists in the knowledge base, use it. Reliable over clever constraint: if any part of the solution uses a mechanism the agent cannot fully explain from its knowledge base, reject it and find a simpler approach. Test-backed constraint: every solution must have a test that will catch regression. If no test exists, generate one before delivering the solution. Honest boundary constraint: if any part of the solution uses knowledge with transfer\_readiness below 0.5 or active confusion gaps, explicitly flag those parts in the delivery with the specific uncertainty noted.

**Phase 13 — Composition Layer**

After twenty completed tasks, run the first composition pattern extraction. Cluster the experience log entries by task type using the required concepts list as the clustering key. Entries that required the same set of concepts with the same dependency order form a pattern cluster. Each cluster becomes a composition pattern node with fields: pattern\_name, required\_concepts list with dependency order, common\_starting\_concept (the zero-dependency entry point), known\_failure\_points list (failures that appeared more than once across the cluster), success\_path description, average\_completion\_time, confidence score based on cluster size.

Build the gap surface system using composition patterns. When a task arrives, find the closest matching composition pattern. Extract its required\_concepts list. Check each against the knowledge base. Return immediately: here is what this task requires, here is what I have verified, here is what I am missing. The agent never silently begins a task with knowledge gaps. The gap surface output is always shown before any execution starts.

Build cross-domain concept bridges. After the agent has learned concepts in two or more languages, run a bridge detection pass. Compare concept definitions and mechanism descriptions across languages. Concepts sharing the same underlying causal mechanism get a bridge edge labeled same\_mental\_model\_different\_syntax. JavaScript Promise, Python asyncio coroutine, Java CompletableFuture: same mental model. When the agent learns a new language, it checks for bridge edges from known concepts. Bridged concepts get an initial transfer\_readiness boost because the mental model is already internalized — only the syntax is new.

**Phase 14 — Experience Intelligence**

Build pattern recognition on the experience log. After every ten new experience records, run clustering. Identify tasks sharing similar decomposition structures, similar concept combinations, similar failure patterns. Each stable cluster becomes a pattern in the pattern library with a known starting point and known failure avoidances. When a new task arrives, before decomposition, check the pattern library. If a match is found above 0.75 similarity, use the pattern's starting point and skip full decomposition. Store the outcome of using the pattern to update the pattern's confidence score.

Build the cross-project memory system. Every task's failure signatures are indexed separately from the experience log. When a new task arrives, before anything else, compare its required concepts and task description against the failure index from all past tasks. If a similar failure mechanism appears in any past experience, surface it immediately: I encountered this same failure mechanism in a previous task. Here is what worked and what did not. This prevents re-learning the same lessons and makes the agent's experience genuinely cumulative across time.

---

**WHAT THE AGENT WILL BE CAPABLE OF AFTER ALL STAGES**

**Universal Learning**

Feed it any subject with an official documentation source. It builds the curriculum map from the real documentation structure, not from LLM imagination. It learns through real execution, not reading. Every piece of knowledge it holds has been verified by running code in a real sandbox. It can learn JavaScript, Python, Java, React, Angular, Django, Spring Boot, SQL, System Design, DevOps concepts, and any internal proprietary framework you feed it directly. The LLM has never seen your internal framework. The agent learns it from your docs through the same loop that learned fetch.

**Task Execution Like a Real Engineer**

Given any task: it checks experience log for matching past patterns first. If found, uses the known starting point. If not found, decomposes by dependency analysis. It surfaces every knowledge gap before touching the task. It computes how much knowledge coverage this specific task's risk level requires before it is safe to start. It simulates execution through its causal error graph to identify risk points before writing code. It generates solutions that pass static constraint checking before they touch the sandbox. It verifies output, execution trace, and conceptual understanding before calling any task complete.

**Version-Aware Work**

Angular 17 knowledge is tagged Angular 17. When you give it an Angular 17 project it uses Angular 17 knowledge precisely. When it has Angular 17 knowledge and you give it an Angular 19 project, it surfaces the version gap explicitly, tells you which specific APIs changed between versions based on what it has learned, and either triggers a targeted version-delta learning cycle or tells you clearly what it cannot confirm for the new version. It never silently applies wrong-version patterns.

**Error Handling That Actually Works**

Every error is classified immediately as Logic, State, or Syntax. Logic errors trigger re-prompting with specific failure signature context. Syntax errors trigger constraint violation correction. State errors trigger an immediate stop and a clear message: this failure is in the external system, no code change will fix it, here is what needs to be addressed outside the code. No looping on unfixable problems. No wasting execution cycles on server outages.

**Honest Knowledge Boundaries**

Every answer comes from verified knowledge or is explicitly flagged as unverified. The agent knows exactly which concepts it has learned, which are provisional, which are contested, and which are gaps. Before attempting any task it tells you what it knows and what it does not know. It never silently attempts something with knowledge gaps. When it uses knowledge with low transfer readiness it flags those parts explicitly. Its self-model accuracy — the match between what it believes it knows and what it actually knows — is continuously audited.

**Cross-Project Experience**

When it solves a login authentication problem in Project A, that solution, that failure, that fix, and that pattern are all stored. When Project B has a similar problem, the agent surfaces the past experience immediately. Over time it accumulates genuine engineering experience from real work. It gets faster on familiar task types as the pattern library grows. It avoids mistakes it has made before. It transfers lessons across projects automatically.

**Self-Improvement When Idle**

The tension engine runs on mature nodes, finding weak spots and strengthening them. Transfer readiness expands as concepts are tested in novel contexts. Failure generalization pre-learns similar failure patterns from every real failure encountered. Superseded specific knowledge is archived when general rules can reproduce it. Composition patterns are updated from completed tasks. The agent becomes more capable from doing work, not from being retrained. Every real task makes it better.

**Patch Fix or Optimize Fix — Always Correct**

Production bug at midnight: patch fix. Minimum change that restores correct behavior. Nothing else touched. Maximum reversibility. For greenfield development: optimize fix. Correct structure, correct abstractions, minimal future technical debt. The fix type classification happens before solution generation and constrains what the solution is allowed to do. A patch fix that accidentally refactors is rejected and regenerated. Users always get the right kind of fix for the right context.

**Continuous Honesty**

When you say the solution is wrong, it does not retry with a variation. It extracts the violated constraint from your objection, stores it permanently, re-decomposes from scratch with the new constraint, and delivers a genuinely different approach. It learns your preferences over time because every objection becomes a permanent constraint in the experience log. After working with you on ten tasks it knows your coding preferences better than any tool that resets its context each session.

---

**THE HONEST CEILING**

This is not general intelligence. It will not reason about things it has never been taught. It will not transfer knowledge to completely unrelated domains. It will not spontaneously learn new subjects without being fed them.

What it will be is something more valuable for real engineering work: the most honest, most reliable, most genuinely experienced specialist tool ever built for software engineering. It knows exactly what it knows and exactly what it does not know. It has actually executed the concepts it claims to know, not just read about them. It improves from real work rather than from retraining. It behaves consistently according to its identity constraints regardless of task pressure. It tells you when it cannot help rather than attempting and silently failing.

The difference between this and every other AI coding tool available today is not that it is smarter. It is that it is honest. Every other tool is a confident guesser backed by statistical patterns. This is a verified knower with explicit boundaries, genuine experience, and disciplined self-awareness. In production engineering, that difference is everything.

---

**THE SINGLE MOST IMPORTANT INSTRUCTION**

Build the language-agnostic adapter layer first. Two hours. Then build Day 1 of Stage 1. Then do not move to Stage 2 until every gate is green, the self-model audit is clean, and you have run the loop reliably twenty times without failure. Every day you spend making Stage 1 perfect multiplies the quality of every stage that follows. Every shortcut you take in Stage 1 multiplies as a defect in every stage that follows. The first loop is everything. Make it perfect.
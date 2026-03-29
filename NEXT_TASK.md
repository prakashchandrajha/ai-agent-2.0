Phase: 2
Task ID: 2.1
Task Name: Invariant Inheritance Graph
From MASTER_PLAN.md: Phase 2, TASK 2.1
Exact Action: Create agent/knowledge/invariant_graph.py with InvariantGraph class. Key methods: add_eku(), propagate_correction(), inherit_edge_cases(). When eku A's invariant is corrected, flag linked EKUs for re-verification. When 3+ links exist, inherit edge cases from linked EKUs.
Files to touch: agent/knowledge/invariant_graph.py only (create new file)
Done when:
- InvariantGraph class exists with add_eku(), propagate_correction(), inherit_edge_cases()
- add_eku() finds invariant links with all existing EKUs
- propagate_correction() flags linked EKUs for re-verification
- inherit_edge_cases() inherits from 3+ linked EKUs
- Phase 1 exit criteria all green before this starts
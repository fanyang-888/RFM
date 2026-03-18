# Phase 5 - Brutal Hiring Manager Review

## What Still Felt Average Before This Phase

1. **No dependency contract**  
   A recruiter cannot quickly verify environment requirements or reproducibility confidence.

2. **No tests**  
   Without even minimal tests, engineering maturity signal remains weak for data/AI roles in 2026.

3. **Weak proof of quality control**  
   The project had methodology notes but little automated validation of core transformation logic.

## Targeted Fixes Applied

1. Added `requirements.txt` to define a baseline runnable environment.
2. Added lightweight tests for critical logic:
   - `tests/test_features.py`
   - `tests/test_labels.py`
3. Focused tests on high-value reliability points:
   - RFM aggregation correctness
   - score column creation and format constraints
   - rule-based label output shape and validity

## Why This Improves Hiring Impact

- Demonstrates transition from notebook analysis to maintainable code practices.
- Signals that candidate understands correctness, not just visualization and model output.
- Improves interview credibility when discussing production-readiness and QA discipline.


# Decisions

## 2026-08-24 - Amendment No. 2026-01

### What changed

The system must now answer policy questions according to the date relevant to the claim or change of circumstances.

Amendment No. 2026-01 is effective from 1 March 2026.

The amendment changes:

- Earnings disregard under Section 6.4.1
- Reporting periods under Section 4.3.2 and Section 9.1.4
- Income thresholds under Section 6.6.1
- Sanction percentage under Section 10.5.2
- Adds new Section 10.5.3A

### What we changed

We treat the consolidated policy manual and Amendment No. 2026-01 as a versioned policy corpus.

The system determines which policy provisions apply based on the relevant date and the amendment's transitional provisions.

For amendments governed by determination date, the amended value is applied to determinations made on or after 1 March 2026.

For reporting changes, the reporting period is determined by the date the change occurred. Changes occurring before 1 March 2026 continue to use the previous reporting period.

Amendment-only clauses, such as Section 10.5.3A, are added to the effective evidence even though they do not exist in the original consolidated manual.

The retriever also follows explicit cross-references. This allows a retrieved clause such as Section 6.4.2, which refers to Section 6.4.1(a), to bring the referenced clause into the evidence set.

Citation validation was extended to support amendment clauses such as Section 10.5.3A.

### What we chose not to change

We did not replace the consolidated policy manual with the amendment.

We did not simply apply the latest amendment to every historical claim.

We preserved the original policy text and apply amendments according to their effective and transitional provisions.

We did not lower the general grounding threshold merely to make amendment questions pass. Instead, explicit policy cross-references and amendment-only clauses are handled as supporting evidence.

### What we would have done differently

If the date-sensitive requirement had been known earlier, the original system would have been designed with policy-version and effective-date handling from the beginning rather than treating the corpus as a single timeless policy version.

We would also have designed amendment insertions and cross-reference expansion as first-class retrieval features instead of adding them after the original retrieval pipeline was built.

### Verification

The original grounded-answer evaluation remains at:

- 10/10 passed
- 100% pass rate

Additional date-sensitive tests verified:

- Reporting before 1 March 2026: 10 calendar days
- Reporting on/after 1 March 2026: 14 calendar days
- Earnings disregard before 1 March 2026: $120/month
- Earnings disregard on/after 1 March 2026: $175/month
- Income thresholds use the appropriate historical or amended values
- First sanction uses the appropriate historical or amended percentage
- Section 10.5.3A is retrievable, grounded, cited, and displayed as evidence

## Answer / Refusal Boundary

The system uses a conservative grounding threshold because an unsupported
policy answer is more harmful than a refusal in a benefits setting.

The current grounding decision requires:

- The best retrieved clause to have a semantic similarity score of at least 0.54.
- At least 30% of the important words in the question to be present in the
  retrieved evidence.
- Additional checks for unsupported question terms.

A question is refused when these grounding requirements are not satisfied.

We deliberately did not lower the threshold simply to increase the number of
questions answered. The goal is to prefer a justified refusal over a fluent
answer that cannot be traced to the policy corpus.

When a question is refused, the system provides a next step by directing the
user to a caseworker at the Calder County Department of Household Services,
supported by §1.1.2.

### Why this boundary

The threshold was chosen as a practical balance between recall and safety.
A threshold that is too high would cause the system to refuse questions that
the policy can answer, while a threshold that is too low would increase the
risk of unsupported answers.

The 10-question evaluation set, including unsupported questions, was used to
check this behavior. The current evaluation result is 10/10 passed.

The threshold remains an explicit design decision rather than an assumption
that semantic similarity alone proves that an answer is supported.
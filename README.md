# Calder County Household Support Program

## Brite Spark 2026 — Problem 1: The Grounded Answer

A grounded AI/RAG assistant for answering questions from the Calder County Household Support Program policy manual.

The system retrieves relevant policy clauses, applies date-sensitive amendments, generates answers using only the supplied policy material, validates citations, and refuses to answer when the evidence is insufficient.

## Features

- Plain-language policy question answering
- Clause-level citations
- Supporting evidence display
- Conservative grounding and refusal logic
- Explicit refusal path with a caseworker referral
- Date-aware policy amendments
- Historical policy handling
- Amendment-only clause support
- Cross-reference expansion
- Citation validation
- Automated 10-question evaluation

## Architecture

```text
User question
     |
     v
Policy Retriever
     |
     v
Relevant policy clauses
     |
     v
Date / Amendment handling
     |
     v
Grounding check
     |
     +---- insufficient evidence ----> Refusal + referral
     |
     v
Gemini answer generation
     |
     v
Citation validation
     |
     v
Answer + supporting evidence


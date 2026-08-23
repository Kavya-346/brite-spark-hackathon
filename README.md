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

Project Structure
hackathon/
|-- data/
|   |-- policy-manual.md
|   |-- Amendment No. 2026-01.md
|   |-- amendments.json
|   `-- README.md
|-- src/
|   |-- answer_generator.py
|   |-- app.py
|   |-- citation_validator.py
|   |-- date_context.py
|   |-- date_parser.py
|   |-- embeddings.py
|   |-- grounding.py
|   |-- loader.py
|   |-- main.py
|   |-- policy_version.py
|   |-- retriever.py
|   |-- vector_store.py
|   `-- templates/
|       `-- index.html
|-- storage/
|   |-- metadata.json
|   `-- policy.index
|-- tests/
|   `-- test_evaluation.py
|-- DECISIONS.md
|-- AI-USAGE.md
|-- evaluation_results.json
|-- requirements.txt
`-- README.md

Requirements
Python 3.10+
A Gemini API key
Internet access when the Gemini model is called

No paid software or license is required.

Setup

Clone the repository:

git clone https://github.com/Kavya-346/brite-spark-hackathon.git
cd brite-spark-hackathon

Create a virtual environment:

python -m venv venv

Activate it on Windows PowerShell:

.\venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt
Environment Configuration

Create a .env file in the project root:

GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.1-flash-lite

The .env file is intentionally excluded from Git.

The evaluator should provide their own Gemini API key.

Run the Application

Run from the project root:

python src/app.py

The application starts a local Flask server.

Open the displayed local address in a browser.

The system accepts:

A policy question
A relevant date
A date type

Supported date types:

change_date
determination_date
Run the Evaluation

From the project root:

$env:PYTHONPATH="src"
python tests/test_evaluation.py

Current evaluation result:

RESULT: 10/10 passed
PASS RATE: 100.0%

To remove the temporary PowerShell environment variable:

Remove-Item Env:PYTHONPATH
Grounding and Refusal

The system does not treat semantic similarity alone as sufficient evidence.

The current grounding boundary requires:

Best retrieval score of at least 0.54
At least 30% coverage of important question words
Additional checks for unsupported terms

If the evidence is insufficient, the system refuses to answer rather than guessing.

The refusal provides a next step by directing the user to a caseworker at the Calder County Department of Household Services, supported by §1.1.2.

Date-Aware Amendments

Amendment No. 2026-01 is effective from 1 March 2026.

The system does not simply apply the newest policy to every question.

It distinguishes between:

Determination-date amendments
Change-of-circumstances amendments
Historical provisions
Amendment-only clauses

For example, the reporting period under §4.3.2 depends on the date the change occurred, while determination-date amendments are applied to determinations made on or after 1 March 2026.

Example Questions
Supported Question
How long do I have to report a change in circumstances?

With a change date before 1 March 2026, the historical reporting period applies.

With a change date on or after 1 March 2026, the amended reporting period applies.

Amendment Question
How much of household earnings from employment is disregarded?

The system applies the appropriate historical or amended value based on the relevant determination date.

Refusal Question
What is the weather in Calder County tomorrow?

The system refuses because the supplied policy manual does not contain weather information.

Evaluation

The self-created evaluation set covers:

Reporting deadlines
Resource limits
Application determination periods
Income disregards
Sanctions
Cross-referenced provisions
Appeals
Alternative evidence
Unsupported questions

Current result:

10/10 passed — 100% pass rate

The evaluation output is stored in:

evaluation_results.json
Limitations
The system answers only from the supplied synthetic policy corpus.
It does not use external policy sources.
It does not support multi-turn conversations or memory.
It does not process documents outside the supplied corpus.
A refusal means the retrieved evidence did not meet the grounding boundary.
Interface quality is not a scoring requirement for Problem 1.
Design Decisions

Important architectural and policy decisions are documented in DECISIONS.md.

These include:

Date-aware amendment handling
Cross-reference expansion
Grounding threshold
Refusal logic
Amendment-only clause handling
AI Usage
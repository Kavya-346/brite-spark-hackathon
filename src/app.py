from flask import Flask, render_template, request

from retriever import PolicyRetriever
from grounding import has_sufficient_evidence
from answer_generator import generate_answer
from citation_validator import validate_citations


app = Flask(__name__)

retriever = PolicyRetriever()


@app.route("/", methods=["GET", "POST"])
def index():
    answer = None
    evidence = []
    question = ""

    if request.method == "POST":
        question = request.form.get("question", "").strip()

        if question:
            clauses = retriever.search(question, top_k=5)

            if not has_sufficient_evidence(question, clauses):
                answer = "I cannot answer this from the policy manual."
            else:
                answer = generate_answer(question, clauses)

                citation_result = validate_citations(
                    answer,
                    clauses
                )

                if not citation_result["all_valid"]:
                    answer = "I cannot provide a grounded answer from the policy manual."
                else:
                    cited_ids = set(citation_result["valid"])

                    evidence = [
                        clause
                        for clause in clauses
                        if clause["clause_id"] in cited_ids
                    ]

    return render_template(
        "index.html",
        answer=answer,
        evidence=evidence,
        question=question
    )


if __name__ == "__main__":
    app.run(debug=True)
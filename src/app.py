import json
from datetime import date
from pathlib import Path

from flask import Flask, render_template, request

from main import answer_question
from date_context import DateContext


app = Flask(__name__)

AMENDMENT_DATE = date(2026, 3, 1)

with open(
    Path("data/amendments.json"),
    "r",
    encoding="utf-8"
) as file:
    AMENDMENTS = json.load(file)


def normalize_clause_id(clause_id):
    return clause_id.replace("Â§", "§").strip()


def get_amended_clause_status(
    clause_id,
    relevant_date,
    date_type
):
    clause_id = normalize_clause_id(clause_id)

    for amendment_clause, change in AMENDMENTS["changes"].items():

        amendment_clause = normalize_clause_id(amendment_clause)

        base_clause = amendment_clause.split("(")[0]

        if clause_id != base_clause and clause_id != amendment_clause:
            continue

        rule = change.get("rule")

        if relevant_date < AMENDMENT_DATE:
            return "unchanged"

        if rule == "change_date" and date_type != "change_date":
            return "unchanged"

        if rule == "determination_date" and date_type != "determination_date":
            return "unchanged"

        return "amended"

    return "unchanged"


@app.route("/", methods=["GET", "POST"])
def index():
    answer = None
    evidence = []
    question = ""
    relevant_date = ""
    date_type = "determination_date"
    policy_version = None
    referral = None
    error = None

    if request.method == "POST":

        question = request.form.get(
            "question",
            ""
        ).strip()

        relevant_date = request.form.get(
            "relevant_date",
            ""
        ).strip()

        date_type = request.form.get(
            "date_type",
            "determination_date"
        ).strip()

        if not question:
            error = "Please enter a policy question."

        elif not relevant_date:
            error = "Please select a relevant date."

        elif date_type not in {
            "change_date",
            "determination_date"
        }:
            error = "Invalid date type."

        else:
            try:
                parsed_date = date.fromisoformat(
                    relevant_date
                )

                date_context = DateContext(
                    relevant_date=parsed_date,
                    date_type=date_type
                )

                result = answer_question(
                    question,
                    date_context
                )

                answer = result["answer"]
                evidence = result["evidence"]
                referral = result.get("referral")

                if parsed_date >= AMENDMENT_DATE:
                    policy_version = (
                        "Amendment No. 2026-01"
                    )
                else:
                    policy_version = "Original manual"

                for clause in evidence:
                    clause["amendment_status"] = (
                        get_amended_clause_status(
                            clause["clause_id"],
                            parsed_date,
                            date_type
                        )
                    )

            except ValueError:
                error = "Please enter a valid date."

            except Exception as exc:
                error = "Unable to process the question."
                print(exc)

    return render_template(
        "index.html",
        answer=answer,
        evidence=evidence,
        question=question,
        relevant_date=relevant_date,
        date_type=date_type,
        policy_version=policy_version,
        referral=referral,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request

from app.agent.agent import AutonomousAgent


app = Flask(__name__)

agent = AutonomousAgent()
pending_states = {}


@app.route("/", methods=["GET", "POST"])
def home():
    state = None

    if request.method == "POST":
        user_request = request.form.get("request", "").strip()

        if user_request:
            state = agent.run(user_request)

            if state.awaiting_human:
                pending_states[state.invoice_id] = state

    return render_template(
        "operator.html",
        state=state,
    )


@app.route("/approve/<invoice_id>", methods=["POST"])
def approve(invoice_id):
    state = pending_states.get(invoice_id)

    if not state:
        return "Approval request not found.", 404

    resumed_state = agent.resume_after_approval(
        state,
        approved=True,
    )

    pending_states.pop(invoice_id, None)

    return render_template(
        "operator.html",
        state=resumed_state,
    )


@app.route("/reject/<invoice_id>", methods=["POST"])
def reject(invoice_id):
    state = pending_states.get(invoice_id)

    if not state:
        return "Approval request not found.", 404

    rejected_state = agent.resume_after_approval(
        state,
        approved=False,
    )

    pending_states.pop(invoice_id, None)

    return render_template(
        "operator.html",
        state=rejected_state,
    )


if __name__ == "__main__":
    app.run(port=5001, debug=True)
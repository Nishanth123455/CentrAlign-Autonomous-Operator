# NexaCore Autonomous Company Operator

A student-built prototype of an autonomous AI employee designed around the CentrAlign Founding Engineer problem statement.

The prototype focuses on a narrow but functional finance-operations workflow: processing company invoices inside a controlled internal environment.

## Problem

Company work often requires an employee to:

- understand an intended outcome
- find relevant company information
- follow policies and procedures
- use multiple systems
- perform actions
- observe results
- recover from failures
- request human approval when required
- verify that the intended result was actually achieved
- provide evidence of the work

An AI-generated answer alone does not complete this workflow.

## Prototype Scope

The system acts as an autonomous finance operations operator for a fictional company called NexaCore Solutions.

Example request:

> Process invoice INV1001 from Acme Supplies.

The operator can:

1. Understand the natural-language request.
2. Create a task plan using company policy context.
3. Retrieve invoice information.
4. Validate the vendor and purchase order.
5. Apply company processing rules.
6. Decide whether automatic processing is allowed or human approval is required.
7. Execute the permitted action through a real browser workflow.
8. Observe execution results.
9. Recover from a controlled temporary failure.
10. Pause for human approval when required.
11. Resume the same task after approval.
12. Independently verify the final invoice status.
13. Generate a persistent audit report.

## Core Loop

Goal → Understand → Plan → Execute → Observe → Adapt → Verify → Complete

## Demonstrated Scenarios

### INV1001 — Automatic Processing

- Invoice amount: ₹42,000
- Vendor: Acme Supplies
- Vendor status: approved
- Purchase order: PO1001
- Invoice amount matches purchase order
- Amount is within the automatic-processing limit

Expected behavior:

Automatic processing → browser execution → verification → completion

### INV1002 — Human Approval

- Invoice amount: ₹68,000
- Vendor: TechNova Systems
- Vendor status: approved
- Purchase order: PO1002
- Invoice amount matches purchase order
- Amount exceeds the ₹50,000 automatic-processing limit

Expected behavior:

Detect approval requirement → pause → human approval → resume → process → verify → completion

### INV1004 — Policy Exception

- Invoice amount: ₹15,000
- Vendor: Acme Supplies
- Vendor status: approved
- Purchase order: PO1004
- Purchase order amount: ₹12,500
- Invoice amount does not match purchase order

Expected behavior:

Detect mismatch → require human approval → stop when approval is rejected

## Architecture

User Request
    ↓
Task Understanding
    ↓
Task Planner
    ↓
Company Context + Company Data
    ↓
Policy Engine
    ↓
    ┌─────────────────────────────┐
    │                             │
    ▼                             ▼
Automatic Processing       Human Approval
    │                             │
    └──────────────┬──────────────┘
                   ↓
             Tool Executor
                   ↓
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
 Company Data            Browser Tool
                              ↓
                           Playwright
                              ↓
                        Finance Portal
                              ↓
                         Observation
                              ↓
                      Recovery / Adapt
                              ↓
                         Verification
                              ↓
                         Audit Trail
                              ↓
                        Final Result

## Main Components

### app/agent

Contains the autonomous operator logic.

- agent.py — coordinates the complete workflow
- understanding.py — extracts the intended task and invoice ID from the request
- planner.py — creates a plan using company context
- policy_engine.py — applies company invoice-processing rules
- tool_selector.py — maps plan steps to controlled tools
- tool_executor.py — executes the selected tools
- observer.py — interprets execution results
- recovery.py — handles recoverable failures
- approval.py — manages human approval decisions
- state.py — stores task state and execution context
- audit.py — generates and saves audit evidence

### app/models

Contains the LLM integration.

- llm_client.py — communicates with the Google Gemini API

### app/tools

Contains controlled capabilities available to the operator.

- browser_tool.py — browser automation using Playwright
- company_data_tool.py — structured company data lookup

### app/retrieval

Provides access to company policy context.

- company_context.py — retrieves relevant company policy documents

### app/verification

Provides independent verification of final system state.

- verifier.py — checks the final invoice status through the finance portal

### app/ui

Provides the user-facing autonomous operator interface.

- operator_app.py — Flask application
- templates/operator.html — operator dashboard

### portal

A controlled internal finance system used by the agent.

The portal is intentionally local and fictional so browser actions can be tested safely.

### company

Contains the controlled company environment:

- policies
- vendor records
- purchase orders
- invoice records
- invoice documents
- audit reports

## What Is Genuinely Autonomous

The prototype genuinely uses an LLM to:

- understand a natural-language company task
- extract the intended goal and invoice identifier
- create a task plan using relevant company policy context

The resulting plan is then executed through controlled application tools and deterministic company rules.

The system also:

- maintains task state
- observes execution results
- recovers from a controlled failure
- requests human approval when required
- resumes paused work
- verifies the final outcome independently
- generates persistent evidence

## What Is Deterministic or Hard-Coded

The prototype intentionally keeps safety-critical and environment-specific behavior controlled.

Examples include:

- invoice-processing policy thresholds
- vendor and purchase-order validation rules
- available tool capabilities
- browser selectors for the controlled finance portal
- fictional company data
- the local finance portal
- the controlled retry behavior

This separation prevents the LLM from directly executing arbitrary code or unrestricted financial actions.

## Human-in-the-Loop

Human approval is required for policy exceptions such as:

- invoices above ₹50,000
- invoice and purchase-order mismatches
- unverified vendors
- conflicting information

The operator pauses before the restricted action, records the approval request, and can resume the same task after a human decision.

The operator also supports rejection, in which case the restricted action is not performed.

## Verification

The operator does not consider a task complete merely because an action was submitted.

After processing, the system returns to the finance portal and independently checks the invoice state.

The task is marked complete only when the actual state matches the expected final state.

## Recovery

The prototype includes a controlled failure scenario.

When a processing attempt fails in a recoverable way:

1. the failure is observed
2. the recovery component determines that retrying is appropriate
3. the agent retries once
4. the system re-checks the actual portal state
5. the task is completed only when the intended result is verified

This demonstrates an Observe → Adapt → Verify pattern rather than blindly retrying or reporting success.

## Audit Evidence

Each task produces a persistent JSON audit report containing information such as:

- timestamp
- invoice
- vendor
- amount
- purchase order
- policy decision
- policy reason
- actions performed
- human approval
- observations
- errors
- verification result
- final result
- completion status

Audit reports are stored in:

company/data/audit/

## Technology Stack

- Python 3.12
- Flask
- Google Gemini API
- google-genai
- Playwright
- python-dotenv
- CSV-based company data
- HTML/CSS

## Setup

Create and activate a Python virtual environment.

Install project dependencies:

    python -m pip install -r requirements.txt

Install the Playwright Chromium browser:

    python -m playwright install chromium

Create a .env file in the project root containing:

    GEMINI_API_KEY=your_gemini_api_key

Do not commit the .env file or API keys to GitHub.

## Running the Prototype

### 1. Start the finance portal

Run:

    portal/app.py

The finance portal runs at:

    http://127.0.0.1:5000

### 2. Start the autonomous operator

Run:

    app/ui/operator_app.py

The operator interface runs at:

    http://127.0.0.1:5001

Open the operator interface in a browser and submit a task such as:

    Process invoice INV1001 from Acme Supplies.

## Testing

The tests directory contains component and integration tests covering:

- Gemini connectivity
- task understanding
- planning
- tool selection
- tool execution
- observation
- policy decisions
- human approval
- approval resume
- rejection
- recovery
- verification
- audit generation
- audit persistence
- three main invoice scenarios
- operator UI flows

## Project Structure

CentrAlign-Autonomous-Operator/
├── app/
│   ├── agent/
│   ├── models/
│   ├── retrieval/
│   ├── tools/
│   ├── ui/
│   │   ├── templates/
│   │   │   └── operator.html
│   │   └── operator_app.py
│   └── verification/
├── company/
│   ├── data/
│   │   ├── audit/
│   │   ├── invoice_records.csv
│   │   ├── purchase_orders.csv
│   │   └── vendors.csv
│   ├── invoices/
│   ├── policies/
│   └── purchase_orders/
├── portal/
│   ├── app.py
│   └── templates/
├── tests/
├── .env
├── .gitignore
├── README.md
└── requirements.txt

## Limitations

This is a controlled student prototype rather than a production finance system.

Current limitations include:

- the company environment is fictional and local
- company records use CSV files
- approval states are currently held in application memory
- authentication and authorization are not implemented
- the finance portal is intentionally simplified
- tool capabilities are deliberately constrained
- recovery currently retries only once
- the system focuses on invoice-processing operations rather than general company work

These limitations are deliberate trade-offs to keep the prototype functional, testable, safe, and explainable.

## Future Improvements

With additional development time, the system could be extended with:

- persistent task storage
- stronger document retrieval
- richer long-term memory
- more robust browser recovery
- authentication and role-based approvals
- additional finance workflows
- richer observability and metrics
- production-grade deployment
- broader company-operator capabilities

## AI Assistance Disclosure

This project was developed using permitted AI coding assistance.

AI assistance was used during development for:

- code generation
- debugging
- architecture iteration
- implementation support
- test creation and refinement

The implementation was tested and modified in the local development environment.

The project is intended to remain understandable, walk-through-ready, and modifiable by the developer.

## Project Status

Functional prototype completed for the selected finance-operations workflow.

The system demonstrates practical autonomous execution across automatic processing, human approval, rejection, recovery, verification, and persistent audit evidence.

The project intentionally focuses on demonstrating genuine autonomous company work within a narrow controlled workflow rather than simulating a broad general-purpose AI employee. 
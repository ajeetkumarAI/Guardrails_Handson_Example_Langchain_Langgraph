# Quickstart

## 1. Clone and set up a virtual environment

```bash
git clone <this-repo-url>
cd langchain-langgraph-guardrails
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. (Optional) configure a real Gemini model

```bash
cp .env.example .env
# then edit .env and set GOOGLE_API_KEY=...
```

You can skip this step entirely. Every example and test in this
repository also runs against a built-in offline stub model
(`guardrails_demo.models.StubChatModel`), so nothing here requires a live
API key to explore.

## 4. Run a LangChain example

```bash
PYTHONPATH=src python examples/langchain/01_input_validation.py
```

## 5. Run a LangGraph example

```bash
PYTHONPATH=src python examples/langgraph/14_production_style_agent.py
```

## 6. Run the tests

```bash
PYTHONPATH=src pytest
```

## Where to go next

- New to guardrails? Start with `docs/01_guardrails_fundamentals.md`.
- Want the full learning path? See the "Learning Path" section of the
  main `README.md`.
- Want to see LangChain and LangGraph combined in one pipeline? Look at
  `examples/langgraph/14_production_style_agent.py`.

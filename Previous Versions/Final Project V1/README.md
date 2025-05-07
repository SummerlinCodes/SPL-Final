# Custom Language Final Project — API Key + Mode Feature

## Feature Summary

This language now supports programmable AI routing by embedding:

- ✅ **API Key Declaration:** `apikey openai = "sk-abc123";`
- ✅ **Mode Definition:** `mode debug uses openai;`
- ✅ **Switching Modes:** `currentMode = "debug";`
- ✅ **Dynamic Prompt Execution:** `callMode("run tests on hash function");`

---

## Project Files

- `tokenizer.py`: recognizes new keywords
- `parser.py`: parses `apikey`, `mode`, `callMode(...)` logic
- `evaluator.py`: evaluates new features + dispatches modes
- `runner.py`: CLI & REPL logic
- `test_modes.t`: sample script for API mode demo

---

## Comment Style

Every new feature block is clearly documented with:

```python
#!------ New feature implemented: API Key + Mode Support ------!
```

This makes it easy for classmates and professors to follow.

---

## Run Demo

To test the system:

```bash
python runner_updated.py test_modes.t
```

Output will simulate routed API calls using the correct mode and API key name.

---

Built with Brandon & Jonah

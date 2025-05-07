# JunoStack — Adaptive AI Language Assistant

JunoStack is a custom programming language designed to act as an intelligent, modular assistant for developers. Inspired by RooCode but uniquely built from the ground up, JunoStack supports API key declarations, multi-model routing, assistant roles (modes), and contextual AI workflows using locally hosted models (e.g., Ollama).

---

## 🌟 Features Overview

- ✅ **API Endpoint Setup** — Define where models are served (e.g., `ollama`)
- ✅ **Mode Assignment** — Assign tasks/roles to specific models
- ✅ **Mode Instructions** — Define how each mode behaves
- ✅ **Profile Groups** — Group modes into named workflows like `production` or `maintenance`
- ✅ **Natural Context Switching** — Use `currentMode` or `callMode(...)` to invoke AI partners

---

## 📄 Project Files

- `tokenizer.py`: token recognition for all language constructs
- `parser.py`: parses all declarations (`apikey`, `mode`, `profile`, etc.)
- `evaluator.py`: evaluates instructions, routes prompts, and invokes Ollama
- `runner.py`: REPL + script executor
- `test_modes.t`: sample demo script for JunoStack's full features

---

## 🧪 Example JunoStack Script

```t
apikey ollama = "http://localhost:11434";

mode debug = "gemma3";
modeInstructions = "debug and explain the issue in the code";

mode coder = "qwen3";
modeInstructions = "implement code based on a blueprint";

profile production {
    debug,
    coder
}

currentProfile = "production";
currentMode = "coder";
callMode("Build a REST API for managing users");
```

---

## 🛠 How to Run

In terminal:

```bash
python runner.py test_modes.t
```

You’ll see output from each routed `callMode()` based on mode settings and profiles.

---

Made with ❤️ by Brandon & Jonah — JunoStack v1.0

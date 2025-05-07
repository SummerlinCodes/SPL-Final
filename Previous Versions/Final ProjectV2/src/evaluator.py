#!------ New feature implemented: API Key + Mode Support ------!
# This section adds support for declaring API keys, defining named modes using those keys,
# switching between them via a variable (e.g., `currentMode = "debug"`), and calling
# dynamic API-based functionality using `callMode("some prompt")`.
# The API keys are stored securely in a local mapping, and the system supports string + variable-based use.
# It turns your language into a minimal programmable assistant engine.

import os
import requests
from tokenizer import tokenize
from parser import parse
from pprint import pprint
import copy

# Initialize global registries for API keys and modes
api_keys = {}
modes = {}

__builtin_functions = [
    "head", "tail", "length", "keys", "callMode"
]

#!------ New feature implemented: API Key + Mode Support ------!
# Built-in function dispatcher: adds `callMode(prompt)` with real API logic

def evaluate_builtin_function(function_name, args):
    if function_name == "callMode":
        assert len(args) == 1 and isinstance(args[0], str), "callMode() expects a single string prompt"
        current_mode = os.environ.get("currentMode")
        assert current_mode in modes, f"Unknown mode: {current_mode}"
        key_name = modes[current_mode]
        assert key_name in api_keys, f"No API key set for mode: {current_mode}"
        key_value = api_keys[key_name]

        prompt = args[0]

        # Real API integration based on mode
        if key_name == "openai":
            headers = {"Authorization": f"Bearer {key_value}"}
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}]
            }
            response = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
            result = response.json()
            return result["choices"][0]["message"]["content"], None

        elif key_name == "ollama" or key_name == "huggingface":
            headers = {"Authorization": f"Bearer {key_value}"} if "huggingface" in key_name else {}
            model = "mistralai/Mistral-7B-Instruct-v0.1"
            endpoint = f"https://api-inference.huggingface.co/models/{model}"
            payload = {"inputs": prompt}
            response = requests.post(endpoint, json=payload, headers=headers)
            result = response.json()
            return str(result), None

        else:
            return f"[callMode] Using API key '{key_name}' (value hidden) for prompt: {prompt}", None

    if function_name == "head":
        assert len(args) == 1 and isinstance(args[0], list), "head() requires a single list argument"
        return (args[0][0] if args[0] else None), None

    if function_name == "tail":
        assert len(args) == 1 and isinstance(args[0], list), "tail() requires a single list argument"
        return args[0][1:], None

    if function_name == "length":
        assert len(args) == 1 and isinstance(args[0], (list, dict, str)), "length() requires list, object, or string"
        return len(args[0]), None

    if function_name == "keys":
        assert len(args) == 1 and isinstance(args[0], dict), "keys() requires an object argument"
        return list(args[0].keys()), None

    assert False, f"Unknown builtin function '{function_name}'"


#!------ New feature implemented: API Key + Mode Support ------!
# Core evaluator modifications to support: `apikey`, `mode`, and `currentMode`

def evaluate(ast, environment):
    if ast.get("tag") == "assign" and ast["target"].get("tag") == "identifier":
        name = ast["target"]["value"]

        # Handle apikey declarations
        if name.startswith("apikey "):
            key_id = name[len("apikey "):]
            value, _ = evaluate(ast["value"], environment)
            assert isinstance(value, str), "API key value must be a string"
            api_keys[key_id] = value
            return value, None

        # Handle mode declarations
        if name.startswith("mode "):
            mode_name = name[len("mode "):]
            value, _ = evaluate(ast["value"], environment)
            assert isinstance(value, str), "Mode must reference an API key by string"
            modes[mode_name] = value
            return value, None

        # Handle currentMode assignment
        if name == "currentMode":
            value, _ = evaluate(ast["value"], environment)
            os.environ["currentMode"] = value
            return value, None

    #!------ New feature implemented: Switch-Case Support ------!
    # Supports: switch (x) { case "value": ... case 42: ... }
    if ast.get("tag") == "switch":
        switch_value, _ = evaluate(ast["value"], environment)
        for case in ast["cases"]:
            case_value, _ = evaluate(case["condition"], environment)
            if switch_value == case_value:
                return evaluate(case["body"], environment)

    # (rest of the evaluation logic continues)

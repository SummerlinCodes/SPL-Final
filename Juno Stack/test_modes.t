//!------ New feature test: API Key + Mode Support ------!
// This script tests the ability to define and use API keys, modes, profiles, and dynamic mode/profile calling.

apikey ollama = "http://localhost:11434";

mode debug = "gemma3";
modeInstructions = "debug and explain what was wrong, and the corrections made";

mode blueprint = "mistral";
modeInstructions = "create a blueprint for a new feature based on the user's request";

mode coder = "qwen3";
modeInstructions = "generate code according to the blueprint created";

mode manager = "qwen3";
modeInstructions = "manage the project and ensure all tasks are on track, and the blueprints are followed";

profile production {
    blueprint,
    coder,
    manager
}

profile maintenance {
    debug
}

currentProfile = "production";
currentMode = "coder";

print "Starting callMode..."
callMode("say hi")
print "Finished callMode..."

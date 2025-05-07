//!------ New feature test: API Key + Mode Support ------!
// This script tests the ability to define and use API keys, modes, profiles, and dynamic mode/profile calling.

apikey ollama = "http://localhost:11434";

mode debug = "gemma 3";
modeInstructions = "debug and explain what was wrong, and the corrections made"

mode blueprint = "mistral";
modeInstructions = "create a blueprint for a new feature based on the user's request";

mode coder = "qwen 3"
modeInstructions = "generate code according to the blueprint created";

mode manager = "qwen 3"
modeInstructions = "manage the project and ensure all tasks are on track, and the blueprints are followed";

callMode("Generate test cases for a string reversal function");

profile1 = "production";

profile production {
    blueprint,
    coder,
    manager
}

profile2 = "maintenance";

profile maintenance {
    debug,
}

//!------ Test file for mode: coder ------!
//

apikey qwen_4b = "http://localhost:11434";

mode coder = "qwen_4b";
modeInstructions["coder"] = "You generate code to implement the blueprint.";

currentMode = "coder";
callMode("Write the Python code for tracking daily water intake.");

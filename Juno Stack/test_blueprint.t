//!------ Test file for mode: blueprint ------!
//

apikey ollama = "http://localhost:11434";
apikey mistral = "http://localhost:11434";

mode blueprint = "mistral";
modeInstructions["blueprint"] = "You create a blueprint for a new feature.";

currentMode = "blueprint";
callMode("Design a feature that helps users track daily water intake.");

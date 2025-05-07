//!------ Test file for mode: debug ------!
//

apikey gemma_4b = "http://localhost:11434";

mode debug = "gemma_4b";
modeInstructions["debug"] = "You analyze and explain bugs in code or logic.";

currentMode = "debug";
callMode("Debug the water tracking code for issues in hydration summary.");

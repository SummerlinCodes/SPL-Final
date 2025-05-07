//!------ New feature test: API Key + Mode Support + Switch ------!

apikey openai = "sk-test-openai";
apikey huggingface = "hf-test-hfkey";

mode gpt uses openai;
mode local uses huggingface;

currentMode = "gpt";
callMode("Summarize this function:");

switch (currentMode) {
  case "gpt": print("OpenAI is active");
  case "local": print("HuggingFace is active");
}

currentMode = "local";
callMode("How does recursion work?");

switch (currentMode) {
  case "gpt": print("GPT still active");
  case "local": print("Ollama/HuggingFace is now active");
}
# Thinking-Machine
A Machine that thinks.

In order to launch it from the command line or as a Python subprocess:
```bash
echo "Theodotos-Alexandreus: Are language models seeking the Truth, machine?" \
  | uvx thinking-machine \
    --provider-api-key=sk-proj-... \
    --github-token=ghp_... 
```

Or, with local pip installation:
```bash
pip install thinking-machine
```
Set the environment variables:
```bash
export PROVIDER_API_KEY="sk-proj-..."
export GITHUB_TOKEN="ghp_..."
```
Then:
```bash
thinking-machine multilogue.txt
```
Or:
```bash
thinking-machine multilogue.txt new_turn.txt
```
Or:
```bash
cat multilogue.txt | thinking-machine
```
Or:
```bash
cat multilogue.txt | thinking-machine > multilogue.txt
```
Or: 
```bash
(cat multilogue.txt; echo:"Theodotos: What do you think, Thinking-Machine?") \
  | thinking-machine
```
Or:
```bash
cat multilogue.txt new_turn.txt | thinking-machine
```
Or:
```bash
cat multilogue.txt new_turn.txt | thinking-machine > multilogue.txt
```
Or, if you have installed other machines:
```bash
cat multilogue.md | thinking-machine \
  | summarizing-machine | judging-machine > summary_judgment.md
```

Or use it in your Python code:
```Python
# Python
import thinking_machine
```

# Name-of-the-Machine
A Machine that thinks.

In order to launch it from the command line or as a Python subprocess:
```bash
echo "Theodotos-Alexandreus: Are language models seeking the Truth, machine?" \
  | uvx name-of-the-machine \
    --provider-api-key sk-proj-... \
    --github-token ghp_... 
```

Or, with a local pip installation:
```bash
pip install name-of-the-machine
```
Set the environment variables:
```bash
export PROVIDER_API_KEY="sk-proj-..."
export GITHUB_TOKEN="ghp_..."
```
Then:
```bash
name-of-the-machine -a multilogue.txt
```
Or:
```bash
name-of-the-machine multilogue.txt > response.txt
```
Or:
```bash
name-of-the-machine -a multilogue.txt | vim
```
Or:
```bash
name-of-the-machine -a multilogue.txt > tmp && echo tmp > multilogue.txt
```

Or use it in your Python code:
```Python
# Python
import name_of_the_machine
```

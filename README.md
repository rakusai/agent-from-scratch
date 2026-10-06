# agent-from-scratch

**An AI that acts on your computer, in 55 lines of Python.**

No frameworks. No SDKs. No `pip install`. Just the Python standard library and a local LLM.

Example session:

```
$ python agent.py
Enter your instruction for Mac (e.g., 'Check free disk space'): how much disk space is left?

[AI Suggested Command]: df -h /
Do you want to execute this command on your Mac? (y/N): y

--- Execution Output ---
Filesystem      Size    Used   Avail Capacity  Mounted on
/dev/disk3s1s1  460Gi    11Gi   180Gi     6%    /
```

## Why

Most people meet "AI agents" through big frameworks, which makes them look complicated.
This repo goes the other way: it strips an agent down to the smallest piece that still
**turns words into actions**, so you can read the whole thing in two minutes.

## What 55 lines can do

The whole thing is one file, [`agent.py`](agent.py): 55 lines, 41 of them code.
Those lines are enough for:

- **Natural language to shell**: say what you want in plain English and get a working Bash command.
- **Real execution**: the command runs on your machine and you see the output.
- **Structured output**: the model must answer in JSON (`{"command": "..."}`), so code can parse it reliably.
- **Human approval**: nothing runs until you type `y`.
- **Fully local**: the model runs through [Ollama](https://ollama.com), so nothing leaves your machine.

### How it works

```
your words ──▶ prompt ──▶ local LLM ──▶ {"command": "..."} ──▶ you approve? ──▶ subprocess ──▶ output
```

| Step | Lines | What it shows |
|---|---|---|
| Prompt template | ~10 | Telling the model its role and output format |
| HTTP call to Ollama | ~10 | An LLM is just an HTTP endpoint |
| JSON parsing | 2 | Constraining output makes it machine-usable |
| `y/N` confirmation | 2 | The simplest possible permission system |
| `subprocess.run` | 3 | The moment AI output touches the real world |

## Is this an agent?

Almost. It acts once and stops. It never sees the result of its own command.

A common definition of an agent is *"an LLM running tools in a loop to reach a goal."*
This script has the tool, but not the loop. Feed the command output back to the model and
let it try again, and you have an agent. That next step is only a few more lines.

That makes this the **atom** of an agent harness: structured output, an executor, and human
approval, with nothing else.

## Quick start

Requirements: macOS, Python 3, and [Ollama](https://ollama.com).

```bash
ollama pull gemma4:e2b
```

```bash
python agent.py
```

To use a different model, edit the `MODEL` variable at the top of `agent.py`
(run `ollama list` to see what you have installed).

## ⚠️ Safety

This script runs whatever shell command the model suggests, with your user's permissions
(`shell=True`). The `y/N` prompt is the only safeguard. **Read every command before you approve it**,
and do not remove the confirmation step.

# chatagent

> **Warning:** This is a toy/learning project and is not intended for real use. For a production-grade AI coding agent, check out [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

A CLI-powered AI coding agent that uses Google's Gemini 2.5 Flash to interact with your filesystem. Give it a natural language prompt and it will read files, list directories, execute Python scripts, and write files autonomously within a sandboxed working directory.

## Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- A [Gemini API key](https://aistudio.google.com/apikey)

## Setup

```bash
# Install dependencies
uv sync

# Set your API key
echo 'GEMINI_API_KEY=your_key_here' > .env
```

## Usage

```bash
uv run main.py "your prompt here"
```

With verbose output (shows token usage and function call details):

```bash
uv run main.py --verbose "your prompt here"
```

## How It Works

The agent runs in a loop (up to 20 iterations) where Gemini can call tools to accomplish the task described in your prompt. The available tools are:

| Tool | Description |
|---|---|
| `get_files_info` | List files and directories with size info |
| `get_file_content` | Read file contents (truncated at 10,000 chars) |
| `run_python_file` | Execute a Python file with optional arguments |
| `write_files` | Write or overwrite file contents |

All file operations are sandboxed to the configured working directory (`calculator/` by default) to prevent unintended access to the rest of the filesystem.

## Project Structure

```
chatagent/
├── main.py              # Entry point and conversation loop
├── prompt.py            # System prompt for the AI agent
├── config.py            # Configuration constants
├── call_function.py     # Function dispatch and tool definitions
├── functions/           # Tool implementations
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── run_python_file.py
│   └── write_file.py
├── calculator/          # Sample sandboxed working directory
├── test_*.py            # Unit tests
└── pyproject.toml       # Project metadata and dependencies
```

## Dependencies

- `google-genai` - Google Generative AI SDK
- `python-dotenv` - Environment variable loading from `.env`
# Interactive Python Example
A simple python example demonstrating how to use the Ortex API to get on-chain data using natural language.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your API key:
```bash
# Linux/Mac
export ORTEX_API_KEY="your-api-key-here"

# Windows (PowerShell)
$env:ORTEX_API_KEY="your-api-key-here"

# Windows (CMD)
set ORTEX_API_KEY=your-api-key-here
```

Get your API key from: https://ortex.cc/settings/api-keys

## Usage

Run the example:
```bash
python main.py
```

### Commands

Once in the chat:
- **Ask questions**: Just type your question and press Enter
- **`/clear`**: Clear conversation history and start fresh
- **`/stats`**: Show session statistics (messages, tokens, cost)
- **`/exit` or `/quit`**: Exit the chat
- **Ctrl+C**: Also exits the chat

## Support

- Documentation: https://docs.ortex.cc

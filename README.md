# Qwen2 MCP Financial Data Agent

This project demonstrates how to use the Qwen2 large language model with the Model Control Protocol (MCP) to create an agent that can retrieve and analyze financial data.

## Features

- Uses Qwen2 model via Ollama for natural language processing
- Implements MCP server with financial data tools powered by yfinance
- Provides context-aware financial data tools with proper error handling
- Supports answering queries about stock prices, company information, and financial metrics

## Prerequisites

- Python 3.13+
- [Poetry](https://python-poetry.org/) for package management
- [Ollama](https://ollama.ai/) installed and running with Qwen2 model pulled
- **VPN Connection**: Yahoo Finance API requires a stable connection, which may require a VPN in some regions

## Setup

1. Install dependencies:

```bash
poetry install
```

2. Make sure you have the Qwen2 model pulled in Ollama:

```bash
ollama pull qwen2.5:14b
```

3. Ensure you have a working internet connection, possibly through a VPN if necessary for accessing Yahoo Finance.

## Usage

1. Run the agent:

```bash
poetry run python main.py
```

2. The agent will process the default query "What is the current stock price of Microsoft?" or you can modify the query in `main.py`.

## Project Structure

- `main.py`: Main script that creates and runs the agent using smolagents
- `server.py`: FastMCP server that provides financial data tools
- `pyproject.toml`: Poetry configuration and dependencies

## Architecture

The project is built using the following architecture:

1. **MCP Server Layer**: Implemented using FastMCP, exposing financial data tools
   - Context-aware tool implementations
   - Proper error handling for network issues
   - Clean separation between tool interfaces and implementations

2. **Agent Layer**: Using smolagents to connect to the MCP server
   - Connects to the server via stdio transport
   - Uses Qwen2 model via Ollama for natural language understanding
   - Handles tool selection and result processing

3. **Financial Data Layer**: Using yfinance to access stock and financial information
   - Real-time stock prices and company information
   - Historical financial statements
   - Key financial metrics like EBITDA

## Available Tools

The MCP server provides the following financial data tools:

- `get_stock_info`: Get basic information about a stock
- `get_stock_price`: Get the current price of a stock
- `get_financial_data`: Get financial statements data for a company
- `get_key_metrics`: Get key financial metrics including EBITDA for a company

Additionally, it provides a resource endpoint:
- `finance://info/{ticker}`: Resource endpoint for basic financial information

## Custom Queries

To run custom queries, modify the `query` variable in the `run_agent()` function of `main.py`.

## Integrating with LLM Applications

### Claude Desktop

To add this MCP server to Claude Desktop:

1. Open Claude Desktop
2. Go to Settings > Model Control Protocol
3. Click "Add MCP"
4. Configure as follows:
   - Name: "Financial Data MCP"
   - Command: `poetry`
   - Arguments: `run python server.py`
   - Working Directory: Path to your project (e.g., `/Users/username/Downloads/qwen2-mcp-test`)
   - Environment Variables: (add any if needed)
5. Click "Save"

You can also use the MCP CLI if installed:
```bash
mcp install server.py --name "Financial Data MCP"
```

### Cursor

To integrate with Cursor:

1. Go to Settings
2. Search for "MCP"
3. Click "Edit in settings.json"
4. Add the following configuration:
   ```json
   "mcp.servers": [
     {
       "name": "Financial Data MCP",
       "command": "poetry",
       "args": ["run", "python", "server.py"],
       "cwd": "/path/to/qwen2-mcp-test"
     }
   ]
   ```

### VSCode Copilot

To integrate with VSCode Copilot:

1. Open Settings (⌘+, on Mac, Ctrl+, on Windows/Linux)
2. Search for "Copilot MCP"
3. Click "Edit in settings.json"
4. Add the following:
   ```json
   "github.copilot.chat.mcp.configurations": [
     {
       "name": "Financial Data MCP",
       "command": "poetry",
       "args": ["run", "python", "server.py"],
       "cwd": "/path/to/qwen2-mcp-test"
     }
   ]
   ```

Replace `/path/to/qwen2-mcp-test` with the actual path to your project directory.

## Development and Testing

You can test your MCP server with the MCP Inspector by installing the MCP CLI:

```bash
pip install "mcp[cli]"
```

Then run:

```bash
mcp dev server.py
```

This opens an interactive inspector where you can test your tools and resources.

## Troubleshooting

- **Connection Issues**: If you encounter "Failed to connect to fc.yahoo.com" errors, ensure you have a stable internet connection, possibly through a VPN.
- **Tool Errors**: Check the server logs for detailed error messages if tools fail to return expected data.
- **Model Issues**: Ensure your Ollama installation is properly set up and the Qwen2 model is available.

## Advanced Configuration

For advanced server configuration, refer to the [MCP Python SDK documentation](https://modelcontextprotocol.io).

## License

MIT

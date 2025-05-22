#!/usr/bin/env python3
"""
Main module for the Qwen2 MCP agent.

This script initializes and runs an agent using the Qwen2 model via Ollama
and connects to an MCP server that provides financial data tools.
"""

import logging
import os
import sys

from mcp import StdioServerParameters
from smolagents import LiteLLMModel, ToolCallingAgent, ToolCollection

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def run_agent(query: str):
    """
    Main function to run the agent with the financial data MCP.
    """
    logger.info("Initializing Qwen2 MCP agent...")

    # Specify Qwen2 model via LiteLLM (using Ollama as the backend)
    model = LiteLLMModel(model_id="ollama_chat/qwen2.5:14b", num_ctx=8192)

    # Get the absolute path to the server.py file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(current_dir, "server.py")

    # Configure server parameters for MCP communication
    server_parameters = StdioServerParameters(
        command=sys.executable,
        args=[server_path],
        env=None,
    )

    try:
        # Use ToolCollection as a context manager
        with ToolCollection.from_mcp(
            server_parameters, trust_remote_code=True
        ) as tool_collection:
            # Initialize agent with tools and model
            agent = ToolCallingAgent(tools=[*tool_collection.tools], model=model)

            logger.info(f"Running query: {query}")

            response = agent.run(query)
            print(f"Response: {response}")
    except Exception as e:
        logger.error(f"Error running agent: {e}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(run_agent(sys.argv[1]))

# AI Agent Instructions for Agent_Test Project

## Project Overview
This is a minimal Python project implementing a simple conversational agent for testing and learning purposes. The core functionality is contained in a single file with basic keyword-based response logic.

## Architecture
- **Main Component**: `agent.py` - Contains the entire agent logic in a single script
- **No external dependencies** - Pure Python standard library usage
- **Simple event loop** - Main loop handles user input/output until "exit" command

## Key Patterns
- **Response Logic**: Use `if/elif/else` chains in `agent_response()` function for keyword matching
- **Input Handling**: Case-insensitive string matching with `.lower()` on user input
- **Exit Condition**: Check for exact "exit" string (case-insensitive) to break the loop

## Development Workflow
- **Run the agent**: Execute `python agent.py` from project root
- **Add responses**: Extend `agent_response()` with additional `elif` conditions for new keywords
- **Test interactions**: Manual testing through the interactive prompt

## Code Style
- **Simple and readable**: Keep functions short, use descriptive variable names
- **No classes**: Functional approach with a single main function
- **Direct I/O**: Use built-in `input()` and `print()` for user interaction

## Examples
- Adding a new response: `elif "help" in user_input.lower(): return "I can respond to hello, how are you, and bye."`
- Modifying exit: Change the exit check to handle variations like "quit" or "stop"

## File Structure
- `agent.py`: Core agent implementation
- `requirements.txt`: Empty (no dependencies required)
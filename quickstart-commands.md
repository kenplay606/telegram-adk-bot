# Quick Reference Commands

## Activate Virtual Environment

**PowerShell:**
```powershell
.venv\Scripts\Activate.ps1
```

**Command Prompt:**
```console
.venv\Scripts\activate.bat
```

## Run Your Agent

### CLI Mode
```console
adk run my_agent
```

### Web Interface
```console
adk web --port 8000
```
Then open: http://localhost:8000

## Test Your Agent

Try asking:
- "What time is it in New York?"
- "Tell me the current time in Tokyo"
- "What's the time in London?"

## Useful ADK Commands

```console
# List all agents
adk list

# Create a new agent
adk create <agent_name>

# Get help
adk --help
```

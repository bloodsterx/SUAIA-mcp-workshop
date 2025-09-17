# SUAIA MCP workshop 18/09/25

## Learning Outcomes

1. Understand a high-level idea about the concepts of model context protocol, the components involved and the interactions between them
   1. MCP hosts and clients, MCP server and the layers of transport connecting them
2. Learn and apply the basic core primitives exposed by MCP servers to provide agents with their functionality
   1. Tools, resources and prompts
3. Build a simple MCP server over STDIO transport (local transport layer) using FastMCP library for Python
4. Configure hosts to use the MCP server via the command line
5. Test the functionality of an MCP server using developer mode
6. Create asynchronous tools which utilise resources
7. Add external integrations

## Part 1: MCP — not AI, a protocol.

**Model Context Protocol** was developed by Anthropic to establish an industry standard for how AI agents interact with systems and APIs.

#### Why do we care?

AI agents are as useful as chatGPT, grok, gemini - any LLM. In other-words, **pretty useless**.

ChatGPT is only as good as the person using it. It might spit out the most elaborate marketing strategy, or software development pipeline, but the road ended there. The user had to make decisions given the information outputted by the LLM.

What made AI 'agentic' was when we decided to allow LLMs to actually enact on their user's inputs. An LLM cannot perform the trivial task of 'sending an email', but it can perform the annoying task of writing it. 

So, you give a component of your system a brain *powered by a large language model*, but strictly define how its outputs are to be used. Given user-input, the component decides on a function to call e.g. `write_email(content: str)`, generates the argument (normal LLM behaviour) and thats it- the logic of the function is developer-designed, a mailing API could be called for example sending the **AI generated** email message to some address.

Before MCP, developers wishing to create agentic AI software would have to manually create the interface which allowed their agents to make these API calls. This would be done **for every integration**, each implementation varying developer to developer.

#### MCP acts as the usb port that works everywhere

While one end of a charging cord may be usb-c or micro-usb or lightning, the other end of all these cords is usb-A (yes yes you have dual usb-c ended cords, not the point).

Notion, for example, would create their own **MCP server** which defines the different functions an agent can call and the outputs they would provide. Developers of agentic AI software can just 'connect' to these servers, exposing these functions and features to their agentic without writing a single line of logic.

You could probably build a simple N8N with an ugly GUI in a week. Maybe 48 hours if you are cracked enough.

MCP has been crucial in revolutionising innovation in SaaS - ship agentic products in weeks, days.
- Cursor
- Claude Code
- Den, Relevance, Manus, N8N, LangChain, etc
- And hundreds of pre-revenue, vibe-coded startup slop (slop by the way, which is shipped faster than you can finish a COMP2123 assignment)

## Part 2: MCP architecture — a high-level exploration

### Hosts (the brain)

The brain of the agent- the MCP host is an AI application (like Cursor, Claude Code, Claude Desktop). I will be using Cursor, but the only different with Claude Desktop is the configuration which I'll show later.

### Clients (the middleman)

The middleman of the agent, MCP clients expose the context of the MCP server to the host. This will make a bit more sense when I explain servers

### Servers (I couldn't think of a punchy nickname)

The gears and cogs of the agent- MCP servers are programs with the functions which are to be called by the agent.

### The Interaction

The host may host many clients, who communicate back and forth between the host and server to give the host (remember, the brain, the large language model) the context of all the different functions in the MCP server, and then to hear back from the host on **which function to call** and **what arguments to give it**.

The communication between client and server is a 1:1 connection called a transport layer. Either the server runs on the same machine (locally, STDIO transport) or remotely (Streamable HTTP transport).

### Example Flow

E.g. user opens claude desktop and enters in the chatbox: 'write an apology email to my manager for pushing the .env file to my remote repository. Make it sincere, but not too ass-kissy'

1. (under the hood): a client launches (remember client ≠ claude desktop, but a component serving a 1:1 connection to a server) and performs a handshake with the 'email-mcp-server' to establish the connection
2. Client wants to know what **tools** are available to the host. It requests 'tools/list' from the server:

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list"
}
```

3. Server responds: "here are my tools! call me x" (literally)

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "send_email",
        "title": "Send Email",
        "description": "Writes an email and sends it to an address",
        "inputSchema": {
          "type": "object",
          "properties": {
            "expression": {
              "type": "string",
              "description": "The formatted contents of the email to be sent"
              // this would've been exposed in a docstring
            }
          },
          "required": ["expression"]
        }
      },
    ]
  }
}
```

The host now has access to a big registry of callable functions. It decides to call `send_email`. The host (claude desktop) fills in the argument (writes the email), and says "hey client, call 'send_email' "

#### Pseudo-code for AI application tool execution (courtesy of https://modelcontextprotocol.io/docs/learn/architecture)

```python
async def handle_tool_call(conversation, tool_name, arguments):
    session = app.find_mcp_session_for_tool(tool_name)
    result = await session.call_tool(tool_name, arguments)
    conversation.add_tool_result(result.content)
```

## Part 3: Building, configuring & Testing

### Step 1. Ensure either Claude Desktop or Cursor has been installed

### Step 2. install uv if you dont already have it. IDC if you use pip, poetry whatever- UV is pip on crack, and makes life easier for us

for Mac
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

for Windows
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Step 3. Create an environment and install fastmcp & yfinance
Please tell me you have been pip installing all your modules inside an environment, right?...

Do this in a directory/folder somewhere

```bash
uv init
uv venv
source .venv/bin/activate
uv add fastmcp
uv add yfinance
```


## Part 4: Make your own 
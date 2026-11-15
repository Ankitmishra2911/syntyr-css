# Optional Syntyr read-only MCP server

Syntyr CSS remains MIT-licensed, independent of MCP, JavaScript-free at runtime,
and free of required API keys or network services. This **local developer
adapter** is not included in the npm CSS package, CDN, or static-site build.

The official MCP Python SDK is the *only optional server dependency*. Requires
Python 3.11+ and [uv](https://docs.astral.sh/uv/) (or install `mcp>=2,<3` in a
dedicated Python environment).

From a checked-out Syntyr repository:

```sh
uv run --no-project --with 'mcp>=2,<3' python -m agent_mcp.server
```

Example local stdio client configuration (replace absolute checkout path):

```json
{
  "mcpServers": {
    "syntyr": {
      "command": "uv",
      "args": [
        "run", "--directory", "/absolute/path/to/syntyr-css",
        "--no-project", "--with", "mcp>=2,<3",
        "python", "-m", "agent_mcp.server"
      ]
    }
  }
}
```

The server offers these **read-only** tools:

- `search_components(query, release)` — curated verified components.
- `get_component(name, release)` — native element guidance and stylesheets.
- `lookup_api(name, release)` — class or token existence.
- `get_theme_tokens(query, release)` — property names, not computed values.
- `validate_markup(html, release, stylesheets)` — unknown `syn-*` classes
  and required CSS files. This is not an accessibility conformance audit.

Version defaults to **published and immutable `0.3.0-alpha.4`**; explicitly
select `0.3.0-alpha.5` only when using the unreleased current-source CSS
candidate. The adapter reads actual checked-in stylesheets and maintained
metadata. The component inventory is curated, not exhaustive. Invalid
releases, selectors, components, and stylesheet names produce tool errors
instead of invented API responses. Do not assume a module is installed simply
because a selector exists.

This is a local stdio tool, *not* an HTTP MCP server, paid API, hosted service,
chatbot, code execution endpoint, or license checker. It never reads user
projects or network resources and does not handle payment credentials.

## Tests

Run the metadata contract tests with Python's standard library:

```sh
python3 -m unittest tests.test_agent_mcp -v
```

Run the real SDK integration and complete repository suite using the optional
SDK in an isolated uv environment:

```sh
uv run --no-project --with 'mcp>=2,<3' python -m unittest tests.test_agent_mcp_sdk -v
uv run --no-project --with 'mcp>=2,<3' python -m unittest discover -s tests -q
```

No MCP dependency is added to `package.json` or to browser-facing assets.

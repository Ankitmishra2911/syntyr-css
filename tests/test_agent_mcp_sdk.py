"""Real MCP SDK discovery and tool calls, not a mocked JSON-RPC interface."""
import asyncio
import unittest

try:
    from mcp import Client
    from agent_mcp import server as adapter
except ImportError:
    Client = None
    adapter = None


@unittest.skipUnless(Client is not None, "Install optional MCP SDK to run integration")
class AgentMcpSdkTests(unittest.TestCase):
    def test_mcp_tools_are_discoverable_and_use_published_api(self):
        self.assertTrue(hasattr(adapter, "server"))
        async def run():
            async with Client(adapter.server) as client:
                listing = await client.list_tools()
                names = {tool.name for tool in listing.tools}
                self.assertGreaterEqual(names, {
                    "search_components", "get_component", "lookup_api",
                    "get_theme_tokens", "validate_markup",
                })
                result = await client.call_tool("lookup_api", {
                    "name": "syn-button--primary", "release": "0.3.0-alpha.4",
                })
                self.assertFalse(result.is_error)
                structured = result.structured_content
                self.assertEqual(structured["release_status"], "published")
                self.assertEqual(structured["entry"]["stylesheet"], "syntyr.core.css")
                invalid = await client.call_tool("get_component", {
                    "name": "Form compositions", "release": "0.3.0-alpha.4",
                })
                self.assertTrue(invalid.is_error)
                self.assertIn("unavailable", str(invalid.content).lower())
                for tool in listing.tools:
                    self.assertIs(tool.annotations.read_only_hint, True)
        asyncio.run(run())


if __name__ == "__main__":
    unittest.main()

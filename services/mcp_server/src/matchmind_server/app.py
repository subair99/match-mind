"""MatchMind MCP server over Streamable HTTP (MCP Python SDK v2).

Run locally:  uv run --package matchmind-server python -m matchmind_server.app
"""
from mcp.server.mcpserver import MCPServer

from . import tools

mcp = MCPServer("matchmind", version="0.1.0")


@mcp.tool()
def find_moments(match_id: str, after_seconds: float = 0.0, limit: int = 3) -> list[dict]:
    """Most important moments after a playback position."""
    return tools.find_moments(match_id, after_seconds, limit)


@mcp.tool()
def player_timeline(match_id: str, player: int) -> list[dict]:
    """All moments for one shirt number, in time order."""
    return tools.player_timeline(match_id, player)


# TODO: explain_moment, build_reel, request_share, get_viewer_state, save_viewer_state

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000, streamable_http_path="/mcp")
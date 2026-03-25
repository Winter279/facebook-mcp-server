import os
import sys
import signal
import logging
from contextlib import asynccontextmanager
from typing import Any

from mcp.server.fastmcp import FastMCP
from manager import Manager

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("facebook-mcp")

# ---------------------------------------------------------------------------
# MCP + Manager
# ---------------------------------------------------------------------------
mcp = FastMCP("FacebookMCP")
manager = Manager()


# ---------------------------------------------------------------------------
# Tools  (all async – never blocks the event loop)
# ---------------------------------------------------------------------------
@mcp.tool()
async def post_to_facebook(message: str) -> dict[str, Any]:
    """Create a new Facebook Page post with a text message."""
    return await manager.post_to_facebook(message)


@mcp.tool()
async def reply_to_comment(post_id: str, comment_id: str, message: str) -> dict[str, Any]:
    """Reply to a specific comment on a Facebook post."""
    return await manager.reply_to_comment(post_id, comment_id, message)


@mcp.tool()
async def get_page_posts() -> dict[str, Any]:
    """Fetch the most recent posts on the Page."""
    return await manager.get_page_posts()


@mcp.tool()
async def get_post_comments(post_id: str) -> dict[str, Any]:
    """Retrieve all comments for a given post."""
    return await manager.get_post_comments(post_id)


@mcp.tool()
async def delete_post(post_id: str) -> dict[str, Any]:
    """Delete a specific post from the Facebook Page."""
    return await manager.delete_post(post_id)


@mcp.tool()
async def delete_comment(comment_id: str) -> dict[str, Any]:
    """Delete a specific comment from the Page."""
    return await manager.delete_comment(comment_id)


@mcp.tool()
async def hide_comment(comment_id: str) -> dict[str, Any]:
    """Hide a comment from public view."""
    return await manager.hide_comment(comment_id)


@mcp.tool()
async def unhide_comment(comment_id: str) -> dict[str, Any]:
    """Unhide a previously hidden comment."""
    return await manager.unhide_comment(comment_id)


@mcp.tool()
async def delete_comment_from_post(post_id: str, comment_id: str) -> dict[str, Any]:
    """Delete a comment on a post."""
    return await manager.delete_comment_from_post(post_id, comment_id)


@mcp.tool()
async def filter_negative_comments(comments: dict[str, Any]) -> list[dict[str, Any]]:
    """Filter comments for basic negative sentiment."""
    return await manager.filter_negative_comments(comments)


@mcp.tool()
async def get_number_of_comments(post_id: str) -> int:
    """Count the number of comments on a given post."""
    return await manager.get_number_of_comments(post_id)


@mcp.tool()
async def get_number_of_likes(post_id: str) -> int:
    """Return the number of likes on a post."""
    return await manager.get_number_of_likes(post_id)


@mcp.tool()
async def get_post_insights(post_id: str) -> dict[str, Any]:
    """Fetch all insights metrics (impressions, reactions, clicks, etc)."""
    return await manager.get_post_insights(post_id)


@mcp.tool()
async def get_post_impressions(post_id: str) -> dict[str, Any]:
    """Fetch total impressions of a post."""
    return await manager.get_post_impressions(post_id)


@mcp.tool()
async def get_post_impressions_unique(post_id: str) -> dict[str, Any]:
    """Fetch unique impressions of a post."""
    return await manager.get_post_impressions_unique(post_id)


@mcp.tool()
async def get_post_impressions_paid(post_id: str) -> dict[str, Any]:
    """Fetch paid impressions of a post."""
    return await manager.get_post_impressions_paid(post_id)


@mcp.tool()
async def get_post_impressions_organic(post_id: str) -> dict[str, Any]:
    """Fetch organic impressions of a post."""
    return await manager.get_post_impressions_organic(post_id)


@mcp.tool()
async def get_post_engaged_users(post_id: str) -> dict[str, Any]:
    """Fetch number of engaged users."""
    return await manager.get_post_engaged_users(post_id)


@mcp.tool()
async def get_post_clicks(post_id: str) -> dict[str, Any]:
    """Fetch number of post clicks."""
    return await manager.get_post_clicks(post_id)


@mcp.tool()
async def get_post_reactions_like_total(post_id: str) -> dict[str, Any]:
    """Fetch number of 'Like' reactions."""
    return await manager.get_post_reactions_like_total(post_id)


@mcp.tool()
async def get_post_reactions_love_total(post_id: str) -> dict[str, Any]:
    """Fetch number of 'Love' reactions."""
    return await manager.get_post_reactions_love_total(post_id)


@mcp.tool()
async def get_post_reactions_wow_total(post_id: str) -> dict[str, Any]:
    """Fetch number of 'Wow' reactions."""
    return await manager.get_post_reactions_wow_total(post_id)


@mcp.tool()
async def get_post_reactions_haha_total(post_id: str) -> dict[str, Any]:
    """Fetch number of 'Haha' reactions."""
    return await manager.get_post_reactions_haha_total(post_id)


@mcp.tool()
async def get_post_reactions_sorry_total(post_id: str) -> dict[str, Any]:
    """Fetch number of 'Sorry' reactions."""
    return await manager.get_post_reactions_sorry_total(post_id)


@mcp.tool()
async def get_post_reactions_anger_total(post_id: str) -> dict[str, Any]:
    """Fetch number of 'Anger' reactions."""
    return await manager.get_post_reactions_anger_total(post_id)


@mcp.tool()
async def get_post_top_commenters(post_id: str) -> list[dict[str, Any]]:
    """Get the top commenters on a post."""
    return await manager.get_post_top_commenters(post_id)


@mcp.tool()
async def post_image_to_facebook(image_url: str, caption: str) -> dict[str, Any]:
    """Post an image with a caption to the Facebook page."""
    return await manager.post_image_to_facebook(image_url, caption)


@mcp.tool()
async def send_dm_to_user(user_id: str, message: str) -> dict[str, Any]:
    """Send a direct message to a user."""
    return await manager.send_dm_to_user(user_id, message)


@mcp.tool()
async def update_post(post_id: str, new_message: str) -> dict[str, Any]:
    """Updates an existing post's message."""
    return await manager.update_post(post_id, new_message)


@mcp.tool()
async def schedule_post(message: str, publish_time: int) -> dict[str, Any]:
    """Schedule a new post for future publishing (publish_time = Unix ts)."""
    return await manager.schedule_post(message, publish_time)


@mcp.tool()
async def get_page_fan_count() -> int:
    """Get the Page's total fan/like count."""
    return await manager.get_page_fan_count()


@mcp.tool()
async def get_post_share_count(post_id: str) -> int:
    """Get the number of shares for a post."""
    return await manager.get_post_share_count(post_id)


@mcp.tool()
async def get_post_reactions_breakdown(post_id: str) -> dict[str, Any]:
    """Get counts for all reaction types on a post."""
    return await manager.get_post_reactions_breakdown(post_id)


@mcp.tool()
async def bulk_delete_comments(comment_ids: list[str]) -> list[dict[str, Any]]:
    """Delete multiple comments by ID."""
    return await manager.bulk_delete_comments(comment_ids)


@mcp.tool()
async def bulk_hide_comments(comment_ids: list[str]) -> list[dict[str, Any]]:
    """Hide multiple comments by ID."""
    return await manager.bulk_hide_comments(comment_ids)


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    transport = sys.argv[1] if len(sys.argv) > 1 else "stdio"
    port = int(os.environ.get("PORT", 8100))

    if transport in ("sse", "streamable-http"):
        import uvicorn

        if transport == "sse":
            app = mcp.sse_app()
        else:
            app = mcp.streamable_http_app()

        uvicorn_cfg = {
            "host": "0.0.0.0",
            "port": port,
            "log_level": "info",
            # Keep-alive: hold TCP connections open for 120s so SSE doesn't drop
            "timeout_keep_alive": 120,
            # Graceful shutdown: wait up to 30s for in-flight requests
            "timeout_graceful_shutdown": 30,
            # Header size: allow large MCP JSON-RPC messages
            "h11_max_incomplete_event_size": 256 * 1024,
        }

        logger.info(f"Starting FacebookMCP ({transport}) on port {port}")
        uvicorn.run(app, **uvicorn_cfg)
    else:
        mcp.run(transport="stdio")

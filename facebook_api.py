import logging
import httpx
from typing import Any
from config import GRAPH_API_BASE_URL, PAGE_ID, PAGE_ACCESS_TOKEN

logger = logging.getLogger("facebook-mcp.api")

# Timeout: 5s connect, 20s read — must complete before tose.sh proxy 30s timeout
DEFAULT_TIMEOUT = httpx.Timeout(connect=5.0, read=20.0, write=5.0, pool=5.0)
MAX_RETRIES = 1  # 1 retry = 2 attempts max, must fit within 30s proxy window


class FacebookAPI:
    def __init__(self):
        transport = httpx.AsyncHTTPTransport(
            retries=1,  # low-level TCP retry
            limits=httpx.Limits(
                max_connections=20,
                max_keepalive_connections=10,
                keepalive_expiry=120,  # match uvicorn keep-alive
            ),
        )
        self._client = httpx.AsyncClient(
            timeout=DEFAULT_TIMEOUT,
            transport=transport,
        )

    async def close(self):
        """Gracefully close the underlying HTTP client."""
        await self._client.aclose()

    async def _request(
        self, method: str, endpoint: str, params: dict[str, Any], json: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        import time
        url = f"{GRAPH_API_BASE_URL}/{endpoint}"
        params["access_token"] = PAGE_ACCESS_TOKEN
        t0 = time.monotonic()
        logger.info(">>> %s %s starting", method, endpoint)

        last_exc: Exception | None = None
        for attempt in range(MAX_RETRIES + 1):
            try:
                resp = await self._client.request(method, url, params=params, json=json)
                logger.info("<<< %s %s done in %.1fs (status=%s)", method, endpoint, time.monotonic() - t0, resp.status_code)
                data = resp.json()

                # Retryable Facebook server errors
                if resp.status_code >= 500 and attempt < MAX_RETRIES:
                    logger.warning(
                        "Facebook API %s (attempt %d/%d): %s",
                        resp.status_code, attempt + 1, MAX_RETRIES + 1, data,
                    )
                    last_exc = Exception(f"Facebook API {resp.status_code}")
                    continue

                # Facebook error in 200 response (rate-limit, auth, etc.)
                if "error" in data:
                    fb_err = data["error"]
                    logger.warning(
                        "Facebook API error: [%s] %s",
                        fb_err.get("code"), fb_err.get("message"),
                    )

                return data

            except httpx.TimeoutException as e:
                last_exc = e
                logger.warning(
                    "Timeout calling %s %s (attempt %d/%d): %s",
                    method, endpoint, attempt + 1, MAX_RETRIES + 1, e,
                )
                if attempt < MAX_RETRIES:
                    continue
            except httpx.HTTPError as e:
                logger.error("HTTP error calling %s %s: %s", method, endpoint, e)
                return {"error": {"message": str(e), "type": "HTTPError"}}
            except Exception as e:
                logger.exception("Unexpected error calling %s %s", method, endpoint)
                return {"error": {"message": str(e), "type": "UnexpectedError"}}

        return {
            "error": {
                "message": f"Request failed after {MAX_RETRIES + 1} attempts: {last_exc}",
                "type": "RetryExhausted",
            }
        }

    # ------------------------------------------------------------------
    # Posts
    # ------------------------------------------------------------------
    async def post_message(self, message: str) -> dict[str, Any]:
        return await self._request("POST", f"{PAGE_ID}/feed", {"message": message})

    async def get_posts(self) -> dict[str, Any]:
        return await self._request("GET", f"{PAGE_ID}/posts", {"fields": "id,message,created_time"})

    async def delete_post(self, post_id: str) -> dict[str, Any]:
        return await self._request("DELETE", f"{post_id}", {})

    async def update_post(self, post_id: str, new_message: str) -> dict[str, Any]:
        return await self._request("POST", f"{post_id}", {"message": new_message})

    async def schedule_post(self, message: str, publish_time: int) -> dict[str, Any]:
        params = {
            "message": message,
            "published": False,
            "scheduled_publish_time": publish_time,
        }
        return await self._request("POST", f"{PAGE_ID}/feed", params)

    async def post_image_to_facebook(self, image_url: str, caption: str) -> dict[str, Any]:
        return await self._request("POST", f"{PAGE_ID}/photos", {"url": image_url, "caption": caption})

    # ------------------------------------------------------------------
    # Comments
    # ------------------------------------------------------------------
    async def get_comments(self, post_id: str) -> dict[str, Any]:
        return await self._request("GET", f"{post_id}/comments", {"fields": "id,message,from,created_time"})

    async def reply_to_comment(self, comment_id: str, message: str) -> dict[str, Any]:
        return await self._request("POST", f"{comment_id}/comments", {"message": message})

    async def delete_comment(self, comment_id: str) -> dict[str, Any]:
        return await self._request("DELETE", f"{comment_id}", {})

    async def hide_comment(self, comment_id: str) -> dict[str, Any]:
        return await self._request("POST", f"{comment_id}", {"is_hidden": True})

    async def unhide_comment(self, comment_id: str) -> dict[str, Any]:
        return await self._request("POST", f"{comment_id}", {"is_hidden": False})

    # ------------------------------------------------------------------
    # Insights
    # ------------------------------------------------------------------
    async def get_insights(self, post_id: str, metric: str, period: str = "lifetime") -> dict[str, Any]:
        return await self._request("GET", f"{post_id}/insights", {"metric": metric, "period": period})

    async def get_bulk_insights(self, post_id: str, metrics: list[str], period: str = "lifetime") -> dict[str, Any]:
        return await self.get_insights(post_id, ",".join(metrics), period)

    # ------------------------------------------------------------------
    # Page / Misc
    # ------------------------------------------------------------------
    async def get_page_fan_count(self) -> int:
        data = await self._request("GET", f"{PAGE_ID}", {"fields": "fan_count"})
        return data.get("fan_count", 0)

    async def get_post_share_count(self, post_id: str) -> int:
        data = await self._request("GET", f"{post_id}", {"fields": "shares"})
        return data.get("shares", {}).get("count", 0)

    async def send_dm_to_user(self, user_id: str, message: str) -> dict[str, Any]:
        payload = {
            "recipient": {"id": user_id},
            "message": {"text": message},
            "messaging_type": "RESPONSE",
        }
        return await self._request("POST", "me/messages", {}, json=payload)

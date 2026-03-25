from typing import Any
from facebook_api import FacebookAPI


class Manager:
    def __init__(self):
        self.api = FacebookAPI()

    async def post_to_facebook(self, message: str) -> dict[str, Any]:
        return await self.api.post_message(message)

    async def reply_to_comment(self, post_id: str, comment_id: str, message: str) -> dict[str, Any]:
        return await self.api.reply_to_comment(comment_id, message)

    async def get_page_posts(self) -> dict[str, Any]:
        return await self.api.get_posts()

    async def get_post_comments(self, post_id: str) -> dict[str, Any]:
        return await self.api.get_comments(post_id)

    async def delete_post(self, post_id: str) -> dict[str, Any]:
        return await self.api.delete_post(post_id)

    async def delete_comment(self, comment_id: str) -> dict[str, Any]:
        return await self.api.delete_comment(comment_id)

    async def hide_comment(self, comment_id: str) -> dict[str, Any]:
        return await self.api.hide_comment(comment_id)

    async def unhide_comment(self, comment_id: str) -> dict[str, Any]:
        return await self.api.unhide_comment(comment_id)

    async def delete_comment_from_post(self, post_id: str, comment_id: str) -> dict[str, Any]:
        return await self.api.delete_comment(comment_id)

    async def filter_negative_comments(self, comments: dict[str, Any]) -> list[dict[str, Any]]:
        keywords = ["bad", "terrible", "awful", "hate", "dislike", "problem", "issue"]
        return [c for c in comments.get("data", []) if any(k in c.get("message", "").lower() for k in keywords)]

    async def get_number_of_comments(self, post_id: str) -> int:
        data = await self.api.get_comments(post_id)
        return len(data.get("data", []))

    async def get_number_of_likes(self, post_id: str) -> int:
        data = await self.api._request("GET", post_id, {"fields": "likes.summary(true)"})
        return data.get("likes", {}).get("summary", {}).get("total_count", 0)

    async def get_post_insights(self, post_id: str) -> dict[str, Any]:
        metrics = [
            "post_impressions", "post_impressions_unique", "post_impressions_paid",
            "post_impressions_organic", "post_engaged_users", "post_clicks",
            "post_reactions_like_total", "post_reactions_love_total", "post_reactions_wow_total",
            "post_reactions_haha_total", "post_reactions_sorry_total", "post_reactions_anger_total",
        ]
        return await self.api.get_bulk_insights(post_id, metrics)

    async def get_post_impressions(self, post_id: str) -> dict[str, Any]:
        return await self.api.get_insights(post_id, "post_impressions")

    async def get_post_impressions_unique(self, post_id: str) -> dict[str, Any]:
        return await self.api.get_insights(post_id, "post_impressions_unique")

    async def get_post_impressions_paid(self, post_id: str) -> dict[str, Any]:
        return await self.api.get_insights(post_id, "post_impressions_paid")

    async def get_post_impressions_organic(self, post_id: str) -> dict[str, Any]:
        return await self.api.get_insights(post_id, "post_impressions_organic")

    async def get_post_engaged_users(self, post_id: str) -> dict[str, Any]:
        return await self.api.get_insights(post_id, "post_engaged_users")

    async def get_post_clicks(self, post_id: str) -> dict[str, Any]:
        return await self.api.get_insights(post_id, "post_clicks")

    async def get_post_reactions_like_total(self, post_id: str) -> dict[str, Any]:
        return await self.api.get_insights(post_id, "post_reactions_like_total")

    async def get_post_reactions_love_total(self, post_id: str) -> dict[str, Any]:
        return await self.api.get_insights(post_id, "post_reactions_love_total")

    async def get_post_reactions_wow_total(self, post_id: str) -> dict[str, Any]:
        return await self.api.get_insights(post_id, "post_reactions_wow_total")

    async def get_post_reactions_haha_total(self, post_id: str) -> dict[str, Any]:
        return await self.api.get_insights(post_id, "post_reactions_haha_total")

    async def get_post_reactions_sorry_total(self, post_id: str) -> dict[str, Any]:
        return await self.api.get_insights(post_id, "post_reactions_sorry_total")

    async def get_post_reactions_anger_total(self, post_id: str) -> dict[str, Any]:
        return await self.api.get_insights(post_id, "post_reactions_anger_total")

    async def get_post_top_commenters(self, post_id: str) -> list[dict[str, Any]]:
        data = await self.get_post_comments(post_id)
        comments = data.get("data", [])
        counter: dict[str, int] = {}
        for comment in comments:
            user_id = comment.get("from", {}).get("id")
            if user_id:
                counter[user_id] = counter.get(user_id, 0) + 1
        return sorted([{"user_id": k, "count": v} for k, v in counter.items()], key=lambda x: x["count"], reverse=True)

    async def post_image_to_facebook(self, image_url: str, caption: str) -> dict[str, Any]:
        return await self.api.post_image_to_facebook(image_url, caption)

    async def send_dm_to_user(self, user_id: str, message: str) -> dict[str, Any]:
        return await self.api.send_dm_to_user(user_id, message)

    async def update_post(self, post_id: str, new_message: str) -> dict[str, Any]:
        return await self.api.update_post(post_id, new_message)

    async def schedule_post(self, message: str, publish_time: int) -> dict[str, Any]:
        return await self.api.schedule_post(message, publish_time)

    async def get_page_fan_count(self) -> int:
        return await self.api.get_page_fan_count()

    async def get_post_share_count(self, post_id: str) -> int:
        return await self.api.get_post_share_count(post_id)

    async def get_post_reactions_breakdown(self, post_id: str) -> dict[str, Any]:
        metrics = [
            "post_reactions_like_total",
            "post_reactions_love_total",
            "post_reactions_wow_total",
            "post_reactions_haha_total",
            "post_reactions_sorry_total",
            "post_reactions_anger_total",
        ]
        raw = await self.api.get_bulk_insights(post_id, metrics)
        results: dict[str, Any] = {}
        for item in raw.get("data", []):
            name = item.get("name")
            value = item.get("values", [{}])[0].get("value")
            results[name] = value
        return results

    async def bulk_delete_comments(self, comment_ids: list[str]) -> list[dict[str, Any]]:
        results = []
        for cid in comment_ids:
            res = await self.api.delete_comment(cid)
            results.append({"comment_id": cid, "result": res})
        return results

    async def bulk_hide_comments(self, comment_ids: list[str]) -> list[dict[str, Any]]:
        results = []
        for cid in comment_ids:
            res = await self.api.hide_comment(cid)
            results.append({"comment_id": cid, "result": res})
        return results

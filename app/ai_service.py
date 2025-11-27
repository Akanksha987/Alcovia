import asyncio
import logging
from dataclasses import dataclass
from typing import Any

import httpx

from .config import settings

logger = logging.getLogger(__name__)


@dataclass
class AIResult:
    summary: str
    sentiment: str
    sentiment_score: float


class AIService:
    def __init__(self) -> None:
        self.api_key = settings.huggingface_api_key
        self.summary_model = settings.summarization_model
        self.sentiment_model = settings.sentiment_model

    async def summarize_and_analyze(self, text: str) -> AIResult:
        summary_task = asyncio.create_task(self._summarize(text))
        sentiment_task = asyncio.create_task(self._sentiment(text))
        summary, sentiment_payload = await asyncio.gather(summary_task, sentiment_task)
        return AIResult(summary=summary, **sentiment_payload)

    async def _summarize(self, text: str) -> str:
        if not self.api_key:
            logger.warning("HuggingFace API key missing, falling back to heuristic summarizer.")
            return self._fallback_summary(text)

        payload = {"inputs": text, "parameters": {"min_length": 15, "max_length": 120}}
        response = await self._call_huggingface(self.summary_model, payload)
        if isinstance(response, list) and response:
            return response[0].get("summary_text", "")
        return self._fallback_summary(text)

    async def _sentiment(self, text: str) -> dict[str, Any]:
        if not self.api_key:
            logger.warning("HuggingFace API key missing, using heuristic sentiment.")
            return self._fallback_sentiment(text)

        response = await self._call_huggingface(self.sentiment_model, {"inputs": text})
        try:
            best = max(response[0], key=lambda item: item["score"])
            label = best["label"].lower()
            label = self._normalize_label(label)
            return {
                "sentiment": label,
                "sentiment_score": float(best["score"]),
            }
        except (KeyError, IndexError, TypeError) as exc:
            logger.error("Failed to parse sentiment response: %s", exc)
            return self._fallback_sentiment(text)

    async def _call_huggingface(self, model: str, payload: dict[str, Any]) -> Any:
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        url = f"https://api-inference.huggingface.co/models/{model}"
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()

    @staticmethod
    def _fallback_summary(text: str) -> str:
        sentences = text.split(".")
        trimmed = ". ".join(sent.strip() for sent in sentences[:2] if sent.strip())
        return trimmed or text[:200]

    @staticmethod
    def _fallback_sentiment(text: str) -> dict[str, Any]:
        lowered = text.lower()
        positive_words = sum(lowered.count(word) for word in ["good", "great", "excellent", "love"])
        negative_words = sum(lowered.count(word) for word in ["bad", "terrible", "hate", "poor"])
        score = positive_words - negative_words
        if score > 0:
            sentiment = "positive"
        elif score < 0:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        normalized = min(max(score / 10.0 + 0.5, 0.0), 1.0)
        return {"sentiment": sentiment, "sentiment_score": normalized}

    @staticmethod
    def _normalize_label(label: str) -> str:
        mapping = {
            "label_0": "negative",
            "label_1": "neutral",
            "label_2": "positive",
        }
        return mapping.get(label, label)


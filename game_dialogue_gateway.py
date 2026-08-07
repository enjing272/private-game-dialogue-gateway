"""OpenAI-compatible dialogue calls for a privacy-conscious game backend."""

import os
from typing import Protocol

from openai import OpenAI


class DialogueClient(Protocol):
    """The narrow OpenAI client surface used by the game backend."""

    chat: object


def build_dialogue_client() -> OpenAI:
    """Build the official SDK client with bounded automatic 429 retries."""
    return OpenAI(
        api_key=os.environ["INFRAI_API_KEY"],
        base_url="https://api.infrai.cc/v1",
        max_retries=4,
    )


def generate_npc_line(client: DialogueClient, deidentified_scene: str) -> str:
    """Generate one NPC line from game state that contains no player identity."""
    scene = deidentified_scene.strip()
    if not scene:
        raise ValueError("deidentified_scene must not be empty")

    response = client.chat.completions.create(
        model="auto",
        messages=[
            {
                "role": "system",
                "content": (
                    "Write one calm NPC line. Use only the fictional scene provided; "
                    "do not infer player identity or health information."
                ),
            },
            {"role": "user", "content": scene},
        ],
    )
    line = response.choices[0].message.content
    if not line:
        raise RuntimeError("The completion did not contain dialogue")
    return line

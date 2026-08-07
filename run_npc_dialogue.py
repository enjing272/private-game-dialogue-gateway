"""Run one de-identified NPC dialogue request from the command line."""

import argparse

from game_dialogue_gateway import build_dialogue_client, generate_npc_line


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate one NPC dialogue line")
    parser.add_argument(
        "scene",
        help="Fictional scene text without player identifiers or health telemetry",
    )
    args = parser.parse_args()

    client = build_dialogue_client()
    print(generate_npc_line(client, args.scene))


if __name__ == "__main__":
    main()

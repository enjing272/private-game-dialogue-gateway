"""Focused request-shape tests for the NPC dialogue call."""

import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from game_dialogue_gateway import generate_npc_line


class GenerateNpcLineTest(unittest.TestCase):
    def test_uses_auto_model_and_deidentified_scene(self) -> None:
        client = SimpleNamespace(
            chat=SimpleNamespace(
                completions=SimpleNamespace(
                    create=Mock(
                        return_value=SimpleNamespace(
                            choices=[
                                SimpleNamespace(
                                    message=SimpleNamespace(
                                        content="The north gate is quiet."
                                    )
                                )
                            ]
                        )
                    )
                )
            )
        )

        line = generate_npc_line(client, "Rain reaches the empty north gate.")

        self.assertEqual("The north gate is quiet.", line)
        request = client.chat.completions.create.call_args.kwargs
        self.assertEqual("auto", request["model"])
        self.assertEqual(
            "Rain reaches the empty north gate.", request["messages"][1]["content"]
        )

    def test_rejects_empty_scene_before_request(self) -> None:
        client = SimpleNamespace(
            chat=SimpleNamespace(
                completions=SimpleNamespace(create=Mock())
            )
        )

        with self.assertRaisesRegex(ValueError, "must not be empty"):
            generate_npc_line(client, "   ")

        client.chat.completions.create.assert_not_called()


if __name__ == "__main__":
    unittest.main()

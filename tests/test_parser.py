
import sys
from pathlib import Path

# Make the src folder available for imports.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from chat_analyzer.parser import parse_chat_text


def test_single_message():
    chat = "05/10/26, 8:02 PM - Aarav: Hello everyone"

    messages = parse_chat_text(chat)

    assert len(messages) == 1
    assert messages[0]["sender"] == "Aarav"
    assert messages[0]["text"] == "Hello everyone"


def test_multiline_message():
    chat = (
        "05/10/26, 8:02 PM - Aarav: First line\n"
        "This is the second line"
    )

    messages = parse_chat_text(chat)

    assert len(messages) == 1
    assert messages[0]["text"] == "First line\nThis is the second line"


def test_multiple_messages():
    chat = (
        "05/10/26, 8:02 PM - Aarav: Hello\n"
        "05/10/26, 8:10 PM - Meera: Hi"
    )

    messages = parse_chat_text(chat)

    assert len(messages) == 2
    assert messages[0]["sender"] == "Aarav"
    assert messages[1]["sender"] == "Meera"

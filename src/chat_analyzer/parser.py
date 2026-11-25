
import re
from datetime import datetime
from pathlib import Path


# Pattern to identify the beginning of a WhatsApp message
MESSAGE_PATTERN = re.compile(
    r"^(?P<date>\d{1,2}/\d{1,2}/\d{2,4}),\s*"
    r"(?P<time>\d{1,2}:\d{2}\s*(?:AM|PM)?)\s+-\s+"
    r"(?:(?P<sender>[^:]+):\s*)?"
    r"(?P<message>.*)$",
    re.IGNORECASE
)


def parse_timestamp(date_text, time_text):
    """Convert the date and time into a Python datetime object."""

    timestamp_text = f"{date_text}, {time_text}"

    formats = [
        "%d/%m/%y, %I:%M %p",
        "%d/%m/%Y, %I:%M %p",
        "%d/%m/%y, %H:%M",
        "%d/%m/%Y, %H:%M",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(timestamp_text, fmt)
        except ValueError:
            continue

    raise ValueError(f"Unsupported timestamp: {timestamp_text}")


def parse_chat_text(chat_text):
    """Convert WhatsApp chat text into structured messages."""

    messages = []

    for line_number, line in enumerate(chat_text.splitlines(), start=1):
        match = MESSAGE_PATTERN.match(line)

        if match:
            # A new message has started.
            date_text = match.group("date")
            time_text = match.group("time").strip()
            sender = match.group("sender")
            message_text = match.group("message")

            timestamp = parse_timestamp(date_text, time_text)

            messages.append({
                "timestamp": timestamp,
                "sender": sender.strip() if sender else None,
                "text": message_text,
                "line_number": line_number
            })

        elif messages:
            # This line continues the previous message.
            messages[-1]["text"] += "\n" + line

    return messages


def parse_chat_file(file_path):
    """Read a chat file and parse its messages."""

    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"Chat file not found: {file_path}")

    chat_text = path.read_text(encoding="utf-8-sig")

    return parse_chat_text(chat_text)

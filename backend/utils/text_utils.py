import html
import re


def sanitize_text(text: str) -> str:
    """Normalize AI output before putting it into downloadable documents."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text.strip()


def text_to_html(text: str) -> str:
    """Convert plain generated text to safe preview HTML."""
    safe = html.escape(sanitize_text(text))
    blocks = []
    for paragraph in re.split(r"\n\s*\n", safe):
        p = paragraph.strip()
        if not p:
            continue
        if re.match(r"^(ARTICLE|SECTION|[0-9]+\.)\b", p, re.I):
            blocks.append(f"<h3>{p}</h3>")
        elif p.startswith(("- ", "• ")):
            items = "<br>".join(
                f"• {line[2:].strip()}" for line in p.splitlines() if line.strip()
            )
            blocks.append(f"<p>{items}</p>")
        else:
            blocks.append(f"<p>{p.replace(chr(10), '<br>')}</p>")
    return "\n".join(blocks)

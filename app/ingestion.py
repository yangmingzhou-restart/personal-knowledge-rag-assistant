import csv
from io import StringIO
from pathlib import Path


class UnsupportedFileTypeError(ValueError):
    """
    UnsupportedFileTypeError: when the file type is not supported
    """
    pass


def extract_text(filename: str, content: bytes) -> str:
    """
    filename: str, the filename of the file
    content: bytes, the content of the file
    return: str, the text extracted from the file
            it will be used to chunk_text()
    """
    extension = Path(filename).suffix.lower()

    if extension in {".txt", ".md"}:
        return content.decode("utf-8")

    if extension == ".csv":
        return _extract_csv_text(content)

    raise UnsupportedFileTypeError(f"Unsupported file type: {extension}")


def _extract_csv_text(content: bytes) -> str:
    """
    content: bytes, the content of the csv file
    return: str, the text extracted from the csv file
            it will be used to chunk_text()
    """
    decoded = content.decode("utf-8")
    reader = csv.DictReader(StringIO(decoded))

    lines = []
    for row in reader:
        parts = []
        for key, value in row.items():
            parts.append(f"{key}={value}")
        lines.append(", ".join(parts))

    return "\n".join(lines)

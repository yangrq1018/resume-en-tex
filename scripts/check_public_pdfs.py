"""Fail a release if contact text or contact hyperlinks reach a public PDF."""

import re
import sys
from pathlib import Path
from urllib.parse import unquote

from pypdf import PdfReader


EMAIL = re.compile(r"[A-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)


def digits(value):
    return re.sub(r"\D", "", value)


def read_pdf(path):
    reader = PdfReader(path)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    uris = []
    for page in reader.pages:
        annotations = page.get("/Annots")
        if annotations is None:
            continue
        for ref in annotations.get_object():
            annotation = ref.get_object()
            action = annotation.get("/A")
            if action:
                uri = action.get_object().get("/URI")
                if uri:
                    uris.append(unquote(str(uri)))
    metadata = "\n".join(str(value) for value in (reader.metadata or {}).values())
    return reader, text, uris, metadata


def check_pair(directory, language):
    private_path = directory / f"main-{language}.pdf"
    public_path = directory / f"main-{language}-public.pdf"
    private, private_text, private_uris, _ = read_pdf(private_path)
    public, text, uris, metadata = read_pdf(public_path)

    private_emails = [uri[7:] for uri in private_uris if uri.lower().startswith("mailto:")]
    private_phones = [digits(uri[4:]) for uri in private_uris if uri.lower().startswith("tel:")]
    if not private_emails or not private_phones:
        raise ValueError(f"{private_path.name}: cannot identify original contact fields")
    if any(email.lower() not in private_text.lower() for email in private_emails):
        raise ValueError(f"{private_path.name}: original email is not extractable")
    if any(phone not in digits(private_text) for phone in private_phones):
        raise ValueError(f"{private_path.name}: original telephone is not extractable")

    if len(public.pages) != len(private.pages):
        raise ValueError(f"{public_path.name}: page count changed")
    if public.is_encrypted or public.get_fields() or public.attachments:
        raise ValueError(f"{public_path.name}: unexpected encryption, form or attachment")
    if any(uri.lower().startswith(("tel:", "mailto:")) for uri in uris):
        raise ValueError(f"{public_path.name}: contact hyperlink remains")
    public_strings = [text, metadata, *uris]
    for value in public_strings:
        if EMAIL.search(value):
            raise ValueError(f"{public_path.name}: email remains in text, metadata or links")
        if any(phone in digits(value) for phone in private_phones):
            raise ValueError(f"{public_path.name}: telephone remains in text, metadata or links")
    if len(text.strip()) < len(private_text.strip()) * 0.8:
        raise ValueError(f"{public_path.name}: too much resume content is missing")
    print(f"PASS {public_path.name}: {len(public.pages)} page(s); no contact text or links")


def main():
    directory = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("build")
    for language in ("cn", "en"):
        check_pair(directory, language)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        raise SystemExit(str(error)) from None

"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str
"""

import re
import config
from generate import generate
from utils.data_loader import load_listings


# ── Helper Functions ──────────────────────────────────────────────────────────

def _size_matches(query_size: str, item_size: str) -> bool:
    """
    Check if query_size matches item_size case-insensitively using token/boundary matching.
    Avoids false positives like 's' in 'us 9' or 'l' in 'xl'.
    """
    q = query_size.strip().upper()
    i = item_size.strip().upper()

    if q == i:
        return True

    # Split combined size strings like "S/M", "M/L", "US 9"
    tokens = [t.strip() for t in re.split(r"[/,\s]+", i) if t.strip()]
    return q in tokens


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        Returns an empty list [] when nothing matches.
    """
    listings = load_listings()
    matches = []

    # Extract keywords from the query description (skip single characters)
    keywords = [kw.lower() for kw in description.split() if len(kw) > 1]

    for item in listings:
        # 1. Filter by max_price (inclusive)
        if max_price is not None and item.get("price", float("inf")) > max_price:
            continue

        # 2. Filter by size with token matching
        if size is not None:
            item_size = str(item.get("size", ""))
            if not _size_matches(size, item_size):
                continue

        # 3. Score keyword overlap across title, description, and style_tags
        tags_str = " ".join(item.get("style_tags", []))
        text_corpus = f"{item.get('title', '')} {item.get('description', '')} {tags_str}".lower()

        score = sum(1 for kw in keywords if kw in text_corpus)

        # 4. Drop anything scoring zero
        if keywords and score == 0:
            continue

        item_copy = dict(item)
        item_copy["_score"] = score
        matches.append(item_copy)

    # 5. Sort by score descending, then price ascending
    matches.sort(key=lambda x: (-x.get("_score", 0), x.get("price", float("inf"))))

    # Strip helper key and limit results to config.SEARCH_RESULT_LIMIT
    limit = getattr(config, "SEARCH_RESULT_LIMIT", 5)
    result = []
    for m in matches[:limit]:
        m.pop("_score", None)
        result.append(m)

    return result


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  It may be empty.

    Returns:
        A non-empty string with outfit suggestions.
    """
    wardrobe_items = wardrobe.get("items", []) if isinstance(wardrobe, dict) else []

    title = new_item.get("title", "thrifted piece")
    description = new_item.get("description", "")
    item_str = f"{title} ({description})"

    if not wardrobe_items:
        prompt = (
            f"You are a personal stylist. The user does not have any saved wardrobe pieces.\n"
            f"Suggest two versatile outfits built around this second-hand item:\n"
            f"Item: {item_str}\n\n"
            f"Explicitly state that these suggestions are general styling ideas because no personal wardrobe was saved. "
            f"Present two clear outfit options."
        )
    else:
        wardrobe_list = "\n".join(
            f"- {w.get('name', w.get('title', 'item'))} ({w.get('category', '')}, {w.get('color', '')})"
            for w in wardrobe_items
        )
        prompt = (
            f"You are a personal stylist. Suggest two distinct outfits built around this new thrift item:\n"
            f"Item: {item_str}\n\n"
            f"User's available wardrobe pieces:\n{wardrobe_list}\n\n"
            f"Rule: Incorporate pieces from the user's wardrobe and name those pieces as written. "
            f"Present two structured outfit suggestions."
        )

    return generate(prompt)


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption mentioning the item, price with digits, and platform.
    """
    if not outfit or not outfit.strip():
        return "Unable to generate fit card: no outfit suggestions were provided."

    price = new_item.get("price", "N/A")
    platform = new_item.get("platform", "thrift app")
    title = new_item.get("title", "this thrift piece")

    prompt = (
        f"Write an engaging social-media-style caption about this second-hand fashion find and how to style it.\n\n"
        f"Item: {title}\n"
        f"Price: ${price}\n"
        f"Platform: {platform}\n"
        f"Styling Context: {outfit}\n\n"
        f"Requirements:\n"
        f"- Exactly 2 to 4 sentences.\n"
        f"- State the price using digits with a dollar sign (e.g. '${price}').\n"
        f"- Explicitly mention the platform name ('{platform}')."
    )

    return generate(prompt)
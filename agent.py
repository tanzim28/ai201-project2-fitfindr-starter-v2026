"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls all three tools no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. **That branch is the graded part of this unit.**

Build and test your three tools in `tools.py` first. Then come here.

    python agent.py          runs both example paths below
"""

import re
import config
import trace
from tools import search_listings, suggest_outfit, create_fit_card
from generate import ModelUnavailable


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.

    The session is the single source of truth for a run. Every tool result goes
    in here, and the next tool reads it back out.
    """
    return {
        "query": query,              # what the user typed
        "parsed": {},                # description / size / max_price you pulled out of it
        "search_results": [],        # everything search_listings returned
        "selected_item": None,       # the one you chose — goes into suggest_outfit
        "wardrobe": wardrobe,        # the user's wardrobe
        "outfit_suggestion": None,   # what suggest_outfit returned
        "fit_card": None,            # what create_fit_card returned
        "error": None,               # set when the run ended early
    }


# ── parser helper ─────────────────────────────────────────────────────────────

def parse_query(query: str) -> dict:
    """
    Parse a plain text query into structured filters: description, size, and max_price.
    """
    text = query

    # 1. Extract maximum price ceiling (e.g. 'under $30', '< $25', 'below 40')
    max_price = None
    price_match = re.search(r"(?:under|less than|<|below)\s*\$?(\d+(?:\.\d+)?)", text, re.IGNORECASE)
    if price_match:
        max_price = float(price_match.group(1))
        text = text[:price_match.start()] + " " + text[price_match.end():]

    # 2. Extract standard clothing size (e.g. 'size M', 'size: XL', or isolated tokens XS/S/M/L/XL/XXL)
    size = None
    size_match = re.search(r"\bsize[:\s]+(XS|S|M|L|XL|XXL|\d+)\b", text, re.IGNORECASE)
    if size_match:
        size = size_match.group(1).upper()
        text = text[:size_match.start()] + " " + text[size_match.end():]
    else:
        standalone_size = re.search(r"\b(XS|S|M|L|XL|XXL)\b", text, re.IGNORECASE)
        if standalone_size:
            size = standalone_size.group(1).upper()
            text = text[:standalone_size.start()] + " " + text[standalone_size.end():]

    # 3. Clean remaining text to form the search description keywords
    description = " ".join(text.split()).strip()

    return {
        "description": description,
        "size": size,
        "max_price": max_price,
    }


def _nothing_found_message(parsed: dict) -> str:
    """Build an actionable explanation for the empty-search branch."""
    details = []
    if parsed.get("description"):
        details.append(f"description '{parsed['description']}'")
    if parsed.get("size"):
        details.append(f"size '{parsed['size']}'")
    if parsed.get("max_price") is not None:
        details.append(f"budget under ${parsed['max_price']:.2f}")

    filters_str = ", ".join(details) if details else "the provided filters"
    return (
        f"No listings found matching {filters_str}. Try increasing your maximum price limit, "
        f"removing the specific size constraint, or using broader style terms."
    )


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Run the loop once and return the finished session.

    Args:
        query:    what the user asked for, in plain language
                  (e.g. "vintage graphic tee under $30, size M").
        wardrobe: a wardrobe dict — get_example_wardrobe() or
                  get_empty_wardrobe() from utils/data_loader.py.

    Returns:
        The session dict. Check session["error"] first — if it isn't None,
        the run ended early and the later fields will still be None.
    """
    # 1. Start a clean session
    session = new_session(query, wardrobe)

    # 2. Check iteration guard
    iteration = 1
    if hasattr(trace, "check_iterations"):
        trace.check_iterations(iteration)

    # 3. Parse query into structured fields and save in session["parsed"]
    session["parsed"] = parse_query(session["query"])

    # 4. Call search_listings and store in session["search_results"]
    parsed = session["parsed"]
    session["search_results"] = search_listings(
        description=parsed["description"],
        size=parsed["size"],
        max_price=parsed["max_price"],
    )

    # ⚠️ THIS IS THE BRANCH: If nothing came back, halt cleanly and explain what to adjust
    if not session["search_results"]:
        session["error"] = _nothing_found_message(session["parsed"])
        return session

    # 5. Choose top result and store in session["selected_item"]
    session["selected_item"] = session["search_results"][0]

    # 6. Call suggest_outfit using session state values
    session["outfit_suggestion"] = suggest_outfit(
        new_item=session["selected_item"],
        wardrobe=session["wardrobe"],
    )

    # 7. Call create_fit_card using session state values
    session["fit_card"] = create_fit_card(
        outfit=session["outfit_suggestion"],
        new_item=session["selected_item"],
    )

    # 8. Return finished session
    return session


# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(f"  fit_card is {session['fit_card']!r} — it should still be None here")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))

    print("\n=== A query it can't ===")
    _show(run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    ))

    print(
        "\nThe second one should stop before the fit card. If both paths look "
        "the same,\nthe branch isn't doing anything yet."
    )
# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. -->

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->

---

## 3. Session state preserves selected item integrity across tool boundaries

In at least 4 of 5 successful runs, the listing dictionary stored in `session["selected_item"]` has the exact same `id`, `title`, and `price` as the dictionary passed into `tools.py::suggest_outfit`.

**Why this target:**
The agent must carry retrieved data from `search_listings` into `suggest_outfit` via the shared `session` dictionary without mutating or dropping keys. Allowing 4 of 5 accounts for test edge cases where multiple listings tie on score, verifying that session memory maintains data integrity across tool calls.



---

## 4. Fit card includes price digits, platform name, and meets length constraints

<!-- YOU WRITE THIS ONE.

     The fit card calls a model, so the same input can produce different words
     each time. That's not a bug — it's the nature of the tool. So what would
     make it acceptable?

     Think about what you'd actually be unhappy to see. A caption that never
     mentions the price? Two different items producing the same opening
     sentence? A card longer than a caption anyone would post? Any of those can
     be turned into a number. -->


Across 5 runs with a matched listing, the generated fit card contains the item's price written with digits (e.g., "$25"), mentions the selling platform name, and consists of between 2 and 4 sentences — in at least 4 of 5 tries.

**Why this target:**
Because `tools.py::create_fit_card` uses an LLM with non-zero temperature, generative phrasing naturally varies across runs. Rather than attempting to evaluate subjective style, this target tests verifiable structural constraints and entity extraction while tolerating minor model formatting drift.



---

## 5. Search strictly enforces maximum price ceilings

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. Speed, the empty
     wardrobe path, what happens when the model can't be reached, whether the
     search respects a price ceiling — anything, as long as it names a number
     or an observable outcome. -->

When a query contains a maximum price (such as "under $30"), every listing returned by `tools.py::search_listings` has a price less than or equal to that maximum threshold — in 5 of 5 tries.

**Why this target:**
Filtering by price in `tools.py::search_listings` is performed by direct numeric comparison against `listing["price"]` in `data/listings.json`. Because numerical filtering in Python does not depend on model generation, it must never leak over-budget items.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->

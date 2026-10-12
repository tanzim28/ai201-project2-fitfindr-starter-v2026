# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->
FitFindr is an agentic styling assistant that finds second-hand fashion pieces and creates tailored outfit ideas using the user's existing wardrobe. A user enters a natural-language search request specifying style keywords, size preferences, and price constraints. The agent parses the request, filters and ranks matching catalog listings, recommends two distinct outfits that incorporate wardrobe pieces, and composes an engaging social-media fit card highlighting the find, its price, and the platform.


---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Searches the local clothing catalogue (`data/listings.json`) by description keywords with optional size and inclusive maximum-price filters.
- **Inputs:** `description` (str), `size` (str | None = None), `max_price` (float | None = None)
- **Returns:** A list of matching listing dictionaries (each containing `id`, `title`, `price`, `size`, `platform`, `description`, `link`), ranked by keyword relevance and price.
- **When it has nothing:** Returns an empty list `[]` (not `None` and not an exception).

### `suggest_outfit`

- **What it does:** Recommends two complementary outfit combinations built around a selected clothing listing, incorporating items from the user's wardrobe when available.
- **Inputs:** `new_item` (dict), `wardrobe` (dict)
- **Returns:** A non-empty string containing two outfit suggestions naming pieces from the wardrobe as written.
- **When it has nothing:** When the wardrobe is empty (`{"items": []}`), returns general styling advice and explicitly states that suggestions are generic because no wardrobe is saved.

### `create_fit_card`

- **What it does:** Drafts a concise, social-media-style caption about the selected thrift item and how to style it.
- **Inputs:** `outfit` (str), `new_item` (dict)
- **Returns:** A string of 2 to 4 sentences highlighting the piece, styling tips, price written with digits (e.g. `$25`), and the selling platform.
- **When it has nothing:** If `outfit` is empty or whitespace, returns a helpful fallback error message rather than calling the model or raising an exception.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

- **Branch rule:** If `search_listings` returns an empty list (`[]`), put an explanatory message in `session["error"]` specifying what the user could change and stop execution immediately. Otherwise, take the first result, store it in `session["selected_item"]`, and proceed to `suggest_outfit`.
- **Where it lives:** `agent.py::run_agent`
- **How the query is parsed:** `agent.py::parse_query` extracts description keywords, detects standard size tokens (e.g., XS, S, M, L, XL), and extracts numerical price ceilings (e.g., `under $30` -> `30.0`).
- **What moves through the session:** The user query string, parsed parameters dictionary, search results list, selected listing dictionary, user wardrobe dictionary, outfit suggestions string, final fit card string, and any error message.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30'
Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

Outfit:   As your personal stylist, I am so excited you scored that Y2K butterfly baby tee! Because it has that fitted, cropped silhouette, it’s the ultimate canvas to play with proportions.

Here are two distinct, vibe-checked outfits using pieces straight from your wardrobe:

Look 1: Off-Duty Model Y2K Streetwear
The Vibe: Effortless, nostalgic, and leaning hard into early 2000s off-duty style by playing with oversized silhouettes.

Top: Y2K Baby Tee — Butterfly Print

Bottoms: Baggy straight-leg jeans, dark wash

Outerwear: Black cropped zip hoodie (worn open or draped over the shoulders)

Shoes: Chunky white sneakers

Accessories: Black crossbody bag

Styling Notes: Let the fitted baby tee be the star by pairing it with your baggy straight-leg jeans for that classic Y2K contrast. Throw the black cropped zip hoodie on top, leaving it unzipped so the butterfly graphic still pops. Finish the look with your chunky white sneakers to lean into the retro athletic aesthetic, and sling the black crossbody bag across your chest for easy street-style utility.

Look 2: Elevated Smart-Casual Contrast
The Vibe: High-low styling that mixes structured tailoring with playful, retro femininity.

Top: Y2K Baby Tee — Butterfly Print

Bottoms: Wide-leg khaki trousers

Outerwear: Vintage black denim jacket

Shoes: Black combat boots

Accessories: Brown leather belt, Black crossbody bag

Styling Notes: Tuck the baby tee into your wide-leg khaki trousers and cinch the waist with the brown leather belt to give the outfit some sharp definition. Layer the vintage black denim jacket on top for a cool, textural contrast against the smooth khaki fabric. Ground the softer, nostalgic tee with your edgy black combat boots, and tie it all together with your black crossbody bag for a polished finish that feels modern and intentional.

Fit card: Look at this absolute Depop steal I scored for just $18.0! I am obsessed with this Y2K butterfly baby tee and love styling it either oversized with baggy jeans for off-duty street vibes, or tucked into khaki trousers with combat boots for an elevated smart-casual look. Which vibe are we wearing out today?

2 model calls this session, 724 prompt + 494 output tokens

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
[{'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}]

```

```
$ python -c "from tools import suggest_outfit; ..."
python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
Hello! As your personal stylist, I am so excited to style those Vintage Levi's 501 Jeans for you. A medium-wash 501 is the ultimate wardrobe chameleon—timeless, versatile, and effortless. 

Here are two distinct outfits built around your new thrift find, using pieces straight from your current wardrobe:

***

### Outfit 1: Effortless Off-Duty Streetwear
*This look plays with proportions and textures, taking inspiration from casual 90s model-off-duty style. It balances an oversized silhouette on top with the classic, straight fit of your new denim.*

* **Top:** Oversized grey crewneck sweatshirt
* **Outerwear:** Vintage black denim jacket (worn layered over the sweatshirt)
* **Shoes:** Chunky white sneakers
* **Accessories:** Black crossbody bag

**Why it works:** 
Layering the oversized grey crewneck sweatshirt under the vintage black denim jacket creates instant cool-factor and depth with contrasting shades of grey and black. Toning down the heaviness of the double-layer top, the chunky white sneakers add a fresh, sporty pop to the bottom while complementing the medium wash of the Levi's. Throwing on the black crossbody bag keeps your hands free and ties the black outerwear and footwear together for a cohesive, street-ready finish.

***

### Outfit 2: Edgy Casual Chic
*This outfit leans into a sharper, more defined aesthetic. By incorporating fitted elements and dark accents, it elevates the vintage jeans for a coffee run, a casual lunch, or a night out.*

* **Top:** White ribbed tank top
* **Shoes:** Black combat boots
* **Accessories:** Brown leather belt, Black crossbody bag

**Why it works:**
Tucking the fitted white ribbed tank top into the vintage Levi's 501 Jeans creates a classic, high-waisted silhouette that highlights the waist. Adding the brown leather belt introduces a rich, warm contrast against the medium-wash denim and anchors the top-to-bottom look. Grounding the outfit with the black combat boots adds an edgy, downtown-girl attitude that contrasts nicely with the clean simplicity of the white tank, finished off simply and practically with the black crossbody bag.


```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Scored these vintage Levi's 501 jeans in the dreamiest medium wash on depop for just $38.0! I'm styling them with crisp white sneakers for that effortlessly cool, off-duty model aesthetic. Sustainable style has truly never looked this good.

```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

### Moment 1
- **What I asked for:** I asked for a function implementation for `tools.py::search_listings` that filters listings by size, price ceiling, and description keywords.
- **What came back:** The generated code used a naive substring check for sizes (`if size.lower() in item['size'].lower()`), which produced false matches (e.g., matching size "S" inside "US 9" or "L" inside "XL").
- **What I changed:** I implemented a custom `_size_matches` helper using token splitting and regular expression boundaries (`re.split(r"[/,\s]+", item_size)`) to ensure exact whole-token matches across compound size labels like "S/M".

### Moment 2
- **What I asked for:** I asked how to parse natural-language search queries in `agent.py::parse_query`.
- **What came back:** The suggested implementation attempted to call the language model API on every user query to extract structured JSON arguments.
- **What I changed:** I replaced the model call with deterministic regex extraction for price limits and size tokens. This eliminated unnecessary API latency, prevented token usage on query preprocessing, and ensured predictable extraction before running `search_listings`.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

- Produced by: `run_eval.py::main`
- Loop: `agent.py::run_agent` · tools: `tools.py`
- Tries per scenario: 5, caching off
- Temperature: 0.9
- When: 2026-10-12 02:33

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all three tools | 4 of 5 | FAIL | PASS | PASS | PASS | PASS | MET (4/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Session state preserves selected item integrity across tool boundaries | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card includes price digits, platform name, and meets length constraints | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Search strictly enforces maximum price ceilings | 5 of 5 | FAIL | FAIL | FAIL | FAIL | FAIL | MISSED (0/5) |

**Real output from one try**, pasted as text, naming the file and function that produced it:

*File: `agent.py::run_agent` (Scenario 1: matching query completes, Try 2)*

```
[1] search_listings (MCP)
      in:  dict with keys: description, size, max_price
      out: 10 listings found
[2] suggest_outfit
      in:  dict with keys: item
      out: outfit suggestions generated
[3] create_fit_card
      in:  dict with keys: item
      out: Run, don’t walk, because scoring this Y2K butterfly baby tee...

selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
search_results: 10

Fit card:
Run, don’t walk, because scoring this Y2K butterfly baby tee on depop for just $18.0 is an absolute steal! We are styling it two ways: keeping it effortless with baggy dark-wash denim for off-duty model vibes, or elevating it with wide-leg khaki trousers and combat boots for an edgy contrast. Which fit are we wearing out first? 🦋✨
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | A matching query completes all three tools | 4 of 5 | MET | 4 of 5 tries completed; Try 1 stopped early when the external model returned a transient 500 error, but Tries 2 through 5 ran all three tools and produced a fit card. |
| 2 | An impossible query stops before the second tool | 5 of 5 | MET | 5 of 5 tries stopped after search returned 0 items, cleanly exiting before calling suggest_outfit and returning actionable advice. |
| 3 | Session state preserves selected item integrity across tool boundaries | 4 of 5 | MET | 5 of 5 tries passed; the listing dictionary in session["selected_item"] retained its exact id, title, and price when passed into suggest_outfit across all completed runs. |
| 4 | Fit card includes price digits, platform name, and meets length constraints | 4 of 5 | MET | 5 of 5 tries generated cards containing the numerical price ($75.0), explicit platform name (Depop), and between 2 and 4 sentences. |
| 5 | Search strictly enforces maximum price ceilings | 5 of 5 | MISSED | 0 of 5 tries passed; the scenario query returned 0 items across all 5 runs and halted early, so no returned items were available to verify against the budget limit. |

**Diagnoses**

### Criterion 5 Miss
* **Place:** A tool (`tools.py::search_listings`).
* **Mechanism:** The test scenario used the query `"tops under $20"`. In `tools.py::search_listings`, keyword matching was evaluated solely against `item["title"]` and `item["description"]`. In `data/listings.json`, matching garments priced under $20 (such as `lst_006` "Cropped Ribbed Tank" at $14.0 and `lst_017` "Mesh Long-Sleeve Top" at $15.0) have their garment type stored in the `category` field (`"category": "tops"`), while their title and description fields contain terms like "tank" or "long-sleeve". Because `search_listings` did not concatenate `item.get("category", "")` into the searchable text, `"tops"` matched zero items, returning an empty list `[]` and triggering the early-exit branch before any price check could take place.

---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->
[1] search_listings (MCP)
      in:  dict with keys: description, size, max_price
      out: 10 listings found
[2] suggest_outfit
      in:  dict with keys: item
      out: outfit suggestions generated
[3] create_fit_card
      in:  dict with keys: item
      out: Look at this absolute Depop steal I scored for just $18.0! I...

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

**What I changed:**
In `tools.py::search_listings`, updated the keyword matching logic to include the garment category (`item.get("category")`) in the searchable text string alongside `title`, `description`, and `style_tags`, ensuring safe string conversion (`str(item.get("category") or "")`) to prevent serialization errors over MCP.

**Which failure it was meant to fix:**
Criterion 5 ("Search strictly enforces maximum price ceilings"). In the baseline run, the query `"tops under $20"` returned 0 listings across all 5 tries because the search corpus only inspected `title` and `description`. Relevant items in `data/listings.json` (such as `lst_006` "Cropped Ribbed Tank" at $14.0 and `lst_017` "Mesh Long-Sleeve Top" at $15.0) have their garment type stored in the `category` field (`"category": "tops"`). Missing this field caused the search to return an empty list `[]` and trigger the early-exit branch before price ceilings could be evaluated.

### Run Log — After

- Produced by: `run_eval.py::main`
- Loop: `agent.py::run_agent` · tools: `tools.py`
- Tries per scenario: 5, caching off
- Temperature: 0.9
- When: 2026-10-12 03:02

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all three tools | 4 of 5 | PASS | FAIL | PASS | PASS | PASS | MET (4/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Session state preserves selected item integrity across tool boundaries | 4 of 5 | FAIL | PASS | PASS | PASS | FAIL | MISSED (3/5) |
| 4. Fit card includes price digits, platform name, and meets length constraints | 4 of 5 | FAIL | PASS | FAIL | PASS | FAIL | MISSED (2/5) |
| 5. Search strictly enforces maximum price ceilings | 5 of 5 | FAIL | PASS | FAIL | PASS | PASS | MISSED (3/5) |

**Did it help, and how do I know:**
Yes, specifically for the diagnosed search retrieval defect. In the `before` log, Criterion 5 produced 0 listings on all 5 tries. In the `after` log, `search_listings (MCP)` successfully retrieved 7 matching listings under $20 on all 5 tries, and every returned item strictly respected the maximum price ceiling ($14.0 to $18.0). 

However, with caching disabled across repeated runs, the second evaluation encountered upstream Gemini API rate-limiting spikes (`503 UNAVAILABLE` errors during generative tool calls). This caused Tries 1 and 3 of Criterion 5, as well as several tries in Criteria 3 and 4, to halt early during subsequent LLM styling steps. The search filtering logic itself was completely resolved.

---

## What's Still Broken

* **Criterion 3 & 4 (Model Resilience to Upstream 503 Errors):**
  * **What I'd do:** Implement an exponential backoff retry loop with jitter around `generate()` inside `generate.py`, or wrap tool-level calls so transient `503 UNAVAILABLE` errors re-attempt up to 3 times before setting an early-stop error in session state.
  * **Why I stopped here:** Unit 4 strictly limits changes to the single diagnosed tool improvement and the MCP migration.

* **Criterion 5 (End-to-End Pipeline Dependency):**
  * **What I'd do:** Separate data retrieval assertion criteria from generative completion stages so upstream LLM unavailability doesn't invalidate deterministic database filtering checks.
  * **Why I stopped here:** Modifying criteria definitions after reviewing evaluation outcomes is not permitted by the grading rubric.

* **MCP Protocol Move Reflection:**
  * **What changed in code:** `search_listings` was decoupled from direct local module imports and registered inside `mcp_server.py` using `FastMCP("fitfindr")` with a published docstring schema. In `agent.py`, the direct function call was replaced with `mcp_client.call_tool("search_listings", {...})`.
  * **Behavioral changes:** The agent preserved identical return data structures (`list[dict]`). However, tool execution now routes through inter-process communication, requiring input/output dictionaries to remain strictly JSON-serializable (avoiding `NoneType` string operations).
<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**

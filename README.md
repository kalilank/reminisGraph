# ReminisGraph

A research-style music retrieval project exploring a single question:

> **When does graph retrieval outperform vector retrieval for music discovery?**

ReminisGraph is not a music recommender app. It's a comparison framework: the same
6-artist dataset is queried through four different retrieval strategies — vector,
graph, hybrid, and an LLM explanation layer — to study *where* each one succeeds,
fails, or overlaps.

---

## Why This Project

Most music recommenders lean entirely on content similarity (genre, tags, audio
features). ReminisGraph tests whether **relational history** — who played in which
band, and when — surfaces connections that text-based similarity structurally
cannot see.

Three retrieval strategies are compared directly:

- **Vector Retrieval** — cosine similarity over artist text embeddings
  (albums + MusicBrainz tags). Captures *style/genre similarity*.
- **Graph Retrieval** — Neo4j traversal over MusicBrainz relationships
  (shared band members, shared tags). Captures *historical/relational similarity*.
- **Hybrid Retrieval** — vector similarity plus a graph-evidence bonus.

A fourth layer, **LLM Explanation**, sits on top — it explains retrieval results
in natural language. It never retrieves or ranks anything itself.

---

## Dataset

- **Source:** [MusicBrainz](https://musicbrainz.org/) — chosen for its open,
  reproducible, relationship-rich metadata.
- **Scope:** 90s alternative / grunge / rock scene.
- **Seed artists (6):** Nirvana, Pearl Jam, Soundgarden, The Smashing Pumpkins,
  Blur, Deftones.
- **Controlled scope:** one clean studio album per artist, 70 track rows total.
- **Graph size:** 177 nodes, 209 relationships across `Artist`, `Person`, `Tag`,
  `ReleaseGroup`, `Release`, and `Recording` labels.

The dataset is intentionally small. This is a controlled comparison, not a
production system — every retrieval result can be manually traced and verified
against real MusicBrainz relationships.

---

## System Architecture

```text
Raw MusicBrainz data
        │
        ▼
Processed CSVs (albums, tracks, artist text)
        │
        ├──────────────► Sentence-transformer embeddings ──► Vector Retriever
        │                  (all-MiniLM-L6-v2, cosine similarity)
        │
        └──────────────► Neo4j graph import ──► Graph Retriever
                           (MEMBER_OF, HAS_TAG relationships)
                                    │
                                    ▼
                          Hybrid Retriever
                    (vector score + graph-evidence bonus)
                                    │
                                    ▼
                       LLM Explanation Layer
                  (Groq / llama-3.3-70b-versatile,
                   explains only, never retrieves)
```

---

## Retrieval Methods

### Vector Retrieval
Artist-level text (album titles + MusicBrainz tags) is embedded with
`all-MiniLM-L6-v2`. Retrieval is plain cosine similarity — no FAISS, since the
6-artist dataset is far too small to need approximate nearest-neighbor search.
Member names and graph-only relationships are deliberately **excluded** from
the embedding text, so vector retrieval can't "cheat" by seeing the same
evidence graph retrieval is supposed to test.

### Graph Retrieval
Two Cypher-based evidence types, queried separately:
- **Shared members** — `(:Artist)<-[:MEMBER_OF]-(:Person)-[:MEMBER_OF]->(:Artist)`
- **Shared tags** — overlapping `HAS_TAG` relationships

Graph retrieval is sparse by design: 3 of 6 artists have zero shared-member
evidence. That sparsity is itself a finding, not a bug — it shows graph
retrieval only speaks when real relational evidence exists.

### Hybrid Retrieval
```text
hybrid_score = vector_score + (0.20 × shared_member_flag) + (0.10 × normalized_shared_tag_overlap)
```
Shared-member evidence gets the larger weight because it's genuinely new
information vector retrieval cannot see. Shared-tag evidence gets a smaller,
discounted weight, because tag overlap is already implicitly present in the
vector embeddings (see Key Findings below).

### LLM Explanation Layer
Structured retrieval facts (vector score, shared members, shared tags, hybrid
score) are rewritten into natural prose by `llama-3.3-70b-versatile` via the
Groq API. The system prompt enforces a strict grounding constraint: the model
may only restate facts already present in the structured input, never add new
ones. An early unconstrained test confirmed the risk was real — without the
constraint, the model added unstated details (e.g. calling Matt Cameron a
"drummer," describing bands as "iconic"). With the constraint in place, four
test cases across all major evaluation categories were rewritten without obvious 
unsupported facts in the inspected outputs.

---

## Key Findings

**1. Real cross-artist relationships exist and are invisible to text similarity.**
- Matt Cameron connects Soundgarden and Pearl Jam
- Jason Everman connects Nirvana and Soundgarden

**2. Vector similarity alone does not consistently surface these relational connections as the top result from each query direction.** The highest vector
similarity pair overall is Pearl Jam ↔ Blur (0.7609) — a style/tag match, not
a historical one.

**3. Hybrid retrieval changes the top-1 recommendation for 4 of 6 artists (66.7%).**
Of those four changes:
- **3 are driven by shared-member evidence** — genuinely new relational
  information that vector retrieval does not consistently prioritize
  (Pearl Jam→Soundgarden, Nirvana→Soundgarden, and Soundgarden→Nirvana as an ambiguous shared-member case)
- **1 is driven by shared-tag evidence** (Deftones→Soundgarden) — a case where
  graph and vector signal overlap rather than diverge

**4. Shared-tag graph evidence correlates heavily with vector similarity.**
Across all 6 artists, shared-tag top-3 results overlapped with vector top-3
results by ~78% on average (3 of 6 artists had *identical* top-3 sets). This
directly justifies discounting the tag-based bonus in the hybrid formula — it
mostly re-encodes information the vector retriever already has.

**5. Soundgarden acts as a relational hub — with an honest ambiguity.**
Soundgarden has two equally-weighted shared-member connections (Jason Everman
→ Nirvana, Matt Cameron → Pearl Jam). Vector retrieval's top pick for
Soundgarden (Pearl Jam) and hybrid's top pick (Nirvana) are *both* legitimately
graph-connected — just via different people. This is documented explicitly in
the evaluation rather than silently resolved by an arbitrary tie-break.

---

## Evaluation Summary

| Query Artist | Vector Top-1 | Graph Top-1 | Hybrid Top-1 | Changed? | Driven by |
|---|---|---|---|---|---|
| Soundgarden | Pearl Jam | Nirvana (tied w/ Pearl Jam) | Nirvana | Yes | shared-member (ambiguous case) |
| Nirvana | Pearl Jam | Soundgarden | Soundgarden | Yes | shared-member |
| Pearl Jam | Blur | Soundgarden | Soundgarden | Yes | shared-member |
| Deftones | Blur | Soundgarden | Soundgarden | Yes | shared-tag |
| The Smashing Pumpkins | Blur | Blur | Blur | No | agreement |
| Blur | Pearl Jam | Pearl Jam | Pearl Jam | No | agreement |

Full data: `data/processed/final_retrieval_comparison.csv` (regenerate via
`notebooks/16_final_retrieval_comparison.ipynb`).

---

## Repository Structure

```text
reminisGraph/
├── data/
│   ├── raw/artists/
│   └── processed/            # gitignored — regenerate by running notebooks in order
├── docs/
│   ├── data_dictionary.md
│   ├── dataset_design.md
│   ├── design_decisions.md
│   ├── learning_journal.md
│   ├── neo4j_import_plan.md
│   └── questions.md
├── notebooks/                 # numbered, run in order to reproduce all results
├── neo4j/
├── src/                       # planned refactor target (see Future Work)
├── .env                        # Neo4j + Groq credentials — never committed
├── .gitignore
└── requirements.txt
```

**Note:** `data/processed/` is intentionally gitignored. All CSVs there are
regenerated by running the numbered notebooks in sequence — they are treated
as reproducible outputs, not source data.

---

## Setup & Reproduction

```bash
git clone https://github.com/kalilank/reminisGraph.git
cd reminisGraph
python -m venv .venv
source .venv/bin/activate      # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Create a `.env` file with:
```text
NEO4J_URI=...
NEO4J_USER=...
NEO4J_PASSWORD=...
GROQ_API_KEY=...
```

Run the notebooks in `notebooks/` in numeric order — each stage's output feeds
the next.

---

## Limitations

- **Small dataset by design** — 6 artists, 1 album each. Enough to validate the
  approach; not enough to generalize.
- **Top-k truncation risk in hybrid scoring** — hybrid candidates are built by
  merging saved top-k vector and graph results rather than full pairwise
  scores. This didn't change any result in the current dataset, but could
  silently distort scores as the graph grows.
- **FAISS intentionally skipped** — plain cosine similarity is exact and
  sufficient at this scale; FAISS only pays off with far more artists.
- **Hybrid weights are manually chosen**, not learned or systematically tuned.
- **LLM output is non-deterministic** — the same structured input can be
  phrased differently across separate API calls (`temperature=0.2` reduces but
  doesn't eliminate this).
- **MusicBrainz metadata is uneven** — e.g. release `country` reflects the
  release edition, not the artist's origin.

---

## Future Work

- Expand the dataset (more artists, more albums, more relationship types)
- Revisit the Korean indie scene as a second, sparser-metadata test case
- Systematically tune hybrid scoring weights instead of hand-picking them
- Add FAISS for scalable vector search if the dataset is expanded significantly.
- Refactor stable retrieval functions from notebooks into `src/`
- Build a small demo app (Streamlit/Gradio) for interactive querying

---

## Author

kalila

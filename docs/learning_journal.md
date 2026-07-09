# Learning Journal — ReminisGraph

## 2026-07-06 — Designing a music database from scratch

**Reflection question:** If I were designing a music database from scratch, 
what entities would I create?

**My initial entity list (15):**
Artist, Album, Song, Genre, Duration, Release Date, Streams, Duet/Featured 
Artist, Producer, Listeners, BPM, License, Composer, Production

**Draft attributes:**

*Artist*
- Name
- Date of birth
- Country
- Gender

*Album*
- Release date
- Total songs
- Album duration

*Song*
- Song duration
- Release date

*Genre*
- (still unclear how this should be modeled — node or property?)

**Why I think graph fits the music domain better than relational (SQL):**

I feel like with a graph, we could dive deeper into more complex queries. 
Personally I prefer Spotify's recommendations over Apple Music's — Spotify 
often surfaces songs similar to what I've listened to before, or new songs 
that still match my taste. I used to just assume "oh, that's just ML doing 
its thing," but thinking about this more, I wonder if graph structures play 
a role too — alongside ML, not instead of it. Maybe it works by reading my 
listening history (e.g. some kind of end-to-end CDC/data ingestion pipeline 
running nightly), summarizing and processing it, so the next day's 
recommendations get a little better.

*(Note: this is a personal hypothesis at this stage, not something I've 
verified yet — good candidate to revisit once I understand hybrid 
retrieval better.)*

---

## 2026-07-07 — MusicBrainz API exploration

**What I learned:**
- `search_artist()` (query by name) vs `get_artist()` (lookup by MBID) are 
  different use cases
- `inc="artist-rels"` returns relationship data, including "member of band"
- Relationships have their own properties (begin, end, ended) — e.g. 
  Danielle left NewJeans on 2025-12-29, while other members are still active

**What confused me initially:**
- Module caching in Jupyter — edited the `.py` file but the notebook 
  didn't see the new method until I restarted the kernel
- Double-slash bug from concatenating `BASE_URL` + endpoint, causing a 404

**Insight:**
- This relationship-with-history structure (who joined/left, and when) is 
  exactly what a flat CSV can't represent — this confirms why graph 
  retrieval could matter for "who was in group X during year Y" type queries

---

## 2026-07-08, 11:18am — Cross-artist relationship discovery

**What I did:**
- Saved 6 seed artists (Nirvana, Smashing Pumpkins, Pearl Jam, Soundgarden, 
  Blur, Deftones) with artist-rels, release-groups, and tags included
- Wrote a loop to find shared "Person" relationships across all 6 artists

**What I found:**
- Matt Cameron: member of both Soundgarden and Pearl Jam
- Jason Everman: member of both Nirvana and Soundgarden
- Both connections are historically accurate (verified against known 
  band history)

**Why this matters:**
- This is a relationship that flat CSV data (artist_name, song, genre) 
  cannot represent — Soundgarden and Pearl Jam don't sound similar 
  sonically, so vector/embedding-based retrieval would likely never 
  surface this connection. Graph traversal finds it in 1-2 hops.
- With only 6 artists, this pattern is still sparse — I expect richer and 
  more surprising connections once the dataset grows (more producers, 
  labels, and collaborators overlapping across artists)

**What confused me / still learning:**
- Realized artist-to-artist relationships don't capture band-to-band 
  overlap directly — I had to specifically filter for shared "Person" 
  entities to find cross-band connections

## 2026-07-08, 15:27 — Phase 3 

I learned that MusicBrainz `country` does not necessarily mean artist origin. It describes the selected release edition. This matters because graph schema design can become misleading if I turn every column into a node without understanding its meaning.

I also clarified that the current dataset uses one clean studio album per artist, not each artist's most famous album.

---

## 2026-07-08 — Phase 4 & 4.5: Graph schema design and review

**What I did:**
- Explored MusicBrainz relationship data beyond album/track metadata.
- Designed Graph Schema v0 with two layers:
  - Catalog structure: Artist → ReleaseGroup → Release → Recording
  - Relationship-rich discovery: Person → Artist and Artist → Tag
- Reviewed which relationships should be included in v0 and which should be deferred.

**Main decision:**
I included `MEMBER_OF` and `HAS_TAG` because they directly support the project’s goal: comparing semantic similarity against graph-based relationships. I excluded relationships like tribute/named-after for now because they add noise and are less central to the first retrieval comparison.

**Insight:**
Graph design is not just “turn everything into nodes.” Each node and relationship needs a reason to exist, especially if it will later affect retrieval results.

---

## 2026-07-09 — Phase 5: Neo4j graph import

**What I did:**
- Prepared clean CSV files for Neo4j import.
- Imported the graph into Neo4j with nodes for Artist, Person, Tag, ReleaseGroup, Release, and Recording.
- Added relationships such as `CREATED`, `HAS_RELEASE`, `HAS_TRACK`, `MEMBER_OF`, and `HAS_TAG`.
- Ran sanity checks for node counts, relationship counts, duplicate IDs, and missing references.

**What I learned:**
Neo4j makes the relationship structure visible in a way that a table does not. Seeing paths like:

Pearl Jam <- MEMBER_OF - Matt Cameron - MEMBER_OF → Soundgarden

---

## 2026-07-09 — Phase 6: Embeddings and vector similarity baseline

**What I did:**

- Created clean artist-level embedding text using album titles and MusicBrainz tags.
- Excluded member names and membership relationships to avoid relational leakage.
- Generated embeddings using all-MiniLM-L6-v2.
- Calculated cosine similarity between artists and saved top-k vector results.

**Main decision:**
The vector baseline should not include graph-only information like shared members. Otherwise, vector retrieval might “cheat” by learning the same relationship signal that graph retrieval is supposed to test.

**Initial result:**
The highest vector similarity pair was Pearl Jam and Blur with a cosine similarity score of 0.760920. Pearl Jam was slightly more similar to Blur than to Soundgarden in the vector baseline, even though Pearl Jam and Soundgarden have stronger graph-relevant evidence through shared membership.

**Insight:**
Vector retrieval seems to capture tag/style similarity, while graph retrieval is expected to better capture relational and historical connections. This supports the core comparison of the project: vector and graph retrieval may be useful for different kinds of music discovery questions.
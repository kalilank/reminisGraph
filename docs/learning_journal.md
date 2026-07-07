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
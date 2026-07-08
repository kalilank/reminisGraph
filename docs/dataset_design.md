## Initial Graph Schema Candidate from Phase 3 EDA

Based on the initial album_tracks.csv EDA, each row represents one recording/track inside one selected release of one release group by one artist.

Candidate nodes:
- Artist
- ReleaseGroup / Album
- Release
- Recording / Track

Candidate relationships:
- Artist -> ReleaseGroup
- ReleaseGroup -> Release
- Release -> Recording

Candidate properties:
- release_date
- country
- medium_format
- track_position
- length_ms / length_min

Notes:
- `country` and `medium_format` describe the selected MusicBrainz release edition, not artist origin.
- `track_position` is sequential for all selected albums, so it can be modeled as a property of the `HAS_TRACK` relationship.

## Phase 4 Preparation

The current EDA suggests a basic hierarchical schema:

Artist → ReleaseGroup/Album → Release → Recording

Before finalizing the graph schema, open design questions are tracked in `docs/questions.md`.


## Member Relationship Findings

After deduplicating `member of band` relationships, the dataset contains 52 clean member relationships across the 6 seed artists.

This supports modeling band membership as:

(:Person)-[:MEMBER_OF {begin, end, roles}]->(:Artist)

The `begin`, `end`, and `roles` fields are important because they preserve temporal and role-based context. For example, Matt Cameron appears in both Soundgarden and Pearl Jam, while Jason Everman appears in both Nirvana and Soundgarden.

However, the data has limitations:
- Some memberships have missing begin/end dates, such as Blur members.
- Some memberships have empty roles, such as Jason Everman in Soundgarden.
- Missing `end` values should be treated as unknown/open-ended, not automatically as currently active.

## Graph Schema v0

This is the first draft of the ReminisGraph knowledge graph schema based on Phase 3 EDA and Phase 4A relationship inventory.

Goal:
Design the first version of the Knowledge Graph structure before implementing it in Neo4j.

The schema has two layers:
1. Catalog structure from `album_tracks.csv`
2. Relationship-rich discovery structure from raw MusicBrainz artist JSON

### Layer 1: Catalog Structure

Nodes:
- Artist
- ReleaseGroup
- Release
- Recording

Relationships:
- `(:Artist)-[:CREATED]->(:ReleaseGroup)`
- `(:ReleaseGroup)-[:HAS_RELEASE]->(:Release)`
- `(:Release)-[:HAS_TRACK {position}]->(:Recording)`

### Layer 2: Relationship-Rich Discovery Structure

Nodes:
- Person
- Tag

Relationships:
- `(:Person)-[:MEMBER_OF {begin, end, roles}]->(:Artist)`
- `(:Artist)-[:HAS_TAG {count}]->(:Tag)`

### Properties

Artist:
- artist_id
- name

ReleaseGroup:
- release_group_id
- title

Release:
- release_id
- title
- release_date
- country
- medium_format

Recording:
- recording_id
- title
- length_ms
- length_min

Person:
- person_id
- name

Tag:
- name

Relationship properties:
- `HAS_TRACK`: position
- `MEMBER_OF`: begin, end, roles
- `HAS_TAG`: count

Notes:
- `person_id` comes from the MusicBrainz artist ID, because MusicBrainz represents people as artist entities.
- `HAS_TAG.count` comes from the MusicBrainz tag count for each artist-tag pair, not from the `tag_summary.artist_count`.

### Design Decisions

- `member of band` is included because it creates strong cross-artist connections.
- Tags are included because they show genre/style overlap across artists.
- `country` and `medium_format` stay as `Release` properties because they describe release editions, not artist origin.
- `track_position` is modeled as a property of `HAS_TRACK`, not as a separate node.

### Deferred / Excluded Relationships for v0

Excluded:
- `tribute`
- `named after artist`

Deferred:
- `instrumental supporting musician`
- `vocal supporting musician`
- `artist rename`

### Known Limitations

- Some membership dates are missing.
- Some roles are empty.
- Missing `end` values should be treated as unknown/open-ended, not automatically as currently active.
- Tag data is useful but noisy because some tags describe genre/style, while others describe country, language, or miscellaneous labels.
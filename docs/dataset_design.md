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
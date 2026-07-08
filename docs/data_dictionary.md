## Album Track Fields

| Field | Meaning | Keep? | Reason |
|---|---|---|---|
| artist_id | MusicBrainz artist ID | Yes | Connects track to artist |
| artist_name | Artist name | Yes | Display/debugging |
| release_group_id | Album concept ID | Yes | Connects track to album concept |
| release_group_title | Album title | Yes | Display |
| release_id | Specific release edition ID | Yes | Tracks come from a specific release |
| release_title | Release title | Yes | Display |
| release_date | Date of this release edition | Yes | Temporal info |
| country | Release country | Yes | Useful metadata |
| medium_format | CD/digital/vinyl/etc. | Yes | Explains edition source |
| track_position | Track order | Yes | Tracklist structure |
| track_title | Track title | Yes | Display/search |
| recording_id | MusicBrainz recording ID | Yes | Primary key for Recording node |
| length_ms | Track duration | Yes | Metadata |
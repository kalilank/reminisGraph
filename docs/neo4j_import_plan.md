# Neo4j Import Plan

## Goal

Prepare clean node and relationship tables before importing data into Neo4j.

## Node Tables

### artists.csv
Source: `album_tracks.csv`

Columns:
- artist_id
- name

Neo4j node:
`(:Artist {artist_id, name})`

---

### release_groups.csv
Source: `album_tracks.csv`

Columns:
- release_group_id
- title

Neo4j node:
`(:ReleaseGroup {release_group_id, title})`

---

### releases.csv
Source: `album_tracks.csv`

Columns:
- release_id
- title
- release_date
- country
- medium_format

Neo4j node:
`(:Release {release_id, title, release_date, country, medium_format})`

---

### recordings.csv
Source: `album_tracks.csv`

Columns:
- recording_id
- title
- length_ms
- length_min

Neo4j node:
`(:Recording {recording_id, title, length_ms, length_min})`

---

### persons.csv
Source: raw MusicBrainz artist JSON relationships

Columns:
- person_id
- name

Neo4j node:
`(:Person {person_id, name})`

---

### tags.csv
Source: raw MusicBrainz artist JSON tags

Columns:
- name

Neo4j node:
`(:Tag {name})`

## Relationship Tables

### created.csv

Relationship:
`(:Artist)-[:CREATED]->(:ReleaseGroup)`

Columns:
- artist_id
- release_group_id

---

### has_release.csv

Relationship:
`(:ReleaseGroup)-[:HAS_RELEASE]->(:Release)`

Columns:
- release_group_id
- release_id

---

### has_track.csv

Relationship:
`(:Release)-[:HAS_TRACK {position}]->(:Recording)`

Columns:
- release_id
- recording_id
- position

---

### member_of.csv

Relationship:
`(:Person)-[:MEMBER_OF {begin, end, roles}]->(:Artist)`

Columns:
- person_id
- artist_id
- begin
- end
- roles

---

### has_tag.csv

Relationship:
`(:Artist)-[:HAS_TAG {count}]->(:Tag)`

Columns:
- artist_id
- tag
- count

## Import Principle

Use stable MusicBrainz IDs as primary identifiers whenever possible.

Do not use names as primary keys except for tags, because artist/person names may not be unique.
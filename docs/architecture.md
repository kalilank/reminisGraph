# Architecture — ReminisGraph

## Current Pipeline

MusicBrainz API
→ Raw artist JSON
→ Preprocessing
→ album_tracks.csv
→ Phase 3 EDA
→ Graph schema design

## Planned Architecture

MusicBrainz API
→ Data ingestion
→ Preprocessing
→ Knowledge Graph dataset
→ Neo4j graph retrieval

MusicBrainz/API text metadata
→ Embedding generation
→ FAISS vector retrieval

Graph retrieval + Vector retrieval
→ Hybrid retrieval
→ LLM explanation layer

## Notes

The LLM layer is only used to generate explanations, not to perform retrieval.
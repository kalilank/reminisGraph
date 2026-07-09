## Why rock/alternative as primary domain (not Korean indie)

Explored Korean indie scene (Hyukoh) as potential focus, motivated by 
personal interest. Found significant tag/relationship sparsity compared 
to Western rock artists (Hyukoh: 1 tag vs Blur: 16 tags, both similarly 
"established" artists). 

Decided to prioritize data-rich domain (rock/alternative) for the core 
6-week project to avoid confounding the retrieval comparison with data 
sparsity issues. Korean indie / cross-scene bias analysis noted as 
potential future work extension (Option B).

## Why one clean album per artist for the initial dataset

The current dataset uses one clean studio album per seed artist to validate the ingestion pipeline and graph schema design before scaling.

This does not mean the selected albums are each artist's most famous or "best" album. The priority is clean, reproducible MusicBrainz metadata.

## Why Neo4j for Graph Retrieval

## What problem does Neo4j solve?

Neo4j is a graph database used to store data as nodes and relationships. It helps represent connected data such as artists, albums, people, memberships, and tags.

## Why Neo4j over alternatives?

Neo4j is widely used for property graphs and supports Cypher, a query language designed for graph traversal. It is a good fit for testing whether graph traversal can surface music relationships that vector retrieval may miss.

## Input / Output

Input:
- Cleaned CSV files or DataFrames representing nodes and relationships.

Output:
- A queryable knowledge graph with nodes such as Artist, ReleaseGroup, Release, Recording, Person, and Tag.
- Relationships such as CREATED, HAS_RELEASE, HAS_TRACK, MEMBER_OF, and HAS_TAG.

## Limitations

- Requires careful schema/import design before loading data.
- Duplicate nodes/relationships can happen if IDs are not handled properly.
- Graph quality depends on MusicBrainz metadata quality.
- Neo4j is not replacing vector retrieval; it only handles the graph retrieval side of the comparison.

## Embedding Text Design for Vector Retrieval

For the default vector retrieval baseline, embedding text should not include graph-only relationship information such as band members, shared people, or membership history.

This prevents relational leakage. For example, if Matt Cameron appears in both Soundgarden and Pearl Jam embedding texts, vector retrieval may connect those artists through shared text rather than semantic/music similarity.

Default v0 embedding text will include:
- album / release group title
- tags / genre-style metadata

Default v0 embedding text will exclude:
- member names
- person relationships
- MEMBER_OF relationships
- graph traversal facts

A later evaluation phase may compare this clean baseline against a "leaky" embedding variant that includes member names as an ablation experiment.

## Why all-MiniLM-L6-v2 for Embeddings

For the first vector retrieval baseline, this project uses `all-MiniLM-L6-v2` from sentence-transformers.

This model is chosen because it is lightweight, fast, and practical for prototyping on a small artist-level dataset. It produces 384-dimensional embeddings, which are sufficient for an initial semantic similarity baseline.

This does not mean it is the best possible embedding model. Larger or more domain-specific models may be evaluated later, but `all-MiniLM-L6-v2` is appropriate for validating the embedding pipeline first.

This choice is documented here so that later comparisons between vector and graph retrieval can be traced back to a specific, reproducible embedding setup.
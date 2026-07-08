def release_to_track_rows(release_detail, artist_id, artist_name, release_group_id, release_group_title):
    rows = []

    for medium in release_detail.get("media", []):
        medium_format = medium.get("format")

        for track in medium.get("tracks", []):
            recording = track.get("recording", {})

            rows.append({
                "artist_id": artist_id,
                "artist_name": artist_name,
                "release_group_id": release_group_id,
                "release_group_title": release_group_title,
                "release_id": release_detail.get("id"),
                "release_title": release_detail.get("title"),
                "release_date": release_detail.get("date"),
                "country": release_detail.get("country"),
                "medium_format": medium_format,
                "track_position": track.get("position"),
                "track_title": track.get("title"),
                "recording_id": recording.get("id"),
                "length_ms": track.get("length"),
            })

    return rows

def pick_best_release(releases_response):
    releases = releases_response.get("releases", [])
    if not releases:
        return None

    official = [r for r in releases if r.get("status") == "Official"]
    candidates = official if official else releases

    single_disc = [r for r in candidates if len(r.get("media", [])) <= 1]
    candidates = single_disc if single_disc else candidates

    candidates.sort(key=lambda r: r.get("date") or "9999")

    return candidates[0]
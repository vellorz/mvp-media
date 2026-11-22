#!/usr/bin/env python3
"""Schedule a YouTube Short through the YouTube Data API v3 (no browser).

Uploads the file as PRIVATE with status.publishAt, so YouTube makes it public at that time.
Needs three environment variables (set by the owner in the cloud environment, never in files):
  YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN   (scope: https://www.googleapis.com/auth/youtube.upload)
Standard library only. Quota: videos.insert has its own bucket, 100 uploads a day.

  python3 yt_upload.py --file short.mp4 --title "..." --description-file desc.txt \
      --tags "a,b,c" --publish-at 2026-11-26T16:00:00-06:00 [--category 27] [--dry-run]

Gate 2 applies: run this only for a video the owner has approved.
Prints one JSON line: {"id": ..., "url": ..., "publishAt": ..., "privacyStatus": ...}
"""
import argparse, datetime, json, os, ssl, sys, urllib.error, urllib.parse, urllib.request

TOKEN_URL = "https://oauth2.googleapis.com/token"
UPLOAD_URL = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"
CHUNK = 8 * 1024 * 1024


def ctx():
    c = ssl.create_default_context()
    for p in (os.environ.get("SSL_CERT_FILE"), "/root/.ccr/ca-bundle.crt"):
        if p and os.path.exists(p):
            c.load_verify_locations(p)
    return c


def call(req):
    try:
        return urllib.request.urlopen(req, context=ctx(), timeout=300)
    except urllib.error.HTTPError as e:
        if e.code == 308:  # resumable upload: chunk accepted, more to send
            return e
        sys.exit("HTTP %s from %s: %s" % (e.code, req.full_url.split("?")[0], e.read().decode("utf-8", "replace")[:800]))


def access_token():
    miss = [k for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN") if not os.environ.get(k)]
    if miss:
        sys.exit("Missing environment variables: " + ", ".join(miss) + " (see tools/youtube/README.md)")
    body = urllib.parse.urlencode({
        "client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    return json.load(call(urllib.request.Request(TOKEN_URL, data=body)))["access_token"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--description", default="")
    ap.add_argument("--description-file")
    ap.add_argument("--tags", default="")
    ap.add_argument("--category", default="27")  # 27 Education, 19 Travel & Events
    ap.add_argument("--publish-at", help="ISO 8601 with UTC offset, in the future")
    ap.add_argument("--private-only", action="store_true",
                    help="test mode: upload as private with NO publish time, so it never goes public")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if bool(a.publish_at) == bool(a.private_only):
        sys.exit("Give exactly one of --publish-at or --private-only")
    when = None
    if a.publish_at:
        when = datetime.datetime.fromisoformat(a.publish_at)
        if when.tzinfo is None:
            sys.exit("--publish-at needs a UTC offset, e.g. 2026-11-26T16:00:00-06:00")
        if when <= datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=10):
            sys.exit("--publish-at must be at least 10 minutes in the future (a past time publishes at once)")
    if len(a.title) > 100:
        sys.exit("Title is over 100 characters")
    desc = open(a.description_file, encoding="utf-8").read() if a.description_file else a.description
    size = os.path.getsize(a.file)
    meta = {
        "snippet": {"title": a.title, "description": desc, "categoryId": a.category,
                    "tags": [t.strip() for t in a.tags.split(",") if t.strip()]},
        "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False},
    }
    if when:
        meta["status"]["publishAt"] = when.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    if a.dry_run:
        print(json.dumps({"dry_run": True, "bytes": size, "metadata": meta}, ensure_ascii=False))
        return
    tok = access_token()
    start = call(urllib.request.Request(UPLOAD_URL, data=json.dumps(meta).encode(), headers={
        "Authorization": "Bearer " + tok, "Content-Type": "application/json; charset=UTF-8",
        "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)}))
    session = start.headers["Location"]
    sent, resp = 0, None
    with open(a.file, "rb") as f:
        while sent < size:
            chunk = f.read(CHUNK)
            resp = call(urllib.request.Request(session, data=chunk, method="PUT", headers={
                "Content-Length": str(len(chunk)),
                "Content-Range": "bytes %d-%d/%d" % (sent, sent + len(chunk) - 1, size)}))
            sent += len(chunk)
    v = json.load(resp)
    print(json.dumps({"id": v["id"], "url": "https://www.youtube.com/shorts/" + v["id"],
                      "publishAt": v["status"].get("publishAt"), "privacyStatus": v["status"]["privacyStatus"]}))


if __name__ == "__main__":
    main()

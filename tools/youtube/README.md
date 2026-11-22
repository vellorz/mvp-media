# YouTube scheduling without a browser

`yt_upload.py` uploads a Short as private with `publishAt`, so YouTube publishes it at the set time.
Facts checked 2026-11-22 against Google's docs: uploads have their own quota of 100 a day; since
2026-11-02 uploads from unverified API projects are no longer locked private.

## Order of routes (owner rule, Nov 22 2026)
1. Metricool until 17 of its 20 monthly posts are used.
2. This script (YouTube Data API).
3. Zapier "Upload Video" (publish_at input) if the API fails.
4. YouTube Studio in the browser, last resort.
Gate 2 always comes first: only approved videos are uploaded.

## One-time setup (owner, about 10 minutes)
1. console.cloud.google.com: create a project, enable "YouTube Data API v3".
2. OAuth consent screen: External, add your own Google account as a test user, then press
   "Publish app" (In production) so the token does not expire after 7 days.
3. Credentials: create an OAuth client ID, type "Web application", with the redirect URI
   https://developers.google.com/oauthplayground
4. developers.google.com/oauthplayground: gear icon, tick "Use your own OAuth credentials", enter the
   client ID and secret, authorize the scope https://www.googleapis.com/auth/youtube.upload with the
   channel's Google account, then "Exchange authorization code for tokens". Copy the refresh token.
5. In the project's cloud environment settings add three environment variables:
   YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN. Never paste them into a chat or a file.

## Use
    python3 tools/youtube/yt_upload.py --file short.mp4 --title "Title #shorts" \
        --description-file desc.txt --tags "tag one,tag two" --publish-at 2026-11-26T16:00:00-06:00
Add `--dry-run` to print the request without uploading. Record the returned id in schedule.md.

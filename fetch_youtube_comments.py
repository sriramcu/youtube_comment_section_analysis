import argparse
import datetime
import os
from urllib.parse import urlparse, parse_qs

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")


def fetch_youtube_comments(video_id, max_comments=None, max_replies=None):
    youtube = build("youtube", "v3", developerKey=API_KEY)

    comments = []
    next_page_token = None

    num_api_calls = 0
    while True:
        response = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token
        ).execute()
        num_api_calls += 1
        for item in response['items']:
            top_comment = item['snippet']['topLevelComment']['snippet']
            comment_text = top_comment['textDisplay']
            like_count = top_comment['likeCount']
            comments.append(f"[{like_count}] {comment_text.strip()}")

            if 'replies' in item and item['replies']['comments']:
                reply_list = item['replies']['comments'][:max_replies]
                for reply in reply_list:
                    reply_text = reply['snippet']['textDisplay']
                    reply_like_count = reply['snippet']['likeCount']
                    comments.append(f"    [{reply_like_count}] {reply_text.strip()}")

        next_page_token = response.get("nextPageToken")
        if not next_page_token or (max_comments and len(comments) >= max_comments):
            print(f"Comments fetched. Number of API calls: {num_api_calls}")
            break

    return comments


def save_comments_to_file(comments, file_path, url):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(url + "\n\n")
        for comment in comments:
            file.write(comment + "\n")


def get_video_id_from_url(url):
    parsed_url = urlparse(url)
    video_id = parse_qs(parsed_url.query).get('v')
    if video_id:
        return video_id[0]
    else:
        raise ValueError("Invalid YouTube URL")


def store_youtube_comments_into_file(url, file_path, max_comments, max_replies):
    video_id = get_video_id_from_url(url)
    comments = fetch_youtube_comments(video_id, max_comments=max_comments, max_replies=max_replies)
    save_comments_to_file(comments, file_path, url)


def main():
    parser = argparse.ArgumentParser(description="Fetch YouTube video comments and save to a text file.")
    parser.add_argument('-u', '--url', type=str, help="YouTube video URL", required=True)
    parser.add_argument('--file_path', type=str, help="Path to the output text file",
                        default=f"fetched_comments/comments_{int(datetime.datetime.now().timestamp())}.txt")
    parser.add_argument('--max_comments', type=int, default=None, help="Maximum number of comments to fetch")
    parser.add_argument('--max_replies', type=int, default=None, help="Maximum number of replies per comment to fetch")
    args = parser.parse_args()
    store_youtube_comments_into_file(args.url, args.file_path, args.max_comments, args.max_replies)


if __name__ == "__main__":
    main()

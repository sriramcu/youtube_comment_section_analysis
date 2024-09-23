import argparse
import os

import google.generativeai as genai
from dotenv import load_dotenv
from tiktoken import encoding_for_model  # To count tokens

from fetch_youtube_comments import fetch_youtube_comments, get_video_id_from_url

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def fetch_and_split_comments(video_id, chunk_size=5000):
    comments = fetch_youtube_comments(video_id)
    chunks = []
    current_chunk = []
    token_count = 0
    tokenizer = encoding_for_model("gpt-3.5-turbo")

    for comment in comments:
        comment_token_count = len(tokenizer.encode(comment))
        if token_count + comment_token_count <= chunk_size:
            current_chunk.append(comment)
            token_count += comment_token_count
        else:
            chunks.append(current_chunk)
            current_chunk = [comment]
            token_count = comment_token_count

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def call_gemini_api(prompt, system_message):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_message)
    response = model.generate_content(prompt)
    return response.text


def analyze_youtube_comments(video_url: str, prompt: str, mode: str):
    video_id = get_video_id_from_url(video_url)
    chunks = fetch_and_split_comments(video_id)
    results = []

    for i, chunk in enumerate(chunks):
        system_message = "Analyze YouTube comments. Give more weightage to comments having more likes or replies. Format: likes in [ ] and indent replies. Each response should contain no more than 200 words- the less words the better."
        chunk_text = "\n".join(chunk)
        result = call_gemini_api(chunk_text + "\n\n" + prompt, system_message)
        results.append(result)

    if mode == "summarize":
        system_message = "Youtube comments have been split into chunks. The prompt contains one or more responses already generated by GeminiAI on each chunk individually. You must now consolidate the multiple model responses in the prompt into a single, unifying response."
        final_prompt = "Summarize the following model responses:\n\n" + "\n\n".join(results)
        final_output = call_gemini_api(final_prompt, system_message)
    else:
        # Output multiple results as a single string in an ordered list
        final_output = ""
        for i, result in enumerate(results):
            final_output += f"Response From Comment chunk number {i}:\n{result}\n\n"
    return final_output


def main():
    parser = argparse.ArgumentParser(description="Analyze YouTube video comments.")
    parser.add_argument('-u', '--url', type=str, help="YouTube video URL", required=True)
    parser.add_argument('-p', '--prompt', type=str, help="Prompt to use for analysis", required=True)
    parser.add_argument('-m', '--mode', type=str, choices=["summarize", "multiple"], help="Mode of analysis",
                        default="multiple")
    args = parser.parse_args()
    output = analyze_youtube_comments(args.url, args.prompt, args.mode)
    print(output)


if __name__ == "__main__":
    main()
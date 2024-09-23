# YouTube Comments Analyzer

Have you ever watched a YouTube video and wanted to know what song was playing in the 
background? Well, you may have written a comment under that video asking for the name 
of the song, only to later encounter a reply by a wisecrack- "Darude Sandstorm". You 
then pull out your phone and try to Shazam it. But due to the other sounds in the 
video, it cannot be identified. You then try singing it yourself into Shazam, to the 
amusement of people nearby. You desperately scroll the comment section for hours, to 
no avail. Wouldn't it be nice if a program could search the comments for you? 

Or perhaps, you came across an interesting recipe or renovation tutorial. You want to 
gauge the community's sentiment towards the video. YouTube dislikes have now been 
abolished. Here's where sentiment analysis could help. 

Many other use cases could be handled. In fact, this program supports a custom prompts 
for any other scenario you could think of, using Gemini 1.5 Flash API which is 
**[absolutely free to a large extent](https://ai.google.dev/pricing)**.


## Introduction

This program analyzes YouTube comments using the Gemini AI model. It fetches comments 
from a YouTube video, splits them into chunks due to Gemini AI's input token limit, and 
generates multiple responses based on the comments, one response for each chunk. 
Alternatively, a summary of Gemini AI's chunk-wise responses can be generated.

This project supports three features: 
1. Fetch comments into a timestamped text file, so you can search the comments in a 
   text file using any text editor using the time-tested Ctrl+F feature. No AI 
   involved here.
2. Fetch comments and analyse them via Gemini AI by using the command line interface.
3. Feature #2, by using a basic GUI created with Tkinter.

## Setup
1. Clone this repo and install the required libraries: `pip install -r requirements.txt`
2. Follow the Google Quickstart guides to generate your own 
[Gemini API Key](https://ai.google.dev/gemini-api/docs/quickstart?lang=python) and
[Youtube API Key](https://developers.google.com/youtube/v3/getting-started#before-you-begin)
3. Create a .env file in the root directory of the project with your API keys:

   YOUTUBE_API_KEY=your-api-key  
   GEMINI_API_KEY=your-api-key

## Usage

### 1. Fetch comments into a text file

`python fetch_youtube_comments.py -u https://www.youtube.com/watch?v=eh3HUsIm6VY`

By default, the text file generated would have a timestamp in it to prevent overwriting.
Use the following command to generate a text file with a custom filepath.

`python fetch_youtube_comments.py -u https://www.youtube.com/watch?v=eh3HUsIm6VY -f 
fetched_comments/output_custom.txt`

![Fetch Comments txt file.png](output_images%2FFetch%20Comments%20txt%20file.png)

Above image shows the content of the text file generated. Number of likes in square 
brackets, replies are indented.

### 2. Fetch and analyze comments via the CLI 
`python analyze_youtube_comments.py -u https://www.youtube.com/watch?v=eh3HUsIm6VY -p  
"Summarize the comment section" -m "summarize"`

The program will generate a summary or multiple Gemini AI responses to the prompt (-p)
based on the comments.

#### Modes:

&nbsp;&nbsp;&nbsp;&nbsp; i) Multiple Responses: Generates multiple responses based on 
the comments, one for each chunk of comments (-m "multiple") 

&nbsp;&nbsp;&nbsp;&nbsp; ii) Summarize: Generates a single summary response, combining 
the multiple responses as explained in the introduction (-m "summarize").

![CLI Comment Analysis.png](output_images%2FCLI%20Comment%20Analysis.png)

### 3. Fetch and analyze comments via the GUI

All inputs will be made via the GUI, the modes work in the same way as the CLI.

`python analyze_youtube_comments_gui.py`

![GUI Multi Response.png](output_images%2FGUI%20Multi%20Response.png)

Chunk-wise multi response.

![GUI Combined Response.png](output_images%2FGUI%20Combined%20Response.png)

Combination/summary of chunk-wise responses by the model.

## Contributing
Contributions are welcome! If you have any ideas, bug fixes, GUI enhancements or 
anything else, please feel free to open an issue or submit a pull request.
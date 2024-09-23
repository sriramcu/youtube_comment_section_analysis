import tkinter as tk
from tkinter import scrolledtext

from analyze_youtube_comments import analyze_youtube_comments


class CommentAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Comment Analyzer")
        width = int(root.winfo_screenwidth() / 1.4)
        height = int(root.winfo_screenheight() / 1.4)
        self.root.geometry(f'{width}x{height}')
        # Create fields
        self.link_label = tk.Label(root, text="YouTube Video Link:")
        self.link_label.pack()

        self.link_entry = tk.Entry(root, width=50)
        self.link_entry.pack()

        self.prompt_label = tk.Label(root, text="Prompt for Gemini API:")
        self.prompt_label.pack()

        self.prompt_entry = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=5)
        self.prompt_entry.pack()

        self.summarize_button = tk.Button(root, text="Summarize All Responses", command=self.summarize_comments)
        self.summarize_button.pack(side=tk.LEFT, padx=20)

        self.multi_button = tk.Button(root, text="List Multiple Responses", command=self.multi_response_comments)
        self.multi_button.pack(side=tk.RIGHT, padx=20)

        # Output Label
        self.output_label = tk.Label(root, text="", wraplength=500, justify=tk.LEFT)
        self.output_label.pack()

    def summarize_comments(self):
        self.process_comments(mode="summarize")

    def multi_response_comments(self):
        self.process_comments(mode="multiple")

    def process_comments(self, mode):
        video_url = self.link_entry.get()
        prompt = self.prompt_entry.get("1.0", tk.END).strip()

        if not video_url or not prompt:
            self.output_label.config(text="Please provide both a YouTube video link and a prompt.")
            return

        try:
            output_text = analyze_youtube_comments(video_url, prompt, mode)
        except Exception as e:
            output_text = str(e)

        self.output_label.config(text=output_text)
        self.root.clipboard_append(output_text)
        print(output_text)


def main():
    # Initialize and run the GUI
    root = tk.Tk()
    CommentAnalyzerApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()

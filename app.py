import tkinter as tk
from tkinter import scrolledtext
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import requests
from bs4 import BeautifulSoup
from readability import Document
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download necessary NLTK data
nltk.download("punkt")
nltk.download("vader_lexicon")

# Initialize the VADER SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

class ArticleAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Article Insight Analyzer")
        self.root.geometry("1000x800")
        
        # Apply modern theme
        self.style = ttk.Style(theme="minty")
        
        self.create_widgets()
        self.create_menu()
        
    def create_menu(self):
        menubar = ttk.Menu(self.root)
        
        # File menu
        file_menu = ttk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Help menu
        help_menu = ttk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def show_about(self):
        about_window = ttk.Toplevel(self.root)
        about_window.title("About")
        about_window.geometry("400x200")
        
        ttk.Label(about_window, 
                text="Article Insight Analyzer\n\nVersion 1.0\n\nA modern GUI for article summarization\nand sentiment analysis",
                justify=CENTER).pack(pady=20)
        
        ttk.Button(about_window, text="Close", command=about_window.destroy).pack(pady=10)
    
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding=(20, 10))
        main_frame.pack(fill=BOTH, expand=YES)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=X, pady=(0, 15))
        
        ttk.Label(
            header_frame, 
            text="Article Insight Analyzer", 
            font=('Helvetica', 16, 'bold'),
            bootstyle=PRIMARY
        ).pack(side=LEFT)
        
        # URL Entry Frame
        url_frame = ttk.Labelframe(
            main_frame, 
            text=" Article URL ", 
            padding=(15, 10),
            bootstyle=INFO
        )
        url_frame.pack(fill=X, pady=5)
        
        self.url_entry = ttk.Entry(
            url_frame, 
            width=70,
            bootstyle=INFO
        )
        self.url_entry.pack(side=LEFT, padx=5, expand=True, fill=X)
        
        # Analyze Button
        self.analyze_btn = ttk.Button(
            url_frame, 
            text="Analyze Article", 
            command=self.analyze_article,
            bootstyle=SUCCESS,
            width=15
        )
        self.analyze_btn.pack(side=RIGHT)
        
        # Results Container
        results_frame = ttk.Frame(main_frame)
        results_frame.pack(fill=BOTH, expand=YES, pady=(10, 0))
        
        # Article Title
        self.title_frame = ttk.Frame(results_frame)
        self.title_frame.pack(fill=X, pady=(0, 10))
        
        self.title_label = ttk.Label(
            self.title_frame, 
            text="", 
            font=('Helvetica', 12, 'bold'),
            bootstyle=PRIMARY
        )
        self.title_label.pack(side=LEFT)
        
        # Sentiment Display (Right side of title)
        self.sentiment_display = ttk.Frame(self.title_frame)
        self.sentiment_display.pack(side=RIGHT, padx=10)
        
        # Main content area
        content_frame = ttk.Frame(results_frame)
        content_frame.pack(fill=BOTH, expand=YES)
        
        # Summary Section
        summary_label = ttk.Label(
            content_frame, 
            text="Article Summary", 
            font=('Helvetica', 12, 'bold'),
            bootstyle=PRIMARY
        )
        summary_label.pack(anchor=W, pady=(0, 5))
        
        self.summary_text = scrolledtext.ScrolledText(
            content_frame, 
            wrap=tk.WORD, 
            height=12,
            font=('Segoe UI', 10),
            padx=10,
            pady=10
        )
        self.summary_text.pack(fill=BOTH, expand=YES)
        
        # Sentiment Analysis Section
        sentiment_label = ttk.Label(
            content_frame, 
            text="Sentiment Analysis", 
            font=('Helvetica', 12, 'bold'),
            bootstyle=PRIMARY
        )
        sentiment_label.pack(anchor=W, pady=(10, 5))
        
        # Sentiment results container
        sentiment_container = ttk.Frame(content_frame)
        sentiment_container.pack(fill=BOTH, expand=YES)
        
        # Left side - Sentiment face
        self.sentiment_face_frame = ttk.Frame(sentiment_container)
        self.sentiment_face_frame.pack(side=LEFT, padx=10)
        
        # Right side - Details
        self.sentiment_details = scrolledtext.ScrolledText(
            sentiment_container, 
            wrap=tk.WORD, 
            height=8,
            font=('Segoe UI', 10),
            padx=10,
            pady=10
        )
        self.sentiment_details.pack(side=RIGHT, fill=BOTH, expand=YES)
        
        # Status Bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(
            main_frame, 
            textvariable=self.status_var, 
            relief=SUNKEN,
            anchor=W,
            bootstyle=(INFO, INVERSE)
        )
        self.status_bar.pack(fill=X, pady=(10, 0))
        
        # Set initial URL for testing
        self.url_entry.insert(0, "https://www.nytimes.com/2025/04/29/us/politics/trump-crypto-world-liberty-financial.html")
    
    def summarize_text(self, text, sentence_count=3):
        try:
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            summarizer = LsaSummarizer()
            summary = summarizer(parser.document, sentence_count)
            return " ".join(str(sentence) for sentence in summary)
        except Exception as e:
            print(f"Summarization failed: {e}")
            return text[:500]  # Return the first 500 characters as a fallback
    
    def analyze_sentiment(self, text):
        sentiment = sia.polarity_scores(text)
        # Sentiment Score Analysis
        if sentiment['compound'] >= 0.05:
            return 'Positive', sentiment
        elif sentiment['compound'] <= -0.05:
            return 'Negative', sentiment
        else:
            return 'Neutral', sentiment
    
    def update_sentiment_face(self, sentiment):
        # Clear previous widgets
        for widget in self.sentiment_face_frame.winfo_children():
            widget.destroy()
        
        # Create emoji label with appropriate color
        if sentiment == 'Positive':
            emoji_text = "😊"
            color = 'success'
        elif sentiment == 'Negative':
            emoji_text = "😠"
            color = 'danger'
        else:
            emoji_text = "😐"
            color = 'warning'
        
        # Create emoji label
        ttk.Label(
            self.sentiment_face_frame,
            text=emoji_text,
            font=('Segoe UI Emoji', 24),
            bootstyle=color
        ).pack()
        
        # Create sentiment label
        ttk.Label(
            self.sentiment_face_frame,
            text=sentiment,
            font=('Helvetica', 14, 'bold'),
            bootstyle=color
        ).pack(pady=5)
    
    def analyze_article(self):
        url = self.url_entry.get().strip()
        if not url:
            self.show_error("Please enter a URL")
            return
        
        self.status_var.set("Fetching article...")
        self.root.update()
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise error if request fails
            doc = Document(response.text)
            
            # Extract article title and body using readability-lxml
            title = doc.short_title()
            html = doc.summary()
            
            # Clean article body
            body = BeautifulSoup(html, 'html.parser').get_text()
            
            # Update UI with title
            self.title_label.config(text=f"Title: {title}")
            
            # Summarize the article content
            self.status_var.set("Summarizing article...")
            self.root.update()
            summary = self.summarize_text(body)
            self.summary_text.config(state=tk.NORMAL)
            self.summary_text.delete(1.0, tk.END)
            self.summary_text.insert(tk.END, summary)
            self.summary_text.config(state=tk.DISABLED)
            
            # Perform sentiment analysis
            self.status_var.set("Analyzing sentiment...")
            self.root.update()
            sentiment, sentiment_details = self.analyze_sentiment(body)
            
            # Update sentiment display
            self.update_sentiment_face(sentiment)
            
            self.sentiment_details.config(state=tk.NORMAL)
            self.sentiment_details.delete(1.0, tk.END)
            self.sentiment_details.insert(tk.END, "Detailed Sentiment Scores:\n\n")
            for key, value in sentiment_details.items():
                self.sentiment_details.insert(tk.END, f"{key}: {value:.4f}\n")
            self.sentiment_details.config(state=tk.DISABLED)
            
            self.status_var.set("Analysis complete!")
            
        except requests.exceptions.RequestException as e:
            self.show_error(f"Failed to fetch article: {e}")
            self.status_var.set("Error fetching article")
        except Exception as e:
            self.show_error(f"Error processing article: {e}")
            self.status_var.set("Error processing article")
    
    def show_error(self, message):
        mb = ttk.dialogs.Messagebox.show_error(
            message,
            "Error",
            parent=self.root
        )

if __name__ == "__main__":
    root = ttk.Window(themename="minty")
    app = ArticleAnalyzerApp(root)
    root.mainloop()
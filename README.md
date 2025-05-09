# Article Insight Analyzer

A modern GUI application that analyzes news articles, providing summaries and sentiment analysis with visual feedback.

## Features

- **Article Summarization**: Extracts key points from news articles
- **Sentiment Analysis**: Determines emotional tone (Positive, Neutral, Negative)
- **Visual Feedback**: Emoji faces to represent sentiment
- **Detailed Metrics**: Shows compound, positive, neutral, and negative scores
- **Modern UI**: Clean, professional interface with ttkbootstrap styling

## Screenshots

![Analysis Example](https://github.com/Pags2003/News-Summarizer/blob/main/screenshorts/analysis_example.png?raw=true) 
*Example of article analysis with positive sentiment*

![Error Handling](https://github.com/Pags2003/News-Summarizer/blob/main/screenshorts/error_message.png?raw=true) 
*Error handling for invalid URLs*

## Installation

### Prerequisites

- Python 3.6 or higher
- pip package manager

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/article-insight-analyzer.git
   cd News-Summarizer
   ```
2. Install them manually:
    ```bash
    pip install requests beautifulsoup4 readability-lxml sumy nltk ttkbootstrap pillow
    ```
3. Run the application:
    ```bash
    python app.py
    ```

## Usage
1. Enter a news article URL in the input field
2. Click "Analyze Article"
3. View results:
    a. Article title at the top
    b. Summary in the main text area
    c. Sentiment analysis with emoji face
    d. Detailed sentiment scores below

## Requirements
   requests>=2.26.0
   beautifulsoup4>=4.10.0
   readability-lxml>=0.8.1
   sumy>=0.10.0
   nltk>=3.6.7
   ttkbootstrap>=1.5.1
   Pillow>=9.0.1
    
## Technical Details
* Text Extraction: Uses readability-lxml to extract main article content
* Summarization: Implements LSA (Latent Semantic Analysis) via sumy
* Sentiment Analysis: Uses NLTK's VADER (Valence Aware Dictionary and sEntiment Reasoner)
* GUI Framework: Built with Tkinter and enhanced with ttkbootstrap

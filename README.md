# AI News Generator

An automated news report generator that creates comprehensive summaries from YouTube videos and Reddit threads using AI.

## Overview

This project combines modern web technologies and AI to automatically generate news reports by analyzing content from multiple sources:
- YouTube videos (including transcripts and comments)
- Reddit threads and discussions

## Tech Stack

### Frontend
- **Next.js** - React framework for the web interface
- Modern, responsive UI with server-side rendering
- Real-time updates and notifications

### Backend
- **FastAPI** - Modern Python web framework
- **Python 3.9+** - Core language
- AI/ML integrations for content processing

## Project Structure
  ├── frontend/ # Next.js frontend application
  │ ├── components/ # Reusable React components
  │ ├── pages/ # Next.js pages and routing
  │ └── styles/ # CSS and styling files
  │
  ├── backend/ # FastAPI backend application
  │ ├── newsletter/ # Core newsletter generation logic
  │ │ ├── api/ # API endpoints and routing
  │ │ ├── utils/ # Utility functions and helpers
  │ │ └── main.py # Application entry point
  │ └── tests/ # Backend test suite
  


## Features

- **Content Aggregation**
  - YouTube video analysis and transcript processing
  - Reddit thread scraping and sentiment analysis
  - Automated content categorization

- **AI Processing**
  - Natural language processing for content summarization
  - Key points extraction
  - Sentiment analysis
  - Topic clustering

- **Report Generation**
  - Customizable report templates
  - Multiple export formats (PDF, HTML, markdown)
  - Scheduled report generation


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

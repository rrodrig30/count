# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Flask-based document analysis application called "Count" that processes text documents and provides comprehensive statistics including word count, character count, whitespace count, and line count. The application supports multiple file formats (TXT, CSV, RTF, DOCX) and features a professional web interface.

## Architecture

The application follows a clean Flask web application structure:

- **Main Application** (`app.py`): Contains Flask routes, file upload handling, and main application logic
- **Document Processing**: The `DocumentProcessor` class handles format-specific text extraction from different document types
- **Text Analysis**: The `TextAnalyzer` class performs statistical calculations on extracted text
- **Templates**: HTML templates with Bootstrap styling for professional UI
- **Static Assets**: CSS and JavaScript for enhanced user experience

## Key Components

### Core Classes
- `DocumentProcessor`: Handles file validation and text extraction from various formats
- `TextAnalyzer`: Performs comprehensive text analysis and statistics calculation

### Supported File Formats
- Plain Text (.txt)
- CSV files (.csv) - extracts all cell content
- Rich Text Format (.rtf) - uses striprtf library
- Microsoft Word (.docx) - uses python-docx library

### Analysis Metrics
- Word count (excluding empty strings)
- Character count (including all characters)
- Whitespace count (spaces, tabs, newlines)
- Line count (using splitlines())
- Additional calculated metrics (average word length, words per line, etc.)

## Development Commands

### Running the Application
```bash
python app.py
```
The application runs on `http://localhost:5000` by default.

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Required Dependencies
- Flask==2.3.3
- python-docx==0.8.11
- striprtf==0.0.24
- Werkzeug==2.3.7

## Application Features

### File Upload
- Drag-and-drop functionality
- File format validation
- 16MB maximum file size limit
- Secure filename handling with werkzeug

### Error Handling
- Comprehensive try-catch blocks for file processing
- Flash messages for user feedback
- Temporary file cleanup
- Unicode encoding fallbacks

### Security Features
- Secure filename processing
- File extension validation
- Temporary file handling
- CSRF protection via Flask secret key

## Directory Structure

The application expects the following structure:
```
count/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates (created automatically)
│   ├── index.html        # Main upload page
│   └── results.html      # Results display page
└── static/               # Static assets (created automatically)
```

Note: The `templates` and `static` directories are created automatically when the application starts if they don't exist.

## Configuration

### Application Settings
- Debug mode enabled for development
- Host: 0.0.0.0 (accessible from network)
- Port: 5000
- Secret key for session management
- Maximum content length: 16MB

### File Processing Settings
- Allowed extensions: txt, csv, rtf, docx, doc
- Temporary file storage in system temp directory
- UTF-8 encoding with latin-1 fallback

## Code Patterns

### Text Extraction Pattern
Each file format has a dedicated static method in `DocumentProcessor`:
- `extract_text_from_txt()`: Handles plain text with encoding fallback
- `extract_text_from_csv()`: Reads all CSV cells and joins content
- `extract_text_from_rtf()`: Uses striprtf library for RTF processing
- `extract_text_from_docx()`: Extracts paragraphs from Word documents

### Analysis Pattern
The `TextAnalyzer.analyze_text()` method returns a dictionary with all statistics, making it easy to extend with additional metrics.

### Error Handling Pattern
All file operations include proper exception handling with cleanup in finally blocks or context managers where appropriate.
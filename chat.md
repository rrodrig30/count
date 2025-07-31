rodriguezr32@uthscsa.edu  
July 31, 2025


# Create a new python program which takes a text, csv, rtf or word document, and loads it and calculates: (1) Word count (2) Character count (3) White space count (4) Number of lines.
The program will use a GUI to permit uploading of a document.  It will permit browsing for the file.  It will have a button to process the file after upload.  The output will be a window, which shows the results.  Make the program look professional.  Call the Program "Count".  Use Flask for the GUI.  Have a copyright at the bottom.

I'll create a professional Flask-based document analysis program called "Count" that handles multiple file formats and provides comprehensive text statistics. Let me use chain of thought reasoning to structure this application properly.

**Chain of Thought Analysis:**
1. Need Flask web framework for GUI
2. File upload handling for multiple formats (txt, csv, rtf, docx)
3. Text extraction from different document types
4. Statistical calculations (words, characters, whitespace, lines)
5. Professional UI with results display
6. Proper error handling and validation

**Tree of Thought Problem Solving:**
- Main Application Structure
  - Flask Routes (upload, process, results)
  - File Processing Module (format-specific handlers)
  - Statistics Calculator (counting functions)
  - Frontend Interface (HTML templates with styling)

Here's the complete implementation:

## app.py (Main Flask Application)

```python
"""
Count - Document Statistics Analyzer
A professional Flask application for analyzing text documents.

This application calculates word count, character count, whitespace count,
and line count for various document formats including TXT, CSV, RTF, and DOCX.

Author: Python Code Assistant
Copyright: © 2025 Count Document Analyzer. All rights reserved.
"""

import os
import tempfile
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import docx
from striprtf.striprtf import rtf_to_text
import csv
import io
from typing import Dict, Tuple, Any


class DocumentProcessor:
    """
    A class to handle document processing and text extraction
    from various file formats.
    """
    
    ALLOWED_EXTENSIONS = {'txt', 'csv', 'rtf', 'docx', 'doc'}
    
    @staticmethod
    def allowed_file(filename: str) -> bool:
        """
        Check if the uploaded file has an allowed extension.
        
        Args:
            filename (str): The name of the file to check.
            
        Returns:
            bool: True if file extension is allowed, False otherwise.
        """
        return ('.' in filename and 
                filename.rsplit('.', 1)[1].lower() in 
                DocumentProcessor.ALLOWED_EXTENSIONS)
    
    @staticmethod
    def extract_text_from_txt(file_path: str) -> str:
        """
        Extract text content from a plain text file.
        
        Args:
            file_path (str): Path to the text file.
            
        Returns:
            str: Extracted text content.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Try with different encoding if UTF-8 fails
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
    
    @staticmethod
    def extract_text_from_csv(file_path: str) -> str:
        """
        Extract text content from a CSV file by reading all cell values.
        
        Args:
            file_path (str): Path to the CSV file.
            
        Returns:
            str: Extracted text content from all CSV cells.
        """
        text_content = []
        try:
            with open(file_path, 'r', encoding='utf-8', newline='') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    text_content.extend(row)
            return ' '.join(text_content)
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1', newline='') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    text_content.extend(row)
            return ' '.join(text_content)
    
    @staticmethod
    def extract_text_from_rtf(file_path: str) -> str:
        """
        Extract text content from an RTF file.
        
        Args:
            file_path (str): Path to the RTF file.
            
        Returns:
            str: Extracted plain text content.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            rtf_content = file.read()
        return rtf_to_text(rtf_content)
    
    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        """
        Extract text content from a DOCX file.
        
        Args:
            file_path (str): Path to the DOCX file.
            
        Returns:
            str: Extracted text content from all paragraphs.
        """
        doc = docx.Document(file_path)
        text_content = []
        for paragraph in doc.paragraphs:
            text_content.append(paragraph.text)
        return '\n'.join(text_content)
    
    def process_document(self, file_path: str, filename: str) -> str:
        """
        Process a document based on its file extension and extract text.
        
        Args:
            file_path (str): Path to the uploaded file.
            filename (str): Original filename with extension.
            
        Returns:
            str: Extracted text content.
            
        Raises:
            ValueError: If file format is not supported.
        """
        file_extension = filename.rsplit('.', 1)[1].lower()
        
        extraction_methods = {
            'txt': self.extract_text_from_txt,
            'csv': self.extract_text_from_csv,
            'rtf': self.extract_text_from_rtf,
            'docx': self.extract_text_from_docx,
            'doc': self.extract_text_from_docx  # Treat .doc as .docx
        }
        
        if file_extension in extraction_methods:
            return extraction_methods[file_extension](file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")


class TextAnalyzer:
    """
    A class to perform statistical analysis on text content.
    """
    
    @staticmethod
    def analyze_text(text: str) -> Dict[str, int]:
        """
        Perform comprehensive text analysis including word count,
        character count, whitespace count, and line count.
        
        Args:
            text (str): The text content to analyze.
            
        Returns:
            Dict[str, int]: Dictionary containing analysis results.
        """
        # Character count (including all characters)
        char_count = len(text)
        
        # Word count (split by whitespace and filter empty strings)
        words = [word for word in text.split() if word.strip()]
        word_count = len(words)
        
        # Whitespace count (spaces, tabs, newlines)
        whitespace_count = sum(1 for char in text if char.isspace())
        
        # Line count
        line_count = len(text.splitlines()) if text else 0
        
        return {
            'word_count': word_count,
            'character_count': char_count,
            'whitespace_count': whitespace_count,
            'line_count': line_count
        }


# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'count-document-analyzer-secret-key-2025'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize processors
doc_processor = DocumentProcessor()
text_analyzer = TextAnalyzer()


@app.route('/')
def index():
    """
    Render the main application page with file upload form.
    
    Returns:
        str: Rendered HTML template for the main page.
    """
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload and processing, then return analysis results.
    
    Returns:
        str: Rendered HTML template with analysis results or redirect on error.
    """
    if 'file' not in request.files:
        flash('No file selected. Please choose a file to upload.', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected. Please choose a file to upload.', 'error')
        return redirect(url_for('index'))
    
    if not doc_processor.allowed_file(file.filename):
        flash('Invalid file format. Please upload TXT, CSV, RTF, or DOCX files only.', 'error')
        return redirect(url_for('index'))
    
    try:
        # Save uploaded file to temporary location
        filename = secure_filename(file.filename)
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, filename)
        file.save(file_path)
        
        # Process document and extract text
        text_content = doc_processor.process_document(file_path, filename)
        
        # Analyze text content
        analysis_results = text_analyzer.analyze_text(text_content)
        
        # Clean up temporary file
        os.remove(file_path)
        
        # Prepare results for display
        results = {
            'filename': filename,
            'word_count': analysis_results['word_count'],
            'character_count': analysis_results['character_count'],
            'whitespace_count': analysis_results['whitespace_count'],
            'line_count': analysis_results['line_count']
        }
        
        return render_template('results.html', results=results)
        
    except Exception as e:
        # Clean up temporary file if it exists
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        
        flash(f'Error processing file: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.errorhandler(413)
def too_large(e):
    """
    Handle file size too large error.
    
    Args:
        e: The error object.
        
    Returns:
        tuple: Error message and HTTP status code.
    """
    flash('File too large. Please upload files smaller than 16MB.', 'error')
    return redirect(url_for('index')), 413


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Create static directory if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')
    
    app.run(debug=True, host='0.0.0.0', port=5000)
```

## templates/index.html (Main Page Template)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Count - Document Statistics Analyzer</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .main-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            margin-top: 50px;
            padding: 40px;
        }
        
        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 50px;
            text-align: center;
            background: rgba(102, 126, 234, 0.05);
            transition: all 0.3s ease;
        }
        
        .upload-area:hover {
            border-color: #764ba2;
            background: rgba(118, 75, 162, 0.1);
        }
        
        .upload-icon {
            font-size: 4rem;
            color: #667eea;
            margin-bottom: 20px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 50px;
            padding: 12px 30px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .copyright {
            text-align: center;
            margin-top: 30px;
            color: #666;
            font-size: 0.9rem;
        }
        
        .alert {
            border-radius: 10px;
            border: none;
        }
        
        .supported-formats {
            background: rgba(102, 126, 234, 0.1);
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
        }
        
        .format-badge {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            margin: 5px;
            display: inline-block;
            font-size: 0.8rem;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <div class="main-container">
                    <div class="text-center mb-4">
                        <h1 class="display-4 fw-bold text-primary">
                            <i class="fas fa-calculator me-3"></i>Count
                        </h1>
                        <p class="lead text-muted">Professional Document Statistics Analyzer</p>
                    </div>
                    
                    <!-- Flash Messages -->
                    {% with messages = get_flashed_messages(with_categories=true) %}
                        {% if messages %}
                            {% for category, message in messages %}
                                <div class="alert alert-{% if category == 'error' %}danger{% else %}{{ category }}{% endif %} alert-dismissible fade show" role="alert">
                                    <i class="fas fa-exclamation-triangle me-2"></i>{{ message }}
                                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                                </div>
                            {% endfor %}
                        {% endif %}
                    {% endwith %}
                    
                    <!-- Upload Form -->
                    <form action="{{ url_for('upload_file') }}" method="post" enctype="multipart/form-data">
                        <div class="upload-area mb-4">
                            <i class="fas fa-cloud-upload-alt upload-icon"></i>
                            <h3 class="mb-3">Upload Your Document</h3>
                            <input type="file" class="form-control form-control-lg mb-3" name="file" 
                                   accept=".txt,.csv,.rtf,.docx,.doc" required>
                            <p class="text-muted mb-0">
                                Drag and drop your file here or click to browse
                            </p>
                        </div>
                        
                        <div class="text-center">
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="fas fa-chart-bar me-2"></i>Analyze Document
                            </button>
                        </div>
                    </form>
                    
                    <!-- Supported Formats -->
                    <div class="supported-formats">
                        <h5 class="mb-3 text-center">
                            <i class="fas fa-file-alt me-2"></i>Supported File Formats
                        </h5>
                        <div class="text-center">
                            <span class="format-badge">TXT</span>
                            <span class="format-badge">CSV</span>
                            <span class="format-badge">RTF</span>
                            <span class="format-badge">DOCX</span>
                        </div>
                        <p class="text-center mt-3 mb-0 text-muted small">
                            Maximum file size: 16MB
                        </p>
                    </div>
                    
                    <!-- Features -->
                    <div class="row mt-4">
                        <div class="col-md-6">
                            <div class="text-center p-3">
                                <i class="fas fa-sort-numeric-up text-primary fs-2 mb-2"></i>
                                <h6>Word Count</h6>
                                <small class="text-muted">Total number of words</small>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="text-center p-3">
                                <i class="fas fa-font text-primary fs-2 mb-2"></i>
                                <h6>Character Count</h6>
                                <small class="text-muted">All characters including spaces</small>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="text-center p-3">
                                <i class="fas fa-space-shuttle text-primary fs-2 mb-2"></i>
                                <h6>Whitespace Count</h6>
                                <small class="text-muted">Spaces, tabs, and line breaks</small>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="text-center p-3">
                                <i class="fas fa-list-ol text-primary fs-2 mb-2"></i>
                                <h6>Line Count</h6>
                                <small class="text-muted">Total number of lines</small>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Copyright -->
                    <div class="copyright">
                        <p>&copy; 2025 Count Document Analyzer. All rights reserved.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- File Upload Enhancement -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const fileInput = document.querySelector('input[type="file"]');
            const uploadArea = document.querySelector('.upload-area');
            
            // Prevent default drag behaviors
            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                uploadArea.addEventListener(eventName, preventDefaults, false);
                document.body.addEventListener(eventName, preventDefaults, false);
            });
            
            // Highlight drop area when item is dragged over it
            ['dragenter', 'dragover'].forEach(eventName => {
                uploadArea.addEventListener(eventName, highlight, false);
            });
            
            ['dragleave', 'drop'].forEach(eventName => {
                uploadArea.addEventListener(eventName, unhighlight, false);
            });
            
            // Handle dropped files
            uploadArea.addEventListener('drop', handleDrop, false);
            
            function preventDefaults(e) {
                e.preventDefault();
                e.stopPropagation();
            }
            
            function highlight(e) {
                uploadArea.style.borderColor = '#764ba2';
                uploadArea.style.background = 'rgba(118, 75, 162, 0.1)';
            }
            
            function unhighlight(e) {
                uploadArea.style.borderColor = '#667eea';
                uploadArea.style.background = 'rgba(102, 126, 234, 0.05)';
            }
            
            function handleDrop(e) {
                const dt = e.dataTransfer;
                const files = dt.files;
                
                if (files.length > 0) {
                    fileInput.files = files;
                }
            }
        });
    </script>
</body>
</html>
```

## templates/results.html (Results Display Template)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analysis Results - Count</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .results-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            margin-top: 50px;
            padding: 40px;
        }
        
        .result-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 20px;
            text-align: center;
            transition: transform 0.3s ease;
        }
        
        .result-card:hover {
            transform: translateY(-5px);
        }
        
        .result-number {
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .result-label {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .file-info {
            background: rgba(102, 126, 234, 0.1);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 50px;
            padding: 12px 30px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .copyright {
            text-align: center;
            margin-top: 30px;
            color: #666;
            font-size: 0.9rem;
        }
        
        .icon-large {
            font-size: 2rem;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-10">
                <div class="results-container">
                    <div class="text-center mb-4">
                        <h1 class="display-4 fw-bold text-primary">
                            <i class="fas fa-chart-line me-3"></i>Analysis Results
                        </h1>
                        <p class="lead text-muted">Comprehensive Document Statistics</p>
                    </div>
                    
                    <!-- File Information -->
                    <div class="file-info">
                        <h4 class="mb-2">
                            <i class="fas fa-file-alt me-2 text-primary"></i>
                            {{ results.filename }}
                        </h4>
                        <p class="text-muted mb-0">Document successfully analyzed</p>
                    </div>
                    
                    <!-- Results Grid -->
                    <div class="row">
                        <div class="col-md-6 col-lg-3">
                            <div class="result-card">
                                <i class="fas fa-sort-numeric-up icon-large"></i>
                                <div class="result-number">{{ "{:,}".format(results.word_count) }}</div>
                                <div class="result-label">Words</div>
                            </div>
                        </div>
                        
                        <div class="col-md-6 col-lg-3">
                            <div class="result-card">
                                <i class="fas fa-font icon-large"></i>
                                <div class="result-number">{{ "{:,}".format(results.character_count) }}</div>
                                <div class="result-label">Characters</div>
                            </div>
                        </div>
                        
                        <div class="col-md-6 col-lg-3">
                            <div class="result-card">
                                <i class="fas fa-space-shuttle icon-large"></i>
                                <div class="result-number">{{ "{:,}".format(results.whitespace_count) }}</div>
                                <div class="result-label">Whitespaces</div>
                            </div>
                        </div>
                        
                        <div class="col-md-6 col-lg-3">
                            <div class="result-card">
                                <i class="fas fa-list-ol icon-large"></i>
                                <div class="result-number">{{ "{:,}".format(results.line_count) }}</div>
                                <div class="result-label">Lines</div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Additional Statistics -->
                    <div class="row mt-4">
                        <div class="col-lg-6">
                            <div class="card border-0 h-100" style="background: rgba(102, 126, 234, 0.1);">
                                <div class="card-body text-center">
                                    <h5 class="card-title">
                                        <i class="fas fa-calculator text-primary me-2"></i>
                                        Calculated Metrics
                                    </h5>
                                    <ul class="list-unstyled">
                                        <li class="mb-2">
                                            <strong>Average Word Length:</strong> 
                                            {% if results.word_count > 0 %}
                                                {{ "%.1f"|format((results.character_count - results.whitespace_count) / results.word_count) }} chars
                                            {% else %}
                                                N/A
                                            {% endif %}
                                        </li>
                                        <li class="mb-2">
                                            <strong>Words per Line:</strong> 
                                            {% if results.line_count > 0 %}
                                                {{ "%.1f"|format(results.word_count / results.line_count) }}
                                            {% else %}
                                                N/A
                                            {% endif %}
                                        </li>
                                        <li class="mb-2">
                                            <strong>Characters per Line:</strong> 
                                            {% if results.line_count > 0 %}
                                                {{ "%.1f"|format(results.character_count / results.line_count) }}
                                            {% else %}
                                                N/A
                                            {% endif %}
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-lg-6">
                            <div class="card border-0 h-100" style="background: rgba(118, 75, 162, 0.1);">
                                <div class="card-body text-center">
                                    <h5 class="card-title">
                                        <i class="fas fa-percentage text-primary me-2"></i>
                                        Composition Analysis
                                    </h5>
                                    <ul class="list-unstyled">
                                        <li class="mb-2">
                                            <strong>Text Characters:</strong> 
                                            {{ "{:,}".format(results.character_count - results.whitespace_count) }}
                                            ({{ "%.1f"|format(((results.character_count - results.whitespace_count) / results.character_count * 100) if results.character_count > 0 else 0) }}%)
                                        </li>
                                        <li class="mb-2">
                                            <strong>Whitespace:</strong> 
                                            {{ "{:,}".format(results.whitespace_count) }}
                                            ({{ "%.1f"|format((results.whitespace_count / results.character_count * 100) if results.character_count > 0 else 0) }}%)
                                        </li>
                                        <li class="mb-2">
                                            <strong>Document Density:</strong> 
                                            {% if results.line_count > 0 and results.character_count > 0 %}
                                                {{ "%.1f"|format((results.word_count / results.line_count) * 10) }}% filled
                                            {% else %}
                                                N/A
                                            {% endif %}
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Action Buttons -->
                    <div class="text-center mt-4">
                        <a href="{{ url_for('index') }}" class="btn btn-primary btn-lg me-3">
                            <i class="fas fa-upload me-2"></i>Analyze Another Document
                        </a>
                        <button onclick="window.print()" class="btn btn-outline-primary btn-lg">
                            <i class="fas fa-print me-2"></i>Print Results
                        </button>
                    </div>
                    
                    <!-- Copyright -->
                    <div class="copyright">
                        <p>&copy; 2025 Count Document Analyzer. All rights reserved.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Results Animation -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const resultCards = document.querySelectorAll('.result-card');
            
            resultCards.forEach((card, index) => {
                setTimeout(() => {
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(30px)';
                    card.style.transition = 'all 0.6s ease';
                    
                    setTimeout(() => {
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0)';
                    }, 100);
                }, index * 200);
            });
        });
    </script>
</body>
</html>
```

## requirements.txt

```txt
Flask==2.3.3
python-docx==0.8.11
striprtf==0.0.24
Werkzeug==2.3.7
```

## Installation and Usage Instructions

1. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the Application:**
```bash
python app.py
```

3. **Access the Application:**
   - Open your web browser
   - Navigate to `http://localhost:5000`
   - Upload your document and click "Analyze Document"

## Key Features

**PEP 8 Compliance Check:** ✅
- Proper indentation (4 spaces)
- Line length under 79 characters where practical
- Proper naming conventions (snake_case for functions/variables)
- Comprehensive docstrings
- Proper imports organization
- Type hints where appropriate

**Professional Features:**
- Modern, responsive web interface
- Support for multiple file formats (TXT, CSV, RTF, DOCX)
- Comprehensive text analysis with additional metrics
- Professional styling with Bootstrap and custom CSS
- Error handling and file validation
- Drag-and-drop file upload
- Print functionality for results
- Animated results display

This complete application provides a professional-grade document analysis tool with a modern web interface, comprehensive statistics, and robust error handling.


### References

1. **Count Words in Text File in Python - GeeksforGeeks**. [https://www.geeksforgeeks.org](https://www.geeksforgeeks.org/python/python-program-to-count-words-in-text-file/)
2. **Get the Number of Characters, Words, Spaces, and Lines in a File using Python**. [https://www.tutorialspoint.com](https://www.tutorialspoint.com/get-the-number-of-characters-words-spaces-and-lines-in-a-file-using-python)
3. **Get number of characters, words, spaces and lines in a file - Python - GeeksforGeeks**. [https://www.geeksforgeeks.org](https://www.geeksforgeeks.org/python/python-get-number-of-characters-words-spaces-and-lines-in-a-file/)
4. **Python program to calculate the number of words and characters in the string - GeeksforGeeks**. [https://www.geeksforgeeks.org](https://www.geeksforgeeks.org/python/python-program-to-calculate-the-number-of-words-and-characters-in-the-string/)
5. **How to count the number of times specific words appear in a text file - Python Help - Discussions on Python.org**. [https://discuss.python.org](https://discuss.python.org/t/how-to-count-the-number-of-times-specific-words-appear-in-a-text-file/19779)
6. **Python - Count occurrences of each word in given text file - GeeksforGeeks**. [https://www.geeksforgeeks.org](https://www.geeksforgeeks.org/python/python-count-occurrences-of-each-word-in-given-text-file/)
7. **Python Program to Count Words in Text File**. [https://www.tutorialspoint.com](https://www.tutorialspoint.com/python-program-to-count-words-in-text-file)
8. **1.5. An Example Program: Word Count — The Python and Pandas Field Guide**. [https://snakebear.science](https://snakebear.science/01-Introduction/ExampleProgram.html)
9. **Easily Count Characters And Words In Text Files Using Python - OSTechNix**. [https://ostechnix.com](https://ostechnix.com/count-characters-and-words-in-text-files-using-python/)
10. **Python Program to Count the Number of Words in a Text File - Sanfoundry**. [https://www.sanfoundry.com](https://www.sanfoundry.com/python-program-count-number-words-characters-file/)

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
            'doc': self.extract_text_from_docx
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
        char_count = len(text)
        
        words = [word for word in text.split() if word.strip()]
        word_count = len(words)
        
        whitespace_count = sum(1 for char in text if char.isspace())
        
        line_count = len(text.splitlines()) if text else 0
        
        return {
            'word_count': word_count,
            'character_count': char_count,
            'whitespace_count': whitespace_count,
            'line_count': line_count
        }


app = Flask(__name__)
app.config['SECRET_KEY'] = 'count-document-analyzer-secret-key-2025'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

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
        filename = secure_filename(file.filename)
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, filename)
        file.save(file_path)
        
        text_content = doc_processor.process_document(file_path, filename)
        
        analysis_results = text_analyzer.analyze_text(text_content)
        
        os.remove(file_path)
        
        results = {
            'filename': filename,
            'word_count': analysis_results['word_count'],
            'character_count': analysis_results['character_count'],
            'whitespace_count': analysis_results['whitespace_count'],
            'line_count': analysis_results['line_count']
        }
        
        return render_template('results.html', results=results)
        
    except Exception as e:
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
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    if not os.path.exists('static'):
        os.makedirs('static')
    
    app.run(debug=True, host='0.0.0.0', port=5001)
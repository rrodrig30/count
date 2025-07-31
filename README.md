# Count - Document Statistics Analyzer

A professional Flask web application for analyzing text documents and providing comprehensive statistics.

![Count Application](https://img.shields.io/badge/Flask-2.3.3-blue)
![Python](https://img.shields.io/badge/Python-3.7%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Features

- **Multi-Format Support**: Analyze TXT, CSV, RTF, and DOCX files
- **Comprehensive Statistics**: 
  - Word count
  - Character count (including spaces)
  - Whitespace count (spaces, tabs, newlines)
  - Line count
  - Additional metrics (average word length, composition analysis)
- **Professional UI**: Modern, responsive design with Bootstrap
- **Drag & Drop**: Intuitive file upload with drag-and-drop functionality
- **Real-time Processing**: Fast document analysis with immediate results
- **Error Handling**: Robust file validation and error management
- **Print Support**: Print-friendly results page

## 📸 Screenshots

### Main Upload Interface
Professional upload interface with drag-and-drop functionality and supported file format indicators.

### Results Display
Comprehensive statistics display with animated cards and detailed metrics breakdown.

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/rrodrig30/count.git
   cd count
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   Open your web browser and navigate to `http://localhost:5001`

## 📋 Requirements

```
Flask==2.3.3
python-docx==0.8.11
striprtf==0.0.24
Werkzeug==2.3.7
```

## 🎯 Usage

1. **Upload a Document**: Click the upload area or drag and drop your file
2. **Supported Formats**: TXT, CSV, RTF, DOCX files (max 16MB)
3. **Analyze**: Click "Analyze Document" to process your file
4. **View Results**: Get comprehensive statistics and metrics
5. **Print or Analyze More**: Print results or upload another document

## 📊 Supported File Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| Plain Text | `.txt` | Standard text files with UTF-8/Latin-1 encoding |
| CSV | `.csv` | Comma-separated values (analyzes all cell content) |
| Rich Text | `.rtf` | Rich Text Format documents |
| Word Document | `.docx` | Microsoft Word documents |

## 🏗️ Architecture

The application follows a clean, modular architecture:

```
count/
├── app.py                 # Main Flask application
├── templates/             # HTML templates
│   ├── index.html        # Main upload interface
│   └── results.html      # Results display page
├── static/               # Static assets (auto-created)
├── requirements.txt      # Python dependencies
├── CLAUDE.md            # Development documentation
└── README.md            # This file
```

### Core Components

- **DocumentProcessor**: Handles file validation and text extraction
- **TextAnalyzer**: Performs statistical analysis on extracted text
- **Flask Routes**: Manages web requests and responses
- **Templates**: Professional UI with Bootstrap styling

## 🔧 Configuration

### Application Settings
- **Host**: 0.0.0.0 (accessible from network)
- **Port**: 5001 (configurable in app.py)
- **Debug Mode**: Enabled for development
- **Max File Size**: 16MB
- **Allowed Extensions**: txt, csv, rtf, docx, doc

### Security Features
- Secure filename processing
- File extension validation
- Temporary file cleanup
- CSRF protection

## 🧪 Testing

A sample test file is included:
```bash
# Test with the included sample
# Upload test_sample.txt through the web interface
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/) web framework
- UI powered by [Bootstrap](https://getbootstrap.com/)
- Icons from [Font Awesome](https://fontawesome.com/)
- Document processing libraries:
  - [python-docx](https://python-docx.readthedocs.io/) for Word documents
  - [striprtf](https://pypi.org/project/striprtf/) for RTF files

## 📞 Support

If you have any questions or need help with the application:

1. Check the [CLAUDE.md](CLAUDE.md) file for development guidance
2. Open an issue on GitHub
3. Review the error messages in the application for troubleshooting

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
For production deployment, consider using:
- **Gunicorn**: `gunicorn -w 4 -b 0.0.0.0:5001 app:app`
- **Docker**: Create a Dockerfile for containerized deployment
- **Cloud Platforms**: Deploy to Heroku, AWS, or Google Cloud

---

**Copyright © 2025 Count Document Analyzer. All rights reserved.**

*Built with ❤️ using Flask and modern web technologies*
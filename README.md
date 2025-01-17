# Resume Reviewer with Claude AI

A Python application that uses Claude AI to analyze resumes and provide actionable feedback. This project demonstrates how to integrate the Anthropic Claude API with a Streamlit web interface.

## 🛠️ Technologies Used

- **Python**: Primary programming language
- **uv**: Fast Python package installer and resolver
- **Streamlit**: Web interface framework
- **Anthropic Claude API**: AI model for resume analysis
- **python-dotenv**: Environment variable management

## 🚀 Implementation Steps

### 1. Project Setup

```bash
# Initialize project with uv
uv init resume-reviewer

# Install dependencies
uv add streamlit anthropic python-dotenv
```

### 2. Environment Configuration

Create a `.env` file in the project root:
```
ANTHROPIC_API_KEY=your-api-key-here
```

### 3. Key Components

#### PDF Processing
- Uses Python's built-in `base64` for PDF encoding
- Converts PDF to base64 format for Claude API compatibility

#### Claude AI Integration
- Implements document analysis using Claude-3-Sonnet model
- Processes PDFs and returns structured feedback
- Handles API responses and error cases

#### Streamlit UI
- File upload interface for PDFs
- Progress indicators and loading states
- Error handling and user feedback
- Download option for analysis results

## 📁 Project Structure

```
resume-reviewer/
├── app.py          # Main Streamlit application
├── .env            # Environment variables
├── pdfs/           # Directory for PDF storage
└── README.md       # Documentation
```

## 💻 Code Explanation

### 1. Environment Setup
```python
def load_environment():
    """Load environment variables and validate API key"""
    load_dotenv()
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        st.error('❌ API key not found')
        st.stop()
    return api_key
```

### 2. PDF Analysis
```python
def analyze_resume(pdf_data, client):
    """Send PDF to Claude for analysis"""
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_data
                    }
                },
                {
                    "type": "text",
                    "text": "Analyze the resume..."
                }
            ]
        }]
    )
    return message.content[0].text
```

### 3. User Interface
- Implements a clean, user-friendly interface
- Shows upload progress and file details
- Provides clear feedback during analysis
- Includes download functionality for results

## 🌟 Features

1. **PDF Upload**
   - Drag-and-drop interface
   - File size and type validation
   - Upload confirmation

2. **Analysis Process**
   - Real-time progress updates
   - Clear error messages
   - Structured feedback presentation

3. **Results**
   - Formatted analysis display
   - Downloadable results
   - Error handling and recovery

## 🔧 Running the Application

```bash
# Clone the repository
git clone [repository-url]

# Navigate to project directory
cd resume-reviewer

# Install dependencies with uv
uv add streamlit anthropic python-dotenv

# Run the application
uv run streamlit run app.py
```

## 📝 Educational Notes

1. **API Integration**
   - Shows how to safely handle API keys
   - Demonstrates proper error handling
   - Implements async operations with feedback

2. **UI/UX Best Practices**
   - Progress indicators for long operations
   - Clear error messages
   - Intuitive user flow

3. **Code Structure**
   - Modular function design
   - Clear separation of concerns
   - Comprehensive error handling

## 🤝 Contributing

Feel free to fork, modify, and use this code for educational purposes. Please maintain proper attribution and documentation.

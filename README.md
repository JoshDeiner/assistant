# Claude Document Loading Tool

This repository provides a streamlined architecture for loading documents into Claude's context window via the Anthropic API. This approach uses Claude's function calling capabilities to load documents on demand during conversations.

## Architecture Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Document File  │────▶│  Document       │────▶│  Claude API     │
│  (.txt, .pdf,   │     │  Loading Tool   │     │  with Tool      │
│   etc.)         │     │                 │     │  Function       │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │                        │
                               │                        │
                               ▼                        ▼
                        ┌─────────────────┐     ┌─────────────────┐
                        │                 │     │                 │
                        │  Formatted      │     │  Claude         │
                        │  Document in    │     │  Response with  │
                        │  System Prompt  │     │  Document       │
                        │                 │     │  Knowledge      │
                        └─────────────────┘     └─────────────────┘
```

## Components

### 1. JSON Schema for Claude's Function Calling

The document loading tool schema is defined in `schema.py`:

```python
document_loading_tool = {
    "name": "load_document",
    "description": "Loads a document from the specified filepath and adds it to the context window.",
    "input_schema": {
        "type": "object",
        "properties": {
            "filepath": {
                "type": "string",
                "description": "Path to the document file to be loaded into the context window"
            },
            "document_type": {
                "type": "string",
                "description": "Type of document being loaded (optional - will try to infer from file extension if not provided)"
            },
            "metadata": {
                "type": "object",
                "description": "Optional metadata about the document"
            }
        },
        "required": ["filepath"]
    }
}
```

### 2. Document Loading Function

The document loading functions in `document_loader.py` handle reading and formatting documents:

- `load_document`: Reads the specified document, processes it according to its type
- `inject_document_into_prompt`: Formats the document with proper XML tags for Claude to recognize

### 3. Claude API Integration

The API integration in `run.py` handles:
- Registering the document loading tool
- Processing tool calls from Claude
- Sending tool responses back
- Managing the conversation flow

## Supported Document Types

- Text (.txt)
- PDF (.pdf) - requires PyPDF2
- CSV (.csv)
- JSON (.json)
- Markdown (.md)
- HTML (.html)
- XML (.xml)

## Getting Started

1. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your API key as an environment variable:
   ```bash
   export ANTHROPIC_API_KEY="your_api_key_here"
   ```

3. Run the example script:
   ```bash
   python run.py
   ```

## Usage Example

The default example asks Claude to analyze the Atlantis population data file. You can modify the `test_document_loading` function in `run.py` to load different documents and ask different questions.

## Key Benefits

- **On-Demand Loading**: Documents are loaded only when needed
- **Flexible Format Support**: Works with various document types
- **Transparent Process**: Claude explains when it's loading documents
- **Context Management**: Documents are properly formatted for Claude's context window
- **Conversation Flow**: Natural integration into Claude conversations
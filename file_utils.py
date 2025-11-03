import os
import docx
from PyPDF2 import PdfReader

class UnsupportedFileError(Exception):
    """Custom exception for unsupported file types."""
    pass

def read_file_content(file_path: str, file_name: str) -> str:
    """
    Reads text content from supported file types.
    Raises UnsupportedFileError for unsupported types and IOError for read errors.
    """
    ext = os.path.splitext(file_name)[1].lower()

    try:
        if ext in [".txt", ".py", ".cpp", ".cc", ".csv", ".js", ".java", ".c"]:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        
        elif ext == ".docx":
            doc = docx.Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        
        elif ext == ".pdf":
            reader = PdfReader(file_path)
            content = "\n".join(
                [page.extract_text() for page in reader.pages if page.extract_text()]
            )
            return content
        
        else:
            # Raise a specific error for unsupported files
            raise UnsupportedFileError(ext)
    
    except Exception as e:
        # Raise a general IO error for any other reading issues
        raise IOError(f"Could not read file {file_name}: {str(e)}")
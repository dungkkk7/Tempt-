import mammoth
import os

def convert_docx_to_markdown(docx_path, output_path):
    try:
        # Ensure the input file exists
        if not os.path.exists(docx_path):
            print(f"Error: Input file not found at {docx_path}")
            return

        # Convert the document
        with open(docx_path, "rb") as docx_file:
            result = mammoth.convert_to_markdown(docx_file)
            markdown = result.value
        
        # Write to output file in a separate operation
        with open(output_path, "w", encoding="utf-8") as md_file:
            md_file.write(markdown)
        
        print(f"Conversion complete: {output_path}")
        
    except Exception as e:
        print(f"Error during conversion: {str(e)}")

convert_docx_to_markdown(r"C:\Users\dungv\OneDrive\Documents\GitHub\Tempt-\dllsearch.docx", 
                         r"C:\Users\dungv\OneDrive\Documents\GitHub\Tempt-\output.md")
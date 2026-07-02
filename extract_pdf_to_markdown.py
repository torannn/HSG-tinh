import os
import sys
import subprocess
import base64
import codecs

# Force sys.stdout and sys.stderr to use UTF-8 to prevent charmap encoding errors on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
if sys.stderr.encoding != 'utf-8':
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# Auto-install dependencies if missing
try:
    import fitz  # PyMuPDF
    from gradio_client import Client, handle_file
except ImportError:
    print("Installing required libraries: pymupdf, gradio_client...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pymupdf", "gradio_client"])
    import fitz
    from gradio_client import Client, handle_file

def image_to_base64(img_path):
    with open(img_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:image/png;base64,{encoded_string}"

def process_pdf(pdf_path, output_md_path, space_id="prithivMLmods/Multimodal-OCR"):
    """
    Converts a PDF file page-by-page into a single Markdown file using a public HF Space API.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: File '{pdf_path}' not found.")
        sys.exit(1)

    print(f"Connecting to Hugging Face Space: '{space_id}'...")
    try:
        client = Client(space_id)
    except Exception as e:
        print(f"Failed to connect to Hugging Face Space: {e}")
        print("Please check your internet connection or the Space ID.")
        sys.exit(1)

    print(f"Opening PDF file: '{pdf_path}'...")
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    print(f"Total pages: {total_pages}\n")

    # Temp directory for rendering pages
    temp_dir = "temp_pdf_pages"
    os.makedirs(temp_dir, exist_ok=True)

    markdown_results = []

    for idx in range(total_pages):
        page_num = idx + 1
        print(f"[{page_num}/{total_pages}] Rendering page...")
        
        # Render page as high-res PNG (DPI=150 is good for OCR)
        page = doc.load_page(idx)
        pix = page.get_pixmap(dpi=150)
        img_path = os.path.join(temp_dir, f"page_{page_num}.png")
        pix.save(img_path)

        print(f"[{page_num}/{total_pages}] Sending page to HF API...")
        try:
            # Check the space_id to customize the API call
            if "Multimodal-OCR" in space_id:
                # Convert the image to base64 as required by this space
                img_b64 = image_to_base64(img_path)
                result = client.predict(
                    model_name="olmOCR-7B-0725", # Set model to olmOCR for math
                    text="Perform OCR on the image precisely. Extract all text and math equations. Wrap math equations in LaTeX format.",
                    image_b64=img_b64,
                    max_new_tokens_v=1024,
                    temperature_v=0.7,
                    top_p_v=0.9,
                    top_k_v=50,
                    repetition_penalty_v=1.1,
                    gpu_timeout_v=60,
                    api_name="/run_ocr"
                )
            else:
                # Fallback to standard gradio file upload prediction
                result = client.predict(
                    image=handle_file(img_path),
                    api_name="/predict"
                )
            
            # Extract text from gradio response
            if isinstance(result, (tuple, list)):
                page_text = result[0]
            elif isinstance(result, dict):
                page_text = result.get("text", str(result))
            else:
                page_text = str(result)
                
            print(f"[{page_num}/{total_pages}] Successfully processed!")
            markdown_results.append(f"<!-- PAGE {page_num} -->\n\n{page_text}\n")
            
        except Exception as e:
            print(f"[{page_num}/{total_pages}] Error calling API: {e}")
            markdown_results.append(f"<!-- PAGE {page_num} ERROR: {e} -->\n")

        # Cleanup temp image for the page
        if os.path.exists(img_path):
            os.remove(img_path)

    # Clean up temp folder
    try:
        os.rmdir(temp_dir)
    except Exception:
        pass

    # Save to file
    print(f"\nWriting compiled Markdown to: '{output_md_path}'...")
    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(markdown_results))
    print("All tasks completed successfully!")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract_pdf_to_markdown.py <path_to_pdf> <output_markdown_file> [gradio_space_id]")
        print("Example: python extract_pdf_to_markdown.py Đề_3_HSG.pdf de3_converted.md")
    else:
        pdf = sys.argv[1]
        out_md = sys.argv[2]
        space = sys.argv[3] if len(sys.argv) > 3 else "prithivMLmods/Multimodal-OCR"
        process_pdf(pdf, out_md, space)

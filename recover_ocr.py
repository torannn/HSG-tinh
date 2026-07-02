import os
import sys
import re
import codecs
import subprocess
import base64

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

def parse_markdown_pages(md_path):
    """
    Parses the markdown file into a list of dictionaries:
    [{'page_num': int, 'header': str, 'content': str, 'has_error': bool}]
    """
    if not os.path.exists(md_path):
        return []

    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by PAGE headers
    # e.g., <!-- PAGE 1 --> or <!-- PAGE 2 ERROR: ... -->
    pattern = r"(<!--\s*PAGE\s+(\d+)(?:\s+ERROR:[^>]*)?\s*-->)"
    parts = re.split(pattern, content)
    
    pages = []
    # If the file didn't start with a PAGE marker, the first part is prepended text
    first_part = parts[0].strip()
    if first_part and not first_part.startswith("<!--"):
        # We can store this as a preamble or header
        pages.append({
            'page_num': 0,
            'header': "",
            'content': first_part,
            'has_error': False
        })

    # The rest of the split parts will be in groups of 3:
    # 1. Full header match (e.g. <!-- PAGE 1 -->)
    # 2. Page number (e.g. 1)
    # 3. Content following the header
    for i in range(1, len(parts), 3):
        header = parts[i]
        page_num = int(parts[i+1])
        page_content = parts[i+2] if (i+2) < len(parts) else ""
        
        # Check if the page content or header contains error signals
        has_error = False
        if "ERROR" in header:
            has_error = True
        elif "[ERROR]" in page_content or "ZeroGPU quota" in page_content:
            has_error = True
            
        pages.append({
            'page_num': page_num,
            'header': header,
            'content': page_content,
            'has_error': has_error
        })
        
    return pages

def save_markdown_pages(md_path, pages):
    with open(md_path, "w", encoding="utf-8") as f:
        for p in pages:
            if p['page_num'] == 0:
                f.write(p['content'] + "\n\n")
            else:
                f.write(f"<!-- PAGE {p['page_num']} -->\n\n{p['content'].strip()}\n\n")
    print(f"Saved updated markdown to '{md_path}'")

def recover_pages(md_path, pdf_path, space_id="prithivMLmods/Multimodal-OCR", hf_token=None):
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file '{pdf_path}' not found.")
        return False
        
    pages = parse_markdown_pages(md_path)
    if not pages:
        print(f"No pages found or markdown file '{md_path}' does not exist.")
        return False
        
    failed_pages = [p for p in pages if p['has_error'] and p['page_num'] > 0]
    if not failed_pages:
        print(f"No failed pages found in '{md_path}'!")
        return True
        
    print(f"Found {len(failed_pages)} failed page(s) in '{md_path}': {[p['page_num'] for p in failed_pages]}")
    
    print(f"Connecting to Hugging Face Space: '{space_id}'...")
    try:
        client = Client(space_id, token=hf_token)
    except Exception as e:
        print(f"Failed to connect to Hugging Face Space: {e}")
        return False
        
    doc = fitz.open(pdf_path)
    temp_dir = "temp_recover_pages"
    os.makedirs(temp_dir, exist_ok=True)
    
    success_count = 0
    
    for p in failed_pages:
        page_num = p['page_num']
        idx = page_num - 1
        if idx >= len(doc):
            print(f"Page {page_num} is out of range for PDF (total pages: {len(doc)}). Skipping.")
            continue
            
        print(f"--- Processing Page {page_num} ---")
        page = doc.load_page(idx)
        pix = page.get_pixmap(dpi=150)
        img_path = os.path.join(temp_dir, f"page_{page_num}.png")
        pix.save(img_path)
        
        print(f"Sending page {page_num} to HF API...")
        try:
            if "Multimodal-OCR" in space_id:
                img_b64 = image_to_base64(img_path)
                result = client.predict(
                    model_name="olmOCR-7B-0725",
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
                result = client.predict(
                    image=handle_file(img_path),
                    api_name="/predict"
                )
                
            if isinstance(result, (tuple, list)):
                page_text = result[0]
            elif isinstance(result, dict):
                page_text = result.get("text", str(result))
            else:
                page_text = str(result)
                
            # Check if output is a Hugging Face ZeroGPU error message disguised as successful response
            if "[ERROR]" in page_text or "ZeroGPU quota" in page_text:
                print(f"Page {page_num} API call returned quota limit error: {page_text.strip()}")
            else:
                print(f"Page {page_num} successfully processed!")
                p['content'] = page_text
                p['has_error'] = False
                success_count += 1
                
        except Exception as e:
            print(f"Page {page_num} error calling API: {e}")
            
        if os.path.exists(img_path):
            os.remove(img_path)
            
    # Clean up temp folder
    try:
        os.rmdir(temp_dir)
    except Exception:
        pass
        
    # Save the progress
    save_markdown_pages(md_path, pages)
    print(f"Successfully recovered {success_count}/{len(failed_pages)} pages.")
    return success_count > 0

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python recover_ocr.py <markdown_path> <pdf_path> [space_id] [hf_token]")
    else:
        md = sys.argv[1]
        pdf = sys.argv[2]
        space = sys.argv[3] if len(sys.argv) > 3 else "prithivMLmods/Multimodal-OCR"
        token = sys.argv[4] if len(sys.argv) > 4 else None
        recover_pages(md, pdf, space, token)

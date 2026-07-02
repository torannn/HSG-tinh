import os
import sys
import json
import re
import shutil
import subprocess
import webbrowser
import socket
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).resolve().parent
STYLE_CONFIG_PATH = ROOT / 'styles_config.json'
FOLDERS_CONFIG_PATH = ROOT / 'folders_config.json'

def load_folders_config():
    default_config = {
        'input_dir': str(ROOT / 'another example'),
        'output_dir': str(ROOT / 'generated_ex_test' / 'hsg-12-khao-sat-ham-so')
    }
    if FOLDERS_CONFIG_PATH.exists():
        try:
            with open(FOLDERS_CONFIG_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'input_dir' in data and 'output_dir' in data:
                    return data
        except Exception as e:
            print(f"Error loading folders_config.json: {e}")
    return default_config

def save_folders_config(config_data):
    try:
        with open(FOLDERS_CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving folders_config.json: {e}")
        return False

# Mặc định seed từ parse_olmocr nếu chưa có file json
def load_base_styles():
    try:
        sys.path.append(str(ROOT))
        import parse_olmocr
        return parse_olmocr.STYLES
    except Exception as e:
        print(f"Error loading base styles from parse_olmocr: {e}")
        return {}

# Đảm bảo có tệp cấu hình styles và chứa đầy đủ các theme cơ bản từ parse_olmocr
base_styles = load_base_styles()
if STYLE_CONFIG_PATH.exists():
    try:
        with open(STYLE_CONFIG_PATH, 'r', encoding='utf-8') as f:
            existing_styles = json.load(f)
        # Bổ sung các theme cơ bản chưa có vào file config
        updated = False
        for k, v in base_styles.items():
            if k not in existing_styles:
                existing_styles[k] = v
                updated = True
            else:
                # Cập nhật các trường cấu hình mới cho các theme cũ nếu chưa có
                for field_k, field_v in v.items():
                    if field_k not in existing_styles[k]:
                        existing_styles[k][field_k] = field_v
                        updated = True
        if updated:
            with open(STYLE_CONFIG_PATH, 'w', encoding='utf-8') as f:
                json.dump(existing_styles, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error merging styles_config.json with base styles: {e}")
else:
    with open(STYLE_CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(base_styles, f, indent=4, ensure_ascii=False)

class CustomHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Tắt logging mặc định để console sạch sẽ
        return

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/' or path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            with open(ROOT / 'index.html', 'rb') as f:
                self.wfile.write(f.read())
            return

        elif path == '/api/styles':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            with open(STYLE_CONFIG_PATH, 'rb') as f:
                self.wfile.write(f.read())
            return

        elif path == '/api/icons':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            filepath = ROOT / 'icons_data.json'
            if filepath.exists():
                with open(filepath, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(b"[]")
            return

        elif path == '/api/info':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            folders = load_folders_config()
            
            input_path = Path(folders['input_dir'])
            tex_files = []
            if input_path.exists() and input_path.is_dir():
                tex_files = [f.name for f in sorted(input_path.glob("*.tex"))]
                
            info_data = {
                'root_dir': str(ROOT),
                'input_dir': folders['input_dir'],
                'output_dir': folders['output_dir'],
                'tex_files': tex_files
            }
            self.wfile.write(json.dumps(info_data).encode('utf-8'))
            return

        elif path == '/api/preview_images':
            query = parse_qs(parsed_path.query)
            doc_type = query.get('doc_type', ['de-thi'])[0]
            file_prefix = query.get('file_prefix', [''])[0]
            
            folders = load_folders_config()
            out_dir = Path(folders['output_dir'])
            prefix = file_prefix if file_prefix else doc_type
            
            preview_images = []
            if out_dir.exists():
                for f in sorted(out_dir.glob(f"{prefix}_preview-*.png")):
                    preview_images.append(f"/serve_preview/{f.name}")
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({'images': preview_images}).encode('utf-8'))
            return

        elif path.startswith('/serve_preview/'):
            filename = path.replace('/serve_preview/', '')
            filename = os.path.basename(filename)
            folders = load_folders_config()
            filepath = Path(folders['output_dir']) / filename
            
            if filepath.exists() and filepath.suffix.lower() == '.png':
                self.send_response(200)
                self.send_header('Content-Type', 'image/png')
                self.end_headers()
                with open(filepath, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
            return

        elif path == '/api/browse_folder':
            query = parse_qs(parsed_path.query)
            initial_dir = query.get('initial_dir', [''])[0]
            
            try:
                import tkinter as tk
                from tkinter import filedialog
                
                root = tk.Tk()
                root.withdraw()
                root.attributes("-topmost", True)
                
                if not initial_dir or not os.path.exists(initial_dir):
                    initial_dir = str(ROOT)
                    
                selected_dir = filedialog.askdirectory(
                    initialdir=initial_dir,
                    title="Chọn Thư Mục"
                )
                root.destroy()
                
                if selected_dir:
                    selected_dir = os.path.normpath(selected_dir)
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps({'success': True, 'directory': selected_dir}).encode('utf-8'))
                else:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps({'success': False, 'message': 'Cancelled'}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'message': str(e)}).encode('utf-8'))
            return

        # Fallback serve static file nếu cần
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8')) if post_data else {}
        except Exception:
            data = {}

        if path == '/api/save_style':
            name = data.get('name')
            theme_data = data.get('data')
            
            if not name or not theme_data:
                self.send_json_response(400, {'success': False, 'message': 'Missing data'})
                return
                
            try:
                with open(STYLE_CONFIG_PATH, 'r', encoding='utf-8') as f:
                    styles = json.load(f)
                
                styles[name] = theme_data
                
                with open(STYLE_CONFIG_PATH, 'w', encoding='utf-8') as f:
                    json.dump(styles, f, indent=4, ensure_ascii=False)
                
                self.send_json_response(200, {'success': True})
            except Exception as e:
                self.send_json_response(500, {'success': False, 'message': str(e)})
            return

        elif path == '/api/delete_style':
            name = data.get('name')
            if not name:
                self.send_json_response(400, {'success': False, 'message': 'Missing name'})
                return
                
            try:
                with open(STYLE_CONFIG_PATH, 'r', encoding='utf-8') as f:
                    styles = json.load(f)
                
                if name in styles:
                    del styles[name]
                    with open(STYLE_CONFIG_PATH, 'w', encoding='utf-8') as f:
                        json.dump(styles, f, indent=4, ensure_ascii=False)
                    self.send_json_response(200, {'success': True})
                else:
                    self.send_json_response(404, {'success': False, 'message': 'Theme not found'})
            except Exception as e:
                self.send_json_response(500, {'success': False, 'message': str(e)})
            return

        elif path == '/api/set_folders':
            input_dir = data.get('input_dir')
            output_dir = data.get('output_dir')
            if not input_dir or not output_dir:
                self.send_json_response(400, {'success': False, 'message': 'Missing folders'})
                return
            
            config_data = {
                'input_dir': input_dir,
                'output_dir': output_dir
            }
            if save_folders_config(config_data):
                input_path = Path(input_dir)
                tex_files = []
                if input_path.exists() and input_path.is_dir():
                    tex_files = [f.name for f in sorted(input_path.glob("*.tex"))]
                
                self.send_json_response(200, {
                    'success': True,
                    'input_dir': input_dir,
                    'output_dir': output_dir,
                    'tex_files': tex_files
                })
            else:
                self.send_json_response(500, {'success': False, 'message': 'Could not save folder config'})
            return

        elif path == '/api/select_file':
            filename = data.get('file')
            folders = load_folders_config()
            file_path = Path(folders['input_dir']) / filename
            if file_path.exists():
                self.send_json_response(200, {'success': True, 'file': filename})
            else:
                self.send_json_response(404, {'success': False, 'message': f'File {filename} not found'})
            return

        elif path == '/api/open_folder':
            try:
                folders = load_folders_config()
                out_dir = Path(folders['output_dir'])
                out_dir.mkdir(parents=True, exist_ok=True)
                if sys.platform == 'win32':
                    os.startfile(out_dir)
                elif sys.platform == 'darwin':
                    subprocess.run(['open', str(out_dir)])
                else:
                    subprocess.run(['xdg-open', str(out_dir)])
                self.send_json_response(200, {'success': True})
            except Exception as e:
                self.send_json_response(500, {'success': False, 'message': str(e)})
            return

        elif path == '/api/run_parser':
            action = data.get('action', 'ocr')
            style_name = data.get('style_name', 'violet-emerald')
            selected_file = data.get('file')
            
            folders = load_folders_config()
            input_dir = folders['input_dir']
            output_dir = folders['output_dir']
            
            cmd = [sys.executable, str(ROOT / 'parse_olmocr.py'), style_name]
            if action == 'inject_single':
                cmd += ['--action', 'inject_single', '--input_dir', input_dir, '--output_dir', output_dir, '--file', selected_file]
            elif action == 'inject_all':
                cmd += ['--action', 'inject_all', '--input_dir', input_dir, '--output_dir', output_dir]
            else:  # ocr
                cmd += ['--action', 'ocr', '--output_dir', output_dir]
                
            result = subprocess.run(cmd, capture_output=True, cwd=str(ROOT))
            
            success = result.returncode == 0
            stdout = result.stdout.decode('utf-8', errors='replace') if result.stdout else ""
            stderr = result.stderr.decode('utf-8', errors='replace') if result.stderr else ""
            output = stdout + "\n" + stderr
            
            self.send_json_response(200, {
                'success': success,
                'output': output
            })
            return

        elif path == '/api/compile':
            compile_type = data.get('compile_type')
            selected_file = data.get('file')
            doc_type = data.get('doc_type', 'all')
            
            folders = load_folders_config()
            out_dir = Path(folders['output_dir'])
            
            files_to_compile = []
            if compile_type == 'single':
                if selected_file:
                    file_prefix = Path(selected_file).stem
                    files_to_compile = [file_prefix]
                else:
                    self.send_json_response(400, {'success': False, 'message': 'Missing file to compile'})
                    return
            elif compile_type == 'all':
                if out_dir.exists():
                    files_to_compile = [f.stem for f in sorted(out_dir.glob("*.tex")) if f.name != 'ex_test.sty' and f.name != 'body.tex' and not f.name.endswith('-body.tex')]
                if not files_to_compile:
                    self.send_json_response(400, {'success': False, 'message': 'No TeX files found in output directory to compile'})
                    return
            else:
                if doc_type == 'all':
                    files_to_compile = ['de-thi', 'de-va-loigiai', 'dap-an']
                else:
                    files_to_compile = [doc_type]
                    
            total_output = ""
            success = True
            
            for file_prefix in files_to_compile:
                tex_file = out_dir / f"{file_prefix}.tex"
                if not tex_file.exists():
                    total_output += f"[Lỗi] Không tìm thấy file {file_prefix}.tex\n"
                    success = False
                    continue
                
                total_output += f"--- Bắt đầu biên dịch {file_prefix}.tex ---\n"
                
                # Biên dịch lần 1
                cmd = ["pdflatex", "-interaction=nonstopmode", f"{file_prefix}.tex"]
                res = subprocess.run(cmd, capture_output=True, cwd=str(out_dir))
                stdout = res.stdout.decode('utf-8', errors='replace') if res.stdout else ""
                stderr = res.stderr.decode('utf-8', errors='replace') if res.stderr else ""
                total_output += stdout
                
                if res.returncode != 0:
                    total_output += f"[Lỗi] Biên dịch lần 1 của {file_prefix}.tex thất bại với mã thoát {res.returncode}.\n"
                    total_output += stderr + "\n"
                    success = False
                    continue
                
                # Biên dịch lần 2 để hoàn thiện bảng đáp án và số trang
                res = subprocess.run(cmd, capture_output=True, cwd=str(out_dir))
                stdout2 = res.stdout.decode('utf-8', errors='replace') if res.stdout else ""
                total_output += f"--- Biên dịch lần 2 của {file_prefix}.tex ---\n"
                total_output += stdout2
                
                # Xóa các ảnh preview cũ
                for old_preview in out_dir.glob(f"{file_prefix}_preview-*.png"):
                    try:
                        old_preview.unlink()
                    except Exception:
                        pass
                
                # Sinh ảnh xem trước (tối đa 4 trang đầu)
                pdf_file = out_dir / f"{file_prefix}.pdf"
                if pdf_file.exists():
                    total_output += f"[Hệ thống] Đang sinh ảnh xem trước cho {file_prefix}.pdf...\n"
                    ppm_cmd = ["pdftoppm", "-png", "-r", "120", "-f", "1", "-l", "4", f"{file_prefix}.pdf", f"{file_prefix}_preview"]
                    subprocess.run(ppm_cmd, capture_output=True, cwd=str(out_dir))
            
            self.send_json_response(200, {
                'success': success,
                'output': total_output
            })
            return

        self.send_response(404)
        self.end_headers()

    def send_json_response(self, status, payload):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode('utf-8'))

def find_free_port():
    # Tìm cổng rảnh ngẫu nhiên nếu 8080 bị bận
    for port in [8080, 8081, 8082, 5000, 5001]:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind(('127.0.0.1', port))
            s.close()
            return port
        except OSError:
            continue
    # Dự phòng cổng động bất kỳ
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 0))
    port = s.getsockname()[1]
    s.close()
    return port

def main():
    port = find_free_port()
    server_address = ('127.0.0.1', port)
    
    httpd = HTTPServer(server_address, CustomHandler)
    url = f"http://127.0.0.1:{port}/"
    print(f"==================================================")
    print(f"  HSG LaTeX Customizer GUI Server is running")
    print(f"  URL: {url}")
    print(f"  Press Ctrl+C in Terminal to stop the server")
    print(f"==================================================")
    
    # Tự động mở trình duyệt
    webbrowser.open(url)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()
        print("Server stopped successfully.")

if __name__ == '__main__':
    main()

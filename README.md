# Bộ Chuyển Đổi Định Dạng và Style LaTeX (JSON -> ex-test.sty)

Dự án này cung cấp các công cụ và giao diện hỗ trợ chuyển đổi dữ liệu tài liệu (từ OCR Markdown/JSON) thành mã nguồn LaTeX hoàn chỉnh, tương thích tốt với gói lệnh định dạng đề thi/câu hỏi chuyên nghiệp `ex_test.sty`.

## 📌 Các Tính Năng Chính
- **Phân Tích OCR & Định Dạng Câu Hỏi**: Hỗ trợ chuyển đổi văn bản thô, tài liệu Markdown từ các mô hình OCR (như MinerU, olmocr) thành cấu trúc câu hỏi của gói lệnh `ex-test`.
- **Hệ Thống Theme Đa Dạng**: Cho phép chọn lựa và tinh chỉnh giao diện đề thi thông qua cấu hình màu sắc (Primary/Accent Colors), font chữ (Open Sans, Palatino, Helvetica), kiểu khung tiêu đề đầu trang/cuối trang, và cách hiển thị nhãn câu hỏi (Ví dụ: `hoang-decor`, `blue-pink`, `elegant-book`, `cyberpunk`).
- **Giao Diện GUI Thân Thiện**: Cung cấp ứng dụng desktop viết bằng Python Tkinter (`app_gui.py`) giúp trực quan hóa cấu hình và thực hiện chuyển đổi nhanh chóng.

---

## 📂 Cấu Trúc Thư Mục Dự Án
```text
├── ex_test/                    # Thư mục chứa gói lệnh ex_test.sty và các file tài liệu mẫu
│   ├── ex_test.sty             # Gói định dạng câu hỏi & đề thi LaTeX cốt lõi
│   └── VD De DGNL.tex          # Ví dụ minh họa đề thi ĐGNL sử dụng ex_test
├── another example/            # Thư mục chứa tài liệu minh họa khác
│   └── DeMH.tex                # Mã nguồn đề minh họa mẫu
├── scratch/                    # Các đoạn mã script nháp để kiểm tra log và thử nghiệm styles
│   ├── read_log.py             # Script kiểm tra và phân tích lỗi từ file log compile LaTeX
│   ├── search_errors.py        # Tìm kiếm nhanh các dòng lỗi bắt đầu bằng dấu "!" trong log
│   └── update_styles.py        # Cập nhật thêm các trường cấu hình mặc định vào styles_config.json
├── app_gui.py                  # Mã nguồn chương trình giao diện cấu hình và điều khiển chính
├── convert_clean_to_ex_test.py # Chuyển đổi mã LaTeX thô sang định dạng ex_test tương thích
├── parse_olmocr.py             # Xử lý kết quả OCR từ olmocr.md sang định dạng câu hỏi LaTeX
├── recover_ocr.py              # Script hỗ trợ khôi phục các trang OCR bị lỗi hoặc mất dữ liệu
├── styles_config.json          # Tệp cấu hình lưu trữ các theme và tùy biến style hiển thị
└── folders_config.json         # Tệp lưu cấu hình đường dẫn thư mục đầu vào và đầu ra mặc định
```

---

## 🛠️ Hướng Dẫn Sử Dụng

### 1. Cài đặt các thư viện cần thiết
Các script tự động kiểm tra và cài đặt thư viện cần thiết khi chạy. Bạn cũng có thể cài đặt thủ công:
```bash
pip install pymupdf gradio_client
```

### 2. Khởi chạy Giao diện điều khiển (GUI)
Để mở ứng dụng GUI quản lý và chuyển đổi cấu hình style đề thi:
```bash
python app_gui.py
```
Ứng dụng sẽ tự động tải các cấu hình từ `styles_config.json` và lưu lại lịch sử làm việc của bạn vào `folders_config.json`.

### 3. Biên dịch kết quả LaTeX
Kết quả sau chuyển đổi sẽ nằm trong thư mục `generated_ex_test/`. Bạn chỉ cần sử dụng trình biên dịch LaTeX yêu thích của mình (như TeXstudio hoặc Overleaf) chạy với engine **XeLaTeX** hoặc **LuaLaTeX** để xuất ra file PDF hoàn thiện.

---

## 📦 Phát Triển Và Triển Khai (GitHub)
Dự án được cấu hình loại trừ các tệp dữ liệu lớn (PDF, DOCX) cũng như các tệp biên dịch tạm thời của LaTeX (`.aux`, `.log`, `.synctex.gz`) thông qua tệp `.gitignore` nhằm đảm bảo dung lượng lưu trữ nhẹ nhàng và tập trung hoàn toàn vào mã nguồn xử lý.

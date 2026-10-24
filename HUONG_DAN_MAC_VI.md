# Hướng dẫn sử dụng bộ dự án lung_4dct_project đã sửa (macOS)

## Thay thế thư mục cũ mà không mất dữ liệu

1. **Đừng xóa ngay thư mục cũ trên Mac.** Trong Finder, đổi tên thư mục hiện tại `lung_4dct_project` thành `lung_4dct_project_BACKUP`.
2. Giải nén file ZIP `lung_4dct_project_CLEAN_FULL.zip` trong cùng vị trí. Bạn sẽ nhận một thư mục mới tên `lung_4dct_project`.
3. Mở thư mục mới. `manuscript.docx`, `manuscript.pdf`, các biểu đồ và `simulation_results.json` đã được cập nhật và đồng bộ từ phép chạy kiểm chứng.
4. Nếu cần chạy lại code: mở Terminal, nhập `bash ` (có dấu cách), kéo `RUN_ON_MAC.command` từ Finder vào cửa sổ Terminal và nhấn Return.
5. Đọc kết quả dòng `PASS` của `validate_project.py` (script Mac đã gọi tự động). Sau khi kiểm tra xong mới cân nhắc bỏ bản backup cũ.

## Tại sao đã xóa/di chuyển một số file?

- Xóa khỏi dự án sạch: thư mục `__MACOSX`, `.DS_Store`, `__pycache__`, `.pyc` và các script tạo tài liệu đời cũ có đường dẫn cứng `/Users/...` hoặc nội dung không còn khớp số liệu.
- Bộ script đời cũ và PDF/DOCX/TeX cũ vẫn có **bản backup ZIP riêng** và lịch sử `.git` được giữ nguyên. Nếu cần phục hồi, không mất khả năng truy xuất.
- Các hồ sơ gửi tạp chí chuyển vào `submission/` (giữ lại chứ không xóa). Phải duyệt lại cover letter/reviewer list trước khi gửi.
- `extras/tcia_loader.py` là mô-đun tùy chọn để tải CT; bạn cần cài `pydicom` nếu dùng. Chưa có dữ liệu bệnh nhân trong dự án này.
- `data/*.csv` được sinh lại theo T6 và kết quả JSON hiện tại. `data/*.npz` là phantom minh họa *riêng biệt*, có seed cố định, không phải bộ bệnh nhân thực.

## Các file nên dùng

- `main.py`: chạy mô phỏng và sinh lại JSON + 6 hình.
- `simulation_results.json`: dữ liệu đầu ra chính của nghiên cứu (có dữ liệu từng bệnh nhân/fraction và từng chu kỳ sub-voxel).
- `manuscript.docx` và `manuscript.pdf`: bài báo sửa đúng các lỗi thống kê được phát hiện.
- `generate_datasets.py`: sinh lại dữ liệu CSV/NPZ.
- `generate_project_docs.py`: đồng bộ README và report.html từ JSON.
- `validate_project.py`: kiểm tra số liệu, CI và dữ liệu.
- `README.md`: tiếng Anh cho repository và hướng dẫn tái lập.

## Các điều chưa được chứng minh

- Đây vẫn là **mô phỏng phantom**, chưa dùng CT bệnh nhân thật, chưa có phân bố liều xạ 4D và chưa mô phỏng chỉnh tư thế CBCT.
- So sánh sub-voxel dùng điểm mẫu trên mask voxel, **không phải phép đo continuous ground truth**. Chưa có kiểm định hội tụ theo N_sub/độ phân giải.
- Không được suy luận margin 5 mm luôn an toàn trên lâm sàng hoặc đo được tỉ lệ kiểm soát khối u từ các CR hình học.
- ZIP đã cập nhật ở môi trường kiểm thử. Nó **không tự thay đổi ổ đĩa Mac và không đẩy file lên GitHub** cho đến khi bạn thay thư mục hoặc chạy script trên Mac.

# V10 — Sửa Figure 5/6 và đồng bộ bản thảo

## Những thay đổi đã thực hiện

1. **Figure 6A — đủ 6.000 fractions / chiến lược:** `main.py` lấy dữ liệu từ `raw_fraction_cr_by_patient` (200 x 30) thay vì trường preview cũ chỉ giữ 300 giá trị. `raw_fraction_crs` trong JSON và kết quả tái chạy hiện lưu **đầy đủ** fractions cho mọi cohort.
2. **Figure 6B — cùng định nghĩa all-pass:** cả ba cột đều sử dụng `patient_all_fraction_success_pct`: SBRT 3/3, SBRT 5/5 và CFRT 30/30 fractions đạt CRmin >=95%. Bổ sung Wilson CI cho mỗi tỷ lệ cấp bệnh nhân. Các cohort độc lập và độ dài liệu trình khác nhau, không được diễn giải thành so sánh hiệu quả lâm sàng.
3. **CFRT >=90% được báo cáo riêng:** tỷ lệ bệnh nhân có **ít nhất 27/30 fractions** đạt ngưỡng vẫn có trong JSON dưới `patient_course_avg_success_pct`, nhưng **không hiển thị chung** với biểu đồ all-pass. Với ITV + 5 mm, CFRT all-pass 6.5% còn phân tích thăm dò >=27/30 là 46.5%. Ngưỡng 90% chỉ là lựa chọn thiết kế mô phỏng, không phải chỉ dẫn lâm sàng.
4. **Figure 5 — n=500:** ghi rõ 500 chu kỳ / biên độ / chiến lược, bảy mức biên độ 10–22 mm; các quỹ đạo dùng cho các chiến lược không được ghép cặp ở thí nghiệm stress này.
5. **Word/PDF:** cập nhật Methods, mục 3.5, Figure 5 và Figure 6, cập nhật caption, giữ nguyên Table 1–5, xuất PDF 8 trang và xem trực tiếp các trang.
6. **README và report:** cập nhật bằng generator từ `simulation_results.json` và thêm giải thích Figure 5/6; `validate_project.py` có kiểm tra mới để ngăn lỗi dùng 300 thay cho 6.000 giá trị.

## Kiểm tra đã làm

- `python validate_project.py` → PASS với dữ liệu đã lưu.
- Kiểm tra cú pháp `main.py`, `generate_project_docs.py`, `validate_project.py`.
- Tạo lại Figure 1–6 từ JSON đã lưu qua `generate_publication_figures()`; không thay đổi ước lượng thống kê đã công bố.
- Xuất Word thành PDF bằng công cụ dựng tài liệu, kiểm tra hình ảnh các trang có Figure 5/6.

## Giới hạn cần biết

- **Không chạy lại toàn bộ 5.000 chu kỳ Monte Carlo hoặc 7.600 phiên điều trị** trong vòng sửa V10; hình và bảng được đồng bộ từ JSON trước đó.
- **Chưa xác minh trên máy Mac của bạn**; việc tải và giải nén ZIP chỉ tạo ra thư mục mới trên Mac, không tự sửa thư mục cũ.
- Không bổ sung dữ liệu bệnh nhân, mô phỏng CBCT hoặc tính liều. Kết quả chỉ là mô phỏng hình học.

## Cách thay thư mục trên Mac

1. Đổi tên thư mục cũ thành `lung_4dct_project_BACKUP`.
2. Giải nén ZIP mới (thư mục bên trong đã tên `lung_4dct_project`).
3. Mở Terminal trong thư mục này. Chạy `python3 validate_project.py` khi đã cài các thư viện trong `requirements.txt`, hoặc `bash RUN_ON_MAC.command` nếu muốn **chạy lại** toàn bộ pipeline (chương trình ghi đè các output *sinh tự động* trong thư mục này).
4. Nếu dùng Git, kiểm tra `git diff` trước khi commit/push; gói ZIP giữ `.git`, chưa tự commit thay đổi.

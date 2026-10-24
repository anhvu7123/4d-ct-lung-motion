# Bản sửa V9 – đồng bộ bài báo với dữ liệu mô phỏng

Nguồn chỉnh sửa: `manuscript(6).pdf` và bản Word tương ứng `manuscript.docx` trong bộ dự án `lung_4dct_project_CLEAN_FULL.zip`.

## Những mục đã hoàn tất

1. **Methods, phần Inference (trang 3):** Loại bỏ câu nói JSON không có dữ liệu theo bệnh nhân. File `simulation_results.json` thực tế chứa `raw_fraction_cr_by_patient`, `per_patient_fraction_pass_counts` trong `setup_uncertainty` và quan sát ghép cặp từng chu kỳ trong `subvoxel_sensitivity`.
2. **Table 5:** Bổ sung cột `Paired bootstrap 95% CI (pp)` từ `simulation_results.json` (không tính bịa số). Các khoảng: Isotropic 5 mm `[0.0, 0.0]`, ITV + 3 mm `[+1.4, +5.9]`, ITV + 4 mm `[-0.1, +0.7]`, ITV + 5 mm `[-3.6, -1.4]`, Aniso + 2 mm `[0.0, +2.5]`.
3. **Methods 2.5 và Results 3.6:** Giải thích độ chênh pass rate được tính trên **cùng 1.000 chu kỳ** và khoảng tin cậy được bootstrap **2.000 lần trên các cặp**, không phải so sánh các mẫu độc lập. CI không giải quyết sai số do 2.500 điểm mẫu chưa hội tụ.
4. **Reference [16]:** Sửa tiêu đề chính xác thành “Quality assurance for image-guided radiation therapy utilizing CT-based technologies: a report of the AAPM TG-179” và thêm DOI `10.1118/1.3690466` (Med Phys. 2012;39(4):1946-1963).
5. **Dàn trang:** Table 3 nằm trọn một trang, không bị chia trang 4–5; Table 5 và các hàng được giữ nguyên; loại bỏ footer chú thích sửa nội bộ. Phiên bản mới vẫn 8 trang.
6. **Figure 4:** Dời nhãn ITV và Anisotropic sang hai hàng riêng, có đường dẫn xuống đúng tọa độ và giữ nguyên dữ liệu. Cập nhật luôn đoạn code tạo Figure 4 trong `main.py` để lần chạy trên Mac sau không quay lại tình trạng chồng chữ.

## Kiểm tra

- `python validate_project.py`: xác thực JSON, dữ liệu raw và CSV.
- `python verify_manuscript_v9.py`: so sánh Table 5 + thông tin công bố dữ liệu với JSON.
- Đã render DOCX và kiểm tra trực quan PDF.

## Chưa được làm / hạn chế

- Không thay đổi kết quả gốc hoặc chạy lại thuật toán 7.600 fraction trong vòng sửa này.
- Vẫn chưa có kiểm định hội tụ point-cloud theo nhiều kích thước mẫu, validation trên 4D-CT bệnh nhân, 4D dose accumulation hoặc mô phỏng CBCT correction. Không khẳng định hiệu quả lâm sàng.
- Nếu mô phỏng lại và kết quả thay đổi, cần cập nhật số trong manuscript và kiểm tra lại trước khi gửi.

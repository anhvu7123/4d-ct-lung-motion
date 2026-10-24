# Nhật ký sửa và dọn dẹp — ngày 24/10/2026

## Sửa code

- `main.py` **không còn ghi ra đường dẫn cứng** `/Users/carwyn/.gemini/antigravity/...`: JSON và 6 biểu đồ luôn được lưu ngay cạnh `main.py`, chạy ở vị trí thư mục bất kỳ trên Mac.
- Giữ thuật toán nghiên cứu đã có và các random seeds của ba cohort (42, 43, 44). Không tự thay các số liệu thực nghiệm.
- Sửa kết luận sub-voxel trong JSON: pass-rate chênh lệch tối đa **3,7 điểm phần trăm**, không phải <=2,7 hay 'không ảnh hưởng'.
- Lưu **1.000 cặp** min-CR discrete/point-cloud theo mỗi chiến lược cùng bootstrap paired CI, độ lệch trung bình, threshold disagreement.
- Lưu **đầy đủ** ma trận min-CR 200 bệnh nhân x (3/5/30 fractions) cho mọi chiến lược, cùng số fraction pass từng bệnh nhân; sử dụng patient-cluster bootstrap hiện có (B=2.000).
- Viết lại `generate_datasets.py` phù hợp JSON phiên bản hiện hành, sửa tham chiếu T5 thành **T6**, sửa tên biến 'ICRU compliant' thành 'study-defined geometric CR'.
- Thêm `generate_project_docs.py`, `validate_project.py`, `RUN_ON_MAC.command`.

## Kết quả đã kiểm tra bằng chạy lại (trong môi trường hiện tại)

- Pipeline chạy thành công: 5.000 unseen MC cycles; 1.000 paired sub-voxel cycles x 2.500 points; 200 bệnh nhân *mỗi* phác đồ; 7.600 tổng fractions.
- Irregular pass: ITV + 3 mm = **68,26%**, ITV + 5 mm = **96,24%** (nominal discrete algorithm).
- 5-fx SBRT ITV + 5 mm whole-course all-pass = **53,0%**; CFRT 30-fx fraction pass = **82,7167%**, CI patient-cluster bootstrap = **[80,48%; 84,88%]**.
- Sub-voxel pass ITV + 3 mm: **68,7% vs 72,4%**, paired bootstrap Δ CI **[1,40;5,90] điểm %**.
- Sub-voxel pass ITV + 5 mm: **97,0% vs 94,5%**, paired bootstrap Δ CI **[-3,60;-1,40] điểm %**.
- `validate_project.py`: PASS, so khớp full patient matrices, 1.000 paired observations, T6 reference, CSV and manuscript summary.

## Dọn dẹp

- Bỏ file sinh bởi macOS `__MACOSX`, `.DS_Store` và Python cache.
- Bỏ 13 script tạo PDF/Word cũ hoặc humanize/upgrade, vì chứa đường dẫn cứng và có thể ghi đè bài báo mới bằng số liệu cũ. Tất cả được giữ trong ZIP sao lưu riêng; lịch sử `.git` vẫn giữ.
- Bỏ ba `Figure_1..3.png` bản cũ trùng chức năng, giữ 6 `fig1_...` đến `fig6_...` cập nhật; bản cũ trong sao lưu.
- Chuyển cover letter, graphical abstract, highlights, suggested reviewers sang `submission/`; `tcia_loader.py` sang `extras/`.
- Không xóa Git history, CSV/NPZ, mã mô phỏng, các bảng và hình hiện hành.
- Sửa manuscript Word và xuất PDF từ cùng tài liệu; 8 trang, không còn trang gần trắng / caption rơi trang.

## Hạn chế còn lại

- Không có validation trên 4D-CT lâm sàng/4D liều, phân tích hội tụ sub-voxel hay hiệu quả CBCT thực nghiệm; không bổ sung số liệu không có bằng chứng.
- Những bản `submission/` chưa được xác thực theo hướng dẫn tạp chí cụ thể.
- Lần chạy trên máy Mac cần môi trường Python phù hợp. `RUN_ON_MAC.command` chỉ ảnh hưởng thư mục dự án mới và `.venv/` bên trong.

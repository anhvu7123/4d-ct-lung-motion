# In Silico 4D-CT Lung Tumor Motion & PTV Margin Optimization Project

**Tác giả:** Vũ Minh Anh (18-11-2006)  
**Đề tài:** In Silico 4D-CT-Based Tumor Motion Modeling and Quantitative Evaluation of PTV Margins for Lung Radiotherapy Planning  
**Target Journal:** Computers in Biology and Medicine (Elsevier)  
**GitHub Repository:** https://github.com/anhvu7123/4d-ct-lung-motion  

---

## 📁 Cấu trúc Thư mục Dự án

```
lung_4dct_project/
├── main.py              # File code Python chính (Mô phỏng 4D-CT, Centroid Tracking, PTV Margins)
├── requirements.txt     # Danh sách thư viện cần thiết (numpy, scipy, matplotlib)
├── report.html          # Báo cáo tương tác giao diện trực quan (Mở bằng trình duyệt)
└── README.md            # Hướng dẫn sử dụng
```

## 🚀 Cách Chạy Dự án trên VS Code

1. **Mở thư mục trên VS Code:**
   - Trong VS Code: Chọn `File` -> `Open Folder...` -> Chọn thư mục `lung_4dct_project`.

2. **Cài đặt thư viện:**
   - Mở Terminal trong VS Code (`Ctrl + ~` hoặc `Cmd + ~`) và gõ:
   ```bash
   pip install -r requirements.txt
   ```

3. **Chạy mô phỏng:**
   - Bấm nút **Run Python File** (nút tam giác ở góc phải trên cùng của VS Code) hoặc gõ:
   ```bash
   python3 main.py
   ```

4. **Xem kết quả:**
   - Kết quả số liệu và bảng IMRaD (Table 1, Table 2) sẽ in ngay trên Terminal của VS Code.
   - Nhấp đúp vào `report.html` để mở giao diện mô phỏng 4D trực quan trên trình duyệt (Chrome/Safari/Edge).

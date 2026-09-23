# Phiếu Nhận Xét Học Viên – CIE VIETNAM

Ứng dụng Streamlit tự động:

1. Mở màn hình chờ.
2. Upload file Excel `.xlsx`.
3. Tự động phân tích điểm và dữ liệu học viên.
4. Tự động tạo phiếu Word cho từng học viên.
5. Đóng toàn bộ phiếu thành `.zip` và tự động tải xuống (có nút tải lại nếu trình duyệt chặn).
6. Bấm **Thêm lớp khác** để xử lý lớp tiếp theo.

## Lớp E (4–6 tuổi)

Lớp E được đánh giá riêng theo hướng phù hợp với trẻ nhỏ, tập trung vào chuyên cần, mức độ tham gia, ghi nhớ và sự tự tin khi nói tiếng Anh. Các mức hiển thị trên phiếu là:

- Tốt
- Khá
- Đang phát triển
- Cần thêm hỗ trợ

## Chạy ứng dụng

```bash
pip install -r requirements.txt
streamlit run app.py
```

Thư mục `assets/` chứa hình nền chờ và nhạc nền của ứng dụng.

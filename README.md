# Tổng Quan Dự Án N-Puzzle Solver

Dự án này là một ứng dụng web giải bài toán N-Puzzle (trò chơi xếp hình trượt) sử dụng thuật toán A* (A-star) với heuristic khoảng cách Manhattan. Ứng dụng cho phép người dùng:
- Sinh ra một trạng thái bàn cờ n-puzzle ngẫu nhiên có thể giải được.
- Kiểm tra trạng thái bàn cờ có giải được không.
- Tìm lời giải tối ưu cho trạng thái n-puzzle bằng thuật toán A*.

## Công Nghệ Sử Dụng
- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS, JavaScript
- **Thư viện hỗ trợ:** numpy, heapq, flask_cors

## Chức Năng Chính
- **Sinh bàn cờ:** Tạo ra một trạng thái n-puzzle ngẫu nhiên hợp lệ.
- **Kiểm tra tính khả giải:** Xác định trạng thái bàn cờ có thể giải được hay không.
- **Giải n-puzzle:** Tìm đường đi ngắn nhất từ trạng thái hiện tại về trạng thái đích.
- **Thống kê:** Trả về số bước, độ phức tạp không gian, thời gian và số node đã duyệt.

## Hướng Dẫn Chạy Dự Án
### 1. Cài đặt môi trường
```bash
pip install -r requirements.txt
```

### 2. Chạy server Flask
```bash
python app.py
```
Server sẽ chạy ở địa chỉ: `http://localhost:5000`

### 3. Sử dụng giao diện web
Mở file `index.html` trên trình duyệt để sử dụng giao diện giải n-puzzle.

## API Backend
- `POST /api/solve`: Giải n-puzzle.
- `POST /api/generate`: Sinh bàn cờ ngẫu nhiên.
- `POST /api/check`: Kiểm tra tính khả giải.

## Tác giả
- [Tên nhóm hoặc cá nhân]
- [Thông tin liên hệ nếu cần] 

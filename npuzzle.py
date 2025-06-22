import tkinter as tk
from tkinter import messagebox, ttk
from heapq import heappush, heappop
import random
import os

# Silence deprecation warning
os.environ['TK_SILENCE_DEPRECATION'] = '1'

class NPuzzle:
    def __init__(self, n):
        self.n = n
        # Mục tiêu: các số tăng dần, ô trống (0) ở cuối
        self.goal = tuple(list(range(1, n*n)) + [0])

    def heuristic(self, state):
        """Tính tổng khoảng cách Manhattan của các ô tới vị trí mục tiêu."""
        dist = 0
        for idx, val in enumerate(state):
            if val == 0:
                continue
            # Tọa độ hiện tại
            x, y = divmod(idx, self.n)
            # Tọa độ mục tiêu của val (val từ 1..n*n-1)
            goal_x = (val-1) // self.n
            goal_y = (val-1) % self.n
            dist += abs(x - goal_x) + abs(y - goal_y)
        return dist

    def neighbors(self, state):
        """Sinh các trạng thái con sau một lần di chuyển ô trống."""
        n = self.n
        zero_idx = state.index(0)
        x, y = divmod(zero_idx, n)
        moves = []
        # Các hướng di chuyển của ô trống
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < n and 0 <= new_y < n:
                new_idx = new_x * n + new_y
                new_state = list(state)
                # Hoán đổi ô trống với ô chỉ định
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                moves.append(tuple(new_state))
        return moves

    def solve(self, start):
        """Áp dụng thuật toán A* để tìm đường đi từ start đến goal."""
        open_set = []
        # (f, g, state, parent_state)
        heappush(open_set, (self.heuristic(start), 0, start, None))
        came_from = {start: None}
        cost = {start: 0}

        while open_set:
            f, g, current, parent = heappop(open_set)
            # Nếu đạt mục tiêu, tái tạo đường đi
            if current == self.goal:
                path = []
                while current is not None:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]  # ngược lại

            # Mở rộng các trạng thái con
            for nxt in self.neighbors(current):
                new_g = g + 1
                # Nếu chưa gặp hoặc có đường đi tốt hơn
                if nxt not in cost or new_g < cost[nxt]:
                    cost[nxt] = new_g
                    priority = new_g + self.heuristic(nxt)
                    heappush(open_set, (priority, new_g, nxt, current))
                    came_from[nxt] = current
        return None  # nếu không tìm được giải pháp

class PuzzleGUI(tk.Frame):
    def __init__(self, master, n):
        super().__init__(master)
        self.n = n
        self.puzzle = NPuzzle(n)
        self.state = self.puzzle.goal
        self.tiles = []
        self.moves = 0
        self.dark_mode = False
        self.create_widgets()
        self.pack(padx=20, pady=20)

    def create_widgets(self):
        """Tạo lưới ô và các nút điều khiển."""
        # Frame cho các nút điều khiển
        control_frame = tk.Frame(self)
        control_frame.pack(pady=10)

        # Nút chọn kích thước
        size_frame = tk.Frame(control_frame)
        size_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(size_frame, text="Kích thước:", font=("Arial", 10)).pack(side=tk.LEFT)
        self.size_var = tk.StringVar(value=str(self.n))
        for size in [3, 4]:
            rb = tk.Radiobutton(size_frame, text=f"{size}x{size}", 
                               variable=self.size_var, value=str(size),
                               command=self.change_size,
                               font=("Arial", 10))
            rb.pack(side=tk.LEFT)

        # Nút xáo trộn
        style = ttk.Style()
        style.configure("Custom.TButton", padding=5)
        
        shuffle_btn = ttk.Button(control_frame, text="Xáo trộn", 
                               command=self.shuffle_puzzle,
                               style="Custom.TButton")
        shuffle_btn.pack(side=tk.LEFT, padx=10)

        # Nút giải tự động
        solve_btn = ttk.Button(control_frame, text="Giải A*", 
                             command=self.solve_puzzle,
                             style="Custom.TButton")
        solve_btn.pack(side=tk.LEFT, padx=10)

        # Nút chuyển đổi dark mode
        self.theme_btn = ttk.Button(control_frame, text="🌙 Dark Mode",
                                  command=self.toggle_theme,
                                  style="Custom.TButton")
        self.theme_btn.pack(side=tk.LEFT, padx=10)

        # Hiển thị số bước di chuyển
        self.moves_label = tk.Label(control_frame, 
                                  text="Số bước: 0",
                                  font=("Arial", 10, "bold"))
        self.moves_label.pack(side=tk.LEFT, padx=10)

        # Frame cho bảng puzzle
        self.board_frame = tk.Frame(self)
        self.board_frame.pack(pady=10)
        
        # Tạo lưới ô
        self.create_board()

    def create_board(self):
        """Tạo bảng puzzle."""
        self.tiles = []
        for i in range(self.n):
            row = []
            for j in range(self.n):
                val = self.state[i*self.n + j]
                text = '' if val == 0 else str(val)
                bg_color = "#2C3E50" if self.dark_mode else "#E3F2FD"
                fg_color = "white" if self.dark_mode else "black"
                label = tk.Label(self.board_frame, text=text, 
                               width=4, height=2,
                               font=("Arial", 16, "bold"),
                               borderwidth=2, relief="raised",
                               bg=bg_color if val != 0 else "#34495E" if self.dark_mode else "#BBDEFB",
                               fg=fg_color)
                label.grid(row=i, column=j, padx=5, pady=5)
                label.bind("<Button-1>", lambda e, r=i, c=j: self.on_click(r, c))
                row.append(label)
            self.tiles.append(row)

    def toggle_theme(self):
        """Chuyển đổi giữa light mode và dark mode."""
        self.dark_mode = not self.dark_mode
        self.theme_btn.config(text="☀️ Light Mode" if self.dark_mode else "🌙 Dark Mode")
        
        # Cập nhật màu nền
        bg_color = "#2C3E50" if self.dark_mode else "#F5F5F5"
        fg_color = "white" if self.dark_mode else "black"
        self.master.configure(bg=bg_color)
        self.configure(bg=bg_color)
        self.moves_label.configure(bg=bg_color, fg=fg_color)
        
        # Cập nhật bảng
        self.update_ui()

    def update_ui(self):
        """Cập nhật lại giao diện theo self.state hiện tại."""
        for i in range(self.n):
            for j in range(self.n):
                val = self.state[i*self.n + j]
                bg_color = "#2C3E50" if self.dark_mode else "#E3F2FD"
                fg_color = "white" if self.dark_mode else "black"
                self.tiles[i][j].config(
                    text='' if val == 0 else str(val),
                    bg=bg_color if val != 0 else "#34495E" if self.dark_mode else "#BBDEFB",
                    fg=fg_color
                )

    def change_size(self):
        """Thay đổi kích thước bảng."""
        new_size = int(self.size_var.get())
        if new_size != self.n:
            self.n = new_size
            self.puzzle = NPuzzle(new_size)
            self.state = self.puzzle.goal
            self.moves = 0
            self.moves_label.config(text="Số bước: 0")
            # Xóa và tạo lại giao diện
            self.board_frame.destroy()
            self.board_frame = tk.Frame(self)
            self.board_frame.pack(pady=10)
            self.create_board()

    def shuffle_puzzle(self):
        """Xáo trộn bảng puzzle."""
        # Tạo một trạng thái ngẫu nhiên có thể giải được
        state = list(range(self.n * self.n))
        random.shuffle(state)
        # Kiểm tra tính khả thi
        inversions = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i] != 0 and state[j] != 0 and state[i] > state[j]:
                    inversions += 1
        # Nếu số nghịch đảo là lẻ, hoán đổi 2 ô không phải ô trống
        if inversions % 2 == 1:
            for i in range(len(state)):
                if state[i] != 0 and state[i+1] != 0:
                    state[i], state[i+1] = state[i+1], state[i]
                    break
        self.state = tuple(state)
        self.moves = 0
        self.moves_label.config(text="Số bước: 0")
        self.update_ui()

    def on_click(self, row, col):
        """Xử lý khi người chơi click vào một ô."""
        idx = row * self.n + col
        zero_idx = self.state.index(0)
        zr, zc = divmod(zero_idx, self.n)
        if abs(zr - row) + abs(zc - col) == 1:
            new_state = list(self.state)
            new_state[zero_idx], new_state[idx] = new_state[idx], new_state[zero_idx]
            self.state = tuple(new_state)
            self.moves += 1
            self.moves_label.config(text=f"Số bước: {self.moves}")
            self.update_ui()
            # Kiểm tra chiến thắng
            if self.state == self.puzzle.goal:
                messagebox.showinfo("Chúc mừng!", 
                                  f"Bạn đã giải xong puzzle trong {self.moves} bước!")

    def solve_puzzle(self):
        """Khởi động thuật toán A* và chạy từng bước giải."""
        path = self.puzzle.solve(self.state)
        if path:
            self.moves = 0
            for step in path:
                self.state = step
                self.moves += 1
                self.moves_label.config(text=f"Số bước: {self.moves}")
                self.update_ui()
                self.after(200)  # đợi 200ms giữa các bước
            messagebox.showinfo("Hoàn thành!", 
                              f"Đã giải xong puzzle trong {self.moves} bước!")
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy giải pháp!")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("N-Puzzle Game")
    root.configure(bg="#F5F5F5")
    app = PuzzleGUI(root, 3)
    root.mainloop()

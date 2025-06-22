from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from heapq import heappush, heappop
import json
import time

app = Flask(__name__)
CORS(app)

class NPuzzleSolver:
    def __init__(self, n):
        self.n = n
        self.goal = tuple(list(range(1, n*n)) + [0])
        # Tạo bảng tra cứu vị trí mục tiêu
        self.goal_positions = {}
        for i in range(n*n):
            if i == 0:
                self.goal_positions[0] = (n-1, n-1)
            else:
                self.goal_positions[i] = ((i-1) // n, (i-1) % n)

    def heuristic(self, state):
        """Tính tổng khoảng cách Manhattan của các ô tới vị trí mục tiêu."""
        dist = 0
        for idx, val in enumerate(state):
            if val == 0:
                continue
            x, y = divmod(idx, self.n)
            goal_x, goal_y = self.goal_positions[val]
            dist += abs(x - goal_x) + abs(y - goal_y)
        return dist

    def get_neighbors(self, state):
        """Sinh các trạng thái con sau một lần di chuyển ô trống."""
        n = self.n
        zero_idx = state.index(0)
        x, y = divmod(zero_idx, n)
        moves = []
        # Ưu tiên các hướng di chuyển có thể dẫn đến mục tiêu
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < n and 0 <= new_y < n:
                new_idx = new_x * n + new_y
                new_state = list(state)
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                moves.append(tuple(new_state))
        return moves

    def solve(self, start):
        """Áp dụng thuật toán A* để tìm đường đi từ start đến goal."""
        start_time = time.time()
        open_set = []
        heappush(open_set, (self.heuristic(start), 0, start, None))
        came_from = {start: None}
        cost = {start: 0}
        nodes_explored = 0
        max_open_size = 1
        total_nodes = 1
        visited = set([start])  # Thêm set để theo dõi các trạng thái đã thăm

        while open_set:
            f, g, current, parent = heappop(open_set)
            nodes_explored += 1
            max_open_size = max(max_open_size, len(open_set))
            
            if current == self.goal:
                path = []
                while current is not None:
                    path.append(current)
                    current = came_from[current]
                end_time = time.time()
                return {
                    'solution': path[::-1],
                    'steps': len(path) - 1,
                    'spaceComplexity': max_open_size,
                    'timeComplexity': total_nodes,
                    'time': (end_time - start_time) * 1000
                }

            for nxt in self.get_neighbors(current):
                if nxt not in visited:  # Chỉ xét các trạng thái chưa thăm
                    new_g = g + 1
                    if nxt not in cost or new_g < cost[nxt]:
                        cost[nxt] = new_g
                        priority = new_g + self.heuristic(nxt)
                        heappush(open_set, (priority, new_g, nxt, current))
                        came_from[nxt] = current
                        visited.add(nxt)
                        total_nodes += 1

        end_time = time.time()
        return {
            'solution': None,
            'steps': 0,
            'spaceComplexity': max_open_size,
            'timeComplexity': total_nodes,
            'time': (end_time - start_time) * 1000
        }

    def is_solvable(self, state):
        """Kiểm tra xem trạng thái có thể giải được không."""
        inversions = 0
        n = self.n
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i] != 0 and state[j] != 0 and state[i] > state[j]:
                    inversions += 1
        if n % 2 == 1:
            return inversions % 2 == 0
        else:
            zero_row = state.index(0) // n
            return (inversions + zero_row) % 2 == 0

    def generate_puzzle(self):
        """Tạo một trạng thái ngẫu nhiên có thể giải được."""
        n = self.n
        while True:
            state = list(range(n*n))
            np.random.shuffle(state)
            if self.is_solvable(state):
                return tuple(state)

@app.route('/api/solve', methods=['POST'])
def solve_puzzle():
    data = request.json
    n = data.get('n', 3)
    state = tuple(data.get('state', []))
    
    solver = NPuzzleSolver(n)
    result = solver.solve(state)
    
    if result and result['solution']:
        return jsonify({
            'success': True,
            'solution': result['solution'],
            'stats': {
                'steps': result['steps'],
                'spaceComplexity': result['spaceComplexity'],
                'timeComplexity': result['timeComplexity'],
                'time': result['time']
            }
        })
    return jsonify({
        'success': False,
        'message': 'No solution found',
        'stats': {
            'steps': 0,
            'spaceComplexity': result['spaceComplexity'],
            'timeComplexity': result['timeComplexity'],
            'time': result['time']
        }
    })

@app.route('/api/generate', methods=['POST'])
def generate_puzzle():
    data = request.json
    n = data.get('n', 3)
    
    solver = NPuzzleSolver(n)
    puzzle = solver.generate_puzzle()
    
    return jsonify({
        'success': True,
        'puzzle': puzzle
    })

@app.route('/api/check', methods=['POST'])
def check_solvable():
    data = request.json
    n = data.get('n', 3)
    state = tuple(data.get('state', []))
    
    solver = NPuzzleSolver(n)
    is_solvable = solver.is_solvable(state)
    
    return jsonify({
        'success': True,
        'is_solvable': is_solvable
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000) 
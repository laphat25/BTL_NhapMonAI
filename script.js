class NPuzzleVisualizer {
    constructor() {
        this.currentState = null;
        this.solution = [];
        this.currentStep = 0;
        this.autoPlayInterval = null;
        this.n = 3;
        this.stats = {
            steps: 0,
            spaceComplexity: 0,
            timeComplexity: 0,
            time: 0
        };

        // DOM Elements
        this.board = document.getElementById('puzzleBoard');
        this.sizeSelect = document.getElementById('puzzleSize');
        this.generateBtn = document.getElementById('generateBtn');
        this.solveBtn = document.getElementById('solveBtn');
        this.prevBtn = document.getElementById('prevBtn');
        this.nextBtn = document.getElementById('nextBtn');
        this.autoPlayBtn = document.getElementById('autoPlayBtn');
        this.stepCounter = document.getElementById('stepCounter');
        
        // Stats Elements
        this.stepsCount = document.getElementById('stepsCount');
        this.spaceComplexity = document.getElementById('spaceComplexity');
        this.timeComplexity = document.getElementById('timeComplexity');
        this.solveTime = document.getElementById('solveTime');

        // Event Listeners
        this.sizeSelect.addEventListener('change', () => this.changeSize());
        this.generateBtn.addEventListener('click', () => this.generatePuzzle());
        this.solveBtn.addEventListener('click', () => this.solvePuzzle());
        this.prevBtn.addEventListener('click', () => this.prevStep());
        this.nextBtn.addEventListener('click', () => this.nextStep());
        this.autoPlayBtn.addEventListener('click', () => this.toggleAutoPlay());

        // Initialize
        this.changeSize();
    }

    async generatePuzzle() {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ n: this.n }),
            });
            const data = await response.json();
            if (data.success) {
                this.currentState = data.puzzle;
                this.solution = [];
                this.currentStep = 0;
                this.updateBoard();
                this.updateControls();
            }
        } catch (error) {
            console.error('Error generating puzzle:', error);
            alert('Không thể tạo puzzle mới. Vui lòng thử lại!');
        }
    }

    async solvePuzzle() {
        if (!this.currentState) return;

        try {
            // Hiển thị thông báo đang giải
            this.solveBtn.disabled = true;
            this.solveBtn.textContent = 'Đang giải...';

            const response = await fetch('http://127.0.0.1:5000/api/solve', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    n: this.n,
                    state: this.currentState,
                }),
            });
            const data = await response.json();
            
            // Khôi phục nút giải
            this.solveBtn.disabled = false;
            this.solveBtn.textContent = 'Giải Puzzle';

            if (data.success) {
                this.solution = data.solution;
                this.currentStep = 0;
                this.stats = data.stats;
                this.updateBoard();
                this.updateControls();
                this.updateStats();
            } else {
                alert('Không tìm thấy giải pháp!');
            }
        } catch (error) {
            console.error('Error solving puzzle:', error);
            alert('Không thể giải puzzle. Vui lòng thử lại!');
            this.solveBtn.disabled = false;
            this.solveBtn.textContent = 'Giải Puzzle';
        }
    }

    updateStats() {
        this.stepsCount.textContent = this.stats.steps;
        this.spaceComplexity.textContent = this.stats.spaceComplexity;
        this.timeComplexity.textContent = this.stats.timeComplexity;
        this.solveTime.textContent = Math.round(this.stats.time);
    }

    changeSize() {
        this.n = parseInt(this.sizeSelect.value);
        this.currentState = null;
        this.solution = [];
        this.currentStep = 0;
        this.stats = {
            steps: 0,
            spaceComplexity: 0,
            timeComplexity: 0,
            time: 0
        };
        this.board.setAttribute('data-size', this.n);
        this.updateBoard();
        this.updateControls();
        this.updateStats();
    }

    updateBoard() {
        this.board.style.gridTemplateColumns = `repeat(${this.n}, ${this.n === 4 ? '45px' : '50px'})`;
        this.board.innerHTML = '';

        const state = this.solution[this.currentStep] || this.currentState;
        if (!state) return;

        for (let i = 0; i < state.length; i++) {
            const tile = document.createElement('div');
            tile.className = 'puzzle-tile' + (state[i] === 0 ? ' empty' : '');
            tile.textContent = state[i] || '';
            this.board.appendChild(tile);
        }
    }

    updateControls() {
        const hasSolution = this.solution.length > 0;
        this.prevBtn.disabled = !hasSolution || this.currentStep === 0;
        this.nextBtn.disabled = !hasSolution || this.currentStep === this.solution.length - 1;
        this.autoPlayBtn.disabled = !hasSolution;
        this.stepCounter.textContent = `Bước: ${this.currentStep + 1}/${this.solution.length || 1}`;
    }

    prevStep() {
        if (this.currentStep > 0) {
            this.currentStep--;
            this.updateBoard();
            this.updateControls();
        }
    }

    nextStep() {
        if (this.currentStep < this.solution.length - 1) {
            this.currentStep++;
            this.updateBoard();
            this.updateControls();
        }
    }

    toggleAutoPlay() {
        if (this.autoPlayInterval) {
            clearInterval(this.autoPlayInterval);
            this.autoPlayInterval = null;
            this.autoPlayBtn.textContent = 'Tự Động';
        } else {
            this.autoPlayBtn.textContent = 'Dừng';
            this.autoPlayInterval = setInterval(() => {
                if (this.currentStep < this.solution.length - 1) {
                    this.nextStep();
                } else {
                    this.toggleAutoPlay();
                }
            }, 500);
        }
    }
}

// Initialize the visualizer when the page loads
window.addEventListener('load', () => {
    new NPuzzleVisualizer();
}); 
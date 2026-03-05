"""
Task 3: Implementation of Search Strategies (BFS, DFS) and Variants
Includes implementations for:
1. Tic Tac Toe
2. Eight Queens Problem
3. Milk and Water Jug Problem
4. Missionaries and Cannibal Problem
And performance comparisons.
"""

import time
from collections import deque

class SearchProblem:
    """Base class for search problems."""
    def __init__(self, initial_state):
        self.initial_state = initial_state

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def is_goal(self, state):
        raise NotImplementedError

# --- 1. Tic Tac Toe Implementation ---

class TicTacToe(SearchProblem):
    def __init__(self):
        super().__init__(tuple([' '] * 9))

    def actions(self, state):
        return [i for i, cell in enumerate(state) if cell == ' ']

    def result(self, state, action):
        new_state = list(state)
        # Simplified: player alternates based on move count
        player = 'X' if state.count(' ') % 2 != 0 else 'O'
        new_state[action] = player
        return tuple(new_state)

    def is_goal(self, state):
        win_conditions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for combo in win_conditions:
            if state[combo[0]] == state[combo[1]] == state[combo[2]] != ' ':
                return True
        return ' ' not in state

# --- 2. Eight Queens Problem ---

class EightQueens(SearchProblem):
    def __init__(self, n=8):
        super().__init__(tuple())
        self.n = n

    def actions(self, state):
        if len(state) == self.n:
            return []
        row = len(state)
        return [col for col in range(self.n) if self.is_safe(state, row, col)]

    def is_safe(self, state, row, col):
        for r, c in enumerate(state):
            if c == col or abs(c - col) == abs(r - row):
                return False
        return True

    def result(self, state, action):
        return state + (action,)

    def is_goal(self, state):
        return len(state) == self.n

# --- 3. Milk and Water Jug Problem ---

class WaterJugProblem(SearchProblem):
    def __init__(self, jug1_cap=4, jug2_cap=3, target=2):
        super().__init__((0, 0))
        self.jug1_cap = jug1_cap
        self.jug2_cap = jug2_cap
        self.target = target

    def actions(self, state):
        j1, j2 = state
        acts = []
        if j1 < self.jug1_cap: acts.append('fill1')
        if j2 < self.jug2_cap: acts.append('fill2')
        if j1 > 0: acts.append('empty1')
        if j2 > 0: acts.append('empty2')
        if j1 > 0 and j2 < self.jug2_cap: acts.append('pour1to2')
        if j2 > 0 and j1 < self.jug1_cap: acts.append('pour2to1')
        return acts

    def result(self, state, action):
        j1, j2 = state
        if action == 'fill1': return (self.jug1_cap, j2)
        if action == 'fill2': return (j1, self.jug2_cap)
        if action == 'empty1': return (0, j2)
        if action == 'empty2': return (j1, 0)
        if action == 'pour1to2':
            amount = min(j1, self.jug2_cap - j2)
            return (j1 - amount, j2 + amount)
        if action == 'pour2to1':
            amount = min(j2, self.jug1_cap - j1)
            return (j1 + amount, j2 - amount)

    def is_goal(self, state):
        return state[0] == self.target or state[1] == self.target

# --- 4. Missionaries and Cannibals ---

class MissionariesCannibals(SearchProblem):
    def __init__(self):
        # (missionaries_left, cannibals_left, boat_pos) boat: 1=left, 0=right
        super().__init__((3, 3, 1))

    def actions(self, state):
        m, c, b = state
        acts = []
        possible_moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
        for dm, dc in possible_moves:
            if b == 1: # Moving left to right
                new_m, new_c = m - dm, c - dc
            else: # Moving right to left
                new_m, new_c = m + dm, c + dc
            
            if 0 <= new_m <= 3 and 0 <= new_c <= 3:
                # Check safety at both sides
                m_right, c_right = 3 - new_m, 3 - new_c
                if (new_m == 0 or new_m >= new_c) and (m_right == 0 or m_right >= c_right):
                    acts.append((dm, dc))
        return acts

    def result(self, state, action):
        m, c, b = state
        dm, dc = action
        if b == 1:
            return (m - dm, c - dc, 0)
        else:
            return (m + dm, c + dc, 1)

    def is_goal(self, state):
        return state == (0, 0, 0)

# --- Search Algorithms ---

def bfs(problem):
    start_node = problem.initial_state
    if problem.is_goal(start_node): return [start_node], 1
    
    frontier = deque([([start_node])])
    explored = {start_node}
    nodes_expanded = 0
    
    while frontier:
        path = frontier.popleft()
        state = path[-1]
        nodes_expanded += 1
        
        for action in problem.actions(state):
            child = problem.result(state, action)
            if child not in explored:
                if problem.is_goal(child):
                    return path + [child], nodes_expanded
                explored.add(child)
                frontier.append(path + [child])
    return None, nodes_expanded

def dfs(problem):
    start_node = problem.initial_state
    frontier = [([start_node])]
    explored = set()
    nodes_expanded = 0
    
    while frontier:
        path = frontier.pop()
        state = path[-1]
        nodes_expanded += 1
        
        if problem.is_goal(state):
            return path, nodes_expanded
        
        if state not in explored:
            explored.add(state)
            for action in problem.actions(state):
                child = problem.result(state, action)
                frontier.append(path + [child])
    return None, nodes_expanded

# --- Performance Comparison ---

def compare_performance():
    problems = [
        ("Water Jug", WaterJugProblem()),
        ("Missionaries & Cannibals", MissionariesCannibals()),
        ("8-Queens", EightQueens(8)),
        ("Tic Tac Toe", TicTacToe())
    ]
    
    print(f"{'Problem':<30} | {'Algo':<5} | {'Path Len':<10} | {'Nodes Exp':<10} | {'Time (ms)':<10}")
    print("-" * 75)
    
    for name, prob in problems:
        # BFS
        start_time = time.time()
        path, nodes = bfs(prob)
        elapsed = (time.time() - start_time) * 1000
        print(f"{name:<30} | BFS   | {len(path) if path else 'N/A':<10} | {nodes:<10} | {elapsed:<10.2f}")
        
        # DFS
        start_time = time.time()
        path, nodes = dfs(prob)
        elapsed = (time.time() - start_time) * 1000
        print(f"{name:<30} | DFS   | {len(path) if path else 'N/A':<10} | {nodes:<10} | {elapsed:<10.2f}")
        print("-" * 75)

if __name__ == "__main__":
    compare_performance()

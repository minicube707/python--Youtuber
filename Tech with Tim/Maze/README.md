# 🧭 A* Pathfinding – Versions & Experiments

This folder contains multiple implementations and optimizations of the **A\*** pathfinding algorithm.  
The file **`A_star 1.py`** is the original reference implementation.  
All other files are **incremental improvements or variations** of this initial version.

---

## 🧩 Original Version

### **A_star 1.py**
- Basic and initial implementation of the A\* pathfinding algorithm
- Serves as the reference for all subsequent versions

---

## 🚀 Improved Versions

### **A_star 2.py**
- Adds two map creation modes:
  - **Clean mode**
  - **New mode**

---

### **A_star 2 + diago.py**
- Same as **A_star 2.py**
- Adds **diagonal movement** support

---

### **A_star 3 (maze).py**
- Same as **A_star 2.py**
- Generates a **maze at startup** instead of an empty map

---

### **A_star 4 (maze).py**
- Same as **A_star 3 (maze).py**
- Adds **doors/openings** to allow multiple possible paths to reach the goal

---

### **A_star 5 (maze + opti).py**
- Same as **A_star 4 (maze).py**
- Refactors the code from **Object-Oriented Programming (OOP)** to an **imperative style** for better performance

---

### **A_star 6 (maze + opti + speed).py**
- Same as **A_star 5 (maze + opti).py**
- Removes all animations
- Adds a **timer** to measure the time taken by the pathfinding algorithm to solve the maze

---

### **A_star 7 (maze + opti + speed + diago).py**
- Same as **A_star 6 (maze + opti + speed).py**
- Adds **diagonal movement**
- Allows multiple paths to reach the goal

---

## 🧱 Maze Generation

### **Generater_maze.py**
- Maze generator implemented using **Object-Oriented Programming**
- Uses the **Depth-First Search (DFS)** algorithm

---

### **Generater_maze 2.py**
- Maze generator implemented in an **imperative style**
- Uses the **Depth-First Search (DFS)** algorithm

---

## 🧠 Maze Solving Projects

### **Solve maze 1.py**
- Generates a maze that the user must solve manually
- Displays the **time taken** to complete the maze

---

### **Solve maze 2.py**
- Same as **Solve maze 1.py**
- Displays the **explored path** in green while solving the maze

---

## 📌 Notes

- File names are kept as-is to reflect the learning and experimentation process
- Each version focuses on a **specific improvement or optimization**
- This folder documents a progressive exploration of:
  - Pathfinding algorithms
  - Performance optimization
  - OOP vs imperative programming styles

---

import tkinter as tk
from tkinter import ttk
import random
import time

# Visualizer main class
class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Visualizer")
        self.root.maxsize(900, 600)
        self.root.config(bg="white")

        self.selected_algo = tk.StringVar()
        self.speed = tk.StringVar()
        self.data = []

        # UI Frame
        self.ui_frame = tk.Frame(root, width=900, height=200, bg="lightgrey")
        self.ui_frame.pack(padx=10, pady=5)

        tk.Label(self.ui_frame, text="Algorithm: ", bg="lightgrey").grid(row=0, column=0, padx=5, pady=5)
        algo_menu = ttk.Combobox(self.ui_frame, textvariable=self.selected_algo, values=["Bubble Sort", "Merge Sort", "Quick Sort"])
        algo_menu.grid(row=0, column=1, padx=5, pady=5)
        algo_menu.current(0)

        tk.Label(self.ui_frame, text="Speed: ", bg="lightgrey").grid(row=1, column=0, padx=5, pady=5)
        speed_menu = ttk.Combobox(self.ui_frame, textvariable=self.speed, values=["Fast", "Medium", "Slow"])
        speed_menu.grid(row=1, column=1, padx=5, pady=5)
        speed_menu.current(0)

        tk.Button(self.ui_frame, text="Generate Array", command=self.generate_array, bg="green", fg="white").grid(row=0, column=3, padx=5, pady=5)
        tk.Button(self.ui_frame, text="Start Sorting", command=self.start_sorting, bg="blue", fg="white").grid(row=1, column=3, padx=5, pady=5)

        self.canvas = tk.Canvas(root, width=880, height=380, bg="white")
        self.canvas.pack(padx=10, pady=5)

    def draw_data(self, data, color_array):
        self.canvas.delete("all")
        c_height = 380
        c_width = 880
        x_width = c_width / (len(data) + 1)
        offset = 10
        spacing = 5
        normalized_data = [i / max(data) for i in data]

        for i, height in enumerate(normalized_data):
            x0 = i * x_width + offset + spacing
            y0 = c_height - height * 340
            x1 = (i + 1) * x_width + offset
            y1 = c_height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color_array[i])
            self.canvas.create_text(x0 + 2, y0, anchor=tk.SW, text=str(data[i]), font=("Arial", 8))

        self.root.update_idletasks()

    def generate_array(self):
        self.data = [random.randint(10, 100) for _ in range(30)]
        self.draw_data(self.data, ["grey" for _ in range(len(self.data))])

    def set_speed(self):
        speeds = {"Slow": 0.3, "Medium": 0.1, "Fast": 0.01}
        return speeds[self.speed.get()]

    def start_sorting(self):
        if self.selected_algo.get() == "Bubble Sort":
            self.bubble_sort(self.data, self.draw_data, self.set_speed())
        elif self.selected_algo.get() == "Merge Sort":
            self.merge_sort(self.data, 0, len(self.data)-1, self.draw_data, self.set_speed())
        elif self.selected_algo.get() == "Quick Sort":
            self.quick_sort(self.data, 0, len(self.data)-1, self.draw_data, self.set_speed())

        self.draw_data(self.data, ["green" for _ in range(len(self.data))])

    # ---------------- Sorting Algorithms ---------------- #
    def bubble_sort(self, data, draw, speed):
        for i in range(len(data) - 1):
            for j in range(len(data) - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
                    draw(data, ["red" if x == j or x == j + 1 else "grey" for x in range(len(data))])
                    time.sleep(speed)

    def merge_sort(self, data, left, right, draw, speed):
        if left < right:
            mid = (left + right) // 2
            self.merge_sort(data, left, mid, draw, speed)
            self.merge_sort(data, mid + 1, right, draw, speed)
            self.merge(data, left, mid, right, draw, speed)

    def merge(self, data, left, mid, right, draw, speed):
        left_part = data[left:mid+1]
        right_part = data[mid+1:right+1]

        i = j = 0
        k = left

        while i < len(left_part) and j < len(right_part):
            if left_part[i] <= right_part[j]:
                data[k] = left_part[i]
                i += 1
            else:
                data[k] = right_part[j]
                j += 1
            k += 1
            draw(data, ["purple" if x == k else "grey" for x in range(len(data))])
            time.sleep(speed)

        while i < len(left_part):
            data[k] = left_part[i]
            i += 1
            k += 1
            draw(data, ["purple" if x == k else "grey" for x in range(len(data))])
            time.sleep(speed)

        while j < len(right_part):
            data[k] = right_part[j]
            j += 1
            k += 1
            draw(data, ["purple" if x == k else "grey" for x in range(len(data))])
            time.sleep(speed)

    def quick_sort(self, data, low, high, draw, speed):
        if low < high:
            pi = self.partition(data, low, high, draw, speed)
            self.quick_sort(data, low, pi - 1, draw, speed)
            self.quick_sort(data, pi + 1, high, draw, speed)

    def partition(self, data, low, high, draw, speed):
        pivot = data[high]
        i = low - 1
        for j in range(low, high):
            if data[j] < pivot:
                i += 1
                data[i], data[j] = data[j], data[i]
                draw(data, ["orange" if x == i or x == j else "grey" for x in range(len(data))])
                time.sleep(speed)
        data[i + 1], data[high] = data[high], data[i + 1]
        draw(data, ["orange" if x == i + 1 or x == high else "grey" for x in range(len(data))])
        time.sleep(speed)
        return i + 1

# ---------------- Run the App ---------------- #
if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()

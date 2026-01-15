from tkinter import *
import tkinter as tk
import random
import time

# Global worker variable for animation control
worker = None

# ==================== HELPER FUNCTIONS ====================

# Swap two bars on canvas with smooth animation
def swap(pos_0, pos_1):
    """
    Swaps the positions of two bars on the canvas
    Args:
        pos_0: First bar canvas object
        pos_1: Second bar canvas object
    """
    bar11, _, bar12, _ = canvas.coords(pos_0)
    bar21, _, bar22, _ = canvas.coords(pos_1)
    canvas.move(pos_0, bar21-bar11, 0)
    canvas.move(pos_1, bar12-bar22, 0)

# Helper function to change bar color during sorting operations
def color_bar(bar_index, color):
    """
    Changes the color of a specific bar
    Args:
        bar_index: Index of the bar in barList
        color: Color to apply to the bar
    """
    if 0 <= bar_index < len(barList):
        canvas.itemconfig(barList[bar_index], fill=color) 

# ==================== SORTING ALGORITHM GENERATORS ====================

def _insertion_sort():
    """
    Insertion Sort Algorithm Generator
    Time Complexity: O(n^2) | Space Complexity: O(1)
    Visualizes each swap as the algorithm inserts elements into sorted position
    """
    global barList
    global lengthList
    for i in range(len(lengthList)):
        cursor = lengthList[i]
        cursorBar = barList[i]
        pos = i
        while pos > 0 and lengthList[pos - 1] > cursor:
            lengthList[pos] = lengthList[pos - 1]
            barList[pos], barList[pos - 1] = barList[pos - 1], barList[pos]
            swap(barList[pos], barList[pos-1])
            yield
            pos -= 1
        lengthList[pos] = cursor
        barList[pos] = cursorBar
        swap(barList[pos], cursorBar)

def _bubble_sort():
    """
    Bubble Sort Algorithm Generator
    Time Complexity: O(n^2) | Space Complexity: O(1)
    Visualizes each swap as larger elements "bubble" to the end
    """
    global barList
    global lengthList
    for i in range(len(lengthList) - 1):
        for j in range(len(lengthList) - i - 1):
            if(lengthList[j] > lengthList[j + 1]):
                lengthList[j], lengthList[j + 1] = lengthList[j + 1], lengthList[j]
                barList[j], barList[j + 1] = barList[j + 1], barList[j]
                swap(barList[j + 1], barList[j])
                yield

def _selection_sort():
    """
    Selection Sort Algorithm Generator
    Time Complexity: O(n^2) | Space Complexity: O(1)
    Visualizes finding minimum element and placing it in sorted position
    """
    global barList
    global lengthList
    for i in range(len(lengthList)):
        min = i
        time.sleep(0.5)
        for j in range(i + 1, len(lengthList)):
            if(lengthList[j] < lengthList[min]):
                min = j
        lengthList[min], lengthList[i] = lengthList[i], lengthList[min]
        barList[min], barList[i] = barList[i], barList[min]
        swap(barList[min], barList[i])
        yield

def _merge_sort(start=0, end=None):
    """
    Merge Sort Algorithm Generator
    Time Complexity: O(n log n) | Space Complexity: O(n)
    Recursively divides array and merges sorted subarrays
    """
    global barList
    global lengthList

    if end is None:
        end = len(lengthList)

    # Helper function to merge two sorted subarrays
    def merge(start, mid, end):
        # Create temporary arrays for merging
        left = lengthList[start:mid]
        right = lengthList[mid:end]
        left_bars = barList[start:mid]
        right_bars = barList[mid:end]

        i = j = 0
        k = start

        # Merge the two arrays back into lengthList
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                lengthList[k] = left[i]
                barList[k] = left_bars[i]
                i += 1
            else:
                lengthList[k] = right[j]
                barList[k] = right_bars[j]
                j += 1

            # Update bar position on canvas
            bar_coords = canvas.coords(barList[k])
            target_x = 5 + k * 10
            canvas.coords(barList[k], target_x, bar_coords[1], target_x + 10, bar_coords[3])
            yield
            k += 1

        # Copy remaining elements from left array
        while i < len(left):
            lengthList[k] = left[i]
            barList[k] = left_bars[i]
            bar_coords = canvas.coords(barList[k])
            target_x = 5 + k * 10
            canvas.coords(barList[k], target_x, bar_coords[1], target_x + 10, bar_coords[3])
            yield
            i += 1
            k += 1

        # Copy remaining elements from right array
        while j < len(right):
            lengthList[k] = right[j]
            barList[k] = right_bars[j]
            bar_coords = canvas.coords(barList[k])
            target_x = 5 + k * 10
            canvas.coords(barList[k], target_x, bar_coords[1], target_x + 10, bar_coords[3])
            yield
            j += 1
            k += 1

    # Recursive merge sort implementation
    def merge_sort_recursive(start, end):
        if end - start <= 1:
            return

        mid = (start + end) // 2

        # Recursively sort left half
        yield from merge_sort_recursive(start, mid)

        # Recursively sort right half
        yield from merge_sort_recursive(mid, end)

        # Merge the sorted halves
        yield from merge(start, mid, end)

    yield from merge_sort_recursive(start, end)

def _quick_sort(low=0, high=None):
    """
    Quick Sort Algorithm Generator
    Time Complexity: O(n log n) average, O(n^2) worst | Space Complexity: O(log n)
    Uses partitioning with pivot element to recursively sort subarrays
    """
    global barList
    global lengthList

    if high is None:
        high = len(lengthList) - 1

    # Recursive quick sort implementation
    def quick_sort_recursive(low, high):
        if low < high:
            # Partition: Choose rightmost element as pivot
            pivot = lengthList[high]
            i = low - 1

            # Rearrange array so smaller elements are on left of pivot
            for j in range(low, high):
                if lengthList[j] < pivot:
                    i += 1
                    lengthList[i], lengthList[j] = lengthList[j], lengthList[i]
                    barList[i], barList[j] = barList[j], barList[i]
                    swap(barList[i], barList[j])
                    yield

            # Place pivot in correct position
            i += 1
            lengthList[i], lengthList[high] = lengthList[high], lengthList[i]
            barList[i], barList[high] = barList[high], barList[i]
            swap(barList[i], barList[high])
            yield

            # Store pivot index
            pi = i

            # Recursively sort elements before and after partition
            yield from quick_sort_recursive(low, pi - 1)
            yield from quick_sort_recursive(pi + 1, high)

    yield from quick_sort_recursive(low, high)

def _heap_sort():
    """
    Heap Sort Algorithm Generator
    Time Complexity: O(n log n) | Space Complexity: O(1)
    Builds max heap and repeatedly extracts maximum element
    """
    global barList
    global lengthList
    n = len(lengthList)

    # Heapify subtree rooted at index i
    def heapify(n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        # Check if left child exists and is greater than root
        if left < n and lengthList[left] > lengthList[largest]:
            largest = left

        # Check if right child exists and is greater than current largest
        if right < n and lengthList[right] > lengthList[largest]:
            largest = right

        # If largest is not root, swap and continue heapifying
        if largest != i:
            lengthList[i], lengthList[largest] = lengthList[largest], lengthList[i]
            barList[i], barList[largest] = barList[largest], barList[i]
            swap(barList[i], barList[largest])
            yield

            # Recursively heapify the affected subtree
            yield from heapify(n, largest)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(n, i)

    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        # Move current root (maximum) to end
        lengthList[0], lengthList[i] = lengthList[i], lengthList[0]
        barList[0], barList[i] = barList[i], barList[0]
        swap(barList[0], barList[i])
        yield

        # Heapify the reduced heap
        yield from heapify(i, 0)

# ==================== SORTING BUTTON HANDLERS ====================

def insertion_sort():
    """Initiates Insertion Sort with animation"""
    global worker
    worker = _insertion_sort()
    animate()
    update_complexity_display("Insertion Sort", "O(n²)", "O(1)")

def selection_sort():
    """Initiates Selection Sort with animation"""
    global worker
    worker = _selection_sort()
    animate()
    update_complexity_display("Selection Sort", "O(n²)", "O(1)")

def bubble_sort():
    """Initiates Bubble Sort with animation"""
    global worker
    worker = _bubble_sort()
    animate()
    update_complexity_display("Bubble Sort", "O(n²)", "O(1)")

def merge_sort():
    """Initiates Merge Sort with animation"""
    global worker
    worker = _merge_sort()
    animate()
    update_complexity_display("Merge Sort", "O(n log n)", "O(n)")

def quick_sort():
    """Initiates Quick Sort with animation"""
    global worker
    worker = _quick_sort()
    animate()
    update_complexity_display("Quick Sort", "O(n log n) avg, O(n²) worst", "O(log n)")

def heap_sort():
    """Initiates Heap Sort with animation"""
    global worker
    worker = _heap_sort()
    animate()
    update_complexity_display("Heap Sort", "O(n log n)", "O(1)")

def update_complexity_display(algorithm, time_complexity, space_complexity):
    """
    Updates the complexity information display
    Args:
        algorithm: Name of the sorting algorithm
        time_complexity: Time complexity notation
        space_complexity: Space complexity notation
    """
    complexity_text = f"{algorithm} | Time: {time_complexity} | Space: {space_complexity}"
    time_complexity_label.config(text=complexity_text)

# ==================== ANIMATION CONTROL ====================

def animate():
    """
    Controls the animation of sorting algorithms using generator pattern
    Calls the next step in the sorting process and schedules the next frame
    """
    global worker
    if worker is not None:
        try:
            next(worker)
            window.after(10, animate)  # Delay between animation frames (10ms)
        except StopIteration:
            worker = None  # Sorting complete
        finally:
            window.after_cancel(animate) 

# ==================== BAR GENERATION ====================

def generate():
    """
    Generates random bars for visualization
    Creates rectangles on canvas with random heights
    Highlights minimum bar in red and maximum bar in dark color
    """
    global barList
    global lengthList
    canvas.delete('all')
    barstart = 5
    barend = 15
    barList = []
    lengthList = []

    # Create rectangles with random heights
    for bar in range(0, (number)):
        randomY = random.randint(1, 360)
        bar = canvas.create_rectangle(barstart, randomY, barend, 365, fill='#82CFFD', width=2)
        barList.append(bar)
        barstart += 10
        barend += 10

    # Calculate bar lengths (heights)
    for bar in barList:
        bar = canvas.coords(bar)
        length = bar[3] - bar[1]
        lengthList.append(length)

    # Highlight special bars: minimum in red, maximum in dark
    for i in range(len(lengthList)-1):
        if lengthList[i] == min(lengthList):
            canvas.itemconfig(barList[i], fill='#FF6F61')
        elif lengthList[i] == max(lengthList):
            canvas.itemconfig(barList[i], fill='#333')

# ==================== UI FUNCTIONS ====================

def Accept_value():
    """
    Accepts the number of bars from user input
    Transitions from input screen to sorting visualization screen
    """
    global number
    t1 = int(a.get())
    number = t1
    input_frame.pack_forget()
    sorting_ui()
    generate()

def create_ui():
    """
    Creates the main Tkinter window
    Returns: Configured Tkinter window object
    """
    window = tk.Tk()
    window.title('Sorting Visualizer')
    window.geometry('800x300')
    window.configure(bg='#F0F0F0')
    window.state('zoomed')

    return window

def input_ui():
    """
    Creates the initial input screen for entering number of bars
    Displays project and student information
    """
    global a, input_frame
    input_frame = Frame(window, bg='#F0F0F0')
    input_frame.pack(fill=BOTH, expand=True)

    # Student and project information
    name_label = Label(input_frame, text="Shubhanshi Shekhar", font=("Arial", 12), fg='#333', bg='#F0F0F0')
    name_label.pack(pady=5)

    reg_label = Label(input_frame, text="2427010175", font=("Arial", 12), fg='#333', bg='#F0F0F0')
    reg_label.pack(pady=5)

    uni_label = Label(input_frame, text="Manipal University Jaipur", font=("Arial", 12), fg='#333', bg='#F0F0F0')
    uni_label.pack(pady=5)

    project_label = Label(input_frame, text="DSA Mini Project", font=("Arial", 12), fg='#333', bg='#F0F0F0')
    project_label.pack(pady=5)

    label = Label(input_frame, text="Enter Number of Bars:", font=("Arial", 14), fg='#333', bg='#F0F0F0')
    label.pack(pady=20)

    # Input field for number of bars
    a = Entry(input_frame, width=20, font=("Arial", 14))
    a.pack(pady=10)

    button = Button(input_frame, text="Submit", command=Accept_value, bg="#82CFFD", fg="white", font=("Arial", 12, "bold"))
    button.pack(pady=20)

def sorting_ui():
    """
    Creates the main sorting visualization UI
    Contains canvas for bar display and buttons for each sorting algorithm
    Also displays time and space complexity information
    """
    global canvas, barList, lengthList, worker, time_complexity_label
    window.configure(bg='#F0F0F0')

    # Canvas for drawing bars
    canvas = tk.Canvas(window, width=1000, height=400, bg="#E8E8E8", bd=0, highlightthickness=0)
    canvas.grid(row=0, column=0, columnspan=6, padx=10, pady=10)

    # First row of sorting buttons (original algorithms)
    insert = tk.Button(window, text='Insertion Sort', command=insertion_sort, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), relief="flat", width=12)
    insert.grid(row=1, column=0, padx=8, pady=15)

    select = tk.Button(window, text='Selection Sort', command=selection_sort, bg="#FF5722", fg="white", font=("Arial", 11, "bold"), relief="flat", width=12)
    select.grid(row=1, column=1, padx=8, pady=15)

    bubble = tk.Button(window, text='Bubble Sort', command=bubble_sort, bg="#00BCD4", fg="white", font=("Arial", 11, "bold"), relief="flat", width=12)
    bubble.grid(row=1, column=2, padx=8, pady=15)

    # Second row of sorting buttons (new algorithms)
    merge = tk.Button(window, text='Merge Sort', command=merge_sort, bg="#9C27B0", fg="white", font=("Arial", 11, "bold"), relief="flat", width=12)
    merge.grid(row=1, column=3, padx=8, pady=15)

    quick = tk.Button(window, text='Quick Sort', command=quick_sort, bg="#FF9800", fg="white", font=("Arial", 11, "bold"), relief="flat", width=12)
    quick.grid(row=1, column=4, padx=8, pady=15)

    heap = tk.Button(window, text='Heap Sort', command=heap_sort, bg="#3F51B5", fg="white", font=("Arial", 11, "bold"), relief="flat", width=12)
    heap.grid(row=1, column=5, padx=8, pady=15)

    # Complexity information label
    time_complexity_label = Label(window, text="Select an algorithm to view complexity", font=("Arial", 12, "bold"), fg="#333", bg="#F0F0F0")
    time_complexity_label.grid(row=2, column=0, columnspan=6, pady=10)

    # Utility buttons
    shuffle = tk.Button(window, text='Shuffle', command=generate, bg="#FFC107", fg="white", font=("Arial", 11, "bold"), relief="flat", width=12)
    shuffle.grid(row=3, column=2, padx=8, pady=10)

    reset_button = Button(window, text="Reset", command=reset, bg="#9E9E9E", fg="white", font=("Arial", 11, "bold"), relief="flat", width=12)
    reset_button.grid(row=3, column=3, padx=8, pady=10)

def reset():
    """
    Resets the visualization
    Stops current animation and generates new random bars
    """
    global worker, barList, lengthList
    worker = None
    canvas.delete('all')
    generate()
    time_complexity_label.config(text="Select an algorithm to view complexity")

# ==================== MAIN PROGRAM ====================

if __name__ == "__main__":
    window = create_ui()
    input_ui()
    window.mainloop()

import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

class TransportationProblemSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Transportation Problem Solver")
        self.root.geometry("950x700")  # Set larger screen size
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill="both")

        self.main_frame = tk.Frame(self.notebook)
        self.notebook.add(self.main_frame, text='Input')

        self.steps_frame = tk.Frame(self.notebook)
        self.notebook.add(self.steps_frame, text='Steps')
        self.steps_canvas = tk.Canvas(self.steps_frame)
        self.steps_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.steps_scrollbar = ttk.Scrollbar(self.steps_frame, orient=tk.HORIZONTAL, command=self.steps_canvas.xview)
        self.steps_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.steps_canvas.configure(xscrollcommand=self.steps_scrollbar.set)
        self.steps_canvas.bind('<Configure>', lambda e: self.steps_canvas.configure(scrollregion=self.steps_canvas.bbox("all")))

        self.steps_inner_frame = tk.Frame(self.steps_canvas)
        self.steps_canvas.create_window((0, 0), window=self.steps_inner_frame, anchor="nw")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill="both")

        self.algorithm_frame = tk.Frame(self.notebook)
        self.notebook.add(self.algorithm_frame, text='Algorithm')

        self.algorithm_text = tk.Text(self.algorithm_frame, wrap=tk.WORD)
        self.algorithm_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.flowchart_frame = tk.Frame(self.notebook)
        self.notebook.add(self.flowchart_frame, text='Flowchart')

        self.flowchart_canvas = tk.Canvas(self.flowchart_frame)
        self.flowchart_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.flowchart_scrollbar = ttk.Scrollbar(self.flowchart_frame, orient=tk.VERTICAL,
                                                 command=self.flowchart_canvas.yview)
        self.flowchart_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.flowchart_canvas.configure(yscrollcommand=self.flowchart_scrollbar.set)
        self.flowchart_canvas.bind('<Configure>', lambda e: self.flowchart_canvas.configure(
            scrollregion=self.flowchart_canvas.bbox("all")))

        self.flowchart_inner_frame = tk.Frame(self.flowchart_canvas)
        self.flowchart_canvas.create_window((0, 0), window=self.flowchart_inner_frame, anchor="nw")

        self.flowchart_images = {
            "NorthWest Method": "nw.png",
            "Least Cost Method": "lc.png",
            "Vogel's Approximation Method": "vam.png"
        }

        self.create_widgets()

    def create_widgets(self):
        # Number of rows and columns entry
        self.rows_label = tk.Label(self.main_frame, text="Enter number of rows:")
        self.rows_label.pack(anchor="center")
        self.rows_entry = tk.Entry(self.main_frame)
        self.rows_entry.pack(anchor="center")

        self.columns_label = tk.Label(self.main_frame, text="Enter number of columns:")
        self.columns_label.pack(anchor="center")
        self.columns_entry = tk.Entry(self.main_frame)
        self.columns_entry.pack(anchor="center")

        # Button to submit dimensions
        self.submit_btn = ttk.Button(self.main_frame, text="Submit", command=self.submit_dimensions)
        self.submit_btn.pack(anchor="center")

    def submit_dimensions(self):
        try:
            self.num_rows = int(self.rows_entry.get())
            self.num_columns = int(self.columns_entry.get())

            # Destroy main frame widgets
            self.rows_label.destroy()
            self.rows_entry.destroy()
            self.columns_label.destroy()
            self.columns_entry.destroy()
            self.submit_btn.destroy()

            # Create table
            self.create_table()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integer values for rows and columns.")

    def create_table(self):
        self.cost_matrix = []
        self.supply = []
        self.demand = []

        self.table_frame = tk.Frame(self.main_frame)
        self.table_frame.pack(padx=20, pady=20)

        self.cost_label = tk.Label(self.table_frame, text="Enter cost matrix:")
        self.cost_label.grid(row=0, column=0, columnspan=self.num_columns, pady=(0, 10))

        for i in range(self.num_rows):
            row = []
            for j in range(self.num_columns):
                entry = tk.Entry(self.table_frame, width=10)
                entry.grid(row=i + 1, column=j, padx=5, pady=5)
                row.append(entry)
            self.cost_matrix.append(row)

        self.supply_label = tk.Label(self.table_frame, text="Enter supply:")
        self.supply_label.grid(row=1, column=self.num_columns + 1, padx=10)
        for i in range(self.num_rows):
            entry = tk.Entry(self.table_frame, width=10)
            entry.grid(row=i + 1, column=self.num_columns + 2, padx=5, pady=5)
            self.supply.append(entry)

        self.demand_label = tk.Label(self.table_frame, text="Enter demand:")
        self.demand_label.grid(row=self.num_rows + 1, column=0, columnspan=self.num_columns, pady=(10, 0))
        for i in range(self.num_columns):
            entry = tk.Entry(self.table_frame, width=10)
            entry.grid(row=self.num_rows + 2, column=i, padx=5, pady=5)
            self.demand.append(entry)

        # Button to select method
        self.method_var = tk.StringVar()
        self.method_var.set("Select Method")
        self.method_menu = ttk.OptionMenu(self.table_frame, self.method_var, "Select Method", "NorthWest Method", "Least Cost Method",
                                         "Vogel's Approximation Method")
        self.method_menu.grid(row=self.num_rows + 3, columnspan=self.num_columns + 2, pady=10)

        self.solve_btn = ttk.Button(self.table_frame, text="Solve", command=self.solve)
        self.solve_btn.grid(row=self.num_rows + 4, columnspan=self.num_columns + 2, pady=10)

    def solve(self):
        method = self.method_var.get()

        if method == "Select Method":
            messagebox.showerror("Error", "Please select a method.")
            return
        elif method == "NorthWest Method":
            min_cost = self.northwest_method(method)
        elif method == "Least Cost Method":
            min_cost = self.least_cost_method(method)
        elif method == "Vogel's Approximation Method":
            min_cost = self.vogel_approximation_method(method)

        messagebox.showinfo("Result", f"The minimum cost of transportation by {method} is {min_cost}")
        self.display_algorithm(method)

        # Reset button
        self.reset_btn = ttk.Button(self.table_frame, text="Reset", command=self.reset)
        self.reset_btn.grid(row=self.num_rows + 5, columnspan=self.num_columns + 2, pady=10)

    def display_algorithm(self, method):
        # Display algorithm description based on selected method
        self.algorithm_text.config(state=tk.NORMAL)
        self.algorithm_text.delete('1.0', tk.END)

        if method == "NorthWest Method":
            algorithm_description = (
                "NorthWest Method Algorithm:\n\n"
                "1. Start with the cell in the top-left corner (north-west corner) of the cost matrix.\n"
                "2. Allocate as much as possible to the selected cell and adjust the supply and demand.\n"
                "3. Move to the next cell to the right if the current column's demand is met, or move down if the current row's supply is exhausted.\n"
                "4. Repeat steps 2-3 until all supply and demand are met."
            )
            flowchart_image_path = self.flowchart_images.get("NorthWest Method", "")
        elif method == "Least Cost Method":
            algorithm_description = (
                "Least Cost Method Algorithm:\n\n"
                "1. Identify the cell with the lowest cost in the cost matrix.\n"
                "2. Allocate as much as possible to the selected cell and adjust the supply and demand.\n"
                "3. Cross out the row or column that has been satisfied.\n"
                "4. Repeat steps 1-3 until all supply and demand are met."
            )
            flowchart_image_path = self.flowchart_images.get("Least Cost Method", "")
        elif method == "Vogel's Approximation Method":
            algorithm_description = (
                "Vogel's Approximation Method Algorithm:\n\n"
                "1. For each row and column, calculate the penalty cost (difference between the two lowest costs).\n"
                "2. Identify the row or column with the highest penalty cost.\n"
                "3. Allocate as much as possible to the cell with the lowest cost in the selected row or column and adjust the supply and demand.\n"
                "4. Cross out the row or column that has been satisfied and recalculate penalties.\n"
                "5. Repeat steps 1-4 until all supply and demand are met."
            )
            flowchart_image_path = self.flowchart_images.get("Vogel's Approximation Method", "")
        else:
            algorithm_description = (
                "Select an algorithm to view its description and flowchart."
            )
            flowchart_image_path = ""

        self.algorithm_text.insert(tk.END, algorithm_description)
        self.algorithm_text.config(state=tk.DISABLED)

        self.load_flowchart(flowchart_image_path)

    def load_flowchart(self, image_path):
        # Load and display flowchart image in the flowchart tab
        try:
            if image_path:
                flowchart_image = Image.open(image_path)
                resized_image = flowchart_image.resize((self.root.winfo_width(), flowchart_image.height), Image.LANCZOS)
                self.flowchart_img = ImageTk.PhotoImage(resized_image)

                # Clear previous widgets in flowchart_inner_frame
                for widget in self.flowchart_inner_frame.winfo_children():
                    widget.destroy()

                self.flowchart_label = tk.Label(self.flowchart_inner_frame, image=self.flowchart_img)
                self.flowchart_label.image = self.flowchart_img
                self.flowchart_label.pack(expand=True, anchor=tk.CENTER)  # Center align the label

            else:
                # If no image path provided, clear the flowchart frame
                for widget in self.flowchart_inner_frame.winfo_children():
                    widget.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Unable to load image: {e}")

    def output(self, supply, demand, cost_matrix, method, allocation):
        step_frame = tk.Frame(self.steps_inner_frame)
        step_frame.pack(side=tk.LEFT, padx=10, pady=10)

        text_widget = tk.Text(step_frame, wrap=tk.WORD, height=20, width=30)
        text_widget.pack(expand=1, fill="both")
        text_widget.insert(tk.END, f"Method: {method}\n")
        text_widget.insert(tk.END, "Cost Matrix:\n")
        for row in cost_matrix:
            text_widget.insert(tk.END, " ".join(map(str, row)) + "\n")
        text_widget.insert(tk.END, "Allocation Matrix:\n")
        for row in allocation:
            text_widget.insert(tk.END, " ".join(map(str, row)) + "\n")
        text_widget.insert(tk.END, "Supply:\n")
        text_widget.insert(tk.END, " ".join(map(str, supply)) + "\n")
        text_widget.insert(tk.END, "Demand:\n")
        text_widget.insert(tk.END, " ".join(map(str, demand)) + "\n")
        text_widget.config(state=tk.DISABLED)

    def balance_problem(self, supply, demand, cost_matrix):
        total_supply = sum(supply)
        total_demand = sum(demand)
        
        if total_supply < total_demand:
            supply.append(total_demand - total_supply)
            cost_matrix.append([0] * len(cost_matrix[0]))
        elif total_supply > total_demand:
            for row in cost_matrix:
                row.append(0)
            demand.append(total_supply - total_demand)

    def northwest_method(self, method):
        self.steps_inner_frame.destroy()
        self.steps_inner_frame = tk.Frame(self.steps_canvas)
        self.steps_canvas.create_window((0, 0), window=self.steps_inner_frame, anchor="nw")
        
        supply = [int(entry.get()) for entry in self.supply]
        demand = [int(entry.get()) for entry in self.demand]
        cost_matrix = [[int(entry.get()) for entry in row] for row in self.cost_matrix]

        self.balance_problem(supply, demand, cost_matrix)

        i = j = 0
        allocation = [[0] * len(demand) for _ in range(len(supply))]
        total_cost = 0

        while i < len(supply) and j < len(demand):
            allocated = min(supply[i], demand[j])
            allocation[i][j] = allocated
            supply[i] -= allocated
            demand[j] -= allocated
            total_cost += allocated * cost_matrix[i][j]
            if supply[i] == 0:
                i += 1
            else:
                j += 1

            self.output(supply, demand, cost_matrix, method, allocation)

        return total_cost

    def least_cost_method(self, method):
        self.steps_inner_frame.destroy()
        self.steps_inner_frame = tk.Frame(self.steps_canvas)
        self.steps_canvas.create_window((0, 0), window=self.steps_inner_frame, anchor="nw")

        supply = [int(entry.get()) for entry in self.supply]
        demand = [int(entry.get()) for entry in self.demand]
        cost_matrix = [[int(entry.get()) for entry in row] for row in self.cost_matrix]

        self.balance_problem(supply, demand, cost_matrix)

        allocation = [[0] * len(demand) for _ in range(len(supply))]
        total_cost = 0

        while any(supply) and any(demand):
            min_cost = float('inf')
            min_cell = (0, 0)
            for i in range(len(supply)):
                for j in range(len(demand)):
                    if supply[i] > 0 and demand[j] > 0 and cost_matrix[i][j] < min_cost:
                        min_cost = cost_matrix[i][j]
                        min_cell = (i, j)

            i, j = min_cell
            allocated = min(supply[i], demand[j])
            allocation[i][j] = allocated
            supply[i] -= allocated
            demand[j] -= allocated
            total_cost += allocated * cost_matrix[i][j]

            self.output(supply, demand, cost_matrix, method, allocation)

        return total_cost

    def vogel_approximation_method(self, method):
        self.steps_inner_frame.destroy()
        self.steps_inner_frame = tk.Frame(self.steps_canvas)
        self.steps_canvas.create_window((0, 0), window=self.steps_inner_frame, anchor="nw")
        self.steps_canvas.configure(scrollregion=self.steps_canvas.bbox("all"))

        supply = [int(entry.get()) for entry in self.supply]
        demand = [int(entry.get()) for entry in self.demand]
        cost_matrix = [[int(entry.get()) for entry in row] for row in self.cost_matrix]

        self.balance_problem(supply, demand, cost_matrix)

        allocation = [[0] * len(cost_matrix[0]) for _ in range(len(cost_matrix))]
        new = [[0] * len(cost_matrix[0]) for _ in range(len(cost_matrix))]

        for i in range(len(cost_matrix)):
            for j in range(len(cost_matrix[0])):
                allocation[i][j] = 0
                new[i][j] = cost_matrix[i][j]
        INF = 10 ** 3
        n = len(cost_matrix)
        m = len(cost_matrix[0])
        ans = 0

        # hepler function for finding the row difference and the column difference
        def findDiff(grid):
            rowDiff = []
            colDiff = []
            for i in range(len(grid)):
                arr = grid[i][:]
                arr.sort()
                rowDiff.append(arr[1] - arr[0])
            col = 0
            while col < len(grid[0]):
                arr = []
                for i in range(len(grid)):
                    arr.append(grid[i][col])
                arr.sort()
                col += 1
                colDiff.append(arr[1] - arr[0])
            return rowDiff, colDiff

        # loop runs until both the demand and the supply is exhausted
        while max(supply) != 0 or max(demand) != 0:
            # finding the row and col difference
            row, col = findDiff(cost_matrix)
            # finding the maxiumum element in row difference array
            maxi1 = max(row)
            # finding the maxiumum element in col difference array
            maxi2 = max(col)

            # if the row diff max element is greater than or equal to col diff max element
            if (maxi1 >= maxi2):
                for ind, val in enumerate(row):
                    if (val == maxi1):
                        # finding the minimum element in grid index where the maximum was found in the row difference
                        mini1 = min(cost_matrix[ind])
                        for ind2, val2 in enumerate(cost_matrix[ind]):
                            if (val2 == mini1):
                                # calculating the min of supply and demand in that row and col
                                mini2 = min(supply[ind], demand[ind2])
                                ans += mini2 * mini1
                                allocation[ind][ind2] = mini2
                                # subtracting the min from the supply and demand
                                supply[ind] -= mini2
                                demand[ind2] -= mini2
                                # if demand is smaller then the entire col is assigned max value so that the col is eliminated for the next iteration
                                if (demand[ind2] == 0):
                                    for r in range(n):
                                        cost_matrix[r][ind2] = INF
                                # if supply is smaller then the entire row is assigned max value so that the row is eliminated for the next iteration
                                else:
                                    cost_matrix[ind] = [INF for i in range(m)]
                                break
                        break
            # if the row diff max element is greater than col diff max element
            else:
                for ind, val in enumerate(col):
                    if (val == maxi2):
                        # finding the minimum element in grid index where the maximum was found in the col difference
                        mini1 = INF
                        for j in range(n):
                            mini1 = min(mini1, cost_matrix[j][ind])

                        for ind2 in range(n):
                            val2 = cost_matrix[ind2][ind]
                            if val2 == mini1:
                                # calculating the min of supply and demand in that row and col
                                mini2 = min(supply[ind2], demand[ind])
                                ans += mini2 * mini1
                                allocation[ind2][ind] = mini2
                                # subtracting the min from the supply and demand
                                supply[ind2] -= mini2
                                demand[ind] -= mini2
                                # if demand is smaller then the entire col is assigned max value so that the col is eliminated for the next iteration
                                if (demand[ind] == 0):
                                    for r in range(n):
                                        cost_matrix[r][ind] = INF
                                # if supply is smaller then the entire row is assigned max value so that the row is eliminated for the next iteration
                                else:
                                    cost_matrix[ind2] = [INF for i in range(m)]
                                break
                        break

            self.output(supply, demand, new, method, allocation)

        return ans

    def reset(self):
        self.table_frame.destroy()
        self.create_widgets()
        self.steps_inner_frame.destroy()
        self.steps_inner_frame = tk.Frame(self.steps_canvas)
        self.steps_canvas.create_window((0, 0), window=self.steps_inner_frame, anchor="nw")
        self.steps_canvas.configure(scrollregion=self.steps_canvas.bbox("all"))
        self.algorithm_text.config(state=tk.NORMAL)
        self.algorithm_text.delete('1.0', tk.END)
        self.algorithm_text.config(state=tk.DISABLED)

        # Reset the flowchart tab
        self.clear_flowchart()

    def clear_flowchart(self):
        # Clear the flowchart tab
        try:
            # Clear the flowchart canvas
            self.flowchart_canvas.delete(tk.ALL)

            # Reset the inner frame and scrollbar
            self.flowchart_inner_frame = tk.Frame(self.flowchart_canvas)
            self.flowchart_canvas.create_window((0, 0), window=self.flowchart_inner_frame, anchor="nw")

            # Reset scroll region
            self.flowchart_canvas.update_idletasks()  # Update widgets to get correct bbox
            self.flowchart_canvas.configure(scrollregion=self.flowchart_canvas.bbox("all"))
        except Exception as e:
            messagebox.showerror("Error", f"Unable to reset flowchart: {e}")

def main():
    root = tk.Tk()
    root.resizable(False, False)
    app = TransportationProblemSolver(root)
    root.mainloop()

if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter import messagebox, ttk

class TransportationProblemSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Transportation Problem Solver")
        self.root.geometry("800x600")  # Set larger screen size
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

        self.algorithm_frame = tk.Frame(self.notebook)
        self.notebook.add(self.algorithm_frame, text='Algorithm')
        self.algorithm_text = tk.Text(self.algorithm_frame, wrap=tk.WORD)
        self.algorithm_text.pack(expand=1, fill="both")

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
        self.algorithm_text.config(state=tk.NORMAL)
        self.algorithm_text.delete('1.0', tk.END)

        if method == "NorthWest Method":
            algorithm = (
                "NorthWest Method Algorithm:\n\n"
                "1. Start with the cell in the top-left corner (north-west corner) of the cost matrix.\n"
                "2. Allocate as much as possible to the selected cell and adjust the supply and demand.\n"
                "3. Move to the next cell to the right if the current column's demand is met, or move down if the current row's supply is exhausted.\n"
                "4. Repeat steps 2-3 until all supply and demand are met."
            )
        elif method == "Least Cost Method":
            algorithm = (
                "Least Cost Method Algorithm:\n\n"
                "1. Identify the cell with the lowest cost in the cost matrix.\n"
                "2. Allocate as much as possible to the selected cell and adjust the supply and demand.\n"
                "3. Cross out the row or column that has been satisfied.\n"
                "4. Repeat steps 1-3 until all supply and demand are met."
            )
        elif method == "Vogel's Approximation Method":
            algorithm = (
                "Vogel's Approximation Method Algorithm:\n\n"
                "1. For each row and column, calculate the penalty cost (difference between the two lowest costs).\n"
                "2. Identify the row or column with the highest penalty cost.\n"
                "3. Allocate as much as possible to the cell with the lowest cost in the selected row or column and adjust the supply and demand.\n"
                "4. Cross out the row or column that has been satisfied and recalculate penalties.\n"
                "5. Repeat steps 1-4 until all supply and demand are met."
            )

        self.algorithm_text.insert(tk.END, algorithm)
        self.algorithm_text.config(state=tk.DISABLED)

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
        # add logic for vogel_approximation_method

    def reset(self):
        self.table_frame.destroy()
        self.create_widgets()
        self.steps_inner_frame.destroy()
        self.steps_inner_frame = tk.Frame(self.steps_canvas)
        self.steps_canvas.create_window((0, 0), window=self.steps_inner_frame, anchor="nw")
        self.steps_canvas.configure(scrollregion=self.steps_canvas.bbox("all"))

def main():
    root = tk.Tk()
    app = TransportationProblemSolver(root)
    root.mainloop()

if __name__ == "__main__":
    main()

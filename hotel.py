import tkinter as tk
from tkinter import messagebox

# Menu data
menu_items = {
    "Burger": 60,
    "Pizza": 40,
    "Pasta": 50,
    "Salad": 70,
    "Coffe": 80,
    "Fries": 100,
    "Coke": 60,
    "Ice Cream": 90
}

class HotelMenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Restaurant Menu")
        self.root.geometry("650x700")
        self.root.configure(bg="#f9f9f9")

        title = tk.Label(root, text="WELCOME TO PYTHON RESTAURANT", font=("Arial", 20, "bold"), bg="#f9f9f9", fg="#333")
        title.pack(pady=10)

        # Menu Table Frame
        table_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
        table_frame.pack(pady=10)

        headers = ["Item", "Price (₹)", "Quantity", "Select"]
        for col, h in enumerate(headers):
            tk.Label(table_frame, text=h, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=15, pady=5, bd=1, relief="ridge").grid(row=0, column=col)

        self.item_vars = {}
        self.qty_entries = {}

        for index, (item, price) in enumerate(menu_items.items(), start=1):
            bg_color = "#eafaf1" if index % 2 == 0 else "#ffffff"

            tk.Label(table_frame, text=item, font=("Arial", 12), bg=bg_color, width=15, bd=1, relief="ridge").grid(row=index, column=0)
            tk.Label(table_frame, text=f"{price}", font=("Arial", 12), bg=bg_color, width=15, bd=1, relief="ridge").grid(row=index, column=1)

            qty_entry = tk.Entry(table_frame, width=10, font=("Arial", 12), bd=1, relief="solid", justify='center')
            qty_entry.insert(0, "0")
            qty_entry.grid(row=index, column=2, padx=2, pady=2)
            self.qty_entries[item] = qty_entry

            var = tk.IntVar()
            chk = tk.Checkbutton(table_frame, variable=var, bg=bg_color)
            chk.grid(row=index, column=3)
            self.item_vars[item] = var

        # Buttons
        btn_frame = tk.Frame(root, bg="#ffffff")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Calculate Total", font=("Arial", 12), bg="#4CAF50", fg="white", command=self.calculate_total, width=15).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Reset", font=("Arial", 12), bg="#f44336", fg="white", command=self.reset, width=15).grid(row=0, column=1, padx=10)

        # Total Display
        self.result_label = tk.Label(root, text="Total: ₹0", font=("Arial", 16, "bold"), bg="#f9f9f9", fg="green")
        self.result_label.pack(pady=10)

        # Receipt Box
        receipt_label = tk.Label(root, text="Order Receipt", font=("Arial", 14, "bold"), bg="#f9f9f9", fg="#555")
        receipt_label.pack()

        self.receipt_box = tk.Text(root, height=12, width=70, font=("Courier New", 10), bd=2, relief="groove")
        self.receipt_box.pack(pady=5)

        tk.Button(root, text="Save Receipt", font=("Arial", 12), bg="#2196F3", fg="white", command=self.save_receipt).pack(pady=5)

    def calculate_total(self):
        total = 0
        self.receipt_box.delete('1.0', tk.END)
        self.receipt_box.insert(tk.END, "------- Python Restaurant Receipt -------\n")
        self.receipt_box.insert(tk.END, f"{'Item':20} {'Qty':>5} {'Price':>10}\n")
        self.receipt_box.insert(tk.END, "-"*40 + "\n")

        for item in menu_items:
            if self.item_vars[item].get() == 1:
                try:
                    qty = int(self.qty_entries[item].get())
                    if qty <= 0:
                        raise ValueError
                    cost = menu_items[item] * qty
                    total += cost
                    self.receipt_box.insert(tk.END, f"{item:20} {qty:>5} {cost:>10}\n")
                except ValueError:
                    messagebox.showerror("Invalid Input", f"Please enter a valid quantity for {item}.")
                    return

        self.receipt_box.insert(tk.END, "-"*40 + "\n")
        self.receipt_box.insert(tk.END, f"{'Total Amount':25} ₹{total}\n")
        self.result_label.config(text=f"Total: ₹{total}")

    def reset(self):
        for item in menu_items:
            self.item_vars[item].set(0)
            self.qty_entries[item].delete(0, tk.END)
            self.qty_entries[item].insert(0, "0")
        self.result_label.config(text="Total: ₹0")
        self.receipt_box.delete('1.0', tk.END)

    def save_receipt(self):
        receipt_text = self.receipt_box.get("1.0", tk.END).strip()
        if receipt_text:
            try:
                with open("order_receipt.txt", "w", encoding="utf-8") as file:
                    file.write(receipt_text)
                messagebox.showinfo("Success", "Receipt saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save receipt: {e}")
        else:
            messagebox.showwarning("No Receipt", "There's no receipt to save!")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = HotelMenuApp(root)
    root.mainloop()

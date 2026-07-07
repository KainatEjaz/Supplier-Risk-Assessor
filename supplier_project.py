import tkinter as tk
from tkinter import ttk, messagebox

# Store supplier data
suppliers = []

# ------------------------------
# Calculate Risk Score
# ------------------------------
def add_supplier():
    name = entry_name.get()

    if name == "":
        messagebox.showerror("Error", "Supplier name is required.")
        return

    try:
        reliability = float(entry_reliability.get())
        financial = float(entry_financial.get())
        delivery = float(entry_delivery.get())

        if not (0 <= reliability <= 100 and
                0 <= financial <= 100 and
                0 <= delivery <= 100):
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Error",
            "Enter numbers between 0 and 100."
        )
        return

    # Weighted Risk Score
    risk_score = (
        (100 - reliability) * 0.4 +
        (100 - financial) * 0.4 +
        (100 - delivery) * 0.2
    )

    # Risk Category
    if risk_score <= 30:
        risk_level = "Low"
    elif risk_score <= 60:
        risk_level = "Medium"
    else:
        risk_level = "High"

    suppliers.append({
        "name": name,
        "reliability": reliability,
        "financial": financial,
        "delivery": delivery,
        "risk": round(risk_score, 2),
        "level": risk_level
    })

    update_table()
    clear_entries()


# ------------------------------
# Update Table
# ------------------------------
def update_table():
    for item in tree.get_children():
        tree.delete(item)

    suppliers.sort(key=lambda x: x["risk"])

    for index, supplier in enumerate(suppliers, start=1):
        tree.insert("", "end", values=(
            index,
            supplier["name"],
            supplier["reliability"],
            supplier["financial"],
            supplier["delivery"],
            supplier["risk"],
            supplier["level"]
        ))


# ------------------------------
# Clear Entry Boxes
# ------------------------------
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_reliability.delete(0, tk.END)
    entry_financial.delete(0, tk.END)
    entry_delivery.delete(0, tk.END)


# ------------------------------
# Delete Selected Supplier
# ------------------------------
def delete_supplier():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select a supplier first.")
        return

    index = tree.index(selected[0])
    suppliers.pop(index)

    update_table()


# ------------------------------
# Main Window
# ------------------------------
root = tk.Tk()
root.title("Supplier Risk Assessor")
root.geometry("950x550")
root.configure(bg="#EAF4FC")

title = tk.Label(
    root,
    text="Supplier Risk Assessor",
    font=("Arial", 20, "bold"),
    bg="#1565C0",
    fg="white",
    pady=10
)

title.pack(fill="x")

# ------------------------------
# Input Frame
# ------------------------------
frame = tk.Frame(root, bg="#EAF4FC")
frame.pack(pady=10)

tk.Label(frame, text="Supplier Name", bg="#EAF4FC").grid(row=0, column=0, padx=10, pady=5)
entry_name = tk.Entry(frame, width=25)
entry_name.grid(row=0, column=1)

tk.Label(frame, text="Reliability (0-100)", bg="#EAF4FC").grid(row=1, column=0, padx=10, pady=5)
entry_reliability = tk.Entry(frame)
entry_reliability.grid(row=1, column=1)

tk.Label(frame, text="Financial Stability (0-100)", bg="#EAF4FC").grid(row=2, column=0, padx=10, pady=5)
entry_financial = tk.Entry(frame)
entry_financial.grid(row=2, column=1)

tk.Label(frame, text="Delivery Performance (0-100)", bg="#EAF4FC").grid(row=3, column=0, padx=10, pady=5)
entry_delivery = tk.Entry(frame)
entry_delivery.grid(row=3, column=1)

btn_frame = tk.Frame(root, bg="#EAF4FC")
btn_frame.pack()

tk.Button(
    btn_frame,
    text="Add Supplier",
    command=add_supplier,
    bg="green",
    fg="white",
    width=15
).grid(row=0, column=0, padx=10)

tk.Button(
    btn_frame,
    text="Delete Selected",
    command=delete_supplier,
    bg="red",
    fg="white",
    width=15
).grid(row=0, column=1, padx=10)

# ------------------------------
# Table
# ------------------------------
table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True, padx=10, pady=10)

scroll = ttk.Scrollbar(table_frame)
scroll.pack(side="right", fill="y")

columns = (
    "Rank",
    "Supplier",
    "Reliability",
    "Financial",
    "Delivery",
    "Risk Score",
    "Risk Level"
)

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    yscrollcommand=scroll.set
)

scroll.config(command=tree.yview)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=120)

tree.pack(fill="both", expand=True)

root.mainloop()
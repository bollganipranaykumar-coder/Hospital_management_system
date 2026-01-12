from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


class Hospital:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("950x550")

        self.name = StringVar()
        self.ref = StringVar()
        self.dose = StringVar()
        self.patient = StringVar()

        Label(root, text="Hospital Management System",
              font=("Arial", 22, "bold")).pack(pady=10)

        form = Frame(root)
        form.pack(pady=10)

        Label(form, text="Tablet Name").grid(row=0, column=0, padx=5, pady=5)
        Entry(form, textvariable=self.name, width=30).grid(row=0, column=1)

        Label(form, text="Reference No").grid(row=1, column=0, padx=5, pady=5)
        Entry(form, textvariable=self.ref, width=30).grid(row=1, column=1)

        Label(form, text="Dose").grid(row=2, column=0, padx=5, pady=5)
        Entry(form, textvariable=self.dose, width=30).grid(row=2, column=1)

        Label(form, text="Patient Name").grid(row=3, column=0, padx=5, pady=5)
        Entry(form, textvariable=self.patient, width=30).grid(row=3, column=1)

        btn = Frame(root)
        btn.pack(pady=10)

        Button(btn, text="Insert", width=12, command=self.insert_data).grid(row=0, column=0, padx=5)
        Button(btn, text="Update", width=12, command=self.update_data).grid(row=0, column=1, padx=5)
        Button(btn, text="Delete", width=12, command=self.delete_data).grid(row=0, column=2, padx=5)
        Button(btn, text="Clear", width=12, command=self.clear).grid(row=0, column=3, padx=5)
        Button(btn, text="Exit", width=12, command=root.destroy).grid(row=0, column=4, padx=5)

        table_frame = Frame(root)
        table_frame.pack(fill=BOTH, expand=1, padx=10, pady=10)

        scroll = Scrollbar(table_frame)
        scroll.pack(side=RIGHT, fill=Y)

        self.table = ttk.Treeview(
            table_frame,
            columns=("name", "ref", "dose", "patient"),
            yscrollcommand=scroll.set
        )
        scroll.config(command=self.table.yview)

        for c, t in [("name", "Tablet"), ("ref", "Reference"),
                     ("dose", "Dose"), ("patient", "Patient")]:
            self.table.heading(c, text=t)
            self.table.column(c, width=200)

        self.table["show"] = "headings"
        self.table.pack(fill=BOTH, expand=1)
        self.table.bind("<ButtonRelease-1>", self.get_cursor)

        self.create_db()
        self.fetch_data()

    def connect(self):
        return sqlite3.connect("hospital.db")

    def create_db(self):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS hospital (
                name TEXT,
                ref TEXT PRIMARY KEY,
                dose TEXT,
                patient TEXT
            )
        """)
        conn.commit()
        conn.close()

    def insert_data(self):
        if self.name.get() == "" or self.ref.get() == "":
            messagebox.showerror("Error", "Fill required fields")
            return
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO hospital VALUES (?,?,?,?)",
                (self.name.get(), self.ref.get(),
                 self.dose.get(), self.patient.get())
            )
            conn.commit()
            conn.close()
            self.fetch_data()
            messagebox.showinfo("Success", "Record Inserted")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def fetch_data(self):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM hospital")
        rows = cur.fetchall()
        self.table.delete(*self.table.get_children())
        for r in rows:
            self.table.insert("", END, values=r)
        conn.close()

    def update_data(self):
        if self.ref.get() == "":
            messagebox.showerror("Error", "Select a record to update")
            return
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("""
            UPDATE hospital SET
            name=?, dose=?, patient=?
            WHERE ref=?
        """, (
            self.name.get(),
            self.dose.get(),
            self.patient.get(),
            self.ref.get()
        ))
        conn.commit()
        conn.close()
        self.fetch_data()
        messagebox.showinfo("Update", "Record Updated")

    def delete_data(self):
        if self.ref.get() == "":
            return
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM hospital WHERE ref=?", (self.ref.get(),))
        conn.commit()
        conn.close()
        self.fetch_data()
        self.clear()

    def get_cursor(self, e=""):
        row = self.table.item(self.table.focus())["values"]
        if row:
            self.name.set(row[0])
            self.ref.set(row[1])
            self.dose.set(row[2])
            self.patient.set(row[3])

    def clear(self):
        self.name.set("")
        self.ref.set("")
        self.dose.set("")
        self.patient.set("")


if __name__ == "__main__":
    root = Tk()
    Hospital(root)
    root.mainloop()

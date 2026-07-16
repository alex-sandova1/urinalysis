"""Urinalysis Diagnostic Analytics desktop dashboard.

Run with: .venv/bin/python Main.py
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import pandas as pd


APP_DIR = Path(__file__).resolve().parent
DATA_FILE = APP_DIR / "urinalysis_tests.csv"

NAVY = "#062c4a"
NAVY_2 = "#0a3b5f"
BLUE = "#2378e8"
PALE_BLUE = "#eaf3ff"
TEXT = "#102a43"
MUTED = "#62748c"
BORDER = "#dce5f0"
BG = "#f7faff"
GREEN = "#1db66a"
RED = "#ef4e54"
AMBER = "#f3a51a"
PURPLE = "#8c57d9"


def clean(value: object) -> str:
    return str(value).strip().upper() if pd.notna(value) else ""


def range_upper(value: object) -> float:
    """Return the upper end of a value like '6-8' or '15-20'."""
    text = clean(value).replace("–", "-")
    try:
        if text.startswith(">"):
            return float(text[1:]) + 1
        return float(text.split("-")[-1])
    except ValueError:
        return 0.0


def is_abnormal(row: pd.Series) -> bool:
    """Apply the reference ranges in DATA_QUALITY_NOTES.md to one sample."""
    if clean(row["Transparency"]) != "CLEAR":
        return True
    if clean(row["Glucose"]) != "NEGATIVE" or clean(row["Protein"]) != "NEGATIVE":
        return True
    if not 4.5 <= float(row["pH"]) <= 8.0:
        return True
    if not 1.005 <= float(row["Specific Gravity"]) <= 1.030:
        return True
    if range_upper(row["WBC"]) > 5 or range_upper(row["RBC"]) > 2:
        return True
    if clean(row["Epithelial Cells"]) in {"MODERATE", "MANY", "PLENTY", "LOADED"}:
        return True
    if clean(row["Mucous Threads"]) in {"MODERATE", "MANY", "PLENTY", "LOADED"}:
        return True
    if clean(row["Amorphous Urates"]) in {"MODERATE", "MANY", "PLENTY", "LOADED"}:
        return True
    # The source uses RARE/OCCASIONAL where the notes use "none to few".
    return clean(row["Bacteria"]) not in {"", "NONE", "NONE SEEN", "RARE", "OCCASIONAL"}


class Dashboard(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Urinalysis Diagnostic Analytics")
        self.geometry("1500x930")
        self.minsize(1180, 760)
        self.configure(bg=BG)
        self.data = self.load_data()
        self.filtered = self.data.copy()
        self.diagnosis_var = tk.StringVar(value="All results")
        self.search_var = tk.StringVar()
        self.parameter_var = tk.StringVar(value="Protein")
        self.build_styles()
        self.build_ui()
        self.refresh()

    def load_data(self) -> pd.DataFrame:
        try:
            frame = pd.read_csv(DATA_FILE)
        except Exception as exc:
            messagebox.showerror("Data unavailable", f"Could not read {DATA_FILE.name}:\n{exc}")
            raise
        frame["Overall Status"] = frame.apply(
            lambda row: "Abnormal" if is_abnormal(row) else "Normal", axis=1
        )
        frame["Sample ID"] = frame["ID"].apply(lambda item: f"SMP-{int(item):05d}")
        return frame

    def build_styles(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Dash.Treeview", background="white", foreground=TEXT,
                        fieldbackground="white", rowheight=27, font=("Arial", 9))
        style.configure("Dash.Treeview.Heading", background="#f4f7fb", foreground=TEXT,
                        font=("Arial", 9, "bold"), relief="flat")
        style.map("Dash.Treeview", background=[("selected", "#dcecff")])
        style.configure("Dash.TCombobox", padding=6, font=("Arial", 10))

    def build_ui(self) -> None:
        header = tk.Frame(self, bg="white", height=47, highlightbackground=BORDER,
                          highlightthickness=1)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="⚗", font=("Arial", 20), fg=BLUE, bg="white").pack(side="left", padx=(24, 10))
        tk.Label(header, text="Urinalysis Diagnostic Analytics", font=("Arial", 12, "bold"),
                 fg=TEXT, bg="white").pack(side="left")

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True)
        self.build_sidebar(body)
        main = tk.Frame(body, bg=BG)
        main.pack(side="left", fill="both", expand=True, padx=22, pady=20)
        self.build_filters(main)
        self.cards_frame = tk.Frame(main, bg=BG)
        self.cards_frame.pack(fill="x", pady=(18, 18))
        charts = tk.Frame(main, bg=BG)
        charts.pack(fill="both", expand=True)
        charts.grid_columnconfigure((0, 1, 2), weight=1, uniform="charts")
        charts.grid_rowconfigure(0, weight=1)
        self.abnormal_panel = self.make_panel(charts, "Abnormal Samples by Parameter")
        self.abnormal_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 7))
        self.diagnosis_panel = self.make_panel(charts, "Samples by Lab Result")
        self.diagnosis_panel.grid(row=0, column=1, sticky="nsew", padx=7)
        self.parameter_panel = self.make_panel(charts, "Parameter Distribution (Normal vs Abnormal)")
        self.parameter_panel.grid(row=0, column=2, sticky="nsew", padx=(7, 0))
        self.build_averages(main)
        self.build_table(main)

    def build_sidebar(self, parent: tk.Widget) -> None:
        side = tk.Frame(parent, bg=NAVY, width=240)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)
        tk.Label(side, text="⚗", bg=NAVY, fg="#81b9ff", font=("Arial", 37)).pack(anchor="w", padx=25, pady=(25, 0))
        tk.Label(side, text="Urinalysis", bg=NAVY, fg="white", font=("Arial", 18, "bold")).pack(anchor="w", padx=25)
        tk.Label(side, text="Analytics Dashboard", bg=NAVY, fg="#c5d7e8", font=("Arial", 10)).pack(anchor="w", padx=26, pady=(2, 25))
        for icon, label in [("▦", "Dashboard"), ("▤", "Data Explorer"), ("♟", "Patient Samples"),
                            ("⌁", "Analysis & Trends"), ("⚠", "Quality Flags"), ("▧", "Reports"),
                            ("⚙", "Settings"), ("ⓘ", "About")]:
            active = label == "Dashboard"
            item = tk.Frame(side, bg=BLUE if active else NAVY, height=46)
            item.pack(fill="x", padx=17, pady=2)
            item.pack_propagate(False)
            icon_label = tk.Label(item, text=icon, bg=item.cget("bg"), fg="white", font=("Arial", 16))
            icon_label.pack(side="left", padx=(12, 14))
            text_label = tk.Label(item, text=label, bg=item.cget("bg"), fg="white", font=("Arial", 10, "bold" if active else "normal"))
            text_label.pack(side="left")
            if label == "Patient Samples":
                item.configure(cursor="hand2")
                icon_label.configure(cursor="hand2")
                text_label.configure(cursor="hand2")
                item.bind("<Button-1>", lambda _event: self.open_all_samples())
                icon_label.bind("<Button-1>", lambda _event: self.open_all_samples())
                text_label.bind("<Button-1>", lambda _event: self.open_all_samples())
        summary = tk.Frame(side, bg=NAVY_2, padx=15, pady=14)
        summary.pack(side="bottom", fill="x", padx=17, pady=18)
        tk.Label(summary, text="DATASET OVERVIEW", bg=NAVY_2, fg="white", font=("Arial", 9, "bold")).pack(anchor="w", pady=(0, 11))
        self.sidebar_summary = tk.Label(summary, bg=NAVY_2, fg="#d8e8f8", font=("Arial", 9), justify="left", anchor="w")
        self.sidebar_summary.pack(fill="x")

    def build_filters(self, parent: tk.Widget) -> None:
        filters = tk.Frame(parent, bg=BG)
        filters.pack(fill="x")
        self.filter_box(filters, "Diagnosis Filter", self.diagnosis_var, ["All results", "NEGATIVE", "POSITIVE"], 205).pack(side="left", padx=(0, 16))
        search = tk.Frame(filters, bg=BG)
        search.pack(side="left")
        tk.Label(search, text="Search Sample ID", bg=BG, fg=TEXT, font=("Arial", 9, "bold")).pack(anchor="w", pady=(0, 7))
        entry = tk.Entry(search, textvariable=self.search_var, width=25, bd=1, relief="solid", font=("Arial", 10), fg=TEXT)
        entry.pack(ipady=7)
        entry.bind("<KeyRelease>", lambda _event: self.refresh())
        tk.Button(filters, text="↥  Export Report", command=self.export_report, bg=BLUE, fg="white", bd=0,
                  activebackground="#1266d0", activeforeground="white", font=("Arial", 10, "bold"), padx=15, pady=9).pack(side="right", pady=22)

    def filter_box(self, parent: tk.Widget, label: str, variable: tk.StringVar, values: list[str], width: int) -> tk.Frame:
        box = tk.Frame(parent, bg=BG, width=width)
        box.pack_propagate(False)
        tk.Label(box, text=label, bg=BG, fg=TEXT, font=("Arial", 9, "bold")).pack(anchor="w", pady=(0, 7))
        combo = ttk.Combobox(box, textvariable=variable, values=values, state="readonly", width=22, style="Dash.TCombobox")
        combo.pack(fill="x")
        combo.bind("<<ComboboxSelected>>", lambda _event: self.refresh())
        return box

    def make_panel(self, parent: tk.Widget, title: str) -> tk.Frame:
        panel = tk.Frame(parent, bg="white", highlightbackground=BORDER, highlightthickness=1)
        tk.Label(panel, text=title, bg="white", fg=TEXT, font=("Arial", 10, "bold")).pack(anchor="w", padx=15, pady=(14, 4))
        return panel

    def build_averages(self, parent: tk.Widget) -> None:
        panel = tk.Frame(parent, bg="#f4f8ff", highlightbackground=BORDER, highlightthickness=1)
        panel.pack(fill="x", pady=12)
        tk.Label(panel, text="Key Averages", bg="#f4f8ff", fg=TEXT, font=("Arial", 10, "bold")).pack(anchor="w", padx=15, pady=(11, 2))
        self.averages = tk.Frame(panel, bg="#f4f8ff")
        self.averages.pack(fill="x", padx=12, pady=(3, 12))

    def build_table(self, parent: tk.Widget) -> None:
        panel = tk.Frame(parent, bg="white", highlightbackground=BORDER, highlightthickness=1)
        panel.pack(fill="both", expand=True)
        table_header = tk.Frame(panel, bg="white")
        table_header.pack(fill="x", padx=15, pady=(9, 7))
        tk.Label(table_header, text="Recent Samples", bg="white", fg=TEXT,
                 font=("Arial", 10, "bold")).pack(side="left")
        tk.Button(table_header, text="View all samples  →", command=self.open_all_samples,
                  bg="white", fg=BLUE, bd=0, cursor="hand2", font=("Arial", 9, "bold"),
                  activebackground="white", activeforeground="#1266d0").pack(side="right")
        columns = ("Sample ID", "Age", "Sex", "Color", "Transparency", "pH", "Specific Gravity", "Protein", "Glucose", "WBC", "RBC", "Bacteria", "Diagnosis", "Overall Status")
        tree_box = tk.Frame(panel, bg="white")
        tree_box.pack(fill="both", expand=True, padx=1)
        self.tree = ttk.Treeview(tree_box, columns=columns, show="headings", style="Dash.Treeview", height=7)
        scroll = ttk.Scrollbar(tree_box, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=scroll.set)
        widths = [100, 50, 55, 100, 115, 55, 110, 82, 82, 75, 70, 90, 85, 105]
        for column, width in zip(columns, widths):
            self.tree.heading(column, text=column)
            self.tree.column(column, width=width, minwidth=50, anchor="center")
        self.tree.tag_configure("Normal", foreground="#12834a")
        self.tree.tag_configure("Abnormal", foreground="#d9363e")
        self.tree.pack(fill="both", expand=True)
        scroll.pack(fill="x")

    def refresh(self) -> None:
        frame = self.data.copy()
        diagnosis = self.diagnosis_var.get()
        if diagnosis != "All results":
            frame = frame[frame["Diagnosis"] == diagnosis]
        term = self.search_var.get().strip().upper()
        if term:
            frame = frame[frame["Sample ID"].str.contains(term, na=False)]
        self.filtered = frame
        self.draw_cards()
        self.draw_abnormal_chart()
        self.draw_diagnosis_chart()
        self.draw_parameter_chart()
        self.draw_averages()
        self.draw_table()
        total = len(frame)
        abnormal = int((frame["Overall Status"] == "Abnormal").sum())
        normal = total - abnormal
        self.sidebar_summary.configure(text=f"Total Samples                              {total}\n\nAbnormal Samples                {abnormal} ({abnormal / total:.1%}" + ")" if total else "Total Samples                              0")
        if total:
            self.sidebar_summary.configure(text=f"Total Samples                              {total}\n\nAbnormal Samples                {abnormal} ({abnormal / total:.1%})\n\nNormal Samples                    {normal} ({normal / total:.1%})\n\nDataset: urinalysis_tests.csv")

    def draw_cards(self) -> None:
        for widget in self.cards_frame.winfo_children(): widget.destroy()
        total = len(self.filtered)
        abnormal = int((self.filtered["Overall Status"] == "Abnormal").sum())
        normal = total - abnormal
        items = [("⚗", "Total Samples", str(total), "Filtered dataset", BLUE), ("✓", "Normal Samples", str(normal), f"{normal / total:.1%}" if total else "—", GREEN),
                 ("⚠", "Abnormal Samples", str(abnormal), f"{abnormal / total:.1%}" if total else "—", RED), ("⌁", "Parameters Analyzed", "10", "Quality measures", AMBER),
                 ("▣", "Positive Results", str(int((self.filtered['Diagnosis'] == 'POSITIVE').sum())), "Lab-positive samples", PURPLE)]
        for icon, label, number, detail, color in items:
            card = tk.Frame(self.cards_frame, bg="white", highlightbackground=BORDER, highlightthickness=1, width=190, height=117)
            card.pack(side="left", fill="x", expand=True, padx=5)
            card.pack_propagate(False)
            tk.Label(card, text=icon, bg="#eef5ff", fg=color, font=("Arial", 23, "bold"), width=3).pack(side="left", padx=(14, 8), pady=25)
            info = tk.Frame(card, bg="white")
            info.pack(side="left", pady=17, anchor="w")
            tk.Label(info, text=label, bg="white", fg=TEXT, font=("Arial", 9, "bold")).pack(anchor="w")
            tk.Label(info, text=number, bg="white", fg=TEXT, font=("Arial", 22, "bold")).pack(anchor="w")
            tk.Label(info, text=detail, bg="white", fg=MUTED, font=("Arial", 8)).pack(anchor="w")

    def chart_canvas(self, panel: tk.Frame) -> tk.Canvas:
        for widget in panel.winfo_children()[1:]: widget.destroy()
        canvas = tk.Canvas(panel, bg="white", highlightthickness=0, height=242)
        canvas.pack(fill="both", expand=True, padx=10, pady=(1, 10))
        return canvas

    def abnormal_columns(self) -> dict[str, pd.Series]:
        return {
            "Transparency": self.filtered["Transparency"].map(lambda v: clean(v) != "CLEAR"),
            "Glucose": self.filtered["Glucose"].map(lambda v: clean(v) != "NEGATIVE"),
            "Protein": self.filtered["Protein"].map(lambda v: clean(v) != "NEGATIVE"),
            "pH": ~self.filtered["pH"].between(4.5, 8.0),
            "Specific Gravity": ~self.filtered["Specific Gravity"].between(1.005, 1.030),
            "WBC": self.filtered["WBC"].map(lambda v: range_upper(v) > 5),
            "RBC": self.filtered["RBC"].map(lambda v: range_upper(v) > 2),
            "Epithelial Cells": self.filtered["Epithelial Cells"].map(lambda v: clean(v) in {"MODERATE", "MANY", "PLENTY", "LOADED"}),
            "Mucous Threads": self.filtered["Mucous Threads"].map(lambda v: clean(v) in {"MODERATE", "MANY", "PLENTY", "LOADED"}),
            "Bacteria": self.filtered["Bacteria"].map(lambda v: clean(v) not in {"", "NONE", "NONE SEEN", "RARE", "OCCASIONAL"}),
        }

    @staticmethod
    def flag_count(values: pd.Series) -> int:
        """Count a flag series safely, including an empty filtered result."""
        return sum(bool(value) for value in values)

    def draw_abnormal_chart(self) -> None:
        canvas = self.chart_canvas(self.abnormal_panel)
        counts = sorted(((name, self.flag_count(values)) for name, values in self.abnormal_columns().items()), key=lambda x: x[1], reverse=True)[:8]
        width, height = max(canvas.winfo_width(), 300), 238
        max_count = max((value for _, value in counts), default=1) or 1
        for index, (name, value) in enumerate(counts):
            y = 10 + index * 27
            canvas.create_text(103, y + 9, text=name, anchor="e", fill=TEXT, font=("Arial", 8))
            end = 112 + (width - 185) * value / max_count
            canvas.create_rectangle(112, y, end, y + 18, fill=RED, outline="")
            canvas.create_text(end + 7, y + 9, text=f"{value} ({value / len(self.filtered):.1%})" if len(self.filtered) else "0", anchor="w", fill=TEXT, font=("Arial", 8))

    def draw_diagnosis_chart(self) -> None:
        canvas = self.chart_canvas(self.diagnosis_panel)
        values = Counter(self.filtered["Diagnosis"])
        total = sum(values.values()) or 1
        colors = {"NEGATIVE": BLUE, "POSITIVE": RED}
        start = 90
        for name, count in values.items():
            extent = count / total * 360
            canvas.create_arc(35, 35, 190, 190, start=start, extent=extent, fill=colors.get(name, PURPLE), outline="white", width=2)
            start += extent
        canvas.create_oval(82, 82, 143, 143, fill="white", outline="white")
        canvas.create_text(112, 105, text=str(sum(values.values())), fill=TEXT, font=("Arial", 15, "bold"))
        canvas.create_text(112, 124, text="samples", fill=MUTED, font=("Arial", 8))
        y = 55
        for name, count in values.items():
            canvas.create_rectangle(210, y, 220, y + 10, fill=colors.get(name, PURPLE), outline="")
            canvas.create_text(228, y + 5, text=f"{name.title():<9} {count:>4} ({count / total:.1%})", anchor="w", fill=TEXT, font=("Arial", 9))
            y += 32

    def draw_parameter_chart(self) -> None:
        for widget in self.parameter_panel.winfo_children()[1:]: widget.destroy()
        top = tk.Frame(self.parameter_panel, bg="white")
        top.pack(fill="x", padx=12)
        ttk.Combobox(top, textvariable=self.parameter_var, values=list(self.abnormal_columns()), state="readonly", width=17, style="Dash.TCombobox").pack(side="right")
        # Rebind every time because this control is recreated with the panel.
        top.winfo_children()[0].bind("<<ComboboxSelected>>", lambda _event: self.draw_parameter_chart())
        canvas = tk.Canvas(self.parameter_panel, bg="white", highlightthickness=0, height=218)
        canvas.pack(fill="both", expand=True, padx=15, pady=(2, 10))
        abnormal = self.flag_count(self.abnormal_columns()[self.parameter_var.get()])
        normal = len(self.filtered) - abnormal
        largest = max(normal, abnormal, 1)
        bottom = 180
        for x, label, count, color in [(70, "Normal", normal, GREEN), (200, "Abnormal", abnormal, RED)]:
            top_y = bottom - 135 * count / largest
            canvas.create_rectangle(x, top_y, x + 62, bottom, fill=color, outline="")
            canvas.create_text(x + 31, top_y - 10, text=str(count), fill=TEXT, font=("Arial", 9, "bold"))
            canvas.create_text(x + 31, bottom + 15, text=label, fill=TEXT, font=("Arial", 9))
            canvas.create_text(x + 31, bottom + 30, text=f"{count / len(self.filtered):.1%}" if len(self.filtered) else "—", fill=MUTED, font=("Arial", 8))
        canvas.create_line(42, bottom, 286, bottom, fill="#b9c6d5")

    def draw_averages(self) -> None:
        for widget in self.averages.winfo_children(): widget.destroy()
        frame = self.filtered
        data = [("Average pH", f"{frame['pH'].mean():.2f}" if len(frame) else "—", "◉", BLUE),
                ("Avg Specific Gravity", f"{frame['Specific Gravity'].mean():.3f}" if len(frame) else "—", "⚗", BLUE),
                ("Average WBC (HPF)", f"{frame['WBC'].map(range_upper).mean():.1f}" if len(frame) else "—", "◌", BLUE),
                ("Average RBC (HPF)", f"{frame['RBC'].map(range_upper).mean():.1f}" if len(frame) else "—", "♦", RED),
                ("Protein Positive Rate", f"{(frame['Protein'].map(lambda v: clean(v) != 'NEGATIVE')).mean():.1%}" if len(frame) else "—", "⚑", BLUE),
                ("Glucose Positive Rate", f"{(frame['Glucose'].map(lambda v: clean(v) != 'NEGATIVE')).mean():.1%}" if len(frame) else "—", "◇", BLUE)]
        for icon, label, value, color in data:
            item = tk.Frame(self.averages, bg="#f4f8ff")
            item.pack(side="left", fill="x", expand=True)
            tk.Label(item, text=icon, bg="#e3efff", fg=color, font=("Arial", 16, "bold"), width=3).pack(side="left", padx=(4, 7), pady=7)
            text = tk.Frame(item, bg="#f4f8ff")
            text.pack(side="left", pady=6)
            tk.Label(text, text=label, bg="#f4f8ff", fg=TEXT, font=("Arial", 8, "bold")).pack(anchor="w")
            tk.Label(text, text=value, bg="#f4f8ff", fg=TEXT, font=("Arial", 14, "bold")).pack(anchor="w")

    def draw_table(self) -> None:
        self.tree.delete(*self.tree.get_children())
        columns = ["Sample ID", "Age", "Gender", "Color", "Transparency", "pH", "Specific Gravity", "Protein", "Glucose", "WBC", "RBC", "Bacteria", "Diagnosis", "Overall Status"]
        for _, row in self.filtered.head(100).iterrows():
            values = self.table_values(row, columns)
            self.tree.insert("", "end", values=values, tags=(row["Overall Status"],))

    @staticmethod
    def table_values(row: pd.Series, columns: list[str]) -> list[object]:
        """Format data consistently in both the dashboard and data explorer."""
        values = [row[column] for column in columns]
        if "Gender" in columns:
            gender_index = columns.index("Gender")
            values[gender_index] = str(values[gender_index]).title()[0] if str(values[gender_index]) else "—"
        if "Diagnosis" in columns:
            values[columns.index("Diagnosis")] = str(values[columns.index("Diagnosis")]).title()
        if "Overall Status" in columns:
            status_index = columns.index("Overall Status")
            values[status_index] = "● " + str(values[status_index])
        return values

    def open_all_samples(self) -> None:
        """Open the full, currently filtered dataset in its own scrollable window."""
        window = tk.Toplevel(self)
        window.title("All Urinalysis Samples")
        window.geometry("1450x760")
        window.minsize(900, 500)
        window.configure(bg=BG)
        tk.Label(window, text="All Data Samples", bg=BG, fg=TEXT,
                 font=("Arial", 16, "bold")).pack(anchor="w", padx=22, pady=(20, 2))
        tk.Label(window, text=f"Showing all {len(self.filtered):,} samples matching the current dashboard filters.",
                 bg=BG, fg=MUTED, font=("Arial", 10)).pack(anchor="w", padx=22, pady=(0, 15))
        table_box = tk.Frame(window, bg="white", highlightbackground=BORDER, highlightthickness=1)
        table_box.pack(fill="both", expand=True, padx=22, pady=(0, 22))
        columns = ["Sample ID", "Age", "Gender", "Color", "Transparency", "Glucose", "Protein", "pH",
                   "Specific Gravity", "WBC", "RBC", "Epithelial Cells", "Mucous Threads",
                   "Amorphous Urates", "Bacteria", "Diagnosis", "Overall Status"]
        tree = ttk.Treeview(table_box, columns=columns, show="headings", style="Dash.Treeview")
        vertical = ttk.Scrollbar(table_box, orient="vertical", command=tree.yview)
        horizontal = ttk.Scrollbar(table_box, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        for column in columns:
            width = max(75, len(column) * 9 + 25)
            tree.heading(column, text=column)
            tree.column(column, width=width, minwidth=65, anchor="center")
        tree.tag_configure("Normal", foreground="#12834a")
        tree.tag_configure("Abnormal", foreground="#d9363e")
        for _, row in self.filtered.iterrows():
            tree.insert("", "end", values=self.table_values(row, columns), tags=(row["Overall Status"],))
        tree.grid(row=0, column=0, sticky="nsew")
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        table_box.grid_columnconfigure(0, weight=1)
        table_box.grid_rowconfigure(0, weight=1)

    def export_report(self) -> None:
        target = filedialog.asksaveasfilename(title="Export filtered report", defaultextension=".csv", initialfile="urinalysis_dashboard_report.csv", filetypes=[("CSV files", "*.csv")])
        if not target:
            return
        self.filtered.to_csv(target, index=False, quoting=csv.QUOTE_MINIMAL)
        messagebox.showinfo("Report exported", f"Saved {len(self.filtered)} samples to:\n{target}")


if __name__ == "__main__":
    Dashboard().mainloop()

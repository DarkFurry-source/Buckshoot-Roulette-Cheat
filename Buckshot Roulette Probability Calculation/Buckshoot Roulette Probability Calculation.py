import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, Spinbox
import random
import os
import json
from collections import Counter

class BuckshotGUI:
    def __init__(self, root):
        self.inverted_last_round = False
        self.root = root
        self.root.title("Buckshot Roulette: Python Edition")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        self.data_path = os.path.join(os.path.dirname(__file__), "Learning behavior")
        self.data_file = os.path.join(self.data_path, "Learning behavior Buckshot Roulette.json")
        self.load_weights()

        self.title_label = tk.Label(root, text="=== Buckshot Roulette: Python Edition ===", font=("Courier", 18, "bold"), fg="white", bg="black")
        self.title_label.pack(pady=10)

        self.probability_label = tk.Label(root, text="Probability: -", font=("Helvetica", 12), fg="lightgray", bg="black")
        self.probability_label.pack(pady=5)

        self.start_button = tk.Button(root, text="Press Start", font=("Helvetica", 16), command=self.setup_game, bg="red", fg="white", width=20, height=2)
        self.start_button.pack(pady=20)

        self.invert_button = None
        self.items = []
        self.counts = {'rot': 0, 'blau': 0}
        self.prediction = None
        self.ITEM_LIST = [
            "Adrenaline", "Beer", "Burner Phone", "Cigarette Pack",
            "Expired Medicine", "Hand Saw", "Handcuffs", "Inverter",
            "Jammer", "Magnifying Glass", "Remote"
        ]

    def load_weights(self):
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
        if os.path.isfile(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    content = f.read().strip()
                    self.weights = json.loads(content) if content else {'rot': 1.0, 'blau': 1.0}
            except (json.JSONDecodeError, IOError):
                self.weights = {'rot': 1.0, 'blau': 1.0}
        else:
            self.weights = {'rot': 1.0, 'blau': 1.0}

    def save_weights(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.weights, f)
        print("[DEBUG] Learning saved:", self.weights)

    def setup_game(self):
        self.start_button.pack_forget()

        rote = simpledialog.askinteger("Red Shells", "Number of red shells (live):", minvalue=0)
        blaue = simpledialog.askinteger("Blue Shells", "Number of blue shells (empty):", minvalue=0)

        if rote is None or blaue is None:
            messagebox.showinfo("Aborted", "Game start canceled.")
            return

        self.counts = {'rot': rote, 'blau': blaue}
        self.update_title_label()
        self.ask_items()

    def update_title_label(self):
        self.title_label.config(text=f"→ Round: {self.counts['rot']} red, {self.counts['blau']} blue")

    def ask_items(self):
        if not messagebox.askyesno("Items", "Are items in play?"):
            self.start_round()
            return

        max_items = simpledialog.askinteger("Items on the table", "How many items (max 8)?", minvalue=0, maxvalue=8)
        if max_items is None or max_items == 0:
            self.start_round()
            return

        self.item_selection_window = Toplevel(self.root)
        self.item_selection_window.title("Item Selection")
        self.item_selection_window.configure(bg="black")

        tk.Label(self.item_selection_window, text=f"Select amount per item (max total {max_items}):", fg="white", bg="black", font=("Helvetica", 12)).pack(pady=10)

        self.item_spinboxes = []
        for item in self.ITEM_LIST:
            frame = tk.Frame(self.item_selection_window, bg="black")
            frame.pack(anchor="w")
            tk.Label(frame, text=item, fg="white", bg="black", width=25, anchor="w").pack(side="left")
            spin = Spinbox(frame, from_=0, to=max_items, width=5)
            spin.pack(side="left")
            self.item_spinboxes.append((item, spin))

        tk.Button(self.item_selection_window, text="Done", command=lambda: self.finish_item_quantity_selection(max_items), bg="green", fg="white").pack(pady=10)

    def finish_item_quantity_selection(self, max_items):
        selected_items = []
        total = 0
        for item, spin in self.item_spinboxes:
            count = int(spin.get())
            if count > 0:
                selected_items.extend([item] * count)
                total += count

        if total > max_items:
            messagebox.showerror("Too many items", f"Please select no more than {max_items} items in total.")
            return

        self.items = selected_items
        self.item_selection_window.destroy()
        self.start_round()

    def get_weighted_prediction(self):
        valid_colors = [c for c in self.counts if self.counts[c] > 0]
        weighted_options = {
            color: self.counts[color] * self.weights[color]
            for color in valid_colors
        }
        total = sum(weighted_options.values())

        if total > 0:
            r_chance = weighted_options.get('rot', 0) / total * 100
            b_chance = weighted_options.get('blau', 0) / total * 100
            self.probability_label.config(text=f"Probability: Red {r_chance:.1f}% | Blue {b_chance:.1f}%")

        rand = random.uniform(0, total)
        cumulative = 0
        for color, value in weighted_options.items():
            cumulative += value
            if rand <= cumulative:
                return color
        return random.choice(valid_colors)

    def start_round(self):
        if hasattr(self, 'round_frame'):
            self.round_frame.destroy()
        self.round_frame = tk.Frame(self.root, bg="black")
        self.round_frame.pack(pady=20)
        self.update_round()

    def update_round(self):
        for widget in self.round_frame.winfo_children():
            widget.destroy()

        if self.counts['rot'] + self.counts['blau'] == 0:
            if messagebox.askyesno("Round finished", "All shells have been used. Start a new round?"):
                self.setup_game()
            return

        self.update_title_label()
        self.prediction = self.get_weighted_prediction()

        max_items_to_show = min(len(self.items), 3)
        shown_items = []
        pool = Counter(self.items)
        for item in pool:
            if pool[item] >= 2 and item == "Hand Saw" and self.prediction == "rot":
                shown_items.append(item)
            else:
                shown_items.extend([item] * min(pool[item], 1))
        shown_items = random.sample(shown_items, min(3, len(shown_items)))

        self.prediction_label = tk.Label(self.round_frame, text=f"Next shell: {self.prediction.upper()}", fg="white", bg="black", font=("Helvetica", 14))
        self.prediction_label.pack(pady=10)

        if shown_items:
            tk.Label(self.round_frame, text="Dealer might use these items:", fg="cyan", bg="black", font=("Helvetica", 12)).pack(pady=5)
            for item in shown_items:
                tk.Label(self.round_frame, text=f"- {item}", fg="white", bg="black").pack(anchor="w")

        if self.items:
            tk.Label(self.round_frame, text="Which items did the dealer use?", fg="yellow", bg="black", font=("Helvetica", 12)).pack(pady=5)
            self.item_vars = []
            unique_items = sorted(set(self.items))
            for item in unique_items:
                var = tk.IntVar()
                cb = tk.Checkbutton(self.round_frame, text=item, variable=var, fg="white", bg="black", selectcolor="gray")
                cb.pack(anchor="w")
                self.item_vars.append((item, var))

        tk.Label(self.round_frame, text="Which shell was drawn?", fg="white", bg="black").pack(pady=10)
        tk.Button(self.round_frame, text="RED", command=lambda: self.evaluate_choice("rot", self.prediction), bg="darkred", fg="white", width=15).pack(pady=2)
        tk.Button(self.round_frame, text="BLUE", command=lambda: self.evaluate_choice("blau", self.prediction), bg="blue", fg="white", width=15).pack(pady=2)
        tk.Button(self.round_frame, text="ABORT GAME", command=self.abort_round, bg="gray", fg="white", width=20).pack(pady=10)
        tk.Button(self.round_frame, text="INVERTER USED?", command=self.invert_prediction, bg="orange", fg="black", width=20).pack(pady=5)

    def invert_prediction(self):
        if self.prediction:
            alte = self.prediction
            self.prediction = 'blau' if self.prediction == 'rot' else 'rot'
            self.inverted_last_round = True
            messagebox.showinfo("Prediction Inverted", f"Was: {alte.upper()} → Now: {self.prediction.upper()}")
            if hasattr(self, 'prediction_label'):
                self.prediction_label.config(text=f"Next shell: {self.prediction.upper()}")

    def evaluate_choice(self, gezogen, prediction):
        if self.inverted_last_round:
            prediction = 'rot' if prediction == 'blau' else 'blau'
            self.inverted_last_round = False

        if prediction != gezogen:
            self.weights[gezogen] += 1.0
            self.save_weights()

        if self.counts[gezogen] > 0:
            self.counts[gezogen] -= 1

        self.update_title_label()

        if hasattr(self, 'item_vars'):
            used_items = [item for item, var in self.item_vars if var.get() == 1]
            for item in used_items:
                if item in self.items:
                    self.items.remove(item)

        self.update_round()

    def abort_round(self):
        messagebox.showinfo("Aborted", "Round was aborted early.")
        self.setup_game()

if __name__ == "__main__":
    root = tk.Tk()
    app = BuckshotGUI(root)
    root.mainloop()

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

        self.data_path = os.path.join(os.path.dirname(__file__), "LearningData")
        self.data_file = os.path.join(self.data_path, "Buckshot_Learning.json")
        self.load_learning_data()

        self.title_label = tk.Label(
            root,
            text="=== Buckshot Roulette: Python Edition ===",
            font=("Courier", 18, "bold"),
            fg="white",
            bg="black"
        )
        self.title_label.pack(pady=10)

        self.probability_label = tk.Label(
            root,
            text="Prediction: -",
            font=("Helvetica", 12),
            fg="lightgray",
            bg="black"
        )
        self.probability_label.pack(pady=5)

        self.start_button = tk.Button(
            root,
            text="Start Game",
            font=("Helvetica", 16),
            command=self.setup_game,
            bg="red",
            fg="white",
            width=20,
            height=2
        )
        self.start_button.pack(pady=20)

        self.invert_button = None
        self.items = []
        self.counts = {'red': 0, 'blue': 0}
        self.prediction = None
        self.ITEM_LIST = [
            "Adrenaline", "Beer", "Burner Phone", "Cigarette Pack",
            "Expired Medicine", "Hand Saw", "Handcuffs", "Inverter",
            "Jammer", "Magnifying Glass", "Remote"
        ]

    def load_learning_data(self):
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
        if os.path.isfile(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    content = f.read().strip()
                    self.learn_data = json.loads(content) if content else {
                        'shells': {'red': 1.0, 'blue': 1.0},
                        'items': {'correct': {}, 'wrong': {}}
                    }
            except (json.JSONDecodeError, IOError):
                self.learn_data = {
                    'shells': {'red': 1.0, 'blue': 1.0},
                    'items': {'correct': {}, 'wrong': {}}
                }
        else:
            self.learn_data = {
                'shells': {'red': 1.0, 'blue': 1.0},
                'items': {'correct': {}, 'wrong': {}}
            }

    def save_learning_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.learn_data, f, indent=2)
        print("[DEBUG] Saved learning data:", self.learn_data)

    def setup_game(self):
        self.start_button.pack_forget()

        red = simpledialog.askinteger("Red Shells", "How many red shells (live)?", minvalue=0)
        blue = simpledialog.askinteger("Blue Shells", "How many blue shells (empty)?", minvalue=0)

        if red is None or blue is None:
            messagebox.showinfo("Canceled", "Game start canceled.")
            return

        self.counts = {'red': red, 'blue': blue}
        self.update_title_label()

        self.ask_items()

    def update_title_label(self):
        self.title_label.config(text=f"→ Round: {self.counts['red']} red, {self.counts['blue']} blue")

    def ask_items(self):
        if not messagebox.askyesno("Items", "Are there items on the table?"):
            self.start_round()
            return

        max_items = simpledialog.askinteger("Items", "How many items (max 8)?", minvalue=0, maxvalue=8)
        if max_items is None or max_items == 0:
            self.start_round()
            return

        self.item_selection_window = Toplevel(self.root)
        self.item_selection_window.title("Item Selection")
        self.item_selection_window.configure(bg="black")

        tk.Label(self.item_selection_window, text=f"Select amount per item (max {max_items} total):", fg="white", bg="black", font=("Helvetica", 12)).pack(pady=10)

        self.item_spinboxes = []
        for item in self.ITEM_LIST:
            frame = tk.Frame(self.item_selection_window, bg="black")
            frame.pack(anchor="w")
            tk.Label(frame, text=item, fg="white", bg="black", width=25, anchor="w").pack(side="left")
            spin = Spinbox(frame, from_=0, to=max_items, width=5)
            spin.pack(side="left")
            self.item_spinboxes.append((item, spin))

        tk.Button(self.item_selection_window, text="Confirm", command=lambda: self.finish_item_quantity_selection(max_items), bg="green", fg="white").pack(pady=10)

    def finish_item_quantity_selection(self, max_items):
        selected_items = []
        total = 0
        for item, spin in self.item_spinboxes:
            count = int(spin.get())
            if count > 0:
                selected_items.extend([item] * count)
                total += count

        if total > max_items:
            messagebox.showerror("Too many items", f"Maximum of {max_items} items allowed.")
            return

        self.items = selected_items
        self.item_selection_window.destroy()
        self.start_round()

    def get_weighted_prediction(self):
        valid = [c for c in self.counts if self.counts[c] > 0]
        weights = {
            color: self.counts[color] * self.learn_data['shells'].get(color, 1.0)
            for color in valid
        }
        total = sum(weights.values())

        if total > 0:
            red_chance = weights.get('red', 0) / total * 100
            blue_chance = weights.get('blue', 0) / total * 100
            self.probability_label.config(text=f"Prediction: Red {red_chance:.1f}% | Blue {blue_chance:.1f}%")

        rand = random.uniform(0, total)
        cumulative = 0
        for color, value in weights.items():
            cumulative += value
            if rand <= cumulative:
                return color
        return random.choice(valid)

    def start_round(self):
        if hasattr(self, 'round_frame'):
            self.round_frame.destroy()
        self.round_frame = tk.Frame(self.root, bg="black")
        self.round_frame.pack(pady=20)
        self.update_round()

    def update_round(self):
        for widget in self.round_frame.winfo_children():
            widget.destroy()

        if self.counts['red'] + self.counts['blue'] == 0:
            if messagebox.askyesno("Round over", "All shells used. Start new round?"):
                self.setup_game()
            return

        self.update_title_label()
        self.prediction = self.get_weighted_prediction()

        self.prediction_label = tk.Label(self.round_frame, text=f"Next Shell: {self.prediction.upper()}", fg="white", bg="black", font=("Helvetica", 14))
        self.prediction_label.pack(pady=10)

        tk.Label(self.round_frame, text="Which shell was drawn?", fg="white", bg="black").pack(pady=10)
        tk.Button(self.round_frame, text="RED", command=lambda: self.evaluate_choice("red", self.prediction), bg="darkred", fg="white", width=15).pack(pady=2)
        tk.Button(self.round_frame, text="BLUE", command=lambda: self.evaluate_choice("blue", self.prediction), bg="blue", fg="white", width=15).pack(pady=2)
        tk.Button(self.round_frame, text="INVERTER USED?", command=self.invert_prediction, bg="orange", fg="black", width=20, highlightthickness=2).pack(pady=5)
        self.inverter_animation_active = False
        self.invert_button = self.round_frame.winfo_children()[-1]
        self.animate_inverter_button()

    def invert_prediction(self):
        if self.prediction:
            old = self.prediction
            self.prediction = 'blue' if self.prediction == 'red' else 'red'
            self.inverted_last_round = True
            self.inverter_animation_active = True
            messagebox.showinfo("Inverter", f"Was: {old.upper()} → Now: {self.prediction.upper()} (this round only)")
            self.prediction_label.config(text=f"Next Shell: {self.prediction.upper()} (INVERTER ACTIVE)")

    def evaluate_choice(self, drawn, prediction):
        self.inverter_animation_active = False
        if self.inverted_last_round:
            prediction = 'red' if prediction == 'blue' else 'blue'
            self.inverted_last_round = False

        if prediction != drawn:
            self.learn_data['shells'][drawn] += 1.0
        else:
            self.learn_data['shells'][drawn] += 0.1
        self.save_learning_data()

        if self.counts[drawn] > 0:
            self.counts[drawn] -= 1

        self.update_round()

    def animate_inverter_button(self):
        if not hasattr(self, 'invert_button') or self.invert_button is None:
            return
        if not getattr(self, 'inverter_animation_active', False):
            self.invert_button.config(bg="orange")
            return
        current = self.invert_button.cget("bg")
        next_color = "yellow" if current == "orange" else "orange"
        self.invert_button.config(bg=next_color)
        self.root.after(500, self.animate_inverter_button)

if __name__ == "__main__":
    root = tk.Tk()
    app = BuckshotGUI(root)
    root.mainloop()

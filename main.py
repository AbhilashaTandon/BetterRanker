import tkinter as tk
from tkinter import ttk
import elo

default_font = ("Arial", 18)


class Page(ttk.Frame):
    def __init__(self, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class Intro(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        category_label = ttk.Label(
            self,
            text="Enter the category of items you would like to sort (singular form please):",
            font=default_font,
        )
        category_label.grid(column=0, row=0)

        self.category = tk.StringVar()
        category_entry = ttk.Entry(self, textvariable=self.category, font=default_font)
        category_entry.grid(column=1, row=0)

        items_label = ttk.Label(
            self,
            text="Enter the list of items you would like to sort (each one on a new line):",
            font=default_font,
        )
        items_label.grid(column=0, row=1)

        self.items_entry = tk.Text(self, font=default_font, height=10)
        self.items_entry.grid(column=1, row=1)

    def get_category(self):
        return self.category.get()

    def get_items(self):
        self.items = self.items_entry.get("1.0", "end")
        return self.items.splitlines()


class Sorting(Page):
    def __init__(self, root, category, items):
        Page.__init__(self, root)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.category = category
        self.tournament = elo.Tournament(items)
        self.after(1, self.matchup)

    def matchup(self):
        pair = self.tournament.next_match()

        self.item1 = pair[0]
        self.item2 = pair[1]

        root.bind("<Left>", lambda e: self.left_win())
        root.bind("<Up>", lambda e: self.draw())
        root.bind("<Right>", lambda e: self.right_win())

        self.item1_name = tk.StringVar(self, self.item1[0])
        item1_label = ttk.Label(self, textvariable=self.item1_name, font=default_font)
        item1_label.grid(column=0, row=0, sticky="E")

        vs_label = ttk.Label(self, text="vs.", font=default_font)
        vs_label.grid(column=1, row=0)

        self.item2_name = tk.StringVar(self, self.item2[0])
        item2_label = ttk.Label(self, textvariable=self.item2_name, font=default_font)
        item2_label.grid(column=2, row=0, sticky="W")

        button1 = ttk.Button(
            self, text="%s on left is better" % self.category, command=self.left_win
        )
        button1.grid(column=0, row=1, sticky="N")

        button_draw = ttk.Button(self, text="Unsure", command=self.draw)
        button_draw.grid(column=1, row=1, sticky="N")

        button2 = ttk.Button(
            self, text="%s on right is better" % self.category, command=self.right_win
        )
        button2.grid(column=2, row=1, sticky="N")

        info_label = ttk.Label(
            self,
            text="You can also use the arrow keys instead of pressing the buttons!\n Use left, up, and right respectively.",
            font=default_font,
        )
        info_label.grid(column=1, row=2)

    def left_win(self):
        self.tournament.update(self.item1[0], self.item2[0], 1)
        self.after(1, self.matchup)

    def right_win(self):
        self.tournament.update(self.item1[0], self.item2[0], 0)
        self.after(1, self.matchup)

    def draw(self):
        self.tournament.update(self.item1[0], self.item2[0], 0.5)
        self.after(1, self.matchup)


class Result(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = ttk.Label(self, text="This is page 3")
        label.grid(column=1, row=1)


class MainView(ttk.Frame):
    def __init__(self, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)

        self.page = 0

        self.intro = Intro(self)

        buttonframe = ttk.Frame(self)
        self.container = ttk.Frame(self)
        buttonframe.pack(side="bottom", fill="x", expand=False)
        self.container.pack(side="top", fill="both", expand=True)

        self.intro.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)

        b = ttk.Button(buttonframe, text="Next", command=self.next_page)

        b.grid(column=0, row=0)

        self.intro.show()

    def next_page(self):
        if self.page == 0:
            self.page = 1
            self.sorting = Sorting(
                self, self.intro.get_category(), self.intro.get_items()
            )
            self.sorting.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
            self.sorting.show()

        elif self.page == 1:
            self.page = 2
            self.result = Result(self)
            self.result.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
            self.result.show()


if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True, padx=20, pady=20)
    root.wm_geometry("1200x600")
    root.mainloop()

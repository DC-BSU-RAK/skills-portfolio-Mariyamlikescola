import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import io
import random

# -----------------------------
# Main App
# -----------------------------
class JuiceWorld(tk.Tk):
    def _init_(self):
        super()._init_()
        self.title("Juice World")
        self.geometry("650x600")
        self.resizable(False, False)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (StartFrame, MenuFrame, DrinkDisplayFrame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartFrame)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()


# -----------------------------
# Frame 1 - Welcome Screen
# -----------------------------
class StartFrame(tk.Frame):
    def _init_(self, parent, controller):
        super()._init_(parent, bg="#f7e3b5")
        self.controller = controller

        # Logo
        try:
            logo_img = Image.open("logo.png").resize((200, 200))
            self.logo = ImageTk.PhotoImage(logo_img)
            tk.Label(self, image=self.logo, bg="#f7e3b5").pack(pady=20)
        except:
            tk.Label(self, text="🍹 Juice World 🍹", font=("Arial", 30, "bold"), bg="#f7e3b5").pack(pady=40)

        tk.Label(self, text="Welcome to Juice World!", font=("Arial", 20, "bold"), bg="#f7e3b5").pack(pady=10)
        ttk.Button(self, text="Enter Juice World",
                   command=lambda: controller.show_frame(MenuFrame)).pack(pady=30)


# -----------------------------
# Frame 2 - Menu
# -----------------------------
class MenuFrame(tk.Frame):
    def _init_(self, parent, controller):
        super()._init_(parent, bg="#ffe7d1")
        self.controller = controller

        tk.Label(self, text="Choose Your Drink", font=("Arial", 22, "bold"), bg="#ffe7d1").pack(pady=30)

        ttk.Button(self, text="🍹 Random Alcoholic Drink",
                   command=lambda: self.get_random_drink(alcoholic=True)).pack(pady=15)

        ttk.Button(self, text="🥤 Random Non-Alcoholic Drink",
                   command=lambda: self.get_random_drink(alcoholic=False)).pack(pady=15)

        ttk.Button(self, text="⬅ Back to Welcome", command=lambda: controller.show_frame(StartFrame)).pack(pady=50)

    def get_random_drink(self, alcoholic=True):
        # API URL
        if alcoholic:
            url = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?a=Alcoholic"
        else:
            url = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?a=Non_Alcoholic"

        # Get list of drinks
        data = requests.get(url).json()
        drink_choice = random.choice(data['drinks'])

        # Get full details
        drink_id = drink_choice['idDrink']
        full_drink = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={drink_id}").json()['drinks'][0]

        # Update display frame
        self.controller.frames[DrinkDisplayFrame].update_drink(full_drink)
        self.controller.show_frame(DrinkDisplayFrame)


# -----------------------------
# Frame 3 - Drink Display
# -----------------------------
class DrinkDisplayFrame(tk.Frame):
    def _init_(self, parent, controller):
        super()._init_(parent, bg="#d4f4dd")
        self.controller = controller

        tk.Label(self, text="Your Drink!", font=("Arial", 24, "bold"), bg="#d4f4dd").pack(pady=10)

        self.drink_name = tk.Label(self, text="", font=("Arial", 20, "bold"), bg="#d4f4dd")
        self.drink_name.pack(pady=10)

        self.img_label = tk.Label(self, bg="#d4f4dd")
        self.img_label.pack(pady=10)

        self.ingredients_label = tk.Label(self, text="", font=("Arial", 14), bg="#d4f4dd", justify="left")
        self.ingredients_label.pack(pady=10)

        self.instructions_label = tk.Label(self, text="", font=("Arial", 14), bg="#d4f4dd", wraplength=600, justify="left")
        self.instructions_label.pack(pady=10)

        ttk.Button(self, text="⬅ Back to Menu", command=lambda: controller.show_frame(MenuFrame)).pack(pady=20)

    def update_drink(self, drink):
        # Name
        self.drink_name.config(text=drink["strDrink"])

        # Ingredients
        ingredients = []
        for i in range(1, 16):
            ing = drink.get(f"strIngredient{i}")
            measure = drink.get(f"strMeasure{i}")
            if ing:
                ingredients.append(f"- {ing} ({measure if measure else ''})")
        self.ingredients_label.config(text="\n".join(ingredients))

        # Instructions
        self.instructions_label.config(text=f"Instructions:\n{drink.get('strInstructions','')}")

        # Image
        img_url = drink["strDrinkThumb"]
        response = requests.get(img_url)
        img_data = Image.open(io.BytesIO(response.content)).resize((250, 250))
        self.drink_img = ImageTk.PhotoImage(img_data)
        self.img_label.config(image=self.drink_img)


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app = JuiceWorld()
    app.mainloop()
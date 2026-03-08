import tkinter as tk
from tkinter import ttk
import championship

class App:
    def __init__(self, root, championship_instance):
        
        self.root = root
        self.f1 = championship_instance

        self.setup_window()

        self.create_widgets()

        self.load_data()

    def setup_window(self):
        self.root.title("F1 Championship Standings")
        width, height = 800, 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        try:
            icon_image = tk.PhotoImage(file='assets/icon.png')
            root.iconphoto(False, icon_image)
        except tk.TclError:
            print("An error occurred while uploading icon.png")

    def drivers_tree_view(self, parent):

        frame = tk.Frame(parent)
        frame.pack(side='left', fill='both', expand=True, padx=5)

        tk.Label(frame, text="Classificação de Pilotos", font=("Arial", 12, "bold")).pack()

        columns = ('pos', 'nome', 'pontos')
        self.drivers_tree = ttk.Treeview(frame, columns=columns, show='headings', height=22)

        self.drivers_tree.heading('pos', text='Posição')
        self.drivers_tree.heading('nome', text='Piloto')
        self.drivers_tree.heading('pontos', text='Pontos')

        self.drivers_tree.column('pos', width=50, anchor='center')
        self.drivers_tree.column('nome', width=150, anchor='center')
        self.drivers_tree.column('pontos', width=50, anchor='center')

        self.drivers_tree.pack(padx=10, pady=10, fill='both', expand=True)

    def teams_tree_view(self, parent):

        frame = tk.Frame(parent)
        frame.pack(side='left', fill='both', expand=True, padx=5)

        tk.Label(frame, text="Classificação de Equipes", font=("Arial", 12, "bold")).pack()

        columns = ('pos', 'nome', 'pontos')
        self.teams_tree = ttk.Treeview(frame, columns=columns, show='headings', height=11)

        self.teams_tree.heading('pos', text='Posição')
        self.teams_tree.heading('nome', text='Equipe')
        self.teams_tree.heading('pontos', text='Pontos')

        self.teams_tree.column('pos', width=50, anchor='center')
        self.teams_tree.column('nome', width=150, anchor='center')
        self.teams_tree.column('pontos', width=50, anchor='center')

        self.teams_tree.pack(padx=10, pady=10, fill='none', expand=False)

    def load_data(self):
        # Avoid duplicates
        for item in self.drivers_tree.get_children():
            self.drivers_tree.delete(item)
        
        drivers = self.f1.getDriversSortedByPoints()
        
        for driver in drivers:
            self.drivers_tree.insert('', tk.END, values=(
                driver.position if driver.position > 0 else "-", 
                driver.name, 
                driver.points
            ))

        for item in self.teams_tree.get_children():
            self.teams_tree.delete(item)

        teams = self.f1.getTeamsSortedByPoints()
        
        for team in teams:
            self.teams_tree.insert('', tk.END, values=(
                team.position if driver.position > 0 else "-", 
                team.name, 
                team.points
            ))

        self.f1.sync_data()

    def update_standings_button(self):
        self.btn_update = tk.Button(
            self.root, 
            text="Atualizar Classificação", 
            command=self.load_data,
            bg="#393737",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.btn_update.pack(pady=10)


        
    def create_widgets(self):

        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill='both', expand=False, padx=10, pady=10)
        
        self.drivers_tree_view(self.main_container)

        self.teams_tree_view(self.main_container)

        self.update_standings_button()

if __name__ == "__main__":
    root = tk.Tk()

    meu_campeonato = championship.Championship()
    print(meu_campeonato.getDriver(44))
    meu_campeonato.sync_data()
    
    app = App(root, meu_campeonato)
    root.mainloop()
    
    

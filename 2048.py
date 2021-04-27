import tkinter as tk
import random
import Colors as c

class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("2048")

        self.main_grid = tk.Frame(
            self, bg=c.GRID_COLOR, bd=3, width=600, height=600
            )
        self.main_grid.grid(pady=(100,0))
        self.crear_GUI()
        self.iniciar_partida()

        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)

        self.mainloop()

    #

    def crear_GUI(self):
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame = tk.Frame(
                    self.main_grid,
                    bg=c.EMPTY_CELL_COLOR,
                    width=150,
                    height=150
                )
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(self.main_grid, bg=c.EMPTY_CELL_COLOR)
                cell_number.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)
        
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5, y=45, anchor="center")
        tk.Label(
            score_frame,
            text="Score",
            font=c.SCORE_LABEL_FONT
        ).grid(row=0)
        self.score_label = tk.Label(score_frame, text="0", font=c.SCORE_FONT)
        self.score_label.grid(row=1)

    def iniciar_partida(self):
        self.matriz = [[0] * 4 for _ in range (4)]
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        self.matriz[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(
            bg=c.CELL_COLORS[2],
            fg=c.CELL_NUMBER_COLORS[2],
            font=c.CELL_NUMBER_FONTS[2],
            text="2"
        )
        while(self.matriz[row][col] != 0):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matriz[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(
            bg=c.CELL_COLORS[2],
            fg=c.CELL_NUMBER_COLORS[2],
            font=c.CELL_NUMBER_FONTS[2],
            text="2"
        )

        self.puntaje = 0
    
    def apilar(self):
        new_matriz = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range (4):
                if self.matriz[i][j] != 0:
                    new_matriz[i][fill_position] = self.matriz[i][j]
                    fill_position += 1
        self.matriz = new_matriz

    def combinar(self):
        for i in range(4):
            for j in range(3):
                if self.matriz[i][j] != 0 and self.matriz[i][j] == self.matriz[i][j+1]:
                   self.matriz[i][j] *=2
                   self.matriz[i][j+1] = 0
                   self.puntaje += self.matriz[i][j]

    def inversa(self):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matriz[i][3 - j])
        self.matriz = new_matrix
 
    def transpuesta(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matriz[j][i]
        self.matriz = new_matrix

    def add_numero(self):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        while(self.matriz[row][col] != 0):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matriz[row][col] = random.choice([2,4])

    def actualizar_GUI(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matriz[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=c.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(bg=c.EMPTY_CELL_COLOR, text="")
                else:
                    self.cells[i][j]["frame"].configure(bg=c.CELL_COLORS[cell_value])
                    self.cells[i][j]["number"].configure(
                        bg=c.CELL_COLORS[cell_value],
                        fg=c.CELL_NUMBER_COLORS[cell_value],
                        font=c.CELL_NUMBER_FONTS[cell_value],
                        text=str(cell_value)
                    )
        self.score_label.configure(text=self.puntaje)
        self.update_idletasks()

    def left(self, event):
        self.apilar()
        self.combinar()
        self.apilar()
        self.add_numero()
        self.actualizar_GUI()
        self.game_over()


    def right(self, event):
        self.inversa()
        self.apilar()
        self.combinar()
        self.apilar()
        self.inversa()
        self.add_numero()
        self.actualizar_GUI()
        self.game_over()

    def up(self, event):
        self.transpuesta()
        self.apilar()
        self.combinar()
        self.apilar()
        self.transpuesta()
        self.add_numero()
        self.actualizar_GUI()
        self.game_over()

    def down(self, event):
        self.transpuesta()
        self.inversa()
        self.apilar()
        self.combinar()
        self.apilar()
        self.inversa()
        self.transpuesta()
        self.add_numero()
        self.actualizar_GUI()
        self.game_over()

    def movimiento_horizontal_valido(self):
        for i in range(4):
            for j in range(3):
                if self.matriz[i][j] == self.matriz[i][j+1]:
                    return True
        return False

    def movimiento_vertical_valido(self):
        for i in range(3):
            for j in range(4):
                if self.matriz[i][j] == self.matriz[i+1][j]:
                    return True
        return False

    def game_over(self):
        if any(2048 in row for row in self.matriz):
           game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
           game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
           tk.Label(
               game_over_frame,
               text="¡Ganó!",
               bg=c.WINNER_BG,
               fg=c.GAME_OVER_FONT_COLOR,
               font=c.GAME_OVER_FONT
           ).pack()
        elif not any(0 in row for row in self.matriz) and not self.movimiento_horizontal_valido() and not self.movimiento_vertical_valido():
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text="¡Perdió!",
                bg=c.LOSER_BG,
                fg=c.GAME_OVER_FONT_COLOR,
                font=c.GAME_OVER_FONT
            ).pack()

def main():
    Game()

if __name__ == "__main__":
    main()
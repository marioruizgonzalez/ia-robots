import tkinter as tk
from tkinter import messagebox, filedialog
import serial
import serial.tools.list_ports
import json
import pygame
import threading
import time  # Asegúrate de importar el módulo time

# Inicializar pygame para reproducir sonidos
pygame.mixer.init()

# Variable para la conexión serial
ser = None

# Variable para grabar la secuencia
recording = False
sequence = []
movimientos_guardados = []

# Lista de variables para los sliders
scales = []
texto_min = ["Izquierda", "Abajo", "Abajo", "Izquierda", "Abajo", "Izquierda", "Cierra"]
texto_max = ["Derecha", "Arriba", "Arriba", "Derecha", "Arriba", "Derecha", "Abre"]

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def connect_serial(port):
    global ser
    try:
        ser = serial.Serial(port, 9600)
        messagebox.showinfo("Conexión Exitosa", f"Conectado al puerto {port}")
    except serial.SerialException as e:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar al puerto {port}\n{str(e)}")
        
def enviar_valor_inicial():
    for i in range(8):
        ser.write(f"{i+1}:90\n".encode())

def on_port_selected(event):
    selected_port = port_var.get()
    if selected_port:
        connect_serial(selected_port)

# Función para mover el servo
def move_servo(servo_num, angle):
    if ser and ser.is_open:
        command = f"{servo_num}:{angle}\n"
        print(f"Enviando comando: {command}")  # Para depuración
        ser.write(command.encode())

# Función para actualizar el ángulo del servo
def update_servo(servo_num, scale_var):
    angle = scale_var.get()
    move_servo(servo_num + 1, angle)  # Asegúrate de enviar el número correcto del servo
    if recording:
        record_movement()

# Función para guardar la posición de los servos
def save_position():
    try:
        with open('servo_positions.json', 'r') as file:
            all_positions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        all_positions = []

    positions = [scale.get() for scale in scales]
    all_positions.append(positions)
    
    with open('servo_positions.json', 'w') as file:
        json.dump(all_positions, file)
        
    messagebox.showinfo("Guardar Posición", "Posición guardada exitosamente.")


# Función para cargar la posición de los servos
def load_position():
    try:
        with open('servo_positions.json', 'r') as file:
            positions = json.load(file)
        for i, position in enumerate(positions):
            scales[i].set(position)
            move_servo(i + 1, position)
        messagebox.showinfo("Cargar Posición", "Posición cargada exitosamente.")
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró ninguna posición guardada.")


# Funciones para importar y exportar posiciones
def exportar_posiciones():
    try:
        # Leer el contenido del archivo 'servo_positions.json'
        with open('servo_positions.json', 'r') as file:
            all_positions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        all_positions = []
    
    # Seleccionar la ruta donde se guardará el archivo exportado
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    
    if file_path:
        # Escribir el contenido en el archivo exportado
        with open(file_path, 'w') as file:
            json.dump(all_positions, file)
        
        # Reproducir el sonido de confirmación y mostrar mensaje de éxito
        messagebox.showinfo("Exportar Posiciones", "Posiciones exportadas exitosamente.")

def importar_posiciones():
    file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            movimientos = json.load(file)
        with open('servo_positions.json', 'w') as servo_file:
            json.dump(movimientos, servo_file)
        messagebox.showinfo("Importar Posiciones", "Posiciones importadas exitosamente.")


def resetear_posiciones():
    movimientos_guardados.clear()
    for i, scale_var in enumerate(scales):
        scale_var.set(90)
        update_servo(i, scale_var)
    
    # Vaciar el contenido de servo_positions.json
    with open('servo_positions.json', 'w') as file:
        json.dump([], file)
    
    messagebox.showinfo("Resetear Posiciones", "Posiciones reseteadas y archivo limpiado exitosamente.")



# Función para reproducir movimientos desde servo_positions.json
def movimientos_guardados1():
    threading.Thread(target=play_movements_and_sound).start()

def play_movements_and_sound():
    global reproduciendo
    reproduciendo = True
    while reproduciendo:
        try:
            with open('servo_positions.json', 'r') as file:
                movimientos_guardados = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            movimientos_guardados = []
            messagebox.showerror("Error", "No se encontraron posiciones guardadas.")
            return

        if movimientos_guardados:
            for movimiento in movimientos_guardados:
                if not reproduciendo:
                    break
                for i, position in enumerate(movimiento):
                    if not reproduciendo:
                        break
                    current_position = scales[i].get()
                    steps = 10  # Considera ajustar este valor según la fluidez deseada
                    step_size = (position - current_position) / steps

                    for step in range(steps):
                        if not reproduciendo:
                            break
                        new_position = current_position + step_size * (step + 1)
                        scales[i].set(new_position)
                        move_servo(i + 1, new_position)
                        time.sleep(velocidad_var.get() / 1000.0 / steps)  # Ajusta el tiempo según la velocidad seleccionada
                if movimiento != movimientos_guardados[-1]:  # Añadido para verificar si es el último movimiento
                    time.sleep(0.1)  # Ajustar este tiempo según sea necesario para una transición suave
    reproduciendo = False



def detener_movimiento():
    global reproduciendo
    reproduciendo = False
    messagebox.showinfo("Reproduccion Detenida.", "Reproduccion Detenida.")

# Crear la ventana principal
# Configuración inicial de colores
fg_title = "#FFFFFF"       # Fondo similar a PowerShell
bg_color = "#BDBDBD"       # Fondo similar a PowerShell
fg_color = "#000000"       # Texto similar a PowerShell
btn_color = "#FB3A3A"      # Botón similar a PowerShell
slider_bg = "#FB3A3A"      # Fondo de slider
slider_fg = "#000000"      # Color de texto de slider

# Crear la ventana principal
root = tk.Tk()
root.title("Avanza Z1")
root.geometry("1000x800")
root.configure(bg=bg_color)

# Banner
banner = tk.Label(root, text="Avanza Z1", font=("Verdana", 120), bg=bg_color, fg=fg_title)
banner.pack()

# Frame para los sliders de los servos
sliders_frame = tk.Frame(root, bg=bg_color)
sliders_frame.pack(side=tk.LEFT, padx=20, pady=20)

# Crear sliders para cada servo
# Crear sliders para cada servo
# Crear sliders para cada servo
for i in range(7):
    frame = tk.Frame(sliders_frame, bg=bg_color)
    frame.pack(pady=10)
    min_label = tk.Label(frame, text=texto_min[i], fg=fg_color, bg=bg_color)
    min_label.pack(side=tk.LEFT)

    # Variable para el slider
    scale_var = tk.IntVar(value=90)  # Establecer el valor inicial a 90 grados
    scales.append(scale_var)

    # Slider
    slider = tk.Scale(frame, from_=0, to=180, orient=tk.HORIZONTAL, variable=scale_var,
                      length=400,  # Hacer los sliders más largos
                      command=lambda val, i=i, scale_var=scale_var: update_servo(i, scale_var),
                      bg=slider_bg, fg=slider_fg, highlightbackground=bg_color, troughcolor=bg_color)
    slider.pack(side=tk.LEFT)

    max_label = tk.Label(frame, text=texto_max[i], fg=fg_color, bg=bg_color)
    max_label.pack(side=tk.LEFT)

    # Establecer la posición inicial del servo a 90 grados
    update_servo(i, scale_var)


# Frame para los botones y el control deslizante de velocidad
controls_frame = tk.Frame(root, bg=bg_color)
controls_frame.pack(side=tk.RIGHT, padx=20, pady=20)

# Botones para las funcionalidades
button_frame = tk.Frame(controls_frame, bg=bg_color)
button_frame.pack(pady=20)

save_button = tk.Button(button_frame, text="Guardar Posiciones", command=save_position, width=20, height=2, bg=btn_color, fg=fg_color)
save_button.grid(row=0, column=0, padx=10, pady=5)

export_button = tk.Button(button_frame, text="Exportar Posiciones", command=exportar_posiciones, width=20, height=2, bg=btn_color, fg=fg_color)
export_button.grid(row=0, column=1, padx=10, pady=5)

import_button = tk.Button(button_frame, text="Importar Posiciones", command=importar_posiciones, width=20, height=2, bg=btn_color, fg=fg_color)
import_button.grid(row=1, column=0, padx=10, pady=5)

reset_button = tk.Button(button_frame, text="Resetear Posiciones", command=resetear_posiciones, width=20, height=2, bg=btn_color, fg=fg_color)
reset_button.grid(row=1, column=1, padx=10, pady=5)

play_button = tk.Button(button_frame, text="Reproducir Movimientos", command=movimientos_guardados1, width=20, height=2, bg=btn_color, fg=fg_color)
play_button.grid(row=2, column=0, padx=10, pady=5)

stop_movement_button = tk.Button(button_frame, text="Detener Movimiento", command=detener_movimiento, width=20, height=2, bg=btn_color, fg=fg_color)
stop_movement_button.grid(row=2, column=1, padx=10, pady=5)

# Control deslizante para regular la velocidad de reproducción
velocidad_var = tk.IntVar()
velocidad_var.set(1000)
velocidad_slider = tk.Scale(controls_frame, from_=200, to=2000, orient=tk.HORIZONTAL, variable=velocidad_var, label="Velocidad de Reproducción", bg=slider_bg, fg=slider_fg, highlightbackground=bg_color, troughcolor=bg_color, length=320)
velocidad_slider.pack(pady=20)

# Menu de selección de puertos con etiqueta
puertos_disponibles = list_serial_ports()
if not puertos_disponibles:
    messagebox.showwarning("Advertencia", "No se encontraron puertos COM disponibles.")
    port_var = tk.StringVar(value="No disponible")
    port_menu = tk.OptionMenu(controls_frame, port_var, "No disponible")
else:
    port_var = tk.StringVar()
    port_menu = tk.OptionMenu(controls_frame, port_var, *puertos_disponibles, command=on_port_selected)
    
port_menu.configure(bg=btn_color, fg=fg_color)
port_label = tk.Label(controls_frame, text="Seleccionar Puerto", bg=bg_color, fg=fg_color)
port_label.pack()
port_menu.pack(pady=20)

# Personalizar el aspecto del menú desplegable
menu = port_menu.nametowidget(port_menu.menuname)
menu.configure(bg=btn_color, fg=fg_color, font=("Helvetica", 10))

root.mainloop()


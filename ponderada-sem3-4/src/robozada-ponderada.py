from serial.tools import list_ports
import inquirer
import typer
import pydobot
from yaspin import yaspin

spinner = yaspin(text="Carregando...", color="white", spinner="dots12", side="right")

app = typer.Typer()

available_ports = list_ports.comports()

# Pede para o usuário escolher uma das portas disponíveis
chosen_port = inquirer.prompt([
    inquirer.List("porta", message="Escolha a porta serial", choices=[x.device for x in available_ports])
])["porta"]

# Variável do robô
robot = pydobot.Dobot(port=chosen_port, verbose=False)

# Define a velocidade e a aceleração do robô
robot.speed(50, 50)

# Define a posição home do robô
home_position = (0, 0, 0, 0)
robot.move_to(*home_position, wait=True)

# Dá uma mexida no robô
spinner.start(text="Mexendo o robô...", color="green")
robot.move_to(200, 0, 0, 0, wait=True)
spinner.stop()

# Ligando a ferramenta do robô
spinner.start(text="Ligando a ferramenta do robô...", color="yellow")
robot.suck(True)
robot.wait(400)
spinner.stop()

# Robô leva objeto para outra posição
spinner.start(text="Mexendo o robô...", color="green")
robot.move_to(200, 200, 0, 0, wait=True)
spinner.stop()

# Desligando a ferramenta do robô
spinner.start(text="Desligando a ferramenta do robô...", color="yellow")
robot.suck(False)
robot.wait(400)
spinner.stop()

# Coloca o robô na posição home
spinner.start(text="Voltando o robô para a posição home...", color="green")
robot.move_to(*home_position, wait=True)
spinner.stop()

# Move o robô para a posição inicial
@app.command()
def move_robot(axis: str, distance: float):
    """
    Move o robô para o eixo e distância especificados
    """
    if axis == "x":
        robot.move_to(robot.pose()[0] + distance, robot.pose()[1], robot.pose()[2], robot.pose()[3], wait=True)
    elif axis == "y":
        robot.move_to(robot.pose()[0], robot.pose()[1] + distance, robot.pose()[2], robot.pose()[3], wait=True)
    elif axis == "z":
        robot.move_to(robot.pose()[0], robot.pose()[1], robot.pose()[2] + distance, robot.pose()[3], wait=True)

    # Pega a posição atual do robô
    current_position = robot.pose()
    print(f"Posição atual: {current_position}")

# Close the connection with the robot
@app.command()
def close_robot():
    """
    Fecha a conexão com o robô
    """
    robot.close()

if __name__ == "__main__":
    app()

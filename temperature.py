from gpiozero import CPUTemperature
from time import sleep

cpu = CPUTemperature()

while(True):
    sleep(1)
    print(cpu.temperature)
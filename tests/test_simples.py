#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

print("Iniciando teste simples do Selenium...")

# Configurar Firefox headless
options = Options()
options.add_argument('--headless')

print("Abrindo Firefox...")
driver = webdriver.Firefox(options=options)

print("Acessando localhost:8000...")
driver.get("http://localhost:8000")

time.sleep(3)

print(f"Título da página: {driver.title}")

driver.save_screenshot("/tmp/teste.png")
print("Screenshot salva em /tmp/teste.png")

driver.quit()
print("Teste concluído com sucesso! ✓")

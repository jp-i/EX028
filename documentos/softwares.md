# Softwares e Bibliotecas

## Ambientes de Desenvolvimento
- **MicroPython** (firmware embarcado na Raspberry Pi Pico W / BitDogLab)
- **Python 3** e **Jupyter Notebook** (análise de dados no computador)
- **Thonny IDE** ou **VS Code** (extensão MicroPython) para envio dos scripts à placa

## Bibliotecas MicroPython (Placa)
- `machine` (`Pin`, `I2C`): controle do display e interrupções (IRQ) no botão para precisão de hardware.
- `neopixel`: controle da matriz de 25 LEDs RGB.
- `ssd1306` / `sh1107`: drivers dos displays OLED (128×64 e 128×128).
- `framebuf`: renderização de pixels e logotipos (Unicamp e BitDogLab).
- `time`: cronometragem em milissegundos via `ticks_ms()`.
- `urandom`: sorteio do tempo de espera aleatório (2000 ms a 5000 ms).
- `gc`: chamada manual de `gc.collect()` antes do sinal verde para evitar *jitter* (atrasos de memória) durante a medição.

## Bibliotecas Python (PC)
- `pandas`: leitura e concatenação dos arquivos `.csv`.
- `numpy`: cálculo de média, mediana, percentis e desvio padrão.
- `scipy.stats`: ajuste das distribuições Normal (`norm`), Assimétrica (`skewnorm`) e Ex-Gaussiana (`exponnorm`).
- `matplotlib`: geração dos histogramas e sobreposição das curvas.
- `glob`: leitura em lote dos arquivos `.csv`.

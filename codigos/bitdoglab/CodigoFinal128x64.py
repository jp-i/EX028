# ==========================================
# EX028 SEMÁFORO DO REFLEXO
# ==========================================

import framebuf
import gc
import machine
import neopixel
import ssd1306
import time
import urandom

# ==========================================
# IDENTIFICAÇÃO DA PLACA 
# ==========================================
BOARD_ID = "Placa_1"  # !Mudar nome placa!
CSV_FILENAME = f"dados_reacao_{BOARD_ID}.csv"

# ==========================================
# CONFIGURAÇÕES DE HARDWARE
# ==========================================
btn_a = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)

i2c = machine.I2C(1, sda=machine.Pin(2), scl=machine.Pin(3), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

NUM_LEDS = 25
np = neopixel.NeoPixel(machine.Pin(7), NUM_LEDS)

# ==========================================
# CORES
# ==========================================
COR_DESLIGADO = (0, 0, 0)
COR_VERMELHO  = (2, 0, 0)
COR_LARANJA   = (2, 1, 0)
COR_VERDE     = (0, 2, 0)

# ==========================================
# VARIÁVEIS DE INTERRUPÇÃO
# ==========================================
botao_pressionado = False
momento_do_clique = 0
ultimo_clique = 0

# ==============================
# FUNÇÕES CORE
# ==============================
def set_matriz(cor):
    np.fill(cor)
    np.write()

def mostrar_oled(linhas):
    oled.fill(0)
    y = 0
    for linha in linhas:
        oled.text(str(linha), 0, y, 1)
        y += 12
    oled.show()

def texto_grande(oled_dev, texto, x_pos, y_pos, escala=2):
    """Desenha texto ampliado (sem negrito)."""
    w = len(texto) * 8
    h = 8
    buf = bytearray(w * h // 8)
    fb = framebuf.FrameBuffer(buf, w, h, framebuf.MONO_HMSB)
    fb.text(texto, 0, 0, 1)

    for row in range(h):
        for col in range(w):
            if fb.pixel(col, row):
                for dx in range(escala):
                    for dy in range(escala):
                        oled_dev.pixel(x_pos + col * escala + dx,
                                       y_pos + row * escala + dy,
                                       1)

def blit_scaled(oled_dev, fb, src_w, src_h, dst_w, dst_h, x_pos, y_pos):
    for row in range(dst_h):
        orig_y = row * src_h // dst_h
        for col in range(dst_w):
            orig_x = col * src_w // dst_w
            if fb.pixel(orig_x, orig_y):
                oled_dev.pixel(x_pos + col, y_pos + row, 1)

def mostrar_tela_inicial():
    """Tela inicial com título em duas linhas, centralizado."""
    oled.fill(0)

    esc = 2
    w_sema = len("SEMAFORO") * 8 * esc
    margem = 0
    x_sema = margem
    texto_grande(oled, "SEMAFORO", x_sema, 0, escala=esc)

    w_do = len("DO") * 8
    x_do = (128 - w_do) // 2
    texto_grande(oled, "DO", x_do, 18, escala=1)

    w_ref = len("REFLEXO") * 8 * esc
    x_ref = (128 - w_ref) // 2
    texto_grande(oled, "REFLEXO", x_ref, 28, escala=esc)

    oled.text("Aperte A!", (128 - 9*8)//2, 54, 1)

    oled.show()

def salvar_dados_csv(resultados):
    """Salva os resultados numa única coluna vertical."""
    try:
        with open(CSV_FILENAME, 'a') as f:
            for tempo in resultados:
                f.write(f"{tempo}\n")
    except Exception as e:
        print("Erro ao salvar:", e)

# ==========================================
# INTERRUPÇÃO
# ==========================================
def irq_botao(pin):
    global botao_pressionado, momento_do_clique, ultimo_clique
    agora = time.ticks_ms()
    # Debounce por tempo (200ms) sem travar a CPU
    if time.ticks_diff(agora, ultimo_clique) > 200:
        momento_do_clique = agora
        botao_pressionado = True
        ultimo_clique = agora

btn_a.irq(trigger=machine.Pin.IRQ_FALLING, handler=irq_botao)

def aguardar_clique():
    """Espera o clique do botão A via interrupção."""
    global botao_pressionado
    botao_pressionado = False
    while not botao_pressionado:
        time.sleep(0.01)

# ==========================================
# LÓGICA PRINCIPAL DO JOGO
# ==========================================
def loop_principal():
    global botao_pressionado, momento_do_clique
    
    while True:
        # TELA INICIAL
        set_matriz(COR_DESLIGADO)
        mostrar_tela_inicial()
        aguardar_clique()

        # Alimenta a semente aleatória UMA ÚNICA VEZ com o instante exato do clique humano
        urandom.seed(momento_do_clique)

        # PREPARAÇÃO INICIAL (Sinal vermelho antes da 1ª rodada)
        set_matriz(COR_VERMELHO)
        mostrar_oled([
            "SINAL VERMELHO",
            "",
            "Prepare-se",
            "",
            "A - Iniciar"
        ])
        aguardar_clique()

        resultados = []
        rodada = 1

        # 7 RODADAS
        while rodada <= 7:
            
            # SINAL LARANJA
            set_matriz(COR_LARANJA)
            mostrar_oled([
                "SINAL LARANJA",
                "",
                "ATENCAO...",
                "Espere o verde",
                "para apertar A!"
            ])

            # Sorteia livremente de 2 a 5 segundos (2000 a 5000 ms) sem resetar a semente
            tempo_espera = urandom.randint(2000, 5000) 
            
            inicio_espera = time.ticks_ms()
            queimou_largada = False
            botao_pressionado = False

            # Monitora queimada de largada
            while time.ticks_diff(time.ticks_ms(), inicio_espera) < tempo_espera:
                if botao_pressionado:
                    queimou_largada = True
                    break
            
            if queimou_largada:
                set_matriz(COR_VERMELHO)
                mostrar_oled([
                    "QUEIMOU LARGADA!",
                    "",
                    "Nao valeu",
                    "",
                    "A - Repetir"
                ])
                aguardar_clique()
                continue

            # SINAL VERDE
            botao_pressionado = False
            
            # Limpa a memória RAM antes de iniciar o cronômetro para evitar jitter (GC)
            gc.collect()
            
            set_matriz(COR_VERDE)
            inicio_reacao = time.ticks_ms()
            
            mostrar_oled([
                "SINAL VERDE",
                "",
                "AGORA!",
                "",
                "Aperte A"
            ])
            
            # Aguarda a reação
            while not botao_pressionado:
                if time.ticks_diff(time.ticks_ms(), inicio_reacao) > 10000:
                    break
            
            if not botao_pressionado:
                set_matriz(COR_VERMELHO)
                mostrar_oled([
                    "TEMPO ESGOTADO!",
                    "> 10 segundos",
                    "",
                    "A - Repetir"
                ])
                aguardar_clique()
                continue
            
            # SUCESSO!
            tempo_reacao = time.ticks_diff(momento_do_clique, inicio_reacao)
            resultados.append(tempo_reacao)
            
            # Define a mensagem com base no tempo de reação
            if tempo_reacao < 200:
                mensagem_desempenho = "NIVEL F1!"
            elif tempo_reacao < 250:
                mensagem_desempenho = "MUITO BOM!"
            elif tempo_reacao < 300:
                mensagem_desempenho = "BOM"
            elif tempo_reacao < 350:
                mensagem_desempenho = "OK"
            else:
                mensagem_desempenho = "+ ATENCAO!"
            
            # Sinal fica vermelho ao mostrar o tempo
            set_matriz(COR_VERMELHO)
            mostrar_oled([
                f"Rodada {rodada} de 7",
                "",
                mensagem_desempenho,
                f"Tempo: {tempo_reacao} ms",
                "A - Proximo"
            ])
            aguardar_clique() 
            rodada += 1

        # ==========================================
        # FIM DAS 7 RODADAS
        # ==========================================
        set_matriz(COR_DESLIGADO)

        # Desconsidera as 2 primeiras rodadas
        # Se houver menos de 2 rodadas (caso de abortos), evita erro.
        tempos_considerados = resultados[2:] if len(resultados) > 2 else []
        media_simples = sum(tempos_considerados) // len(tempos_considerados) if tempos_considerados else 0

        # Define a mensagem com base na média do tempo de reação
        if media_simples < 210:
            classificacao_final = "NIVEL F1!"
        elif media_simples < 250:
            classificacao_final = "MUITO BOM!"
        elif media_simples < 300:
            classificacao_final = "BOM"
        elif media_simples < 350:
            classificacao_final = "OK"
        else:
            classificacao_final = "+ATENCAO NA PROX"

        # Salva o .csv
        salvar_dados_csv(tempos_considerados)

        mostrar_oled([
            f"M: {media_simples} ms",
            classificacao_final,
            f"3:{resultados[2]}ms  6:{resultados[5]}ms" if len(resultados) > 5 else "",
            f"4:{resultados[3]}ms  7:{resultados[6]}ms" if len(resultados) > 6 else "",
            f"5:{resultados[4]}ms" if len(resultados) > 4 else "",
        ])
        aguardar_clique()

# Execução
try:
    loop_principal()
except KeyboardInterrupt:
    print("Programa finalizado.")
finally:
    btn_a.irq(handler=None)
    set_matriz(COR_DESLIGADO)
    oled.fill(0)
    oled.show()
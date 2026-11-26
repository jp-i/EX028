# Quão rápido é seu cérebro?

> **Disciplina:** EX028 (FEEC/Unicamp) · **Aplicação:** E.E. Dr. Telêmaco Paioli Melges · **Público:** 6º ao 9º ano (~180 estudantes)

Atividade prática de medição de tempo de reação visual e análise estatística usando a placa **BitDogLab** (MicroPython) e **Python**. O objetivo é transformar reflexos humanos reais em dados estatísticos debatidos em sala de aula.

---

## Índice

| Conteúdo | Caminho |
|---|---|
| Documentação de hardware e materiais | [`documentos/materiais.md`](documentos/materiais.md) |
| Roteiro de aplicação e alinhamento à BNCC | [`documentos/roteiro.md`](documentos/roteiro.md) |
| Softwares e bibliotecas | [`documentos/softwares.md`](documentos/softwares.md) |
| Códigos BitDogLab | [`codigos/bitdoglab`](codigos/bitdoglab) |
| Códigos análise de dados e arquivos `.csv`  | [`codigos/analise-dados`](codigos/analise-dados) |
| Gráficos e histogramas gerados | [`histogramas/`](histogramas/) |
| Slides utilizados na escola | [`slides/`](slides/) |
| Registros fotográficos da oficina | [`fotos/`](fotos/) |

---

## Funcionamento

### 1. Dinâmica na placa BitDogLab
Cada participante realiza **7 tentativas** pressionando o **Botão A** no instante em que a matriz de LEDs 5×5 acende em verde:

- 🔴 **Vermelho:** preparo com o dedo próximo ao botão.
- 🟠 **Laranja:** espera aleatória (entre 2 s e 5 s) para evitar previsibilidade.
- 🟢 **Verde:** estímulo visual — o cronômetro inicia até o clique no Botão A.

**Regras de validação:**
- Clicar antes do verde registra **queima de largada** e invalida a rodada.
- Demoras acima de 10 s encerram a tentativa por *timeout*.
- As **2 primeiras rodadas** servem de adaptação e são descartadas automaticamente. O display OLED exibe a média das 5 finais em milissegundos e uma faixa de desempenho (*NÍVEL F1*, *MUITO BOM*, *BOM* ou *OK*).

### 2. Processamento estatístico em Python
Os arquivos `.csv` gravados nas placas são reunidos no notebook [`histogramas.ipynb`](codigos/analise-dados/histogramas.ipynb). O script aplica o filtro do **limite biológico humano (100 ms a 600 ms)** para remover antecipações e distrações, gerando o histograma ajustado pela **Distribuição Ex-Gaussiana**.

---

## Resultados da aplicação

- **Volume coletado:** 1.210 medições válidas em sala de aula.
- **Resumo estatístico:** Média de **263,8 ms** · Mediana de **244,0 ms** · Moda de **227 ms** · Desvio padrão de **79,7 ms**.
- **Modelagem:** A curva **Ex-Gaussiana** foi adotada no lugar da Normal tradicional por refletir a barreira fisiológica mínima (~100 ms) e a cauda longa à direita típica de tempos de reação.

---

## Guia de uso

1. Instale o firmware MicroPython na Pico W de cada BitDogLab (detalhes em [`documentos/softwares.md`](documentos/softwares.md)).
2. Carregue [`CodigoFinal128x64.py`](codigos/bitdoglab/CodigoFinal128x64.py) ou [`CodigoFinal128x128.py`](codigos/bitdoglab/CodigoFinal128x128.py), de acordo com o modelo do display OLED da placa.
3. Conecte as baterias 18650 carregadas para operação sem fio.
4. No computador responsável pela projeção, instale as bibliotecas de análise:
   ```bash
   pip install -r codigos/analise-dados/requirements.txt
   ```
   
---

## Equipe

- Antonio Silva de Santana
- Erik Ventorini de Oliveira
- João Pedro Lupinacci Tófoli

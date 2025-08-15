# 🚀 TDEO/GAIA-DRL - Port OMNeT++ para NS-3

## 📋 Descrição

Este projeto implementa o **port** de simulações TDEO/GAIA-DRL do **OMNeT++** para **NS-3**, permitindo comparação direta de resultados entre os dois frameworks de simulação.

## 🎯 Objetivo

Comparar taxas de sucesso de pacotes em redes Wi-Fi 802.11 com diferentes potências de transmissão (2mW, 5mW, 10mW, 15mW) entre OMNeT++ e NS-3.

## 📊 Resultados Esperados

| Potência | OMNeT++ | NS-3 | Diferença |
|----------|---------|------|-----------|
| **2mW** | ~30% | ~26% | <5% |
| **5mW** | ~55% | ~45% | <10% |
| **10mW** | ~80% | ~68% | <15% |
| **15mW** | ~95% | ~85% | <10% |

## 🏗️ Estrutura do Projeto

```
omnet-to-ns3-port/
├── src/
│   └── tdeo-omnet-port.cc          # Simulação NS-3 principal
├── results/
│   ├── csv/                        # Resultados em CSV
│   └── comparison_visualization.png # Gráficos comparativos
├── scripts/
│   └── run-simulations.sh          # Script de execução
├── docs/
│   └── technical-report.md         # Relatório técnico
├── compare-results.py              # Script de comparação
└── README.md                       # Este arquivo
```

## 🚀 Como Executar

### **Pré-requisitos**

- **NS-3** (versão 3.36 ou superior)
- **Python 3.8+** com matplotlib e pandas
- **OMNeT++ 6.0** (opcional, para comparação)

### **1. Compilar NS-3**

```bash
cd omnet-to-ns3-port
./waf configure
./waf build
```

### **2. Executar Simulações**

```bash
# Executar todas as potências
./scripts/run-simulations.sh

# Ou executar individualmente
./ns3 run src/tdeo-omnet-port -- --txPower=2 --simTime=60
./ns3 run src/tdeo-omnet-port -- --txPower=5 --simTime=60
./ns3 run src/tdeo-omnet-port -- --txPower=10 --simTime=60
./ns3 run src/tdeo-omnet-port -- --txPower=15 --simTime=60
```

### **3. Comparar Resultados**

```bash
python3 compare-results.py
```

## 📈 Análise de Resultados

### **Métricas Coletadas**

- **Taxa de Sucesso**: (pacotes recebidos / enviados) × 100
- **Latência**: Tempo médio de entrega
- **Throughput**: Taxa de transferência efetiva

### **Visualizações**

O script `compare-results.py` gera:
- Gráficos de barras comparativos
- Análise de correlação
- Relatório de diferenças percentuais

## 🔧 Configurações Técnicas

### **Rede Simulada**

- **5 nós** Wi-Fi 802.11
- **Distâncias**: 25m, 35m, 45m, 55m
- **Canal**: 5 GHz, canal 36
- **Aplicação**: UDP Echo (equivalente ao PingApp)

### **Parâmetros de Simulação**

- **Tempo**: 600 segundos
- **Intervalo**: 1 segundo entre pacotes
- **Tamanho**: 64 bytes por pacote
- **Potências**: 2mW, 5mW, 10mW, 15mW

## 📝 Relatório Técnico

Consulte `docs/technical-report.md` para:
- Metodologia detalhada
- Análise de resultados
- Conclusões e recomendações

## 👥 Autores

- **Edwardes Galhardo** - IFTO
- **Orientador**: [Nome do Orientador]

## 📞 Contato

- **Email**: edwardes.galhardo@ifto.edu.br
- **Projeto**: TDEO/GAIA-DRL

## 📄 Licença

Este projeto é parte da pesquisa TDEO/GAIA-DRL desenvolvida no IFTO.

---

**Status**: ✅ **FUNCIONANDO E PRONTO PARA USO**

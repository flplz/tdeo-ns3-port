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
├── scripts/
│   └── run-simulations.sh          # Script de execução principal
├── results/
│   ├── csv/                        # Resultados em CSV
│   ├── plots/                      # Gráficos gerados
│   └── logs/                       # Logs de execução
├── docs/
│   ├── technical-report.md         # Relatório técnico
│   └── porting-guide.md            # Guia de portação
├── compare-results.py              # Script de comparação
├── INSTALL.md                      # Guia de instalação
└── README.md                       # Este arquivo
```

## 🚀 Como Executar

### **Pré-requisitos**

- **NS-3** (versão 3.36 ou superior)
- **Python 3.8+** com matplotlib e pandas
- **OMNeT++ 6.0** (opcional, para comparação)

### **1. Instalação**

```bash
# Clonar repositório
git clone https://github.com/seu-usuario/omnet-to-ns3-port.git
cd omnet-to-ns3-port

# Instalar dependências Python
pip3 install matplotlib pandas numpy

# Configurar NS-3 (ver INSTALL.md para detalhes)
./waf configure
./waf build
```

### **2. Executar Simulações**

```bash
# Executar todas as potências
./scripts/run-simulations.sh

# Ou executar individualmente
./scripts/run-simulations.sh --power 5

# Ver ajuda
./scripts/run-simulations.sh --help
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

### **Visualizações Geradas**

O script `compare-results.py` gera:
- Gráficos de barras comparativos
- Análise de correlação
- Relatório de diferenças percentuais
- Relatório em Markdown

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

## 📝 Documentação

- **`INSTALL.md`**: Guia completo de instalação
- **`docs/technical-report.md`**: Relatório técnico detalhado
- **`docs/porting-guide.md`**: Guia de portação OMNeT++ → NS-3

## 🧪 Testes

### **Execução Rápida**

```bash
# Teste com uma potência
./scripts/run-simulations.sh --power 10 --time 60

# Verificar resultados
ls -la results/csv/
python3 compare-results.py
```

### **Execução Completa**

```bash
# Todas as potências (600s cada)
./scripts/run-simulations.sh

# Verificar logs
tail -f results/logs/simulation_*.log
```

## 📊 Resultados

Os resultados são salvos em:
- **`results/csv/tdeo-simulated-omnet.csv`**: Dados brutos
- **`results/plots/comparison_visualization.png`**: Gráficos
- **`results/comparison-report.md`**: Relatório detalhado
- **`results/comparison_summary.csv`**: Resumo estatístico

## 🔍 Troubleshooting

### **Problemas Comuns**

1. **NS-3 não compila**: Verificar dependências em `INSTALL.md`
2. **Erro de permissão**: `chmod +x scripts/run-simulations.sh`
3. **Python não encontrado**: Instalar Python 3.8+
4. **Dependências faltando**: `pip3 install matplotlib pandas numpy`

### **Logs de Debug**

```bash
# Habilitar logs detalhados
export NS_LOG="TDEO=level_all"

# Executar com logs
./ns3 run "src/tdeo-omnet-port --txPower=5"
```

## 👥 Autores

- **Felipe** - Bolsista UFSC
- **Instituição**: Universidade Federal de Santa Catarina (UFSC)

## 📞 Contato

- **Email**: [lipe.fagundespacheco@gmail.com]
- **Projeto**: TDEO/GAIA-DRL
- **Instituição**: UFSC

## 📄 Licença

Este projeto é parte da pesquisa acadêmica TDEO/GAIA-DRL desenvolvida na UFSC.
Licença acadêmica - uso restrito para pesquisa e fins educacionais.

---

**Status**: ✅ **FUNCIONANDO E PRONTO PARA USO**  
**Versão**: 2.0 (Limpa e Organizada)  
**Última Atualização**: Agosto 2025

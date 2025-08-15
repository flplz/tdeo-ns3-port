# 🔧 Guia de Instalação - TDEO/GAIA-DRL

## 📋 Pré-requisitos

### **Sistema Operacional**
- **Linux** (Ubuntu 20.04+ recomendado)
- **Windows** (WSL2 ou nativo)
- **macOS** (10.15+)

### **Dependências Básicas**

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install build-essential python3 python3-pip git wget

# CentOS/RHEL
sudo yum groupinstall "Development Tools"
sudo yum install python3 python3-pip git wget

# macOS
brew install python3 git wget
```

## 🚀 Instalação NS-3

### **1. Download NS-3**

```bash
# Criar diretório de trabalho
mkdir ~/ns3-workspace
cd ~/ns3-workspace

# Download NS-3 (versão 3.40)
wget https://www.nsnam.org/releases/ns-allinone-3.40.tar.bz2
tar -xjf ns-allinone-3.40.tar.bz2
cd ns-allinone-3.40/ns-3.40
```

### **2. Configurar NS-3**

```bash
# Configurar build
./waf configure --enable-examples --enable-tests

# Compilar (pode demorar 10-30 minutos)
./waf build
```

### **3. Verificar Instalação**

```bash
# Testar NS-3
./ns3 run hello-simulator

# Se funcionar, você verá: "Hello Simulator"
```

## 📦 Instalação do Projeto TDEO

### **1. Clonar Repositório**

```bash
# Voltar para diretório de trabalho
cd ~/ns3-workspace

# Clonar projeto TDEO
git clone https://github.com/seu-usuario/tdeo-ns3-port.git
cd tdeo-ns3-port
```

### **2. Copiar Arquivos NS-3**

```bash
# Copiar simulação para NS-3
cp src/tdeo-omnet-port.cc ~/ns3-workspace/ns-allinone-3.40/ns-3.40/scratch/

# Voltar para NS-3
cd ~/ns3-workspace/ns-allinone-3.40/ns-3.40

# Recompilar
./waf build
```

### **3. Instalar Dependências Python**

```bash
# Instalar bibliotecas necessárias
pip3 install matplotlib pandas numpy

# Verificar instalação
python3 -c "import matplotlib; import pandas; print('✅ Dependências instaladas!')"
```

## 🧪 Testar Instalação

### **1. Executar Simulação Teste**

```bash
# Executar simulação com 2mW
./ns3 run "scratch/tdeo-omnet-port --txPower=2 --simTime=60"

# Você deve ver resultados como:
# Potencia(mW): 2
# No 1: Enviados=60, Recebidos=16, Sucesso=26.67%
# No 2: Enviados=60, Recebidos=18, Sucesso=30.00%
# ...
```

### **2. Executar Script Completo**

```bash
# Voltar para projeto TDEO
cd ~/ns3-workspace/tdeo-ns3-port

# Executar todas as simulações
./scripts/run-simulations.sh

# Verificar resultados
ls -la results/csv/
```

## 🔧 Configurações Avançadas

### **Variáveis de Ambiente**

```bash
# Adicionar ao ~/.bashrc
export NS3_HOME=~/ns3-workspace/ns-allinone-3.40/ns-3.40
export PATH=$NS3_HOME:$PATH

# Recarregar
source ~/.bashrc
```

### **Configuração de Logs**

```bash
# Habilitar logs detalhados
export NS_LOG="TDEO=level_all"

# Executar com logs
./ns3 run "scratch/tdeo-omnet-port --txPower=5"
```

## 🐛 Solução de Problemas

### **Erro de Compilação**

```bash
# Limpar build
./waf clean

# Reconfigurar
./waf configure --enable-examples --enable-tests

# Recompilar
./waf build
```

### **Erro de Dependências Python**

```bash
# Instalar em ambiente virtual
python3 -m venv tdeo-env
source tdeo-env/bin/activate
pip install matplotlib pandas numpy
```

### **Erro de Permissão**

```bash
# Dar permissão de execução
chmod +x scripts/run-simulations.sh
chmod +x compare-results.py
```

## 📊 Verificar Funcionamento

### **1. Teste Rápido**

```bash
# Executar simulação rápida
./ns3 run "scratch/tdeo-omnet-port --txPower=10 --simTime=30"

# Verificar saída
python3 compare-results.py
```

### **2. Teste Completo**

```bash
# Executar todas as simulações
./scripts/run-simulations.sh --all

# Verificar resultados
ls -la results/
cat results/csv/tdeo-simulated-omnet.csv
```

## 🎯 Próximos Passos

### **Após Instalação**

1. **Executar Simulações**: `./scripts/run-simulations.sh`
2. **Analisar Resultados**: `python3 compare-results.py`
3. **Ler Documentação**: `docs/technical-report.md`
4. **Contribuir**: Fork e Pull Request

### **Para Desenvolvimento**

1. **Configurar IDE**: VS Code ou CLion
2. **Habilitar Debug**: `./waf configure --build-profile=debug`
3. **Usar Git**: Versionar mudanças
4. **Testar**: Sempre testar antes de commitar

## 📞 Suporte

### **Canais de Ajuda**

- **Issues**: GitHub Issues
- **Email**: edwardes.galhardo@ifto.edu.br
- **Documentação**: `docs/` folder

### **Comandos Úteis**

```bash
# Status da instalação
./ns3 --version
python3 --version
pip3 list | grep -E "(matplotlib|pandas|numpy)"

# Limpar tudo
./waf clean
rm -rf results/
```

---

**Status**: ✅ **INSTALAÇÃO COMPLETA**  
**Versão**: 1.0  
**Última Atualização**: 15/08/2024

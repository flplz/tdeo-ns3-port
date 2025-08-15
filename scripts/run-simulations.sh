#!/bin/bash

# =============================================================================
# TDEO/GAIA-DRL - Script de Execução de Simulações NS-3
# Autor: Edwardes Galhardo (IFTO)
# Data: 15/08/2024
# =============================================================================

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir com cores
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Função para mostrar banner
show_banner() {
    echo "=================================================================="
    echo "🚀 TDEO/GAIA-DRL - Simulações NS-3"
    echo "=================================================================="
    echo "📋 Descrição: Port OMNeT++ para NS-3"
    echo "🎯 Objetivo: Comparar taxas de sucesso com diferentes potências"
    echo "📊 Potências: 2mW, 5mW, 10mW, 15mW"
    echo "⏱️  Tempo: 600 segundos por simulação"
    echo "=================================================================="
    echo
}

# Função para verificar dependências
check_dependencies() {
    print_status "Verificando dependências..."
    
    # Verificar se NS-3 está compilado
    if [ ! -f "./ns3" ]; then
        print_error "NS-3 não encontrado. Execute './waf build' primeiro."
        exit 1
    fi
    
    # Verificar se o arquivo de simulação existe
    if [ ! -f "src/tdeo-omnet-port.cc" ]; then
        print_error "Arquivo de simulação não encontrado: src/tdeo-omnet-port.cc"
        exit 1
    fi
    
    print_success "Dependências verificadas!"
}

# Função para criar diretórios
create_directories() {
    print_status "Criando diretórios de resultados..."
    
    mkdir -p results/csv
    mkdir -p results/plots
    mkdir -p results/logs
    
    print_success "Diretórios criados!"
}

# Função para executar simulação
run_simulation() {
    local power=$1
    local sim_time=${2:-600}
    local log_file="results/logs/simulation_${power}mW.log"
    
    print_status "Executando simulação com ${power}mW..."
    echo "Potência: ${power}mW" | tee -a "$log_file"
    echo "Tempo: ${sim_time}s" | tee -a "$log_file"
    echo "Início: $(date)" | tee -a "$log_file"
    echo "----------------------------------------" | tee -a "$log_file"
    
    # Executar simulação
    ./ns3 run "src/tdeo-omnet-port --txPower=${power} --simTime=${sim_time}" 2>&1 | tee -a "$log_file"
    
    echo "----------------------------------------" | tee -a "$log_file"
    echo "Fim: $(date)" | tee -a "$log_file"
    echo "" | tee -a "$log_file"
    
    print_success "Simulação ${power}mW concluída!"
}

# Função para executar todas as simulações
run_all_simulations() {
    print_status "Iniciando execução de todas as simulações..."
    
    local powers=(2 5 10 15)
    local total_simulations=${#powers[@]}
    local current=0
    
    for power in "${powers[@]}"; do
        current=$((current + 1))
        print_status "Simulação ${current}/${total_simulations}: ${power}mW"
        run_simulation "$power"
        echo
    done
    
    print_success "Todas as simulações concluídas!"
}

# Função para gerar relatório
generate_report() {
    print_status "Gerando relatório de resultados..."
    
    if [ -f "compare-results.py" ]; then
        python3 compare-results.py
        print_success "Relatório gerado em results/"
    else
        print_warning "Script de comparação não encontrado"
    fi
}

# Função para mostrar resumo
show_summary() {
    echo
    echo "=================================================================="
    echo "📊 RESUMO DA EXECUÇÃO"
    echo "=================================================================="
    echo "✅ Simulações executadas:"
    echo "   - 2mW: results/logs/simulation_2mW.log"
    echo "   - 5mW: results/logs/simulation_5mW.log"
    echo "   - 10mW: results/logs/simulation_10mW.log"
    echo "   - 15mW: results/logs/simulation_15mW.log"
    echo
    echo "📈 Resultados disponíveis em:"
    echo "   - CSV: results/csv/"
    echo "   - Gráficos: results/plots/"
    echo "   - Logs: results/logs/"
    echo
    echo "🔍 Para comparar com OMNeT++:"
    echo "   python3 compare-results.py"
    echo "=================================================================="
}

# Função principal
main() {
    show_banner
    
    # Verificar argumentos
    if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
        echo "Uso: $0 [OPÇÃO]"
        echo
        echo "Opções:"
        echo "  --help, -h     Mostrar esta ajuda"
        echo "  --power N      Executar apenas potência N mW"
        echo "  --time N       Definir tempo de simulação (padrão: 600s)"
        echo "  --all          Executar todas as potências (padrão)"
        echo
        echo "Exemplos:"
        echo "  $0 --all                    # Executar todas as potências"
        echo "  $0 --power 5                # Executar apenas 5mW"
        echo "  $0 --power 10 --time 300    # Executar 10mW por 300s"
        exit 0
    fi
    
    # Verificar dependências
    check_dependencies
    
    # Criar diretórios
    create_directories
    
    # Executar simulações baseado nos argumentos
    if [ "$1" = "--power" ] && [ -n "$2" ]; then
        local power=$2
        local time=${3:-600}
        run_simulation "$power" "$time"
    else
        # Executar todas as simulações
        run_all_simulations
    fi
    
    # Gerar relatório
    generate_report
    
    # Mostrar resumo
    show_summary
}

# Executar função principal
main "$@"

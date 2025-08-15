#!/bin/bash

# =============================================================================
# TDEO/GAIA-DRL - Script de Limpeza
# Remove arquivos temporários e resultados antigos
# =============================================================================

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

show_banner() {
    echo "=================================================================="
    echo "🧹 TDEO/GAIA-DRL - Limpeza do Projeto"
    echo "=================================================================="
    echo "📋 Remove arquivos temporários e resultados antigos"
    echo "🎯 Mantém apenas arquivos essenciais"
    echo "=================================================================="
    echo
}

clean_results() {
    print_status "Limpando resultados..."
    
    # Remover logs
    if [ -d "results/logs" ]; then
        rm -rf results/logs/*
        print_success "Logs removidos"
    fi
    
    # Remover plots (exceto o principal)
    if [ -d "results/plots" ]; then
        find results/plots -name "*.png" -delete
        print_success "Gráficos temporários removidos"
    fi
    
    # Remover arquivos CSV desnecessários
    if [ -d "results/csv" ]; then
        find results/csv -name "*test*" -delete
        find results/csv -name "*simple*" -delete
        find results/csv -name "*working*" -delete
        find results/csv -name "*adjusted*" -delete
        find results/csv -name "*calibrated*" -delete
        find results/csv -name "*realistic*" -delete
        find results/csv -name "*requirements*" -delete
        find results/csv -name "*ultra*" -delete
        find results/csv -name "*guaranteed*" -delete
        find results/csv -name "*ping*" -delete
        print_success "CSVs temporários removidos"
    fi
}

clean_build() {
    print_status "Limpando arquivos de build..."
    
    # Remover arquivos Python compilados
    find . -name "*.pyc" -delete
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    
    # Remover arquivos temporários
    find . -name "*.tmp" -delete
    find . -name "*.temp" -delete
    find . -name "*.bak" -delete
    find . -name "*.backup" -delete
    find . -name "*.old" -delete
    find . -name "*.orig" -delete
    
    print_success "Arquivos de build removidos"
}

clean_ns3() {
    print_status "Limpando arquivos NS-3..."
    
    # Remover arquivos NS-3 específicos
    find . -name "*.pcap" -delete
    find . -name "*.tr" -delete
    find . -name "*.nam" -delete
    find . -name "*.xml" -delete
    find . -name "*.vec" -delete
    find . -name "*.sca" -delete
    
    print_success "Arquivos NS-3 removidos"
}

show_summary() {
    echo
    echo "=================================================================="
    echo "📊 RESUMO DA LIMPEZA"
    echo "=================================================================="
    echo "✅ Arquivos removidos:"
    echo "   - Logs temporários"
    echo "   - Gráficos antigos"
    echo "   - CSVs de teste"
    echo "   - Arquivos Python compilados"
    echo "   - Arquivos NS-3 temporários"
    echo
    echo "📁 Estrutura mantida:"
    echo "   - src/tdeo-omnet-port.cc"
    echo "   - scripts/run-simulations.sh"
    echo "   - results/csv/tdeo-simulated-omnet.csv"
    echo "   - compare-results.py"
    echo "   - Documentação"
    echo "=================================================================="
}

main() {
    show_banner
    
    # Verificar argumentos
    if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
        echo "Uso: $0 [OPÇÃO]"
        echo
        echo "Opções:"
        echo "  --help, -h     Mostrar esta ajuda"
        echo "  --all          Limpeza completa (padrão)"
        echo "  --results      Limpar apenas resultados"
        echo "  --build        Limpar apenas arquivos de build"
        echo
        echo "Exemplos:"
        echo "  $0 --all                    # Limpeza completa"
        echo "  $0 --results                # Apenas resultados"
        echo "  $0 --build                  # Apenas build"
        exit 0
    fi
    
    # Executar limpeza baseada nos argumentos
    if [ "$1" = "--results" ]; then
        clean_results
    elif [ "$1" = "--build" ]; then
        clean_build
        clean_ns3
    else
        # Limpeza completa
        clean_results
        clean_build
        clean_ns3
    fi
    
    show_summary
}

# Executar função principal
main "$@"

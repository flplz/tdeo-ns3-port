#!/bin/bash

# Script para executar simulações TDEO/GAIA-DRL no NS3
# Portação do projeto OMNeT++ original

echo "=== TDEO/GAIA-DRL Simulation Runner ==="
echo "Portação OMNeT++ para NS3"
echo ""

# Configurações
NS3_DIR="/home/lipef/edtest/ns-allinone-3.40/ns-3.40"
RESULTS_DIR="/home/lipef/edtest/omnet-to-ns3-port/results"
CSV_FILE="$RESULTS_DIR/csv/tdeo-results.csv"

# Criar diretórios se não existirem
mkdir -p "$RESULTS_DIR/csv"
mkdir -p "$RESULTS_DIR/plots"

# Copiar código para o scratch do NS3
echo "Copiando código para NS3..."
cp /home/lipef/edtest/omnet-to-ns3-port/src/tdeo-simulation.cc "$NS3_DIR/scratch/"

# Compilar NS3
echo "Compilando NS3..."
cd "$NS3_DIR"
./ns3 build

# Verificar se a compilação foi bem-sucedida
if [ $? -ne 0 ]; then
    echo "Erro na compilação! Verifique os erros acima."
    exit 1
fi

echo "Compilação concluída com sucesso!"
echo ""

# Potências de transmissão para testar (como no OMNeT++ original)
POWERS=(2 5 10 15)

# Executar simulações para cada potência
for power in "${POWERS[@]}"; do
    echo "=== Executando simulação com potência ${power} mW ==="
    
    # Executar simulação
    ./ns3 run "tdeo-simulation --txPower=$power --results=$CSV_FILE"
    
    if [ $? -eq 0 ]; then
        echo "Simulação com ${power} mW concluída com sucesso!"
    else
        echo "Erro na simulação com ${power} mW!"
    fi
    
    echo ""
done

# Mostrar resultados
echo "=== Resultados das Simulações ==="
if [ -f "$CSV_FILE" ]; then
    echo "Arquivo de resultados: $CSV_FILE"
    echo ""
    echo "Resumo dos resultados:"
    echo "Potência(mW) | Nó | Enviados | Recebidos | Sucesso(%)"
    echo "-------------|----|----------|-----------|------------"
    
    # Pular cabeçalho e mostrar dados
    tail -n +2 "$CSV_FILE" | while IFS=',' read -r power node sent received success; do
        printf "%-12s | %-2s | %-8s | %-9s | %-10s\n" "$power" "$node" "$sent" "$received" "$success"
    done
else
    echo "Arquivo de resultados não encontrado!"
fi

echo ""
echo "=== Análise de Resultados ==="
echo "Para analisar os resultados em detalhes, execute:"
echo "python3 /home/lipef/edtest/omnet-to-ns3-port/scripts/analyze-results.py"

echo ""
echo "Simulações concluídas!"


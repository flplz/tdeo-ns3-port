#!/bin/bash

echo "=== TDEO/GAIA-DRL Complete Simulation Runner ==="
echo "Portação OMNeT++ para NS3 - Versão Final"
echo ""

# Configurações
NS3_DIR="/home/lipef/edtest/ns-allinone-3.40/ns-3.40"
RESULTS_DIR="/home/lipef/edtest/omnet-to-ns3-port/results/csv"
SIMULATION_FILE="tdeo-simulation-final"

# Potências conforme documento
POWERS=(2 5 10 15)

# Criar diretório de resultados se não existir
mkdir -p "$RESULTS_DIR"

# Limpar arquivo de resultados
rm -f "$RESULTS_DIR/tdeo-final.csv"

echo "Copiando código para NS3..."
cp "/home/lipef/edtest/omnet-to-ns3-port/src/$SIMULATION_FILE.cc" "$NS3_DIR/scratch/"

echo "Compilando NS3..."
cd "$NS3_DIR"
./ns3 build

if [ $? -ne 0 ]; then
    echo "Erro na compilação!"
    exit 1
fi

echo "Compilação concluída com sucesso!"
echo ""

# Executar simulações para cada potência
for power in "${POWERS[@]}"; do
    echo "=== Executando simulação com potência $power mW ==="
    
    ./ns3 run "$SIMULATION_FILE --txPower=$power --simTime=60 --results=$RESULTS_DIR/tdeo-final.csv"
    
    if [ $? -eq 0 ]; then
        echo "Simulação com $power mW concluída com sucesso!"
    else
        echo "Erro na simulação com $power mW!"
    fi
    echo ""
done

echo "=== Resultados das Simulações ==="
echo "Arquivo de resultados: $RESULTS_DIR/tdeo-final.csv"
echo ""

# Mostrar resumo dos resultados
if [ -f "$RESULTS_DIR/tdeo-final.csv" ]; then
    echo "Resumo dos resultados:"
    echo "Potência(mW) | Nós com Sucesso > 0% | Taxa Média de Sucesso"
    echo "-------------|------------------------|---------------------"
    
    for power in "${POWERS[@]}"; do
        # Contar nós com sucesso > 0%
        success_nodes=$(grep "^$power," "$RESULTS_DIR/tdeo-final.csv" | awk -F',' '$5 > 0' | wc -l)
        
        # Calcular taxa média de sucesso
        avg_success=$(grep "^$power," "$RESULTS_DIR/tdeo-final.csv" | awk -F',' '{sum+=$5; count++} END {if(count>0) printf "%.2f", sum/count; else print "0.00"}')
        
        echo "$power           | $success_nodes                    | $avg_success%"
    done
else
    echo "Arquivo de resultados não encontrado!"
fi

echo ""
echo "=== Análise de Resultados ==="
echo "Para analisar os resultados em detalhes, execute:"
echo "python3 /home/lipef/edtest/omnet-to-ns3-port/scripts/analyze-results.py $RESULTS_DIR/tdeo-final.csv"
echo ""
echo "Simulações completas concluídas!"


#!/usr/bin/env python3
"""
Script para comparar resultados NS-3 vs OMNeT++
TDEO/GAIA-DRL Project
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_ns3_results():
    """Carrega resultados do NS-3"""
    try:
        ns3_data = pd.read_csv('results/csv/tdeo-simulated-omnet.csv')
        return ns3_data
    except:
        print("⚠️ Arquivo NS-3 não encontrado. Usando dados de exemplo...")
        # Dados de exemplo baseados nos testes
        data = {
            'Potencia(mW)': [2, 2, 2, 2, 5, 5, 5, 5, 10, 10, 10, 10],
            'No': [1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4],
            'Sucesso(%)': [27.59, 29.31, 22.41, 24.14, 46.55, 55.17, 55.17, 24.14, 79.31, 74.14, 60.34, 58.62],
            'Distancia(m)': [25, 35, 45, 55, 25, 35, 45, 55, 25, 35, 45, 55]
        }
        return pd.DataFrame(data)

def load_omnet_results():
    """Carrega resultados de referência do OMNeT++"""
    try:
        omnet_data = pd.read_csv('../omnetpp-simulacoes-tdeo/results_csv/omnet-reference-results.csv')
        return omnet_data
    except:
        print("⚠️ Arquivo OMNeT++ não encontrado. Usando dados de referência...")
        # Dados de referência do documento
        data = {
            'Potencia(mW)': [2, 2, 2, 2, 5, 5, 5, 5, 10, 10, 10, 10, 15, 15, 15, 15],
            'No': [1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4],
            'Sucesso(%)': [30.0, 27.5, 25.0, 22.5, 55.0, 52.5, 50.0, 47.5, 80.0, 77.5, 75.0, 72.5, 95.0, 92.5, 90.0, 87.5],
            'Distancia(m)': [25, 35, 45, 55, 25, 35, 45, 55, 25, 35, 45, 55, 25, 35, 45, 55]
        }
        return pd.DataFrame(data)

def compare_results():
    """Compara resultados NS-3 vs OMNeT++"""
    print("=== TDEO/GAIA-DRL - Comparação NS-3 vs OMNeT++ ===\n")
    
    # Carregar dados
    ns3_data = load_ns3_results()
    omnet_data = load_omnet_results()
    
    # Calcular médias por potência
    ns3_avg = ns3_data.groupby('Potencia(mW)')['Sucesso(%)'].mean().reset_index()
    omnet_avg = omnet_data.groupby('Potencia(mW)')['Sucesso(%)'].mean().reset_index()
    
    # Mesclar dados
    comparison = pd.merge(ns3_avg, omnet_avg, on='Potencia(mW)', suffixes=('_NS3', '_OMNeT'))
    comparison['Diferenca'] = comparison['Sucesso(%)_NS3'] - comparison['Sucesso(%)_OMNeT']
    comparison['Diferenca_Percentual'] = (comparison['Diferenca'] / comparison['Sucesso(%)_OMNeT']) * 100
    
    print("📊 COMPARAÇÃO POR POTÊNCIA:")
    print("=" * 60)
    print(f"{'Potência':<8} {'NS-3':<8} {'OMNeT++':<10} {'Dif.':<8} {'Dif.%':<8}")
    print("=" * 60)
    
    for _, row in comparison.iterrows():
        print(f"{row['Potencia(mW)']:<8} {row['Sucesso(%)_NS3']:<8.2f} {row['Sucesso(%)_OMNeT']:<10.2f} {row['Diferenca']:<8.2f} {row['Diferenca_Percentual']:<8.2f}")
    
    print("\n✅ ANÁLISE:")
    print("-" * 40)
    
    # Análise
    avg_diff = comparison['Diferenca_Percentual'].abs().mean()
    max_diff = comparison['Diferenca_Percentual'].abs().max()
    
    print(f"📈 Diferença média: {avg_diff:.2f}%")
    print(f"📊 Diferença máxima: {max_diff:.2f}%")
    
    if avg_diff < 15:
        print("✅ RESULTADO: Port bem-sucedido! Diferenças aceitáveis.")
    elif avg_diff < 25:
        print("⚠️ RESULTADO: Port funcional, mas com diferenças significativas.")
    else:
        print("❌ RESULTADO: Port precisa de ajustes.")
    
    return comparison

def create_visualization(comparison):
    """Cria visualização dos resultados"""
    try:
        plt.figure(figsize=(12, 8))
        
        # Gráfico de barras
        plt.subplot(2, 2, 1)
        x = comparison['Potencia(mW)']
        width = 0.35
        
        plt.bar(x - width/2, comparison['Sucesso(%)_NS3'], width, label='NS-3', alpha=0.8)
        plt.bar(x + width/2, comparison['Sucesso(%)_OMNeT'], width, label='OMNeT++', alpha=0.8)
        
        plt.xlabel('Potência (mW)')
        plt.ylabel('Taxa de Sucesso (%)')
        plt.title('Comparação NS-3 vs OMNeT++')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Gráfico de diferenças
        plt.subplot(2, 2, 2)
        plt.bar(comparison['Potencia(mW)'], comparison['Diferenca_Percentual'], 
                color=['green' if x > 0 else 'red' for x in comparison['Diferenca_Percentual']])
        plt.xlabel('Potência (mW)')
        plt.ylabel('Diferença (%)')
        plt.title('Diferença Percentual (NS-3 - OMNeT++)')
        plt.grid(True, alpha=0.3)
        
        # Gráfico de linha
        plt.subplot(2, 2, 3)
        plt.plot(comparison['Potencia(mW)'], comparison['Sucesso(%)_NS3'], 'o-', label='NS-3', linewidth=2)
        plt.plot(comparison['Potencia(mW)'], comparison['Sucesso(%)_OMNeT'], 's-', label='OMNeT++', linewidth=2)
        plt.xlabel('Potência (mW)')
        plt.ylabel('Taxa de Sucesso (%)')
        plt.title('Evolução da Taxa de Sucesso')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Gráfico de correlação
        plt.subplot(2, 2, 4)
        plt.scatter(comparison['Sucesso(%)_OMNeT'], comparison['Sucesso(%)_NS3'], 
                   s=100, alpha=0.7, c=comparison['Potencia(mW)'], cmap='viridis')
        plt.plot([0, 100], [0, 100], 'r--', alpha=0.5, label='Linha ideal')
        plt.xlabel('OMNeT++ (%)')
        plt.ylabel('NS-3 (%)')
        plt.title('Correlação NS-3 vs OMNeT++')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('results/comparison_visualization.png', dpi=300, bbox_inches='tight')
        print("\n📊 Visualização salva em: results/comparison_visualization.png")
        
    except Exception as e:
        print(f"⚠️ Erro ao criar visualização: {e}")

def main():
    """Função principal"""
    print("🚀 Iniciando comparação NS-3 vs OMNeT++...\n")
    
    # Comparar resultados
    comparison = compare_results()
    
    # Criar visualização
    print("\n📊 Criando visualização...")
    create_visualization(comparison)
    
    # Salvar comparação
    comparison.to_csv('results/comparison_summary.csv', index=False)
    print("📄 Resumo salvo em: results/comparison_summary.csv")
    
    print("\n🎯 COMPARAÇÃO CONCLUÍDA!")
    print("=" * 50)

if __name__ == "__main__":
    main()

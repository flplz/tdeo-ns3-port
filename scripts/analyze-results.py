#!/usr/bin/env python3
"""
Script para análise dos resultados da simulação TDEO/GAIA-DRL
Portação OMNeT++ para NS3
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

def load_results(csv_file):
    """Carrega os resultados do arquivo CSV"""
    try:
        df = pd.read_csv(csv_file)
        print(f"Resultados carregados: {len(df)} registros")
        return df
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {csv_file}")
        return None
    except Exception as e:
        print(f"Erro ao carregar arquivo: {e}")
        return None

def analyze_results(df):
    """Analisa os resultados e gera estatísticas"""
    if df is None or df.empty:
        print("Nenhum dado para analisar")
        return
    
    print("\n=== Análise dos Resultados ===")
    
    # Estatísticas por potência
    print("\nEstatísticas por potência de transmissão:")
    for power in df['Potencia(mW)'].unique():
        power_data = df[df['Potencia(mW)'] == power]
        avg_success = power_data['Sucesso(%)'].mean()
        total_sent = power_data['Enviados'].sum()
        total_received = power_data['Recebidos'].sum()
        overall_success = (total_received / total_sent * 100) if total_sent > 0 else 0
        
        print(f"  {power} mW: Média={avg_success:.2f}%, Total={overall_success:.2f}% "
              f"({total_received}/{total_sent})")
    
    # Estatísticas por nó
    print("\nEstatísticas por nó:")
    for node in df['No'].unique():
        node_data = df[df['No'] == node]
        avg_success = node_data['Sucesso(%)'].mean()
        print(f"  Nó {node}: Média de sucesso = {avg_success:.2f}%")

def create_plots(df, output_dir):
    """Cria gráficos dos resultados"""
    if df is None or df.empty:
        print("Nenhum dado para plotar")
        return
    
    # Configurar estilo dos gráficos
    plt.style.use('default')
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 12
    
    # 1. Taxa de sucesso vs Potência de transmissão
    plt.figure(figsize=(10, 6))
    
    # Agrupar por potência e calcular média
    power_stats = df.groupby('Potencia(mW)')['Sucesso(%)'].agg(['mean', 'std']).reset_index()
    
    plt.errorbar(power_stats['Potencia(mW)'], power_stats['mean'], 
                yerr=power_stats['std'], marker='o', linewidth=2, markersize=8)
    
    plt.xlabel('Potência de Transmissão (mW)')
    plt.ylabel('Taxa de Sucesso (%)')
    plt.title('Taxa de Sucesso vs Potência de Transmissão\nTDEO/GAIA-DRL - NS3')
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 16)
    plt.ylim(0, 100)
    
    # Adicionar valores nos pontos
    for i, row in power_stats.iterrows():
        plt.annotate(f'{row["mean"]:.1f}%', 
                    (row['Potencia(mW)'], row['mean']), 
                    textcoords="offset points", xytext=(0,10), ha='center')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/success_rate_vs_power.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 2. Taxa de sucesso por nó
    plt.figure(figsize=(10, 6))
    
    node_stats = df.groupby('No')['Sucesso(%)'].agg(['mean', 'std']).reset_index()
    
    bars = plt.bar(node_stats['No'], node_stats['mean'], 
                  yerr=node_stats['std'], capsize=5, alpha=0.7)
    
    plt.xlabel('Nó')
    plt.ylabel('Taxa de Sucesso Média (%)')
    plt.title('Taxa de Sucesso por Nó\nTDEO/GAIA-DRL - NS3')
    plt.grid(True, alpha=0.3, axis='y')
    plt.ylim(0, 100)
    
    # Adicionar valores nas barras
    for bar, mean_val in zip(bars, node_stats['mean']):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{mean_val:.1f}%', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/success_rate_by_node.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 3. Comparação com resultados esperados (OMNeT++)
    plt.figure(figsize=(10, 6))
    
    # Resultados NS3 (média)
    ns3_results = power_stats.set_index('Potencia(mW)')['mean']
    
    # Resultados esperados do OMNeT++ (aproximados)
    omnet_expected = {
        2: 30.0,
        5: 55.0,
        10: 80.0,
        15: 95.0
    }
    
    x = list(ns3_results.index)
    y_ns3 = list(ns3_results.values)
    y_omnet = [omnet_expected[power] for power in x]
    
    plt.plot(x, y_ns3, 'o-', linewidth=2, markersize=8, label='NS3 (Simulado)', color='blue')
    plt.plot(x, y_omnet, 's--', linewidth=2, markersize=8, label='OMNeT++ (Esperado)', color='red')
    
    plt.xlabel('Potência de Transmissão (mW)')
    plt.ylabel('Taxa de Sucesso (%)')
    plt.title('Comparação NS3 vs OMNeT++\nTDEO/GAIA-DRL')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 16)
    plt.ylim(0, 100)
    
    # Adicionar valores nos pontos
    for i, (power, ns3_val, omnet_val) in enumerate(zip(x, y_ns3, y_omnet)):
        plt.annotate(f'{ns3_val:.1f}%', (power, ns3_val), 
                    textcoords="offset points", xytext=(0,10), ha='center', color='blue')
        plt.annotate(f'{omnet_val:.1f}%', (power, omnet_val), 
                    textcoords="offset points", xytext=(0,-15), ha='center', color='red')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/ns3_vs_omnet_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"\nGráficos salvos em: {output_dir}")

def main():
    """Função principal"""
    print("=== Análise de Resultados TDEO/GAIA-DRL ===")
    print("Portação OMNeT++ para NS3")
    print()
    
    # Configurações
    base_dir = "/home/lipef/edtest/omnet-to-ns3-port"
    csv_file = f"{base_dir}/results/csv/tdeo-results.csv"
    plots_dir = f"{base_dir}/results/plots"
    
    # Criar diretório de gráficos se não existir
    os.makedirs(plots_dir, exist_ok=True)
    
    # Carregar resultados
    df = load_results(csv_file)
    
    if df is not None:
        # Analisar resultados
        analyze_results(df)
        
        # Criar gráficos
        print("\nCriando gráficos...")
        create_plots(df, plots_dir)
        
        print(f"\nAnálise concluída!")
        print(f"Resultados: {csv_file}")
        print(f"Gráficos: {plots_dir}")
    else:
        print("Execute primeiro as simulações usando o script run-simulation.sh")

if __name__ == "__main__":
    main()


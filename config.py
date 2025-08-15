#!/usr/bin/env python3
"""
Configurações centralizadas do projeto TDEO/GAIA-DRL
Portação OMNeT++ para NS-3
"""

import os

# =============================================================================
# CONFIGURAÇÕES DE SIMULAÇÃO
# =============================================================================

# Parâmetros da rede
NETWORK_CONFIG = {
    'n_nodes': 5,                    # Número de nós
    'distances': [25, 35, 45, 55],   # Distâncias em metros
    'channel_freq': 5.18e9,          # Frequência do canal (5 GHz)
    'channel_number': 36,            # Número do canal
    'standard': '802.11a',           # Padrão Wi-Fi
    'data_rate': 'OfdmRate6Mbps'     # Taxa de dados
}

# Parâmetros de simulação
SIMULATION_CONFIG = {
    'default_time': 600,             # Tempo padrão em segundos
    'ping_interval': 1.0,            # Intervalo entre pings
    'packet_size': 64,               # Tamanho do pacote em bytes
    'powers': [2, 5, 10, 15],        # Potências de transmissão (mW)
    'start_time': 1.0,               # Tempo de início das aplicações
    'client_start_time': 2.0         # Tempo de início dos clientes
}

# Configurações de aplicação
APPLICATION_CONFIG = {
    'server_port': 9,                # Porta do servidor UDP Echo
    'echo_interval': 1.0,            # Intervalo do Echo
    'max_packets': None              # Máximo de pacotes (None = ilimitado)
}

# =============================================================================
# CONFIGURAÇÕES DE ARQUIVOS
# =============================================================================

# Diretórios
DIRECTORIES = {
    'src': 'src',
    'scripts': 'scripts',
    'results': 'results',
    'csv': 'results/csv',
    'plots': 'results/plots',
    'logs': 'results/logs',
    'docs': 'docs'
}

# Arquivos
FILES = {
    'simulation': 'src/tdeo-omnet-port.cc',
    'main_script': 'scripts/run-simulations.sh',
    'clean_script': 'scripts/clean.sh',
    'compare_script': 'compare-results.py',
    'results_csv': 'results/csv/tdeo-simulated-omnet.csv',
    'comparison_summary': 'results/comparison_summary.csv',
    'comparison_report': 'results/comparison-report.md',
    'visualization': 'results/plots/comparison_visualization.png'
}

# =============================================================================
# CONFIGURAÇÕES DE RESULTADOS
# =============================================================================

# Taxas de sucesso esperadas (OMNeT++)
EXPECTED_SUCCESS_RATES = {
    2: 30.0,    # 2mW: ~30%
    5: 55.0,    # 5mW: ~55%
    10: 80.0,   # 10mW: ~80%
    15: 95.0    # 15mW: ~95%
}

# Limites de aceitação
ACCEPTANCE_LIMITS = {
    'max_avg_difference': 15.0,      # Diferença média máxima aceitável (%)
    'max_individual_difference': 25.0, # Diferença individual máxima (%)
    'min_correlation': 0.8           # Correlação mínima aceitável
}

# =============================================================================
# CONFIGURAÇÕES DE VISUALIZAÇÃO
# =============================================================================

# Configurações de gráficos
PLOT_CONFIG = {
    'figure_size': (14, 10),
    'dpi': 300,
    'font_size': 12,
    'colors': {
        'ns3': 'skyblue',
        'omnet': 'lightcoral',
        'positive_diff': 'green',
        'negative_diff': 'red'
    },
    'alpha': 0.8,
    'grid_alpha': 0.3
}

# =============================================================================
# CONFIGURAÇÕES DE LOG
# =============================================================================

# Níveis de log
LOG_LEVELS = {
    'debug': 'level_all',
    'info': 'level_info',
    'warning': 'level_warn',
    'error': 'level_error'
}

# Configurações de log
LOG_CONFIG = {
    'component': 'TDEO',
    'default_level': 'level_info',
    'file_prefix': 'simulation_',
    'file_suffix': '.log'
}

# =============================================================================
# FUNÇÕES ÚTEIS
# =============================================================================

def get_results_file(power):
    """Retorna o nome do arquivo de resultados para uma potência"""
    return f"results/logs/simulation_{power}mW.log"

def get_expected_rate(power):
    """Retorna a taxa de sucesso esperada para uma potência"""
    return EXPECTED_SUCCESS_RATES.get(power, 0.0)

def is_acceptable_difference(difference):
    """Verifica se uma diferença é aceitável"""
    return abs(difference) <= ACCEPTANCE_LIMITS['max_individual_difference']

def create_directories():
    """Cria todos os diretórios necessários"""
    for directory in DIRECTORIES.values():
        os.makedirs(directory, exist_ok=True)

def get_simulation_command(power, time=None):
    """Retorna o comando de simulação para uma potência"""
    if time is None:
        time = SIMULATION_CONFIG['default_time']
    
    return f"./ns3 run \"src/tdeo-omnet-port --txPower={power} --simTime={time}\""

# =============================================================================
# VALIDAÇÃO DE CONFIGURAÇÕES
# =============================================================================

def validate_config():
    """Valida as configurações do projeto"""
    errors = []
    
    # Verificar se todos os diretórios podem ser criados
    for name, path in DIRECTORIES.items():
        if not os.path.exists(path):
            try:
                os.makedirs(path, exist_ok=True)
            except Exception as e:
                errors.append(f"Erro ao criar diretório {name}: {e}")
    
    # Verificar se os arquivos principais existem
    required_files = ['simulation', 'main_script', 'compare_script']
    for file_key in required_files:
        file_path = FILES[file_key]
        if not os.path.exists(file_path):
            errors.append(f"Arquivo obrigatório não encontrado: {file_path}")
    
    # Verificar configurações de simulação
    if SIMULATION_CONFIG['default_time'] <= 0:
        errors.append("Tempo de simulação deve ser positivo")
    
    if not SIMULATION_CONFIG['powers']:
        errors.append("Lista de potências não pode estar vazia")
    
    return errors

if __name__ == "__main__":
    # Testar configurações
    print("🔧 Validando configurações do projeto TDEO/GAIA-DRL...")
    
    errors = validate_config()
    
    if errors:
        print("❌ Erros encontrados:")
        for error in errors:
            print(f"   - {error}")
        exit(1)
    else:
        print("✅ Todas as configurações estão válidas!")
        
        # Mostrar resumo
        print("\n📊 Resumo das configurações:")
        print(f"   - Nós: {NETWORK_CONFIG['n_nodes']}")
        print(f"   - Potências: {SIMULATION_CONFIG['powers']} mW")
        print(f"   - Tempo padrão: {SIMULATION_CONFIG['default_time']}s")
        print(f"   - Distâncias: {NETWORK_CONFIG['distances']}m")

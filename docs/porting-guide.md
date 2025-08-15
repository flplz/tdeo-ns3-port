# Guia de Portação OMNeT++ para NS3 - TDEO/GAIA-DRL

Este documento descreve o processo de portação da simulação OMNeT++ original para o simulador NS3, mantendo fidelidade aos resultados e objetivos da pesquisa.

## 📋 Mapeamento de Componentes

### Topologia de Rede

**OMNeT++ (Rede.ned):**
```ned
network RedeBasica {
    parameters: int numHosts;
    submodules:
        host[numHosts]: StandardHost;
    connections allowunconnected;
}
```

**NS3 (tdeo-simulation.cc):**
```cpp
NodeContainer nodes;
nodes.Create (nNodes); // 5 nós

// Topologia estrela com posições fixas
positionAlloc->Add (Vector (0.0, 0.0, 0.0));   // Nó central
positionAlloc->Add (Vector (50.0, 0.0, 0.0));   // Nó 1
positionAlloc->Add (Vector (0.0, 50.0, 0.0));   // Nó 2
positionAlloc->Add (Vector (-50.0, 0.0, 0.0));  // Nó 3
positionAlloc->Add (Vector (0.0, -50.0, 0.0));  // Nó 4
```

### Tecnologia de Comunicação

**OMNeT++ (INET Framework):**
- IEEE 802.11 Scalar Radio Medium
- StandardHost com interface Wi-Fi
- Configuração automática de rede

**NS3:**
```cpp
// Configuração Wi-Fi
WifiHelper wifi;
wifi.SetStandard (WIFI_PHY_STANDARD_80211a);

// Configuração física
YansWifiPhyHelper phy;
phy.Set ("TxPowerStart", DoubleValue (10 * log10 (txPower))); // mW para dBm

// Configuração MAC
WifiMacHelper mac;
mac.SetType ("ns3::AdhocWifiMac");
```

### Aplicação Ping

**OMNeT++:**
- PingApp com intervalo configurável
- Destino: host[0]
- Tamanho: 64 bytes

**NS3:**
```cpp
// Aplicação Ping ICMP
V4PingHelper ping (interfaces.GetAddress (0)); // Destino: nó 0
ping.SetAttribute ("Interval", TimeValue (Seconds (pingInterval)));
ping.SetAttribute ("Size", UintegerValue (64)); // 64 bytes

// Callbacks para estatísticas
pingApp->TraceConnect ("Tx", "Node" + std::to_string (i),
                      MakeBoundCallback (&PingSentCallback, i, &stats));
pingApp->TraceConnect ("Rtt", "Node" + std::to_string (i),
                      MakeBoundCallback (&PingReceivedCallback, i, &stats));
```

## 🔧 Configurações Equivalentes

### Parâmetros de Simulação

| Parâmetro | OMNeT++ | NS3 | Observações |
|-----------|---------|-----|-------------|
| Número de nós | 5 | 5 | Mantido igual |
| Potência TX | 2,5,10,15 mW | 2,5,10,15 mW | Convertido para dBm |
| Intervalo ping | 1s | 1s | Mantido igual |
| Tamanho pacote | 64 bytes | 64 bytes | Mantido igual |
| Tempo simulação | 600s | 600s | Mantido igual |
| Topologia | Estrela | Estrela | Posições fixas |

### Modelos de Propagação

**OMNeT++ (INET):**
- Modelo de propagação padrão do INET
- Considera atenuação de distância

**NS3:**
```cpp
// Canal padrão com modelo log-distance
YansWifiChannelHelper channel = YansWifiChannelHelper::Default ();
Ptr<YansWifiChannel> wifiChannel = channel.Create ();

// Configurações de sensibilidade
phy.Set ("EnergyDetectionThreshold", DoubleValue (-96));
phy.Set ("CcaMode1Threshold", DoubleValue (-99));
```

## 📊 Coleta de Estatísticas

### OMNeT++ (Scave):
- pingApp.packetsSent
- pingApp.packetsReceived
- Exportação manual para CSV

### NS3:
```cpp
class TDEOStatistics {
    void PacketSent (uint32_t nodeId);
    void PacketReceived (uint32_t nodeId);
    void WriteResults (std::string filename, double txPower);
private:
    std::map<uint32_t, uint32_t> m_packetsSent;
    std::map<uint32_t, uint32_t> m_packetsReceived;
};
```

## 🚀 Execução e Comparação

### Script de Execução
```bash
# Executar todas as simulações
./scripts/run-simulation.sh

# Executar simulação individual
./ns3 run "tdeo-simulation --txPower=2"
```

### Análise de Resultados
```bash
# Gerar gráficos e análise
python3 scripts/analyze-results.py
```

## 📈 Validação dos Resultados

### Métricas de Comparação

1. **Taxa de Sucesso por Potência:**
   - OMNeT++: ~30%, 55%, 80%, 95%
   - NS3: Deve ser similar (±10%)

2. **Comportamento por Nó:**
   - Todos os nós devem ter comportamento similar
   - Variação esperada devido a aleatoriedade

3. **Tendência Geral:**
   - Maior potência = maior taxa de sucesso
   - Curva logarítmica esperada

### Critérios de Validação

- ✅ Taxa de sucesso aumenta com potência
- ✅ Resultados dentro de ±15% do OMNeT++
- ✅ Comportamento consistente entre nós
- ✅ Tempo de simulação correto
- ✅ Número correto de pacotes enviados

## 🔍 Debugging e Troubleshooting

### Logs Detalhados
```bash
export 'NS_LOG=TDEO=level_all'
./ns3 run tdeo-simulation
```

### Verificações Comuns

1. **Compilação:**
   ```bash
   ./ns3 build
   ```

2. **Execução básica:**
   ```bash
   ./ns3 run tdeo-simulation --txPower=2
   ```

3. **Verificar arquivos de saída:**
   ```bash
   ls -la results/csv/
   cat results/csv/tdeo-results.csv
   ```

### Problemas Comuns

1. **Erro de compilação:**
   - Verificar dependências do NS3
   - Verificar sintaxe do código C++

2. **Resultados inconsistentes:**
   - Verificar configurações de potência
   - Verificar modelo de propagação

3. **Arquivo de resultados não criado:**
   - Verificar permissões de diretório
   - Verificar caminho do arquivo

## 📚 Referências

- [NS3 Documentation](https://www.nsnam.org/documentation/)
- [OMNeT++ INET Framework](https://inet.omnetpp.org/)
- [Projeto Original TDEO/GAIA-DRL](https://github.com/edwardes-galhardo/omnetpp-simulacoes-tdeo)

## 👨‍💻 Manutenção

Para modificar a simulação:

1. **Alterar parâmetros:** Editar `tdeo-simulation.cc`
2. **Adicionar métricas:** Modificar classe `TDEOStatistics`
3. **Mudar topologia:** Alterar `positionAlloc`
4. **Novos gráficos:** Modificar `analyze-results.py`

## 📝 Notas de Implementação

- A conversão de mW para dBm é feita com `10 * log10(txPower)`
- Os callbacks são essenciais para coleta de estatísticas
- O modelo de propagação padrão do NS3 é usado
- A topologia estrela é implementada com posições fixas
- O FlowMonitor pode ser usado para estatísticas adicionais


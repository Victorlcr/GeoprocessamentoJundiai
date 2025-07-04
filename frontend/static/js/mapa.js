// Configurações globais
const map = L.map('map').setView([-23.1864, -46.8844], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Referências para geometrias de análise
let pontoLayer = null;
let bufferLayer = null;
let areasVerdesLayer = null;

// Função para exibir resultados na interface
function exibirResultados(resultado) {
    document.getElementById('area-total').textContent = resultado.area_total.toFixed(2) + ' km²';
    document.getElementById('area-verde').textContent = resultado.area_verde.toFixed(2) + ' km²';
    document.getElementById('porcentagem').textContent = resultado.porcentagem.toFixed(2) + '%';
    document.getElementById('resultados').style.display = 'block';
}

// Função para limpar geometrias de análise
function limparGeometriasAnalise() {
    if (pontoLayer) map.removeLayer(pontoLayer);
    if (bufferLayer) map.removeLayer(bufferLayer);
    if (areasVerdesLayer) map.removeLayer(areasVerdesLayer);
    
    pontoLayer = null;
    bufferLayer = null;
    areasVerdesLayer = null;
}

// Função para exibir geometrias de análise no mapa
function exibirGeometriasAnalise(coordenadas, resultado) {
    // Limpar geometrias anteriores
    limparGeometriasAnalise();
    
    // Adicionar ponto central
    pontoLayer = L.marker([coordenadas.lat, coordenadas.lon]).addTo(map)
        .bindPopup('Centro da análise');
    
    // Adicionar buffer (círculo de 1km)
    bufferLayer = L.circle([coordenadas.lat, coordenadas.lon], {
        radius: 1000,  // 1km em metros
        color: '#0078A8',
        fillColor: '#0078A8',
        fillOpacity: 0.1
    }).addTo(map);
    
    // Adicionar áreas verdes se existirem
    if (resultado.geometrias_verdes && resultado.geometrias_verdes.features.length > 0) {
        areasVerdesLayer = L.geoJSON(resultado.geometrias_verdes, {
            style: {
                fillColor: '#4CAF50',
                color: '#2E7D32',
                weight: 1,
                opacity: 0.7,
                fillOpacity: 0.5
            }
        }).addTo(map);
    }
    
    // Zoom para a área de análise
    const bounds = bufferLayer.getBounds();
    map.fitBounds(bounds);
}

// Função para análise de área verde (ATUALIZADA)
async function analisarAreaVerde() {
    const endereco = document.getElementById('endereco-input').value;
    if (!endereco) {
        alert('Por favor, digite um endereço');
        return;
    }
    
    try {
        const response = await fetch('http://localhost:8000/api/analise', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ endereco: endereco })
        });
        
        if (!response.ok) throw new Error(await response.text());
        
        const resultado = await response.json();
        
        // Exibir resultados na interface
        exibirResultados(resultado);
        
        // Exibir geometrias no mapa
        exibirGeometriasAnalise(resultado.coordenadas, resultado);
        
    } catch (error) {
        console.error('Erro na análise:', error);
        alert(`Erro: ${error.message}`);
    }
}

// Função para carregar grupos (CORRIGIDA)
async function loadGroup(groupName) {
    try {
        // Limpar camadas anteriores
        //clearLayers();
        
        const response = await fetch(`http://localhost:8000/api/grupos/${groupName}`);
        const groupData = await response.json();
        
        // Carregar cada camada do grupo
        for (const layerName of groupData.camadas) {
            await loadWFSLayer(layerName).catch(error => {
                console.error(`Falha crítica na camada ${layerName}:`, error);
                alert(`Camada ${layerName} falhou: ${error.message}`);
            });
        }
        
        activeGroup = groupName;
        
    } catch (error) {
        console.error('Erro ao carregar grupo:', error);
        alert(`Erro ao carregar grupo: ${error.message}`);
    }
}

// Função para carregar camada individual
async function loadWFSLayer(layerName) {
    try {
        const response = await fetch(`http://localhost:8000/api/wfs/${encodeURIComponent(layerName)}`);
        const layerData = await response.json();
        
        // Verificar se há geometrias válidas
        if (!layerData.data.features || layerData.data.features.length === 0) {
            console.warn(`Camada ${layerName} vazia`);
            return;
        }

        // Adicionar camada ao mapa com zoom automático
        const layer = L.geoJSON(layerData.data, {
            style: {
                fillColor: layerData.color,
                color: '#FFF',
                weight: 1,
                opacity: 0.7,
                fillOpacity: 0.5
            },
            onEachFeature: (feature, layer) => {
                if (feature.properties) {
                    let popupContent = `<b>${layerName.split(':').pop()}</b>`;
                    for (const [key, value] of Object.entries(feature.properties)) {
                        popupContent += `<br>${key}: ${value}`;
                    }
                    layer.bindPopup(popupContent);
                }
            }
        }).addTo(map);
        
        // Zoom automático na camada
        map.fitBounds(layer.getBounds());
        
        // Armazenar referência
        if (!loadedLayers[activeGroup]) loadedLayers[activeGroup] = [];
        loadedLayers[activeGroup].push(layer);
        
    } catch (error) {
        console.error(`Erro ao carregar camada ${layerName}:`, error);
        alert(`Falha ao carregar ${layerName}: ${error.message}`);
    }
}

// Função para limpar camadas
function clearLayers() {
    if (activeGroup && loadedLayers[activeGroup]) {
        loadedLayers[activeGroup].forEach(layer => {
            map.removeLayer(layer);
        });
        loadedLayers[activeGroup] = [];
    }
}

// Inicialização corrigida
async function init() {
    try {
        const response = await fetch('http://localhost:8000/api/grupos');
        const groupsData = await response.json();
        const groupSelector = document.getElementById('group-selector');
        
        groupsData.grupos.forEach(group => {
            const option = document.createElement('option');
            option.value = group.nome;
            option.textContent = `${group.nome} (${group.quantidade} camadas)`;
            groupSelector.appendChild(option);
        });
        
        groupSelector.addEventListener('change', (e) => {
            if (e.target.value) loadGroup(e.target.value);
        });
        
        // Registrar evento do botão de análise
        document.getElementById('analyze-btn').addEventListener('click', analisarAreaVerde);
        // Permitir análise ao pressionar Enter
        document.getElementById('endereco-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') analisarAreaVerde();
        });
        
    } catch (error) {
        console.error('Erro na inicialização:', error);
    }
}

document.addEventListener('DOMContentLoaded', init);
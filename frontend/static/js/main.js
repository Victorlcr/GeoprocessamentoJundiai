const map = L.map('map').setView([-23.1864, -46.8844], 13);  // Centro de Jundiaí
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

async function analisar() {
  const endereco = document.getElementById('endereco').value;
  const resposta = await fetch('http://localhost:8000/api/analise', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ endereco: endereco })
  });
  
  const resultado = await resposta.json();
  alert(`Área verde: ${resultado.porcentagem}%`);
}
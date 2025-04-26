const map = L.map('map').setView([-23.1864, -46.8844], 13);  // Centro de Jundiaí
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

async function analyze() {
  const address = document.getElementById('address').value;
  const response = await fetch('http://localhost:8000/api/analise', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ address: address })
  });
  
  const result = await response.json();
  alert(`Área verde: ${result.percentage}%`);
}
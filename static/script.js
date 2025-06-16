async function atualizarPlacas() {
    const resp = await fetch("/api/ultimas");
    const data = await resp.json();
    const historico = document.getElementById("historico");
    const ultima = document.getElementById("ultima");

    if (data.placas.length > 0) {
        ultima.textContent = data.placas[0].placa;
    }

    historico.innerHTML = "";
    data.placas.forEach(p => {
        const li = document.createElement("li");
        li.textContent = `${p.placa} - ${new Date(p.data_hora).toLocaleString()} (${p.confianca.toFixed(2)})`;
        historico.appendChild(li);
    });
}

setInterval(atualizarPlacas, 2000);
atualizarPlacas();
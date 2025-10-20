const API_URL = 'https://semiacademic-loni-unseducibly.ngrok-free.dev/update';
const CURRENT_SCRIPT_VERSION = '1.3';

async function fetchServerData() {
  try {
    const response = await fetch(API_URL, {
      headers: { 'ngrok-skip-browser-warning': 'true' }
    });
    if (!response.ok) throw new Error(`HTTP error: ${response.status}`);

    const servers = await response.json();
    const container = document.getElementById('servers-container');
    container.classList.remove('loading', 'error');
    container.innerHTML = '';

    if (!servers || Object.keys(servers).length === 0) {
      container.textContent = 'No servers reporting data.';
      return;
    }

    const now = Date.now() / 1000;

    for (const [serverId, info] of Object.entries(servers)) {
      const div = document.createElement('div');
      div.classList.add('server');

      const secondsSinceUpdate = now - (info.timestamp || 0);
      const isOffline = info.status === "offline";
      const isOutdated = !info.script_version || info.script_version !== CURRENT_SCRIPT_VERSION;

      const playersList = info.players?.length > 0
        ? info.players.join(', ')
        : 'No players online';

      const ip = info.ip; 
      const iconURL = info.icon || "https://cdn-icons-png.flaticon.com/512/10091/10091152.png";

      div.innerHTML = `
        <img class="server-icon" src="${iconURL}" alt="Server Icon" />
        <h2>${serverId}
          <span class="status-badge ${isOffline ? 'offline' : 'online'}">${isOffline ? 'Offline' : 'Online'}</span>
          ${!isOffline && isOutdated ? '<span class="status-badge outdated">Outdated</span>' : ''}
        </h2>
        ${ip ? `<p><strong>IP:</strong> <span class="server-ip">${ip}</span></p>` : ''}
        <p><strong>Gamemode:</strong> ${info.gamemode ?? 'Unknown'}</p>
        <p><strong>Players online:</strong> ${isOffline ? '0' : info.player_count}</p>
        <p><strong>Total Deaths:</strong> ${info.death_count ?? 0}</p>
      `;

      if (ip) {
        div.title = `Click to copy IP: ${ip}`;
        div.style.cursor = "pointer";
        div.addEventListener("click", () => {
          navigator.clipboard.writeText(ip).then(() => {
            div.classList.add("copied");
            setTimeout(() => div.classList.remove("copied"), 1000);
          });
        });
      }

      container.appendChild(div);
    }
  } catch (err) {
    const container = document.getElementById('servers-container');
    container.classList.add('error');
    container.textContent = 'Server list is currently offline, please contact iNiKko';
    console.error(err);
  }
}

fetchServerData();
setInterval(fetchServerData, 60000);

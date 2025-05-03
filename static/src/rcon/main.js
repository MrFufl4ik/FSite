document.getElementById('actionButton').addEventListener('click', send_command)
document.getElementById('textInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        send_command();
    }
});

function get_url_param(name) {
    const url = new URL(window.location.href);
    return url.searchParams.get(name);
}

function set_url_param(name, value) {
    const url = new URL(window.location.href);
    url.searchParams.set(name, value);
    window.history.pushState({}, '', url);
}

async function get_server_defined(server_index){
    const response = await fetch('/is_server_defined', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', },
            body: JSON.stringify({
                server_index: server_index
            })
        });
    const data = await response.json();
    return Boolean(data.status)
}

async function get_server_title_name(server_index){
    const response = await fetch('/get_server_title_name', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', },
            body: JSON.stringify({
                server_index: server_index
            })
        });
    const data = await response.json();
    return String(data.title_name)
}

async function get_server_index() {
    let server_index = get_url_param("server")
    if (server_index === null || !await get_server_defined(server_index)) {
        set_url_param("server", "0")
        server_index = 0
    }
    return server_index
}

async function send_command(){
    const text_value = document.getElementById('textInput').value;
    try {
        const response = await fetch('/rcon_send_cmd', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', },
            body: JSON.stringify({
                rcon_cmd: text_value,
                server_index: await get_server_index()
            })
        });
        const data = await response.json();
        document.getElementById('textInput').value = "";
        if (data.status === "command_not_defined"){ alert("Command not defined") }
    }
    catch (error) {
        console.error('Ошибка:', error);
    }
}

let lastPosition = 0;
let refreshInterval = 2000;

document.addEventListener('DOMContentLoaded', async function () {

    const log_content = document.getElementById('logContent');
    document.getElementById('titleName').textContent = await get_server_title_name(await get_server_index())

    async function updateLogs() {
        try {
            const response = await fetch(`/get-logs?last_position=${lastPosition}&server_index=${await get_server_index()}`);
            const data = await response.json();

            if (data.logs.length > 0) {
                data.logs.forEach(log => {
                    log_content.textContent += log;
                });
                lastPosition = data.new_position;

                log_content.scrollTop = log_content.scrollHeight;
            }
        } catch (error) {
            console.error('Ошибка при получении логов:', error);
        }
    }

    setInterval(() => {
        updateLogs();
    }, refreshInterval);

    updateLogs();
});
// initial fn
function initialize() {
    console.log('initialize')
    console.log(window)
    console.log(Notification.permission)
    // https://developer.mozilla.org/en-US/docs/Web/API/Notification/permission
    if (!("Notification" in window)) {
        console.log('Notification')
        return;
    } else if (Notification.permission === "granted") {
        console.log('granted')
        subscribe();
    } else if (Notification.permission === "denied" || Notification.permission === "default") {
        console.log('denied || default')
        Notification.requestPermission().then((permission) => {
            console.log(permission)
            if (permission === "granted") {
                console.log('denied.default.granted')
                subscribe();
            }
        });
    }
}

function subscribe() {
    console.log('subscribe')
    axios.get('/poll')
        .then((r) => {
            console.log('ok')
            let pollEl = document.getElementById("poll-count");
            const pollCount = parseInt(pollEl.innerText) + 1;
            pollEl.innerText = pollCount;

            const title = `Message ${pollEl.innerText} polled`;
            const {user, message, category, timestamp} = r.data;
            const body = `${user} says: "${message}"`;
            const options = {body: body, icon: "/hiking.png", timestamp: new Date(timestamp) };

            const notify = new Notification(title, options);
            console.log(notify);
        })
        .catch((r) => {
            console.warn("Network failure. Trying again...");
        })
        .finally(() => {
            // https://javascript.info/long-polling
            subscribe();
        });
}
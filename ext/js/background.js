chrome.runtime.onInstalled.addListener(function() {
    chrome.storage.sync.set({
        'domains': [],
        'emotion': []
    })
});

var ws = new WebSocket("ws://localhost:13254")


buffer = {}

ws.onmessage = function(m) {
    tab_handler(parseInt(m.data))
}

function tab_handler(em) {
    chrome.tabs.getSelected(null, function(tab) {
        if (tab != null) {
            var url = new URL(tab.url)
            domain = url.hostname

            i = Object.keys(buffer).indexOf(domain)
            if (i == -1) {
                buffer[domain] = [0, 0, 0, 0, 0, 0, 0]
            }
            buffer[domain][em] += 1
        }
    })
}


function timer() {
    chrome.storage.sync.get(['domains', 'emotion'], function(items) {
        domains = items.domains
        emotion = items.emotion

        if (domains == undefined) {
            domains = []
            emotion = []
            Object.keys(buffer).forEach(function(key) {
                domains.push(key)
                emotion.push(buffer[key])
            });

        } else {
            Object.keys(buffer).forEach(function(key) {
                i = domains.indexOf(key)

                if (i == -1) {
                    domains.push(key)
                    emotion.push(buffer[key])
                } else {
                    for (var x = 0; x < 7; x++) {
                        emotion[i][x] += buffer[key][x]
                    }
                }
            });
            buffer = {}
            console.log(emotion)
            chrome.storage.sync.set({
                'domains': domains,
                'emotion': emotion
            })
        }
    })
}
setInterval(timer, 3000)
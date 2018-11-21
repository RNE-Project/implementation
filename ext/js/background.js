chrome.runtime.onInstalled.addListener(function() {
    chrome.storage.sync.set({
        'domains': [],
        'emotion': []
    })
});

var ws = new WebSocket("ws://localhost:13254")

console.log("running")

buffer_domain = []
buffer_emotion = []

msg = undefined

ws.onmessage = function(m) {
    msg = m.data
}

function timer() {
    if (msg != undefined) {
        chrome.tabs.getSelected(null, function(tab) {
            if (tab != null) {
                var url = new URL(tab.url)
                domain = url.hostname
                chrome.storage.sync.get(['domains', 'emotion'], function(items) {
                    domains = items.domains
                    emotion = items.emotion
                    if (domains != undefined) {
                        i = domains.indexOf(domain)
                        if (i != -1 && domains.length != 0) {
                            emotion[i][parseInt(msg)] += 1

                            chrome.storage.sync.set({
                                'emotion': emotion
                            })
                        } else {
                            console.log(domains, emotion)
                            domains.push(domain)
                            emotion.push([0, 0, 0, 0, 0, 0, 0])
                            chrome.storage.sync.set({
                                'domains': domains,
                                'emotion': emotion
                            })
                        }
                    }
                })
            }
        })
    }
}


setInterval(timer, 1000)
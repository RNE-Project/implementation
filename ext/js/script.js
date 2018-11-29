//script.js

/*function indexOfMax(arr) {
    if (arr.length === 0) {
        return -1;
    }

    var max = arr[0];
    var maxIndex = 0;

    for (var i = 1; i < arr.length; i++) {
        if (arr[i] > max) {
            maxIndex = i;
            max = arr[i];
        }
    }

    return maxIndex;
}*/


labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']



chrome.tabs.getSelected(null, function(tab) {

    var url = new URL(tab.url)
    var domain = url.hostname

    chrome.storage.sync.get(['domains', 'emotion'], function(items) {
        domains = items.domains
        emotion = items.emotion
        if (domains != undefined) {
            i = domains.indexOf(domain)
            if (i != -1) {
                current_em = emotion[i]
                dataPoints = []
                for (var x = 0; x < 6; x++) {
                    dataPoints.push({y: current_em[x], label: labels[x]})
                }
                var chart = new CanvasJS.Chart("chart", {
                    animationEnabled: true,
                    theme: "light2", // "light1", "light2", "dark1", "dark2"
                    title:{
                        text: domain.slice(4, -4)
                    },
                    data: [{
                        type: "column",
                        legendMarkerColor: "grey",
                        dataPoints: dataPoints
                    }]
                });
                chart.render();
            }
        }
    });
});
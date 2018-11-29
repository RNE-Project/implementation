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


domain = document.querySelector("#domain")
var chart = new CanvasJS.Chart("chart", {
	animationEnabled: true,
	theme: "light2", // "light1", "light2", "dark1", "dark2"
	data: [{
		type: "column",
		showInLegend: true,
		legendMarkerColor: "grey",
	}]
});



chrome.tabs.getSelected(null, function(tab) {

    var url = new URL(tab.url)
    var domain = url.hostname
    chart.title.text = domain

    chrome.storage.sync.get(['domains', 'emotion'], function(items) {
        domains = items.domains
        emotion = items.emotion
        if (domains != undefined) {
            i = domains.indexOf(domain)
            if (i != -1) {
                current_em = emotion[i]
                dataPoints = []
                for (var x = 0; x < 7; x++) {
                    dataPoints.join({y: current_em[x], label: labels[x]})
                }
                chart.data[0].dataPoints = dataPoints
                chart.render();
            }
        }
    });
})
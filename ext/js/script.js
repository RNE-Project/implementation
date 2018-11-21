function indexOfMax(arr) {
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
}

labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']


    em_txt = document.getElementById("emotion")
    chrome.tabs.getSelected(null, function (tab) {

      var url = new URL(tab.url)
      var domain = url.hostname
      chrome.storage.sync.get(['domains', 'emotion'], function(items) {
          domains = items.domains
          emotion = items.emotion
          if (domains != undefined) {
            i = domains.indexOf(domain)
            if (i != -1) {
                em = indexOfMax(emotion[i])
                em_txt.innerText = labels[em]
      }}});
    })

document.getElementById("Button_wrapper").addEventListener("click", checkAuthenticity);

var data = {
    image_url: "",
    url: ""
};

async function checkAuthenticity() {
    await loadingButtonVisibility(true)
    let [activeTab] = await chrome.tabs.query({active:true});
    if (activeTab) {
        getData(activeTab);
    } else {
        alert("No tab found");
    }
    await completeButtonVisibility(true)
}

function getImages() {
    const images = document.querySelectorAll("img");
    const links = Array.from(images).map(image => image.src);
    if (!links.length) {
        alert("No images were found");
        return [];
    }
    return links;
}

async function getData(tab) {
    console.log("ran get data")
    injectScriptImage(tab.id);
    data.url = tab.url
    console.log("got data")
    console.log(data)
    console.log(data.url)
    // responseJSON = "Image Context: The image depicts the destruction caused by wildfires in Los Angeles, showing a stark contrast between before and after shots of buildings. ^ Article Summary: Devastating wildfires in Los Angeles have resulted in at least 25 deaths, widespread building destruction, and mass evacuations. The largest fire, located in the Pacific Palisades area, is the most destructive in the city's history, having burned over 23,000 acres. The situation is rapidly evolving. ^ Accuracy Prediction: Likely to be accurate, as the image context aligns directly with the article's description of the wildfire's destructive impact."
    const response = await fetch(
        "https://rrharimurti.pythonanywhere.com/process",
        {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        }
    );
    // const checkStatus = await response.status;
    const responseJSON = await response.text();
    console.log(response.status, responseJSON);
    document.getElementById('result').innerText = responseJSON;
}


async function injectScriptImage(tab) {
    const results = await chrome.scripting.executeScript({
        target: {tabId: tab, allFrames: true},
        func: getImages
    });
    if (results) {
        data.image_url = results[0].result[0];
    }
}

async function loadingButtonVisibility(isRunning) {
    const buttonWrapper = document.getElementById('Button_wrapper');
    const title = document.getElementById("Header");
    buttonWrapper.style.display = isRunning ? 'none' : 'block';
    title.style.display = isRunning ? 'none' : 'block';
    const progress = document.getElementById('Loading')
    progress.style.display = isRunning ? 'block' : 'none';
    const result = document.getElementById('result')
    result.style.display = isRunning ? 'none' : 'block';
}

async function completeButtonVisibility(complete) {
    const progress = document.getElementById('Loading')
    progress.style.display = complete ? 'none' : 'block';
    const result = document.getElementById('result')
    result.style.display = complete ? 'block' : 'none';
}

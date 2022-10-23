function makeSelection(num) {
    let selection = document.getElementsByClassName("choices-links")[num-1];
    if (selection == null) return;
    document.getElementById("selection-made").innerText = num;
    setTimeout(selection.click(), 150);
}

document.addEventListener("DOMContentLoaded", () => {
    "use strict";

    document.addEventListener("keydown", (event) => {
        const allowedVals = "b123";
        let keyIndex = allowedVals.indexOf(event.key.toLowerCase());

        switch (keyIndex) {
            case 0:
                let header = document.getElementsByTagName('h1')[0]
                if (header != null && (header.innerText == "Top Songs" || header.innerText == "Top Artists" || header.innerText == "Recently Played"))
                    window.location.href = '/profile';
                else 
                    window.location.href = '/index';
                break;
            case -1:
                return;
            default:
                makeSelection(keyIndex);
        }
    });
});
function makeSelection(num) {

}

document.addEventListener("DOMContentLoaded", () => {
    "use strict";

    document.addEventListener("keydown", (event) => {
        const allowedVals = "b123";
        let keyIndex = allowedVals.indexOf(event.key.toLowerCase());

        switch (keyIndex) {
            case 0:
                window.location.href = '/index'
                break;
            case -1:
                return;
            default:
                makeSelection(keyIndex);
        }
    });
});
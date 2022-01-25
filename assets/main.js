function getViewportHeight() {
    return window.innerHeight
}
function getViewportWidth() {
    return window.innerWidth
}


function main_looper() {


    var viewportHeight = getViewportHeight();
    var viewportWidth = getViewportWidth();

    // Set section-divs height
    if (viewportHeight <= 1440) { //    
        var section_height = getViewportHeight() * 0.4;
    } else {
        var section_height = getViewportHeight() * 0.6;
    }
    var sectionDivs = document.getElementsByClassName('section-div');
    for(var i = 0; i < sectionDivs.length; i++) { 
        sectionDivs[i].style.minHeight = `${section_height}px`;
    }

    // Uncomment to populate dev tool area
    try {
        var devinfo = document.getElementById('dev-info');
        var devinfo_text = "Viewport dimensions: " + viewportWidth + " x " + viewportHeight;
        devinfo.textContent = devinfo_text;
        devinfo.style.display = block;
    } catch (error) {
        console.log(error);
    }


    setTimeout(main_looper, 500);

}

main_looper();

function componentToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}
function rgbToHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

let viewportHeight = getViewportHeight() 
function testLooper() {
    try {
        var color_items = document.getElementsByClassName("us-nat-death-num");
        var centerViewport = viewportHeight / 2;
        var centerViewportBot = viewportHeight - 70;
        // console.log(rect.top, rect.right, rect.bottom, rect.left);

        for(var i = 0; i < color_items.length; i++) { 
            var rect = color_items[i].getBoundingClientRect()

            if (rect.top < centerViewportBot && rect.top > 0) {
                var closeVal = parseFloat(centerViewport/rect.top).toFixed(2)
                var colorVal = ((1.0 - closeVal) * 1.11)* 255;
                // var colorVal = 0;
                if (closeVal > 1.0) {
                    colorVal = 0;
                }
                if (closeVal < 0.55 || colorVal > 255) {
                    colorVal = 255;
                }
                
                colorVal = Math.round(colorVal);
                var hexVal = rgbToHex(255,colorVal,colorVal)
                // console.log("Closeness: " + closeVal);
                // console.log("Color value: " + colorVal);
                // console.log("Hex value: " + hexVal);
                color_items[i].style.color = hexVal;
            }

        }

    } catch (error) {
        console.log("Error getting the natNum " + error)
    }

    setTimeout(testLooper, 50);
}
testLooper();

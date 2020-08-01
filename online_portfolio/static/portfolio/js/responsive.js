//==================================For buttons disappearance in smaller screen ====================================//

function myFunction(x) {
    if (x.matches) {
        document.querySelectorAll(".skillButton").forEach(btn => {
            btn.style.display = "none";
        })
    } else {
        document.querySelectorAll(".skillButton").forEach(btn => {
            btn.style.display = "block";
        })
    }
}

var x = window.matchMedia("(max-width: 450px)");
myFunction(x); // Call listener function at run time
x.addListener(myFunction);

//===============================================Adding Swipe Feature==============================================//

var bindEvents = function () {

    var touchstartX = 0;
    var touchstartY = 0;
    var touchendX = 0;
    var touchendY = 0;

    var skillContentDiv = document.getElementById('skillContentDiv');

    skillContentDiv.addEventListener('touchstart', function (event) {
        touchstartX = event.touches[0].clientX;
        touchstartY = event.touches[0].clientY;

    }, false);

    skillContentDiv.addEventListener('touchend', function (event) {
        touchendX = event.changedTouches[0].clientX;
        touchendY = event.changedTouches[0].clientY;

        handleGesure();
    }, false);


    function handleGesure() {
        var swiped = 'swiped: ';
        if (touchendX < touchstartX) {
            // console.log(swiped + 'left!');
            $('.carousel').carousel('next');
        }
        if (touchendX > touchstartX) {
            // console.log(swiped + 'right!');
            $('.carousel').carousel('prev');
        }
        // if (touchendY < touchstartY) {
        //     console.log(swiped + 'up!');
        // }
        // if (touchendY > touchstartY) {
        //     console.log(swiped + 'down!');
        // }
        // if (touchendY == touchstartY) {
        //     alert('tap!');
        // }
    }
}

bindEvents();

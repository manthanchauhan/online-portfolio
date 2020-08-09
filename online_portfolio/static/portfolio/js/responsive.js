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
            $('.carousel').carousel('next');
        }
        if (touchendX > touchstartX) {
            $('.carousel').carousel('prev');
        }
    }
}

bindEvents();

//==========================================Scroll slide stop=========================================================//

$(document).bind('scroll', function (e) {
    console.log("scroll");
    // console.log(e);
});

$('.carousel').carousel({
    interval: false,
});
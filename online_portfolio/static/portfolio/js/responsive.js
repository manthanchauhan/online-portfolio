console.log("respinsive.js")

var addE = function () {
    // console.log("add E function called!!")

    // var list = document.querySelectorAll(".carousel-item");
    // console.log(list);
    // // list.forEach(
    // //     el =>
    // //         el.addEventListener("click", function () {
    // //             console.log("clicked");
    // //         })
    // // )

    // var ele = document.querySelector("#skillContentDiv");
    // console.log(ele);

    // if (ele != null) {
    //     ele.addEventListener("click", function (e) {
    //         console.log("mouseover");
    //         e.stopPropagation();
    //     })
    // }

    // $(document).ready(function () {
    //     $("#skillContentDiv").swiperight(function () {
    //         $(this).carousel('prev');
    //     });
    //     $("#skillContentDiv").swipeleft(function () {
    //         $(this).carousel('next');
    //     });
    // });
}

function myFunction(x) {
    if (x.matches) { // If media query matches
        console.log("matched");

        var btns = document.querySelectorAll(".skillButton");
        console.log(btns);

        btns.forEach(btn => {
            btn.style.display = "none";
        })

    } else {
        document.querySelectorAll(".skillButton").forEach(btn => {
            btn.style.display = "block";
        })
    }
}

var x = window.matchMedia("(max-width: 621px)");
myFunction(x) // Call listener function at run time
x.addListener(myFunction);
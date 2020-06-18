// $(function () {
//   $(".project_image").on("click", function() {
//     $("#myModal").modal("show");
//   });
// });
function getCookie(name) {
  var cookieValue = null;

  if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

$(document).ready(function () {
  $.ajaxSetup({
      beforeSend: function (xhr, settings) {
        var csrftoken = getCookie('csrftoken');
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
  });
});

$("#save_about").on("click", function() {
  var name = $('#name').text();
  var tagline = $('#tagline').text();
  var about = $('#about').text();

  $.ajax({
    url: '/portfolio/update_about/',
    type: 'POST',
    data: {
      'name': name,
      'tagline': tagline,
      'about': about
    },
    dataType: "json",
    complete: function (response) {
      alert(response.responseJSON.message);
    }
  });
});

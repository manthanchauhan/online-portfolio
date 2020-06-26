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

function UploadProjectImage(username, sno) {
  var image = document.getElementById("project_picture" + sno).files;

  if (!image.length) {
    return alert("Upload an image first");
  }

  image = image[0];
  var filename = image.name;
  console.log(filename);

  var upload = new AWS.S3.ManagedUpload({
    params: {
      Bucket: mediaPath + "/projectImages",
      Key: username + "_projectImage_" + sno + "." + filename.split('.').pop(),
      Body: image,
      ACL: "public-read"
    }
  });

  var promise = upload.promise();

  promise.then(function(data) {
    url = "https://" + albumBucketName + ".s3." + bucketRegion + ".amazonaws.com/media/projectImages/" + username + "_projectImage_" + sno + "." + filename.split('.').pop();
    $("#project_thumb" + sno).attr("src", url);
  },
  function(err){
    return alert("There was an error uploading your photo: ", err.message);
  });
};

function UploadProfilePic(username) {
  // console.log("hi");
  var image = document.getElementById("profile_picture").files;

  return alert("Upload an image first");
  if (!image.length) {
  }

  var picture = image[0];
  var filename = picture.name;

  // console.log(filename);

  var upload = new AWS.S3.ManagedUpload({
    params: {
      Bucket: mediaPath,
      Key: username + "_profile_pic." + filename.split('.').pop(),
      Body: picture,
      ACL: "public-read"
    }
  });

  var promise = upload.promise();

  promise.then(
    function(data) {
      console.log(data);
      url = "https://" + albumBucketName + ".s3." + bucketRegion + ".amazonaws.com/media/" + username + "_profile_pic." + filename.split('.').pop();
      $("#profile_pic_alt").attr("src", url);
      // alert("Successfully uploaded photo.");
    },
    function(err) {
      return alert("There was an error uploading your photo: ", err.message);
    }
  );
};

$("#save_about").on("click", function() {
  var name = $('#name').text();
  var tagline = $('#tagline').text();
  var about = $('#about_me').text();
  var profile_pic = $("#profile_pic_alt").attr("src");
  //console.log(tagline);

  $.ajax({
    url: '/portfolio/update_about/',
    type: 'POST',
    data: {
      'name': name,
      'tagline': tagline,
      'about': about,
      'profile_pic': profile_pic,
    },
    dataType: "json",
    complete: function (response) {
      alert(response.responseJSON.message);
    }
  });
});

$("#profile_pic_alt").on("click", function() {
  // console.log("hi");
  $("#profile_picture").click();
});

function uploadProjImage(sno) {
  // console.log(sno);
  $("#project_picture" + sno).click();
};

function save_project(project) {
  id = project.attr("proj_id");
  title = $("#proj_title" + id).text();
  description = $("#proj_desc" + id).text();
  skills = $("#proj_skills" + id).text();
  image = $("#project_thumb" + id).attr("src");
  // console.log(description);

  $.ajax({
    url: '/portfolio/edit_projects/',
    type: 'POST',
    data: {
      'id': id,
      'title': title,
      'description': description,
      'skills': skills,
      'image': image
    },
    dataType: "json",
    complete: function (response) {
      alert(response.responseJSON.message);
    }
  });
};

function delete_project(project) {
  id = project.attr("proj_id");

  if (!confirm('Do you want to delete the project?')) {
    return false;
  }

  project = $("#proj" +  id).hide();

  $.ajax({
    url: '/portfolio/delete_project/',
    type: 'POST',
    data: {
      'id': id,
    },
    dataType: "json",
    complete: function (response) {
      alert(response.responseJSON.message);
    }
  });
  //console.log("hidden");
}

function saveProjLinks(sno){
  liveLink = $("#projLiveLink" + sno).val();
  codeLink = $("#projCodeLink" + sno).val();

  $.ajax({
    url: '/portfolio/edit_projects/',
    type: 'POST',
    data: {
      'id': sno,
      'liveLink': liveLink,
      'codeLink': codeLink,
    },
    dataType: "json",
    complete: function (response) {
      alert(response.responseJSON.message);
    }
  });

  $('#projectLinks' + sno).modal('toggle');
  // console.log(liveLink);
}

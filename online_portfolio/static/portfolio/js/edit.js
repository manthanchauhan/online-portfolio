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

  data = {
    'id': id,
    'title': title,
    'description': description,
    'skills': skills,
    'image': image
  };

  console.log(data);

  $.ajax({
    url: '/portfolio/edit_projects/',
    type: 'POST',
    data: data,
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

function addProject(avatar){
  // console.log("hi");

  $.ajax({
    url: '/portfolio/add_project/',
    type: 'POST',
    data: {},
    dataType: "json",
    error: function (response) {
      alert(response.responseJSON.message);
      return false;
    },
    success: function (response) {
      // console.log(response);
      // console.log(response.responseJSON);
      // console.log(response.project_data);
      project = response.project_data;

      var element = `<div class="modal" tabindex="-1" role="dialog" id="projectLinks` + project.serial_no + `">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Project Links</h5>

              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>

            <div class="modal-body">
              <form>
                <div class="form-group" style="text-align:left;">
                  <label for="projLiveLink` + project.serial_no + `">Live Project Link:</label>
                  <input type="text" class="form-control" id="projLiveLink` + project.serial_no + `">
                </div>

                <div class="form-group" style="text-align:left;">
                  <label for="projCodeLink` + project.serial_no + `">GitHub (VCS) Link:</label>
                  <input type="text" class="form-control" id="projCodeLink` + project.serial_no + `"
                  placeholder="https://github.com/manthanchauhan/online-portfolio">
                </div>
              </form>
            </div>

            <div class="modal-footer">
              <button type="button" class="btn btn-success" onclick="saveProjLinks('` + project.serial_no + `')">Save</button>
            </div>
          </div>
        </div>
      </div>



      <div class="container project" id="proj` + project.serial_no + `">
          <div class="card bg-dark project_card" proj_id="` + project.serial_no + `">
            <div class="card-header project_title" style="color:white;">
              <span class="float-left" id="proj_title-1" contenteditable="true">` + project.title + `</span>
            </div>

            <div class="card-body project_body">
              <div class="project_desc float-left col-lg-7" id="proj_desc` + project.serial_no + `" style="text-align:left;color:white;" contenteditable="true">` + project.description + `</div>
              <div class="project_images float-right col-lg-5" style="text-align:center;">
                <img class="img-fluid img-thumbnail project_image" id="project_thumb` + project.serial_no + `" onclick="uploadProjImage('` + project.serial_no + `')" src="` + project.image + `" alt="">
                <input type="file" id="project_picture` + project.serial_no + `" style="display:none;" onchange="UploadProjectImage('{{request.user.username}}', '` + project.serial_no + `');">
              </div>
            </div>

            <div class="card-footer project-footer" style="color:white; text-align:left;">
              <div class="container col-lg-7 float-left" style="padding:0px;">
                <strong>Skills Used: </strong>
                <span id="proj_skills` + project.serial_no + `" contenteditable="true">` + project.skills + `</span>
              </div>

              <div class="project_links col-lg-5 float-right" style="text-align:right;">
                  <button class="btn btn-success" proj_id="` + project.serial_no + `" onclick="save_project($(this));" type="button" name="button">Save</button>
                  <button class="btn btn-primary" data-toggle="modal" data-target="#projectLinks` + project.serial_no + `" type="button" name="button">Live Project</button>
                  <button class="btn btn-light" data-toggle="modal" data-target="#projectLinks` + project.serial_no + `" type="button" name="button">Code</button>
                  <button class="btn btn-danger" proj_id="` + project.serial_no + `" onclick="delete_project($(this));" type="button" name="button">Delete</button>
              </div>
            </div>
          </div>

      </div>`;
      $("#projectList").append(element);
      $("#addProjectButton").attr("disabled", true);

    }
  });


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

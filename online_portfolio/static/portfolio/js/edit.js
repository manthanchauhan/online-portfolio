let skillMap = {};
let skillOnAPage = 8;
let AddNew = "s5Ryu";
let skillNameLength = 25;

function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
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
            let csrftoken = getCookie('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });

    let titleNameElement = $("#titleName");
    let nameCharCountElement = $("#titleNameCharCount");
    titleNameElement.keyup(function (e) { check_charcount(titleNameElement, nameCharCountElement, 40, "1rem", "1.5rem", "green", e); });

    let taglineTextElement = $("#titleTagline");
    let taglineCharCountElement = $("#titleTaglineCharCount");
    taglineTextElement.keyup(function (e) { check_charcount(taglineTextElement, taglineCharCountElement, 55, "1rem", "1.5rem", "green", e); });

    setSkills();
    fillSkillCarousel();

    $(".skillCell").each(function () {
        let element = $(this);
        resize_skill_names(element);
    });
});

function UploadProjectImage(username, sno) {
    let image = document.getElementById("project_picture" + sno).files;

    if (!image.length) {
        return alert("Upload an image first");
    }

    image = image[0];
    let filename = image.name;

    let upload = new AWS.S3.ManagedUpload({
        params: {
            Bucket: mediaPath + "/projectImages",
            Key: username + "_projectImage_" + sno + "." + filename.split('.').pop(),
            Body: image,
            ACL: "public-read"
        }
    });

    let promise = upload.promise();

    promise.then(function (data) {
        let url = "https://" + albumBucketName + ".s3." + bucketRegion + ".amazonaws.com/media/projectImages/" + username + "_projectImage_" + sno + "." + filename.split('.').pop();
        $("#project_thumb" + sno).attr("src", url);
    },
        function (err) {
            return alert("There was an error uploading your photo!!");
        });
}

function UploadProfilePic(username) {
    let image = document.getElementById("profile_picture").files;

    if (!image.length) {
        return alert("Upload an image first");
    }

    let picture = image[0];
    let filename = picture.name;


    let upload = new AWS.S3.ManagedUpload({
        params: {
            Bucket: mediaPath,
            Key: username + "_profile_pic." + filename.split('.').pop(),
            Body: picture,
            ACL: "public-read"
        }
    });

    let promise = upload.promise();

    promise.then(
        function (data) {
            let url = "https://" + albumBucketName + ".s3." + bucketRegion + ".amazonaws.com/media/" + username + "_profile_pic." + filename.split('.').pop();
            $("#profile_pic_alt").attr("src", url);
            updateAboutData(null, null, url, null);
        },
        function (err) {
            return alert("There was an error uploading your photo: " + err.message);
        }
    );
}

$("#profile_pic_alt").on("click", function () {
    $("#profile_picture").click();
});

function uploadProjImage(sno) {
    $("#project_picture" + sno).click();
}

function save_project(project) {
    let id = project.attr("proj_id");
    let title = $("#proj_title" + id).text();
    let description = $("#proj_desc" + id).summernote('code');
    let project_skills = $("#proj_skills" + id).text();
    let image = $("#project_thumb" + id).attr("src");

    let data = {
        'id': id,
        'title': title,
        'description': description,
        'skills': project_skills,
        'image': image
    };


    $.ajax({
        url: '/portfolio/edit_projects/',
        type: 'POST',
        data: data,
        dataType: "json",
        complete: function (response) {
            alert(response.responseJSON.message);
        }
    });
}

function delete_project(project) {
    let id = project.attr("proj_id");

    if (!confirm('Do you want to delete the project?')) {
        return false;
    }

    project = $("#proj" + id).hide();

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
}

function addProject(avatar) {

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

            let project = response.project_data;

            let element = `<div class="modal" tabindex="-1" role="dialog" id="projectLinks` + project.serial_no + `">
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

function saveProjLinks(sno) {
    let liveLink = $("#projLiveLink" + sno).val();
    let codeLink = $("#projCodeLink" + sno).val();

    $.ajax({
        url: edit_project_url,
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
}

function exportPortfolio() {
    if (!confirm("Do you want to export your new portfolio?")) {
        return false;
    }

    $.ajax({
        url: export_url,
        type: 'POST',
        data: {},
        dataType: "json",
        success: function (response) {
            $("#portLink").attr("value", response.url);
            $("#portLink2").attr("href", response.url);
            $("#portfolioLink").show();
        },
        error: function (response) {
            alert(response);
        }
    });
}

function closePortLink() {
    $("#portfolioLink").hide();
}

function toSummernote(element, type) {
    let content = $(element).innerHTML;

    if (type === "aboutOrange") {
        $(element).summernote({
            toolbar: [
                ['style', ['bold', 'italic', 'underline', 'clear']],
            ],
            code: content,
        });
    }

    else if (type === 'projectDesc') {
        $(element).summernote({
            toolbar: [
                ['style', ['style']],
                ['font', ['bold', 'underline', 'clear']],
                ['fontname', ['fontname']],
                ['color', ['color']],
                ['para', ['ul', 'ol', 'paragraph']]
            ],
            code: content,
        });
    }
}

function updateTagline() {
    let tag_line = document.getElementById("titleTagline").innerText;
    let len = tag_line.length;
    let max = 55;

    if (len > max) {
        return;
    }

    $("#titleTaglineCharCount").hide();
    updateAboutData(null, tag_line, null, null);
}

function updateName() {
    let new_name = document.getElementById("titleName").innerText;
    let len = new_name.length;
    let max = 40;

    if (len > max) {
        return;
    }

    $("#titleNameCharCount").hide();

    updateAboutData(new_name, null, null, null);
}

function showErrorModal(data, reason) {
    let errorModal = $("#errorModal");
    errorModal.show();
    errorModal.find(".modal-title").text(reason);

    let html = '';
    for (let key in data) {
        html = html + `<h7>Field '` + key + `' has the following error(s):</h7>`;
        html = html + `<ul>`;

        for (let n = 0; n < data[key].length; n++) {
            html = html + `<li>` + data[key][n] + `</li>`;
        }

        html = html + `</ul><br>`;
    }

    errorModal.find(".modal-body").html(html);
}

function closeErrorModal() {
    $("#errorModal").hide();
}

function updateAboutData(name, tag_line, profile_pic, about) {
    let data = { "name": name, "tag_line": tag_line, "profile_pic": profile_pic, "about": about }

    $.ajax({
        url: update_about_url,
        type: 'POST',
        data: data,
        dataType: "json",
        success: function (data, textStatus, response) {
            // alert(response.statusText);
        },
        error: function (data) {
            showErrorModal(data.responseJSON, data.statusText);
        }
    });
}

function check_charcount(textElement, charCountElement, max, fontSize, maxExceedFontSize, color, e) {
    let len = textElement.text().length;

    charCountElement.css("font-size", fontSize);
    charCountElement.text(len + "/" + max);
    charCountElement.css("color", color);

    if (len > max) {
        charCountElement.css("color", "red");
        charCountElement.css("font-size", maxExceedFontSize);
    }

}

function showCharCount(element, max, isID = true) {
    let len = $(element).text().length;
    let charCountElement = $("#" + element.id + "CharCount");
    charCountElement.show();
    charCountElement.text(len + "/" + max);
}

function aboutOrangeFocusIn(element, max) {
    let content = $(element).innerHTML;

    $(element).summernote({
        codemirror: { "theme": "ambiance" },
        fontNames: ['Arial', 'Arial Black', 'Comic Sans MS', 'Courier New', 'Open Sans'],
        toolbar: [
            ['fontsize', ['fontsize']],
            ['fontname', ['fontname']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']]
        ],
        code: content,
    });

    let aboutDiv = $("#aboutDiv");

    aboutDiv.find(".note-editable").css({
        "opacity": "86%",
        "font-family": "'Open Sans', sans-serif",
        "width": "90%",
        "min-height": "450px",
        "color": "black",
        "padding": "30px 5% 50px 15%",
        "border-radius": "0 25px 25px 0",
        "background": "#ececec",
        "font-size": "1.6rem",
    });

    aboutDiv.find(".note-toolbar").css({
        "text-align": "center",
    });

    aboutDiv.find(".note-toolbar").find(".note-btn").css({
        "background": "#ff8080",
    });

    let aboutTextElement = aboutDiv.find(".note-editable");
    let aboutCharCount = $("#aboutOrangeCharCount")
    aboutTextElement.keyup(function (e) { check_charcount(aboutTextElement, aboutCharCount, 500, "1.5rem", "1.7rem", e); });

    aboutDiv.find(".note-editor").focusout(function () {
        updateAbout();
    });

    showCharCount(element, max);
}

function updateAbout() {
    let aboutHtml = $("#aboutOrange").summernote('code');
    let max = 2000;

    if (aboutHtml.length >= max) {
        return;
    }

    updateAboutData(null, null, null, aboutHtml);
}


$('#carouselExampleControls').on('slid.bs.carousel', function () {
    $(".skillCell").each(function () {
        let element = $(this);
        resize_skill_names(element);
    });
})

function resize_skill_names(element) {
    let child = element.find(".skillName").first();

    if ((child.height() > element.height()) || (child.width() > element.width())) {
        let fontsize = child.css("font-size");
        child.css("font-size", parseFloat(fontsize) - 1);
        resize_skill_names(element);
    }
}

function setSkills() {
    skillMap = skills;

    for (let category in skillMap) {
        skillMap[category].push(AddNew);
    }
}

function fillSkillCarousel() {
    let slideIndx = 0;
    let buttonUrl = CarouselButton;

    for (let category in skillMap) {

        for (let i = 0; i < skillMap[category].length; i += skillOnAPage) {

            let skills = skillMap[category].slice(i, i + skillOnAPage);

            let carouselSlide = `<div class="carousel-item `;

            if (slideIndx === 0) {
                carouselSlide += `active`;
            }

            carouselSlide += `">
                <a class="carousel-control-prev skillButton" href="#carouselExampleControls" role="button"
                    data-slide="prev">
                    <img src="` + buttonUrl + `">
                </a>

                <div class="sectionHeadingDiv">
                    <h2>` + category + `</h2>
                </div>
                <div id="skillDataContainer">
                    <div class="skillData">`;

            for (let j = 0; j < skills.length; j++) {
                let skill_index = i+j;
                let text = `<p class="skillName">` + skills[j] + `</p> 
                <img src="` + DeleteButtonPath + `" alt ="X" class="skillCross"  category="` + category + `" onclick="skillRemove(this, ` + skill_index + `)">`;

                if (skills[j] === AddNew) {
                    text = `<img src="` + AddButtonPath + `"alt="Add Skill" class="add-new-skill" category="` + category + `" onclick="showSkillNameInput(this);">

                    <p class="newSkillInput skillName" contenteditable="true" onfocusin="showSkillNameCharCount(this,25,'1rem');" carousel-index="` + slideIndx + `" id="newSkillNameInput" category="` + category + `" onfocusout="updateSkillName(this,event);"></p>
                    <small class="skillNameCharCount"></small>`;
                }

                let skillCell = `<div class="skillCellContainer">
                            <div class="skillCell float-left" onmouseover="skillCellHover(this);" onmouseout ="skillCellHoverOut(this);">
                               `+ text + `
                            </div>
                        </div>`;

                carouselSlide += skillCell;
            }

            carouselSlide += `</div>
                </div>
                <a class="skillButton carousel-control-next" href="#carouselExampleControls" role="button"
                    data-slide="next" style="transform: rotate(180deg);">
                    <img src="` + buttonUrl + `">
                </a>
            </div>`;

            $("#skillContentDiv").append(carouselSlide);
            slideIndx += 1;
        }
    }
}

function showSkillNameInput(element) {
    let spanEle = element.parentElement.querySelector(".newSkillInput");
    spanEle.style.display = "block";
    $(element).hide();

    let ele = $(spanEle);
    let skillCharCountElement = $(element).parent().find(".skillNameCharCount");
    ele.focus();
    ele.keyup(function (e) { check_charcount(ele, skillCharCountElement, 25, "1rem", "1rem", "white", e); });
}

function showSkillNameCharCount(element, max, fontSize) {
    let len = $(element).text().length;

    let skillCharCountElement = $(element).parent().find(".skillNameCharCount");

    skillCharCountElement.show();
    skillCharCountElement.text(len + "/" + max);
}


function updateSkillName(ele, event) {
    let new_skill = ele.innerText;
    let len = new_skill.length;


    if (len > skillNameLength || len === 0) {
        $(ele).parent().find(".add-new-skill").show();
        $(ele).parent().find(".skillNameCharCount").hide();
        $(ele).parent().find(".add-new-skill").css('margin-top', '40%');

        if (len !== 0) {
            alert("Skill name is too long!!");
            $(ele).empty();
        }
        return false;
    }
    else {

        $(ele).parent().find(".skillNameCharCount").hide();

        let category = $(ele).attr("category");
        let slideIndex = $(ele).attr("carousel-index");

        let already_exists = false;

        for (let cat in skillMap) {
            for (let i = 0; i < skillMap[cat].length; i++) {
                if (skillMap[cat][i] === new_skill) {
                    already_exists = true;
                }
            }
        }

        if (already_exists) {
            alert("This skill already exists!!");
            $(ele).parent().find(".add-new-skill").show();
            $(ele).parent().find(".skillNameCharCount").hide();
            $(ele).parent().find(".add-new-skill").css('margin-top', '40%');
            $(ele).empty();
            return false;
        }

        $.ajax({
            url: add_skill_url,
            type: "POST",
            data: { "skill_name": new_skill, "category": category },
            dataType: "json",
            success: function () {
                skillMap[category].pop();
                skillMap[category].push(new_skill);
                skillMap[category].push(AddNew);

                $("#skillContentDiv").empty();
                fillSkillCarousel();

                $("#carouselExampleControls").carousel(parseInt(slideIndex));
            },
            error: function (data) {
                showErrorModal(data.responseJSON, data.statusText);
            },
        });
    }

}

function skillCellHover(element) {
    const delete_btn = element.querySelector('.skillCross');
    if (delete_btn) delete_btn.style.display = "block";
}

function skillCellHoverOut(element) {
    const delete_btn = element.querySelector('.skillCross');
    if (delete_btn) delete_btn.style.display = "none";
}

function skillRemove(ele, index) {

    let category = $(ele).attr("category");

    let should_delete = confirm("Are you sure you want to delete this skill ?");
    if (should_delete === true) {
        console.log(skillMap[category][index]);
        // Add ajax call here...
    }
}

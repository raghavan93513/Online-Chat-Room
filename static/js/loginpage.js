// js to make login request

// after page is loaded
$(document).ready(function () {
  //  add listener to form submit
  console.log("loginpage.js loaded");
  $("#createaccountform").submit(function (event) {
    // prevent default submit action
    event.preventDefault();
    // get form data
    var formData = {
      display_name: $("#usernamecreate").val(),
      email: $("#emailcreate").val(),
      password: $("#passwordcreate").val(),
    };
    // make ajax request with data as a json object
    $.ajax({
      type: "POST",
      url: "/create_user",
      data: JSON.stringify(formData),
      dataType: "json",
      contentType: "application/json",
      encode: true,
    })
      .done(function (data) {
        // if success, data contains the user object, transfer data to cookie
        // if the first word is "Error", then there was an error
        if (data.split(":")[0] != "ERROR") {
          document.cookie = "token=" + data;
          // redirect to home page
          window.location.href = "/";
        } else {
          // if error, display error
          alert(data);
          // clear all fields
          $("#usernamecreate").val("");
          $("#emailcreate").val("");
          $("#passwordcreate").val("");
        }
      })
      .fail(function (data) {
        // if fail, display error
        alert("Error: " + data.responseText);
      });
  });

  // add listener to form submit of loginform
  $("#loginform").submit(function (event) {
    // prevent default submit action
    event.preventDefault();
    // get form data
    var formData = {
      email: $("#emaillogin").val(),
      password: $("#passwordlogin").val(),
    };
    // make ajax request with data as a json object
    $.ajax({
      type: "POST",
      url: "/login",
      data: JSON.stringify(formData),
      dataType: "json",
      contentType: "application/json",
      encode: true,
    })
      .done(function (data) {
        // if success, data contains the user object, transfer data to cookie
        // if the first word is "Error", then there was an error
        if (data.split(":")[0] != "ERROR") {
          document.cookie = "token=" + data;
          // redirect to home page
          window.location.href = "/";
        } else {
          // if error, display error
          alert(data);
          // clear all fields
          $("#email").val("");
          $("#password").val("");
        }
      })
      .fail(function (data) {
        // if fail, display error
        alert("Error: " + data.responseText);
      });
  });
});

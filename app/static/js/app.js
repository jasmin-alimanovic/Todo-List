//static/js/app.js

function show_profile_info(firstName, lastName, email, username) {
  showData = document.getElementById("show-data");
  showData.innerHTML = "";
  htmlCode = ` <ul class="info-data">
        <li>First name: ${firstName}</li>
        <li>Last name: ${lastName}</li>
        <li>Username: ${username}</li>
        <li>E-mail: ${email}</li>
    </ul>`;
  showData.innerHTML += htmlCode;
}

function change_password() {
  showData = document.getElementById("show-data");
  showData.innerHTML = "";
  htmlCode = `  <form class="change-pass" action="changepassword" method="post">
    <label for="oldpassword">Enter your current password</label>
    <input class="form-control" type="password" name="oldpassword" required />
    <br/>
    <label for="newpassword">Enter your new password</label>
    <input class="form-control" type="password" name="newpassword" required />
    <br/>
    <label for="repeatpassword">Enter again new password</label>
    <input oninput="validatePass()" class="form-control" type="password" name="repeatpassword" required />
    <p class="repass"></p>
    <input name="update-pass" class="btn-ch-pass form-control" type="submit" value="Save"/>
  </form>`;
  showData.innerHTML += htmlCode;
}

function validatePass() {
  newpass = document.getElementsByName("newpassword")[0].value;
  repass = document.getElementsByName("repeatpassword")[0].value;
  error = document.getElementsByClassName("repass")[0];
  btn_ch_pass = document.querySelector(".btn-ch-pass");
  //   btn_ch_pass.style.pointerEvents = "all";
  //   btn_ch_pass.style.cursor = "none";
  error.innerHTML = "";
  if (newpass != repass) {
    error.innerHTML = "Passwords do not match";
    error.style.color = "red";
    // btn_ch_pass.style.pointerEvents = "none";
  }
}

//button href

function href(loc) {
  location.href = loc;
}

//fetch users

function fec() {
  fetch("/admin/fetch")
    .then((response) => response.json())
    .then((data) => console.log(data));
}

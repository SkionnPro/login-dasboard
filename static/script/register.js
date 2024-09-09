"use strict";

//  function to enable "Submit button" on password match
function validatePasswords(){
  console.log("inside validatePassword function");
  const password = document.getElementById('password').value;
  const confirmPassword = document.getElementById('confirmPassword').value;
  const registerButton = document.getElementById('registerBtn');

  //  check if passwords match
  if (password && confirmPassword && password === confirmPassword) {
    registerButton.disabled = false; // Enable the button
  } else {
    registerButton.disabled = true;  // Disable the button
  }
}

document.addEventListener('DOMContentLoaded', function () {
  console.log("dom content loaded");
  // Attach input event listeners for password fields
  document.getElementById('password').addEventListener('input', validatePasswords);
  document.getElementById('confirmPassword').addEventListener('input', validatePasswords);
  console.log("event listeners added");

  validatePasswords();
  console.log("called validatePassword function");
});

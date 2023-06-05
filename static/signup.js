function genDays() {
    for (var i = 1; i <= 31; i ++) {
        document.write('<option value="' + i + '">' + i + '</option>');
    }
}

function genMonths() {

    var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

    for (var i = 0; i < 12; i ++) {
        document.write('<option value="' + months[i] + '">' + months[i] + '</option>');
    }
}

function genYears() {

    var currentYear = new Date().getFullYear();

    for (var i = currentYear; i >= currentYear - 100; i --) {
        document.write('<option value="' + i + '">' + i + '</option>');
    }  
}

function checkExistance(field) {

    var element = document.getElementById(field)
    var val = document.getElementById(field).value;

    $.ajax(
        {
            url: '/datavalidation',
            method: "GET",
            dataType: "json",
            data: {
                [field] : val
            },
            success: function (res) {

                if (res['status'] === 'Already exists') {
                    element.setAttribute("data-validation", true);
                    alert(field + " already exists!");
                }
                else {
                    element.setAttribute("data-validation", false);
                }

            }
        }
    );

}

function inputValidation() {

    var user = document.getElementById("username");
    var email = document.getElementById("email");
    var password = document.getElementById("form__input-pass");
    var password2 = document.getElementById("form__input-pass2");

    if (user.getAttribute("data-validation") === "true" || email.getAttribute("data-validation") === "true" || !passwordStrength("form__input-pass") || password.value !== password2.value) {
        if (password.value !== password2.value) {
            alert("Passwords are different!");
        }
        return false;
    }
    else {
        return true;
    }

}

function showEye() {
    const password = document.getElementById("form__input-pass");
    const password2 = document.getElementById("form__input-pass2");
    const input = password.value.trim();
    const input2 = password2.value.trim();
    const eye = document.getElementById('form__input-eye');

    if (input !== '' || input2 !== '') {
        eye.style.visibility = 'visible';
    }
    else {
        eye.style.visibility = 'hidden';
        password.type = 'password';
        password2.type = 'password';
        eye.style.background = 'url(/static/eye.svg)'
    }
}

function showPassword() {
    const password = document.getElementById('form__input-pass');
    const password2 = document.getElementById('form__input-pass2');
    const eye = document.getElementById('form__input-eye');

    if (password.type === 'password') {

        password.type = 'text';
        password2.type = 'text';
        eye.style.background = 'url(/static/eye_crossed.svg)'
    }
    else {

        password.type = 'password';
        password2.type = 'password';
        eye.style.background = 'url(/static/eye.svg)'
    }
}

function passwordStrength(password_field_name) {
    /* Returns true if the password is strong enough */
    var password =  document.getElementById(password_field_name).value;

    /* Check if the password is long enough */
    if (password.length < 8) {
        return false;
    }
    /* Check if the string has a digit */
    if (!/\d/.test(password)) {
        return false;
    }
    /* Special character */
    if (!/[^a-zA-Z0-9]/.test(password)) {
        return false;
    }
    /* Check if there's a uppercase letter */
    if (!/[A-Z]/.test(password)) {
        return false;
    }
    /* Check if there's a lowercase letter */
    if (!/[a-z]/.test(password)) {
        return false;
    }

    return true;
}
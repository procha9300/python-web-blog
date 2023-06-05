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
                    element.setAttribute("data-validation", false);
                }
                else {
                    element.setAttribute("data-validation", true);
                    alert(field + " does not exist!");
                }

            }
        }
    );

}


function inputValidation() {

    var user = document.getElementById("username");

    if (user.getAttribute("data-validation") === "true") {
        /* Não deixa submeter */
        return false;
    }
    else {
        return true;
    }

}

function newPwValidation() {
    var password = document.getElementById("form__input-pass").value;
    var password2 = document.getElementById("form__input-pass2").value;

    if (password !== password2) {
        /* Não deixa submeter */
        alert("Passwords do not match.");
        return false;
    }
    if (!passwordStrength("form__input-pass")) {
        alert("Password not stromg enough!");
        return false;
    }
    return true;
}

function showEye() {

    const password_field = document.getElementById('form__input-pass');
    const input = password_field.value.trim();
    const password_field2 = document.getElementById('form__input-pass2');
    const input2 = password_field2.value.trim();
    const eye = document.getElementById('form__input-eye');

    if (input !== '' || input2 !== '') {
        eye.style.visibility = 'visible';
    }
    else {
        eye.style.visibility = 'hidden';
        password_field.type = 'password';
        password_field2.type = 'password';
        eye.style.background = 'url(/static/eye.svg)'
    }
}

function showPassword(){
    const password_field = document.getElementById('form__input-pass');
    const password_field2 = document.getElementById('form__input-pass2');
    const eye = document.getElementById('form__input-eye');

    if (password_field2.type === 'password') {
        password_field.type = 'text';
        password_field2.type = 'text';
        eye.style.background = 'url(/static/eye_crossed.svg)'
    }
    else {
        password_field.type = 'password';
        password_field2.type = 'password';
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
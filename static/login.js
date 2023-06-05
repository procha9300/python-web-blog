function showPassword(){

    const password_field = document.getElementById('form__input-pass');
    const eye = document.getElementById('form__input-eye');

    if (password_field.type === 'password') {

        password_field.type = 'text';
        eye.style.background = 'url(/static/eye_crossed.svg)'
    }
    else {

        password_field.type = 'password';
        eye.style.background = 'url(/static/eye.svg)'
    }

}

function showEye() {

    const password_field = document.getElementById('form__input-pass');
    const input = password_field.value.trim();
    const eye = document.getElementById('form__input-eye');

    if (input !== '') {

        eye.style.visibility = 'visible';
    }
    else {

        eye.style.visibility = 'hidden';
        password_field.type = 'password';
        eye.style.background = 'url(/static/eye.svg)'
    }
}
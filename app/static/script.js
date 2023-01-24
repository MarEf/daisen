document.getElementById("password_toggle").addEventListener("click", function () { togglePassword() })

function togglePassword() {
    let toggle = document.getElementById("password_toggle");
    let password_field = document.getElementById("password");
    if (toggle.checked) {
        password_field.type = 'text';
    }
    else {
        password_field.type = 'password';
    }
}
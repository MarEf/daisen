if (document.getElementById("password_toggle")) {
    document.getElementById("password_toggle").addEventListener("click", function () { togglePassword() })
}

function togglePassword() {
    let toggle = document.getElementById("password_toggle");
    const passwords = document.querySelectorAll("[id$='password']");

    for (let i = 0; i < passwords.length; i++) {
        if (toggle.checked) {
            passwords[i].type = 'text';
        }
        else {
            passwords[i].type = 'password';
        }
    }
}


function selectAll(checkbox, toSelect) {
    const boxes = document.querySelectorAll("[name^=" + toSelect + "]");

    for (let i = 0; i < boxes.length; i++) {
        if (checkbox.checked) {
            boxes[i].checked = true;
        } else {
            boxes[i].checked = false;
        }
    }
}
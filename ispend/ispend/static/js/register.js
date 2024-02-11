console.log('register.js working')

const usernameField = document.querySelector('#usernameField');
const usernameMsg = document.querySelector('.usernameMsg');

usernameField.addEventListener('focusout', (e) => {
    const usernameVal = e.target.value;

    usernameField.classList.remove('is-invalid');
    usernameMsg.style.display = 'none';


    if (usernameVal.length > 0) {
        fetch('/accounts/validate-username', {
            body: JSON.stringify({ username: usernameVal }),
            method: 'POST'
        }).then(response => response.json().then(data => {
            console.log('data', data);
            if (data.username_error) {
                usernameField.classList.add('is-invalid');
                usernameMsg.style.display = 'block';
                usernameMsg.innerHTML = `<p>${data.username_error}</p>`;
            }
        }));
    }
    
});

const emailField = document.querySelector('#emailField');
const emailMsg = document.querySelector('.emailMsg');

emailField.addEventListener('focusout', (e) => {
    const emailVal = e.target.value;

    emailField.classList.remove('is-invalid');
    emailMsg.style.display = 'none';


    if (emailVal.length > 0) {
        fetch('/accounts/validate-email', {
            body: JSON.stringify({ email: emailVal }),
            method: 'POST'
        }).then(response => response.json().then(data => {
            console.log('data', data);
            if (data.email_error) {
                emailField.classList.add('is-invalid');
                emailMsg.style.display = 'block';
                emailMsg.innerHTML = `<p>${data.email_error}</p>`;
            }
        }));
    }
    
});

const passwordField = document.querySelector("#passwordField");
const showPasswordToggle = document.querySelector('.showPasswordToggle');
const handleTogleInput = (e) => {
    if (showPasswordToggle.textContent === 'SHOW') {
        showPasswordToggle.textContent = "HIDE";
        passwordField.setAttribute("type", "text");
    }
    else {
        showPasswordToggle.textContent = "SHOW";
        passwordField.setAttribute("type", "password");
    }
}
showPasswordToggle.addEventListener('click', handleTogleInput);

const submitBtn = document.querySelector(".submit-btn");
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
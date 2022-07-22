function setFormMessage(formElement, type, message) {
	const messageElement = formElement.querySelector(".form__message");

	messageElement.textContent = message;
	messageElement.classList.remove("form__message--success", "form__message--success")
	messageElement.classList.add(`form__message--${type}`)
}

signupForm = document.getElementById("createAccount");
signupForm.addEventListener("submit", (event) => {
	username = document.getElementById("username");
	email = document.getElementById("email");
	password1 = document.getElementById("password1");
	password2 = document.getElementById("password2");

	if(password1 != password2) {
		event.preventDefault();
	}
})

document.addEventListener("DOMContentLoaded", () => {
	const loginForm = document.querySelector("#login")
	const signupForm = document.querySelector("#signup")
	loginForm.addEventListener("submit", e=> {
		
		setFormMessage(loginForm, 'error', "Invalid username/password combination")
	});
});

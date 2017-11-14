// export function validateEmail(email) {
//     const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
//     return re.test(email);
// }

//checks to see if username and password fields are non empty with a regular expression
export function validateUserName(userName) {
    const re = "^\\s+$";
    return re.test(userName);
}

export function validatePassword(password) {
    const re = "^\\s+$";
    return re.text(password);
}
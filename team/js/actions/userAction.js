export function userLogin(userName, firstName, lastName){
    return {
        type:'USER_LOGIN',
        userName,
        firstName,
        lastName
    }
}

export function userLogout(){
    return {
        type: 'USER_LOGOUT',
    }
}
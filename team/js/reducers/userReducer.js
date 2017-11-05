initialState = {
    userName: "",
    fistName: "",
    lastName: "",
    loggedIn: false
}

export default function testReducer(userData = initialState, action) {
    switch(action.type){
        case 'USER_LOGIN':
            return [
                ...state,
                {
                    userName: action.userName,
                    firstName: action.firstName,
                    lastName: action.lastName,
                    loggedIn: true
                }
            ]
            break;
        case 'USER_LOGOUT':
            return [
                ...state,
                {
                    userName: "",
                    firstName: "",
                    lastName: "",
                    loggedIn: false
                }
            ]
        default :
            return userData;
            break;
    }
}
import React ,{Component} from 'react'
import userLogin from '../components/userLogin'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import testActions from '../actions/testAction'
//import * as userActions from '../actions/userAction'

function mapStateToProps(store) {
    return{
        // userName
        //rememberMe
    }
}

function mapDispatchToProps(dispatch) {
    return {
        actions: bindActionCreators(testActions/*userActions*/, dispatch)
    }
}


let userLoginContainer=connect(
    mapStateToProps,
    mapDispatchToProps
)(userLogin);

export default userLoginContainer;
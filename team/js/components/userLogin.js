import React from 'react';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import Paper from 'material-ui/Paper';
import { browserHistory } from 'react-router';
import { validateUserName, validatePassword } from '../utils/validations';

const style = {
    marginTop: 50,
    paddingBottom: 50,
    paddingTop: 25,
    width: '100%',
    textAlign: 'center',
    display: 'inline-block',
};

export default class userLogin extends React.Component {

    constructor(props) {
        super(props);
        const redirectRoute = '/login';
        this.state = {
            userName: '',
            password: '',
            userNameErrorText: null,
            passwordErrorText: null,
            redirectTo: '/graphs',
            disabled: true,
        };
    }
    changeValue(e, type) {
        if (type == 'userName'){
            this.setState({
                userName: e
            })
        }
        else{
            this.setState({
                //will need to change this to encrypted password
                password: e
            })
        }
    }
    login(e) {
        let userNameIsValid = validatePassword(this.state.userName);
        let passwordIsValid = validatePassword(this.state.password);
        if(!userNameIsValid){
            this.setState({
                userNameErrorText: "Please enter your user name."
            })
        }
        else if (!passwordIsValid){
            this.setState({
                passwordErrorText: "Please enter your password.npm"
            })
        }
        else {
            browserHistory.push('/graphs');
            //this.props.actions.loginUser();
        }
    }
    render() {
        return (
            <div className="col-md-6 col-md-offset-3" onKeyPress={(e) => this._handleKeyPress(e)}>
                <Paper style={style}>
                    <form role="form">
                        <div className="text-center">
                            <h2>Login to view protected content!</h2>
                            {
                                this.props.statusText &&
                                <div className="alert alert-info">
                                    {this.props.statusText}
                                </div>
                            }

                            <div className="col-md-12">
                                <TextField
                                    hintText="User Name"
                                    type="userName"
                                    errorText={this.state.userNameErrorText}
                                    onChange={(e) => this.changeValue(e, 'userName')}
                                />
                            </div>
                            <div className="col-md-12">
                                <TextField
                                    hintText="Password"
                                    type="password"
                                    errorText={this.state.passwordErrorText}
                                    onChange={(e) => this.changeValue(e, 'password')}
                                />
                            </div>

                            <RaisedButton
                                disabled={this.state.disabled}
                                style={{ marginTop: 50 }}
                                label="Submit"
                                onClick={(e) => this.login(e)}
                            />

                        </div>
                    </form>
                </Paper>

            </div>
        );

    }
}

import React,{Component} from 'react'

export default class Test extends Component{
	componentDidMount(){
		this.props.actions.testAction()
	}
	render(){
        /*
		return(
				<div>{this.props.data}</div>
                
			)
        */
        console.log("Test component has rendered")
		return(
            <div>HELLO WORLD</div>
        )
	}
}

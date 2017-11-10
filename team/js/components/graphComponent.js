import React,{Component} from 'react'
import graphPage from '../../templates/layouts/base.html'

export default class GraphCointainer extends Component
    render(){
        return(
            <div dangerouslySetInnerHTML={graphPage} />
        )
    }
}
import * as React from 'react';

import { Socket } from './Socket';

export class Content extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'arrowDir': '',
        };
         
    }
    
    componentDidMount() {
        
        
        Socket.on('arrow', (data) => {
            this.setState({
                'arrowDir': data['arrowDir'],
                
            });
            // console.log(this.state.arrowDir);
        })
        
    }
    
    render() {
        var imgSrc = "../static/arrows/"
        imgSrc = imgSrc.concat(this.state.arrowDir)
        imgSrc = imgSrc.concat(".png")
        let image = <img id="arrow" src={imgSrc} />
        return (
            <div>
                <h1>Hello from React!!! w/ compass</h1>
                {image}
                
            </div>
        );
    }
}

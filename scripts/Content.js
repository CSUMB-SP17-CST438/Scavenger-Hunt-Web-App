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
        let image = null;
        if (this.state.arrowDir == ''){
            image = <img id="arrow" />
        } else {
            var imgSrc = "../static/arrows/";
            imgSrc = imgSrc.concat(this.state.arrowDir);
            imgSrc = imgSrc.concat(".png");
            image = <img id="arrow" src={imgSrc} />;
        }
        
        return (
            <div>
                
                
                
               {image}
                
            </div>
        );
    }
}

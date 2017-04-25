import * as React from 'react';

import { Socket } from './Socket';

export class Facebook extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            
        };
         
    }
    
    componentDidMount() {
        
        
        
        
    }
    
    render() {
        
        return (
            <div>
                
                <div
                    className="fb-login-button"
                    data-max-rows="1"
                    data-size="medium"
                    data-show-faces="false"
                    data-auto-logout-link="true">
                </div>


                
                
            </div>
        );
    }
}

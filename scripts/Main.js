import * as React from 'react';
import * as ReactDOM from 'react-dom';

import { Content } from './Content';
import { Facebook } from './Facebook';

ReactDOM.render(<Content />, document.getElementById('content'));
ReactDOM.render(<Facebook />, document.getElementById('facebook'));
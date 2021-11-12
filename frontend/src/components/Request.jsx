import { useState } from 'react';
import VisDisplay from './VisDisplay';
import TextBox from './TextBox';

export default function Request(props) {
    const axios = require('axios').default;
    const [obsPlot, setObsPlot] = useState('')
    const [obsPath, setObsPath] = useState('')

    function handleRequest() {
        console.log('handling request...')
        axios.post('/api/candidates', {
            n: 1,
            obsPath: obsPath
        })
            .then((response) => {
                setObsPlot(response.data['obs'])
                console.log('Success.')
            })
            .catch((err) => console.log(err))
    }

    return <>
    <TextBox text='Observed data' change={setObsPath}></TextBox> 
    <button onClick={handleRequest}>Fetch candidates</button>
    <VisDisplay data={obsPlot}></VisDisplay>
    </>
}
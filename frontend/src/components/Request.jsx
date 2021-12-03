import { useState } from 'react';
import VisDisplay from './VisDisplay';
import TextBox from './TextBox';
import ReactLoading from 'react-loading'
import StatusBar from './StatusBar';
import SelectMenu from './SelectMenu';

var applyLog = false 

export default function Request(props) {
    const setApplyLog = (str) => {
        if (str === 'Yes') {
            applyLog = true 
        } else if (str === 'No') {
            applyLog = false 
        } else {
            return 
        }
    };
    const axios = require('axios').default;
    const [obsPath, setObsPath] = useState('');
    const [n, setN] = useState("1");
    const [data, setData] = useState({obs: [], sims: []});
    const [status, setStatus] = useState('idle');
    const [error, setError] = useState(null);

    function handleRequest() {
        console.log('handling request...')
        setStatus('loading');
        setError(null);
        axios.get('/api/candidates/', {
            params: {
                n: parseInt(n),
                obsPath: obsPath,
                applyLog: applyLog
            }
        })
            .then((response) => {
                props.setData({obs: response.data['obs'], sims: response.data['sims']})
                console.log(response.data['obs'])
                console.log(response.data['sims'])
                setStatus('success');
                console.log('Success.')
            })
            .catch((error) => {
                if (error.response) {
                    setError(error.response.data.message)
                    // Request made and server responded
                    console.log(error.response.data);
                    console.log(error.response.status);
                    console.log(error.response.headers);
                } else if (error.request) {
                    // The request was made but no response was received
                    console.log(error.request);
                } else {
                    // Something happened in setting up the request that triggered an Error
                    console.log('Error', error.message);
                }
            });
        }


    var submitButton = <button onClick={handleRequest}>Submit</button>
    if (status === 'loading') {
        submitButton = <button disabled>Submit</button>
    }

    return <>
    <TextBox text='Observed data' change={setObsPath}></TextBox> 
    <div style={{marginBottom:'10px'}}>
        <span>
        <SelectMenu text='Apply logscale to obs.' change={setApplyLog} options={["No", "Yes"]}></SelectMenu>
        </span>
    </div>
    <div className="flexSpaced">
        <span>
        <SelectMenu text='Number of candidates' change={setN} options={["1", "2", "3", "4", "5"]}></SelectMenu>
        </span>
        {submitButton}
    </div>
    <StatusBar task='Getting data...' status={status} error={error}></StatusBar>
    </>
}
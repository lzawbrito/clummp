import ReactLoading from 'react-loading';

export default function StatusBar(props) {
    
    if (props.error) {
        return <div className='errorMsg'>
            Error: {props.error}
        </div>
    } 
    
    const style = (props.status === 'idle') ? 'hiddenStatusBar' : 'statusBar';
    if (props.status === 'success') {
        return <div className='successMsg'>
            Successfully loaded data.
        </div>
    } else {
        return <div className={style}>
            <div className='status'>{props.task}</div>
            <ReactLoading className='loadingAnimation' type='bars'></ReactLoading>
        </div>
    }


}
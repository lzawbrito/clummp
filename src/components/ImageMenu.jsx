import { useState } from 'react';
import { activeRank } from './ControlPanel';
import Rotate from '../icons/rotate-left-svgrepo-com.svg'
import FlipX from '../icons/edit-flip-h-svgrepo-com.svg'
import FlipY from '../icons/edit-flip-v-svgrepo-com.svg'

const transforms = [
	{
		text: "ROT",
		action: 'cw', 
		icon: Rotate
	},
	{
		text: "VERT FLIP",
		action: 'flip-y',
		icon: FlipX
	},
	{
		text: "HORI FLIP",
		action: 'flip-x',
		icon: FlipY
	},
]

// function updateData(data, rank, new_sim) {
// 	var new_sims = []
// 	for (let i in data.sims) {
// 		if (data.sims[i].rank === rank) {
// 			new_sims.push({
// 				rank: data.sims[i].rank, 
// 				name: data.sims[i].name,
// 				t: data.sims[i].t, 
// 				data: new_sim
// 			})
// 		} else {
// 			new_sims.push(data.sims[i])
// 		}
// 	}
// 	return {obs: data.obs, sims: new_sims}
// }

export default function ImageMenu(props) {
	const [toggleText, setToggleText] = useState('View Sim')

	function toggle() {
		let viewSim = props.toggleViewSim();
		if (viewSim) {
			setToggleText('View Sim')
		} else {
			setToggleText('View Obs')
		}
	}

    const axios = require('axios').default;
	var activeSimFile = props.data.sims.find((s) => s.rank === activeRank).name
    function handleRequest(action) {
        axios.get(`/api/transform/${action}/`, {
			params: {
				filename: activeSimFile
			}
		})
			.then((response) => {
				props.setData(response.data)
                console.log('Success.')
            })
            .catch((error) => {
                if (error.response) {
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


	function makeButton(v) {
		return <button className='visButton' 
			onClick={() => handleRequest(v.action)}><img src={v.icon} alt={v.action}></img></button>	
	}

	function makeToggleButton() {
		if (props.vis === 'flicker') {
			return <button className='visButton'
				onClick={toggle}>{toggleText}</button>
		} else {
			return <button className='visButton'
				onClick={toggle} disabled>{toggleText}</button>
		}
	}

	return <>
	<h3>Image Controls:</h3> 
	<div className="buttonRow">
		{transforms.map(makeButton)}
		{makeToggleButton()}
	</div>
	</>
}
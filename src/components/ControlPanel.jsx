import SimMenu from "./SimMenu"
import VisMenu from "./VisMenu"
import ImageMenu from "./ImageMenu"

export var activeRank = 1

function setActiveRank(v) {
	activeRank = v
	console.log('activeRank:',  activeRank)
}


export default function ControlPanel(props) {
	
	return <>
		<SimMenu setActiveSim={props.setActiveSim} data={props.data} setActiveRank={setActiveRank}/>
		<ImageMenu data={props.data} setData={props.setData} vis={props.vis} toggleViewSim={props.toggleViewSim}></ImageMenu>
		<VisMenu setVis={props.setVis}></VisMenu>
	</>
}
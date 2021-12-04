import Request from "./Request"
import ControlPanel from './ControlPanel'
import InfoIcon from '../icons/info-svgrepo-com.svg'

export default function SideBar(props) {
	function controlPanel(data) {
		if (data.sims.length !== 0) {
			return <ControlPanel 
				data={props.data} 
				setData={props.setData} 
				toggleViewSim={props.toggleViewSim} 
				setVis={props.setVis} 
				vis={props.vis}
				setActiveSim={props.setActiveSim} 
			/>
		} else {
			return <></>
		}
	}

	return <>
	<div className="sideBar">
		<div>
			<a href='https://github.com/lzawbrito/clummp' target='_blank' rel="noreferrer">
				<img id='info' src={InfoIcon} height='20px' alt="info"></img>
			</a>
		</div>
		<div className="centerText">
			<h1 id="title">CluMMP<span id='versionTag'>v0.1</span></h1> 
			<div id="subtitle">(Cluster Merger Matching Program)</div>
		</div>
		<div id="request">
			<Request setData={props.setData}/>
		</div>
		<div id="controlPanel">
			{controlPanel(props.data)}
		</div>
	</div>
	</>
}
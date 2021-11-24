import Request from "./Request"
import ControlPanel from './ControlPanel'

export default function SideBar(props) {
	function controlPanel(data) {
		if (data.sims.length !== 0) {
			return <ControlPanel data={props.data}></ControlPanel>
		} else {
			return <></>
		}
	}

	return <>
	<div className="sideBar">
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
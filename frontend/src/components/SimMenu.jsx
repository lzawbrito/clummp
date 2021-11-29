import { activeRank } from "./ControlPanel";

const dummyData = [
	{
		rank: 1, 
		t: 0.21, 
	},
	{
		rank: 2, 
		t: 0.45
	},
	{
		rank: 3, 
		t: 0.45
	},
	{
		rank: 4, 
		t: 0.45
	},
	{
		rank: 5, 
		t: 0.45
	},
	{
		rank: 4, 
		t: 0.45
	},
	{
		rank: 5, 
		t: 0.45
	},
]

export default function SimMenu(props) {
	function makeFile(sim) {
		function changeActiveSim() {
			props.setActiveSim(sim);
			props.setActiveRank(sim.rank);
		}

		let button = <button onClick={changeActiveSim}>Show</button>
		if (activeRank === sim.rank) {
			button = <button onClick={changeActiveSim} disabled>Show</button>
		}

		return <tr>
			<td>
				{sim.rank}
			</td>
			<td>
				{sim.t.toFixed(2)}
			</td>
			{/* <td>
				{sim.name}
			</td> */}
			<td align="right" >
				{button}
			</td>
		</tr>
	}

	return <>
		<h3>Simulations:</h3>
		<div id="fileList">
			<table>
				<tr>
					<th>Rank</th>
					<th>t <span style={{fontWeight: 'normal', color: 'rgb(200, 200, 200)'}}>(Gyr)</span></th>
					{/* <th>Fname</th> */}
					<th></th>
				</tr>
			{props.data.sims.map(makeFile)}
			{/* {dummyData.map(makeFilpp.e)} */}
			</table>
		</div>
	</>
}
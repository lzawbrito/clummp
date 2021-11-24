export default function ControlPanel(props) {
	const testFiles = [
		{
			id: 1,
			name: 'a',
			t: 2,
		},
		{
			id: 2,
			name: 'b',
			t: 2,
		},
		{
			id: 3,
			name: 'c',
			t: 2,
		},
		{
			id: 4,
			name: 'd',
			t: 2,
		},
	]

	function makeFile(sim) {
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
				<button>Show</button>
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
			</table>
		</div>
		{/* {props.data.sims.map(makeFile)} */}
	</>
}
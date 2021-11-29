var activeVis = 'side-by-side'

const vis = [
	{
		id: 'side-by-side',
		text: "Side-by-side",
	},
	{
		id: 'diff',
		text: "Difference"
	},
	{
		id: 'flicker',
		text: "Flicker"
	},
]


export default function VisMenu(props) {
	function changeActiveVis(v) {
		console.log('pressed ' + v.id)
		activeVis = v.id;
		props.setVis(v.id);
	}
	
	function makeButton(v) {
		if (v.id === activeVis) {
			return <button className='visButton' 
				onClick={() => changeActiveVis(v)} disabled>{v.text}</button>	
		} else {
			return <button className='visButton' 
				onClick={() => changeActiveVis(v)}>{v.text}</button>	
		}
	}
	return <>
		<h3>Visualization: </h3>
		<div className="buttonRow">
			{vis.map(makeButton)}
		</div>
	</>
}
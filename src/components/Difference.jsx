import createPlotlyComponent from 'react-plotly.js/factory';
import Plotly from 'plotly.js'
const Plot = createPlotlyComponent(Plotly);

export default function Difference(props) {

    const data = [
        {
            z: props.sim.diff,
            type: 'heatmap',
            showscale: true,
			colorbar: {tickfont: {color: 'white'}}
        },
    ]

    const layout = {
        font: {family: 'Roboto Mono, monospace', color: 'white'},
        plot_bgcolor: '#141414',
        paper_bgcolor: '#141414',
        xaxis: {color: 'white'},
        yaxis: {scaleanchor: 'x', color: 'white'},
		title: {
			text: 'abs(Simulation - Observation)',
			font: {
				size: 24,
			}
		},
    }

    return <>
        <Plot divId="visDisplay" data={data} layout={layout}></Plot>
    </>
}
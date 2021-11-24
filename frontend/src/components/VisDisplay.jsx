import createPlotlyComponent from 'react-plotly.js/factory';
import Plotly from 'plotly.js'
const Plot = createPlotlyComponent(Plotly);

export default function VisDisplay(props) {
    const sims = props.sims
    // const w = 600
    const gap = 0.1
    const data = [
        {
            z: props.obs,
            type: 'heatmap',
            showscale: false,
        },
        {
            z: props.sims[0].data,
            type: 'heatmap',
            showscale: false,
            xaxis: 'x2', 
            yaxis: 'y2',
        },
    ]

    const layout = {
        font: {family: 'Roboto Mono, monospace'},
        plot_bgcolor: '#141414',
        paper_bgcolor: '#141414',
        grid: {rows:1, columns: 2, pattern: 'independent', xgap: gap},
        xaxis: {color: 'white'},
        xaxis2: {color: 'white'},
        yaxis: {scaleanchor: 'x', color: 'white'},
        yaxis2: {scaleanchor: 'x2', color: 'white'},
        annotations: [{
                text: "Observation",
                font: {size: 24, color: 'white'},
                showarrow: false,
                align: 'center',
                x: 0.25, //position in x domain
                y: 1.1, //position in y domain
                xref: 'paper',
                yref: 'paper',
            },
                {
                text: "Simulation 1",
                font: {size: 24, color: 'white'},
                showarrow: false,
                align: 'center',
                x: 0.75, //position in x domain
                y: 1.1,  // position in y domain
                xref: 'paper',
                yref: 'paper',
                }
            ]
    }

    return <div className='visDisplay'>
        <Plot divId="visDisplay" data={data} layout={layout}></Plot>
    </div>
}
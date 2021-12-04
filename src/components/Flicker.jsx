import createPlotlyComponent from 'react-plotly.js/factory';
import Plotly from 'plotly.js'
import { useState } from 'react';
const Plot = createPlotlyComponent(Plotly);


export default function Flicker(props) {
    // var [viewSim, setViewSim] = useState(false)
    let viewSim = props.viewSim

    const simData = [
        {
            z: props.sim.data,
            type: 'heatmap',
            showscale: false,
        },
    ]

    const simLayout = {
        font: {family: 'roboto mono, monospace', color: 'white'},
        plot_bgcolor: '#141414',
        paper_bgcolor: '#141414',
        xaxis: {color: 'white'},
        yaxis: {scaleanchor: 'x', color: 'white'},
		title: {
            text: 'Simulation',
			font: {
                size: 24,
			}
		},
        autosize: true,
    }
    
    const obsData = [
        {
            z: props.obs,
            type: 'heatmap',
            showscale: false
        },
    ]

    const obsLayout = {
        font: {family: 'roboto mono, monospace', color: 'white'},
        plot_bgcolor: '#141414',
        paper_bgcolor: '#141414',
        xaxis: {color: 'white'},
        yaxis: {scaleanchor: 'x', color: 'white'},
		title: {
            text: 'Observation',
			font: {
                size: 24,
			}
		},
        autosize: true,
    }

    let obsStyle = {display: 'block'} 
    let simStyle = {display: 'none'}
    if (viewSim) {
        obsStyle = {display: 'none'}
        simStyle = {display: 'block'}
    }

    // let obsStyle = 'visDisplay' 
    // let simStyle = 'visDisplayHidden'
    // if (viewSim) {
    //     obsStyle = 'visDisplayHidden'
    //     simStyle = 'visDisplay'
    // }
    return <>
        <div style={obsStyle}>
            <Plot divId="visDisplay" data={obsData} layout={obsLayout}></Plot>
        </div>
        <div style={simStyle}>
            <Plot divId="visDisplay" data={simData} layout={simLayout}></Plot>
        </div>
        {/* <Plot divId={obsStyle} data={obsData} layout={obsLayout}></Plot>
        <Plot divId={simStyle} data={simData} layout={simLayout}></Plot> */}
    </>
}
import InnerHtml from 'dangerously-set-html-content'
import * as d3 from 'd3'
import createPlotlyComponent from 'react-plotly.js/factory';
import Plotly from 'plotly.js'
const Plot = createPlotlyComponent(Plotly);

export default function VisDisplay(props) {
        const h = 600
        const gap = 0.1
        const data = [
        {
            z: [[1,2],[3,4]], // props.data,
            type: 'heatmap',
            showscale: false,
        },
        {
            z: [[2,2],[1,2]], // props.data,
            type: 'heatmap',
            showscale: false,
            xaxis: 'x2', 
            yaxis: 'y2'
        },
    ]

    const layout = {
        grid: {rows:1, columns: 2, pattern: 'independent', xgap: gap},
        width: (2 * h) / (1 - (gap / 2)), 
        height: h,
        title: "test",
        yaxis: {scaleanchor: 'x'},
        yaxis2: {scaleanchor: 'x2'}
    }

    return <div className='visDisplay'>
        <Plot data={data} layout={layout}></Plot>
    </div>
}
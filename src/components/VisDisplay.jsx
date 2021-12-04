import SideBySide from "./SideBySide"
import Difference from './Difference'
import Flicker from "./Flicker"

export default function VisDisplay(props) {
    function renderVis(vis) {
        if (vis === 'side-by-side') {
            return <SideBySide sim={props.sim} obs={props.obs}></SideBySide>
        } else if (vis === 'diff') {
            return <Difference sim={props.sim} obs={props.obs}></Difference>
        } else if (vis === 'flicker') {
            return <Flicker viewSim={props.viewSim} sim={props.sim} obs={props.obs}></Flicker>
        }
    }

    return renderVis(props.vis)
}
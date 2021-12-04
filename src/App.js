import { useState } from 'react';
import './App.css';
import SideBar from './components/SideBar';
import VisDisplay from './components/VisDisplay';
import VisFiller from './components/VisFiller'
import { activeRank } from './components/ControlPanel';

function App() {
  const [data, setData] = useState({obs: [], sims: []});
  const [activeSim, setActiveSim] = useState({});
  const [vis, setVis] = useState('side-by-side');
  const [viewSim, setViewSim] = useState(false)

  function toggleViewSim() {
    setViewSim(!(viewSim))
    return viewSim
  }

  // Wrapper function to display filler in case there's no data. 
  function visDisplay(data) {
    if (data.sims.length !== 0) {
      return <VisDisplay sim={activeSim} obs={data.obs} vis={vis} viewSim={viewSim}/>
    } else {
      return <VisFiller></VisFiller>
    }
  }

  return (
    <div className="App">
      <SideBar 
        setData={(d) => {
          setData(d);
          setActiveSim(d.sims[activeRank - 1]);
        }} 
        data={data} 
        setActiveSim={setActiveSim}
        setVis={setVis}
        toggleViewSim={toggleViewSim}
        vis={vis}
      />
      {visDisplay(data)}
    </div>
  );
}

export default App;

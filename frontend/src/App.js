import { useState } from 'react';
import './App.css';
import Request from './components/Request'
import SideBar from './components/SideBar';
import VisDisplay from './components/VisDisplay';
import VisFiller from './components/VisFiller'

function App() {
  const [data, setData] = useState({obs: [], sims: []});
  function vis(data) {
    if (data.sims.length !== 0) {
      return <VisDisplay sims={data.sims} obs={data.obs}/>
    } else {
      return <VisFiller></VisFiller>
    }
  }
  return (
    <div className="App">
      <SideBar setData={setData} data={data}/>
      {vis(data)}
    </div>
  );
}

export default App;

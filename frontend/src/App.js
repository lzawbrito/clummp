import logo from './logo.svg';
import './App.css';
import Request from './components/Request'

function App() {
  return (
    <div className="App">
      <h1>CluMMP</h1>
      <h3 style={{marginTop:'-16px'}}>(Cluster Merger Matching Program)</h3>
      <Request/>
    </div>
  );
}

export default App;

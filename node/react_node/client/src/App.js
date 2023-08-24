import './App.css';
import React, { useEffect, useState } from 'react';

function App() {
  const [Result1, setResult1] = useState()
  const [Result2, setResult2] = useState();

  useEffect(() => {
    fetch("http://localhost:8080/")
      .then(res => res.json())
      .then(data => {
        console.log(data)
        setResult1(data.message)
      })
    fetch("http://localhost:8080/api")
      .then(res => res.json())
      .then(data => {
        console.log(data)
        setResult2(data.message)
      })
  }, []);

  return (
    <div className="App">
      <h2>React Client ---- Node Server</h2>
      <h3>{Result1}</h3>
      <h3>{Result2}</h3>
    </div>
  );
}

export default App;

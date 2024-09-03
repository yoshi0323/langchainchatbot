import React from 'react';
import ChatWindow from './components/ChatWindow';
import './App.css';

function App() {

  const handleFetch = () => {
    fetch("http://127.0.0.1:8000/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ question: "名言を1つ教えて" })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
  };

  return (
    <div className="App">
      <ChatWindow />
      <button onClick={handleFetch}>Get Quote</button>
    </div>
  );
}

export default App;

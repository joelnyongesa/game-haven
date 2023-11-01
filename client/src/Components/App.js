import './App.css';
import Navbar from './Navbar';
import Hero from './Hero';
import { useEffect, useState } from 'react';
import GameCard from './GameCard';
import Footer from './Footer';

function App() {
  const [games, setGames] = useState([])

  useEffect(()=>{
    fetch('http://localhost:8080/games')
    .then(r => r.json())
    .then(data=>setGames(data))
    .catch(e=> console.log(e))
  }, [])
  return (
    <div className="App">
      <Navbar />
      <Hero />
      <GameCard games={games}/>
      <Footer />

    </div>
  );
}

export default App;

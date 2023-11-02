import './App.css';
import { Routes, Route } from 'react-router-dom';
import SignUp from './SignUp';
import Login from './Login';
import Landing from './Landing';
import Home from './Home';
import AllGames from './AllGames';
import {useState, useEffect} from 'react'


function App() {

  const [games, setGames] = useState([])

    useEffect(()=>{
        fetch('/games')
        .then(r => r.json())
        .then(data=>setGames(data))
        .catch(e=> console.log(e))
    }, [])

    console.log(games)
  
  return (
    <div className="App">
      <Routes>
        <Route element={<Landing />}>
          <Route path='/' element={<Home />}/>
          <Route path='/home' element={<Home games={games}/>}/>
          <Route path='/signup' element={<SignUp />}/>
          <Route path='/login' element={<Login />}/>
          <Route path='/all-games' element={<AllGames games={games}/>}/>
        </Route>
        
      </Routes>

    </div>
  );
}

export default App;

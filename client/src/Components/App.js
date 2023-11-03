import './App.css';
import { Routes, Route } from 'react-router-dom';
import SignUp from './SignUp';
import Login from './Login';
import Landing from './Landing';
import Home from './Home';
import AllGames from './AllGames';
import Game from './Game'
import {motion} from "framer-motion"

import {useState, useEffect} from 'react'


function App() {

  const [games, setGames] = useState([])
  const [user, setUser] = useState(null)

    useEffect(()=>{
        fetch('/games')
        .then(r => r.json())
        .then(data=>setGames(data))
        .catch(e=> console.log(e))
    }, [])

    function updateUser(username){
        setUser(username)
    }

    // console.log(games)
    // console.log(user)
  
  return (
    <div
    // initial={{opacity: 0}}
    // animate={{opacity: 1}}
    // transition={{duration: 2, delay: 2}}
    >
      <Routes>
        <Route element={<Landing />}>
          <Route path='/' element={<Home />}/>
          <Route path='/home' element={<Home games={games}/>}/>
          <Route path='/signup' element={<SignUp />}/>
          <Route path='/login' element={<Login updateUser={updateUser}/>}/>
          <Route path='/all-games' element={<AllGames games={games}/>}/>
          <Route path='/all-games/:id' element={<Game />} />
        </Route>
        
      </Routes>

    </div>
  );
}

export default App;

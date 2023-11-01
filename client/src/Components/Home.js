import { useState, useEffect } from "react"
import Hero from "./Hero"
import GameCard from "./GameCard"
import Footer from "./Footer"


function Home() {
    const [games, setGames] = useState([])

    useEffect(()=>{
        fetch('http://localhost:8080/games')
        .then(r => r.json())
        .then(data=>setGames(data))
        .catch(e=> console.log(e))
    }, [])

  return (
    <>
        <Hero />
        <GameCard games={games}/>
        <Footer />
        
    </>
  )
}

export default Home
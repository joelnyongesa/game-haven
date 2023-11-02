import React from 'react'
import Button from './Button'

function AllGames({ games }) {

    const gameCard = games.map((game)=>(
        <div key={game.id} className='max-w-sm rounded overflow-hidden m-10 w-1/6'>
            <img className='w-full h-400' src={game.image_url} alt={game.title} loading='lazy'/>
            <div className='flex flex-col items-start my-3'>
                <h1 className='font-bold text-sm'>{game.title}</h1>
                <p className='text-sm'>{game.description}</p>
                <div className="w-20px">
                    <Button content="Game reviews" className='text-sm my-3 px-2 py-1 mx-auto'/>
                </div>
                {games.map((game)=>(console.log(game)))}
                
            </div>
        </div>
    ))

  return (
    <div>
        <h1 className='text-3xl font-bold text-center'>All Games</h1>
        <div className='flex flex-row flex-wrap justify-center'>
            {gameCard}
        </div>
    </div>
  )
}

export default AllGames
import {useState, useEffect} from 'react'
import { useParams } from 'react-router-dom'
import {MdReviews} from 'react-icons/md'
import GameReviews from './GameReviews'
import {motion} from 'framer-motion'


function Game() {
    const [game, setGame] = useState([])
    const [showReviews, setShowReviews] = useState(false)

    let {id} = useParams()

    useEffect(()=>{
        fetch(`/games/${id}`)
        .then(r=>r.json())
        .then(data=>setGame(data))
        .catch(e=>console.log(e))
    }, [])

    const gameReviewsCount = game.game_reviews ? game.game_reviews.length : 0;

    const gameReviews = game.game_reviews ? game.game_reviews : []
    console.log(gameReviews);

    const gameGenres = game.game_genres ? game.game_genres.map(genre => genre.genre.name) : [];

    // console.log(game);

    // To show the reviews
    function toggleReviews(){
        setShowReviews((showReviews) => !showReviews)
    }

    const genres = gameGenres.length > 0 ? (
        gameGenres.map((genre, index)=>(
            <span key={index}
                className='inline-block bg-platinum rounded-full text-sm font-semibold text-rich-black mr-2 mb-2 px-1'
            >#{genre}</span>
        )
    )) : (
        <span></span>
    )

    // Handle animations
    const variants = {
        visible: {opacity: 1, x:5, transition: {type: "spring", stiffness:100}},
        hidden: {opacity: 0, transition: {type: "spring", stiffness:100}}
    }


  return (
    <div className='w-screen max-w-lg rounded overflow-hidden p p-10 mx-auto'>
        <img src={game.image_url} alt={game.name} />
        <h1 className='text-xl font-bold my-3'>Game Description</h1>
        <p className='mb-3'>{game.description}</p>
        <span className='flex mb-5' onClick={toggleReviews}>
            <MdReviews className='text-2xl mx-3 cursor-pointer' />
            <p>{gameReviewsCount }</p>
        </span>
        <motion.div
            variants={variants}
            animate={showReviews? "visible": "hidden"}
        >
            {showReviews && <GameReviews reviews={gameReviews} />}
        </motion.div>
        {genres}
    </div>
  )
}

export default Game
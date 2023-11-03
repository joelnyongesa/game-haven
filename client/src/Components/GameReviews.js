import ReactStars from 'react-rating-stars-component'

function GameReviews({ reviews }) {

    const allReviews = reviews ? reviews.map((review)=>(
        <div key={review.id}>
            <p className='text-sm text-platinum'>user: {review.user.username}</p>
            <p>Comments: {review.comment}</p>
            Rating: <ReactStars count={5} value={(review.rating/2)} isHalf={true} />
            <hr className='w-6/6 my-3'/>
        </div>
    )) : <span>This game has no reviews yet!</span>

  return (
    <div>
        {allReviews}
    </div>
  )
}

export default GameReviews
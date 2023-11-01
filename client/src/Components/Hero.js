import Button from './Button'
import gaming_vector from '../gaming_vector.png'

function Hero() {
  return (
    <div className='flex flex-row justify-between h-2/6 p-10 m-10'>
        <div className='flex flex-col justify-center content-evenly w-3/6'>
            <h1 className='text-3xl font-bold py-5'>Add your Games, Review Games, and More...</h1>
            <p className='py-10'>
                Tell us what games you are playing, and review other user's games ON THE FLY
            </p>
            <div>
                <Button content="Sign Up and Get Started"/>
            </div>
            
        </div>
        <div className='w-3/6'>
            <img className='object-contain h-450 w-680 rounded-md' src={gaming_vector} alt='Gaming son'/>
        </div>
    </div>
  )
}

export default Hero
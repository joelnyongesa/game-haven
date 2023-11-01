import Button from "./Button"
import { Link } from "react-router-dom"
import { useNavigate } from "react-router-dom"

function Navbar() {
    const navigate = useNavigate()

    function handleHeaderClick(){
        navigate('/home')
    }

  return (
    <nav className='flex flex-row justify-between p-10'>
        <div></div>
        <h1 className='text-3xl font-bold' onClick={handleHeaderClick}>Game<span className="text-platinum">Haven</span></h1>
        <section className='flex flex-row justify-end '>
            <Link to='/signup'>
                <Button content="Sign Up"className='py-1'/>
            </Link>
            <Link to='/login'>
                <Button content="Log In" className='py-1'/>
            </Link>
            
        </section>
    </nav>
  )
}

export default Navbar
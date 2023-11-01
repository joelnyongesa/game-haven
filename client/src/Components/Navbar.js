import Button from "./Button"

function Navbar() {
  return (
    <nav className='flex flex-row justify-between p-10'>
        <div></div>
        <h1 className='text-3xl font-bold'>Game<span className="text-platinum">Haven</span></h1>
        <section className='flex flex-row justify-end '>
            <Button content="Sign Up"/>
            <Button content="Log In"/>
        </section>
    </nav>
  )
}

export default Navbar
import './App.css';
import { Routes, Route } from 'react-router-dom';
import SignUp from './SignUp';
import Login from './Login';
import Landing from './Landing';
import Home from './Home';

function App() {
  
  return (
    <div className="App">
      <Routes>
        <Route element={<Landing />}>
          <Route path='/' element={<Home />}/>
          <Route path='/home' element={<Home />}/>
          <Route path='/signup' element={<SignUp />}/>
          <Route path='/login' element={<Login />}/>
        </Route>
        
      </Routes>

    </div>
  );
}

export default App;

import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import { BrowserRouter, Routes, Route} from "react-router-dom";
import Nav from './components/Navbar.js';
import Home from './components/Home.js';

function App() {
  return (
    <BrowserRouter>
        <Nav />
      <Routes>
        <Route exact path="/" element={<Home />}></Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;

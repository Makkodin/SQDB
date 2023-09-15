import React, { useState } from 'react';
import { Card, Container } from "react-bootstrap";
import { Routes, Route } from "react-router-dom";
import './App.css';

import logo from "./image/logo.png"
import { GiBinoculars } from "react-icons/gi";
import { AiOutlineProject, AiOutlineCodeSandbox } from "react-icons/ai";
import { BiTestTube } from "react-icons/bi";

import Home from './components/Home';
import Projects from "./components/Projects";
import ProjectsID from './components/ProjectsID';
import DropdownHeader from './components/Header';

//import Flowcells from './components/Flowcells';

function App() {

  const [open, setOpen] = useState(false);

  return (
    <>
    <div className='menu-container'>
      <div className='menu-trigger' onClick={()=>{setOpen(!open)}}>
        <img src={logo} alt="Logo"></img>
      </div>

      <div className={`dropdown-menu ${open? 'active' : 'inactive'}`}>
        <h3><b>Навигация по сервису:</b></h3>
        <ul>
          <DropdownHeader link = {"/"} img = {<GiBinoculars/>} text = {"SQDB"}/>
          <DropdownHeader link = {"/projects"} img = {<AiOutlineProject/>} text = {"Проекты"}/>
          <DropdownHeader link = {"/flowcells"} img = {<AiOutlineCodeSandbox/>} text = {"Ячейки"}/>
          <DropdownHeader link = {"/biosamples"} img = {<BiTestTube/>} text = {"Биообразцы"}/>
        </ul>
      </div>
    </div>
    <br />

    <Container>
      <Card>
        <Routes>
          <Route path='/' element={<Home />} />
          <Route path='/projects' element={<Projects />}/>
          <Route path="/projects/:id" element={<ProjectsID />}/>
          
        </Routes>
      </Card>
    </Container>
    </>
  );
}

export default App;
//<Route path='/flowcells' element={<Flowcells />}/>
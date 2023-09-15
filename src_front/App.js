import React from 'react';
import { Card, Container } from "react-bootstrap";
import { Routes, Route } from "react-router-dom";
import './App.css';

import Header from './components/Header';
import Home from './components/Home';

import Projects from "./components/Projects";
import ProjectsID from './components/ProjectsID';

import Types from './components/Types';
import TypesID from './components/TypesID';

import Flowcells from './components/Flowcells';
import FlowcellsID from './components/FlowcellsID';

function App() {
  return (
    

    <>
    <Header/>
    <br />
    <Container>
      <Card>
        <Routes>
          <Route path='/' element={<Home />} />
          <Route path='/projects' element={<Projects />}/>
          <Route path="/projects/:id" element={<ProjectsID />}/>
          <Route path="/types" element={<Types />}/>
          <Route path="/types/:id" element={<TypesID />}/>
          <Route path="/flowcells" element={<Flowcells />}/>
          <Route path="/flowcells/:id" element={<FlowcellsID />}/>
        </Routes>
      </Card>
    </Container>
    </>
  );
}

export default App;
//<Route path='/flowcells' element={<Flowcells />}/>
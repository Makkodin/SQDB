import React, { useState } from 'react';
import { Nav } from "react-bootstrap";
import { NavLink } from "react-router-dom";

import logo from "./../image/logo.png"
import { GiBinoculars } from "react-icons/gi";
import { AiOutlineProject, AiOutlineCodeSandbox } from "react-icons/ai";
import { BiTestTube } from "react-icons/bi";

import './../styles/Dropdown.css'

function DropdownHeader(props) {
    
    
    return (
        <li className="dropdownItem"> 
            {props.img}           
            <Nav.Link as={NavLink} to={props.link}>
                {props.text}
            </Nav.Link>       
        </li>
    );
}

function Header() {
    const [open, setOpen] = useState(false);

    return (
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
                  <DropdownHeader link = {"/types"} img = {<BiTestTube/>} text = {"Тип секвенирования"}/>
                </ul>
            </div>
        </div>
    );

}

export default Header;
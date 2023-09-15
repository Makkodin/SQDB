import React from "react";
import { Nav } from "react-bootstrap";
import { NavLink } from "react-router-dom";









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

export default DropdownHeader;

//<Navbar expand="lg" bg="dark" variant="dark" sticky="top">
//    <Container>
//        <Navbar.Brand as={NavLink} to="/">
//            <GiBinoculars /> SQBD
//        </Navbar.Brand>
//        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
//        <Navbar.Collapse id="responsive-navbar-nav">
//            <Nav className="me-auto">
//                <Nav.Link as={NavLink} to="/projects">
//                <AiOutlineProject /> Проекты
//                </Nav.Link>
//                <Nav.Link as={NavLink} to="/flowcells">
//                <AiOutlineCodeSandbox /> Ячейки
//                </Nav.Link>
//                <Nav.Link as={NavLink} to="/biosamples">
//                <BiTestTube /> Биообразцы
//                </Nav.Link>
//            </Nav>
//        </Navbar.Collapse>
//    </Container>
//</Navbar>
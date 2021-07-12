import React from 'react'
import {Navbar,Nav,NavDropdown,Form,Button,FormControl} from'react-bootstrap'
import {Link} from 'react-router-dom'

const NavigationBar =()=>{
    return(
        <div>
            <Navbar bg="dark" variant="dark" expand="lg">
            <Navbar.Brand href="#home">Security Surveillence</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="ml-auto" style={{justifyContent:"space-around"}}>
                <Nav.Link><Link style={{color:"white"}}  to="/Home">Home </Link></Nav.Link>
                <Nav.Link><Link style={{color:"white"}} to="/Recognition">Recognition</Link></Nav.Link>
                <Nav.Link><Link style={{color:"white"}} to="/Records">Records</Link></Nav.Link>
                <Nav.Link><Link style={{color:"white"}} to="/AllSuspects">Suspects</Link></Nav.Link>
                <Nav.Link><Link style={{color:"white"}} to="/Profile">Profile</Link></Nav.Link>
                <Nav.Link><Link style={{color:"white"}} to="/ImageUpload">Capture</Link></Nav.Link>
                </Nav>
            </Navbar.Collapse>
           
            </Navbar>
           
        </div>
        )
}
export default NavigationBar
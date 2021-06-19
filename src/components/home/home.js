import React,{useState} from 'react'
import {Container,Row,Col} from 'react-bootstrap'
import Image from '../../assets/images/download.png'
import './home.scss'
import {Credentials} from '../../credentials'

let time = new Date().toLocaleString();

const Home=()=>{
    const [date, setDate] =useState(new Date());
    
    function tick() {
        setDate(new Date());
       }

    var timerID = setInterval( () => tick(), 1000 );
       
     function cleanup() {
        clearInterval(timerID);
      };
 

   


    return(
        <div>
            <Container className="homeContainer">
                <Row className="liveWindowTitle">
                    <Col sm={10}>
                        <Row>
                        <Col sm={6}><h5>LIVE MONITORING</h5></Col>
                        <Col sm={6} className="liveTime" ><h5 style={{float:"right"}} >{date.toLocaleTimeString()}</h5></Col>
                        </Row>
                    </Col>
                </Row>
                <Row className="liveWindowRow">
                    <Col sm={10}>
                        <div className="liveWindow">
                            <img className="liveContent" src={Credentials.IMGENDPOINT} alt="sample" />
                        </div>
                    </Col>
                    
                </Row>
                <br/>
            <br/>
            <br/>
            <br/>
            <br/>
            <br/>
            </Container>
        </div>
    )
};

export default Home
import React, {Component} from 'react';
import {storage} from '../../firebase';
import { Container,Row,Col,Button,Form } from 'react-bootstrap';
import './ImageUpload.scss'
import {Modal,Figure} from 'react-bootstrap'
import MaterialTable from 'material-table'
import { forwardRef } from 'react';
import AddBox from '@material-ui/icons/AddBox';
import ArrowDownward from '@material-ui/icons/ArrowDownward';
import Check from '@material-ui/icons/Check';
import ChevronLeft from '@material-ui/icons/ChevronLeft';
import ChevronRight from '@material-ui/icons/ChevronRight';
import Clear from '@material-ui/icons/Clear';
import DeleteOutline from '@material-ui/icons/DeleteOutline';
import Edit from '@material-ui/icons/Edit';
import FilterList from '@material-ui/icons/FilterList';
import FirstPage from '@material-ui/icons/FirstPage';
import LastPage from '@material-ui/icons/LastPage';
import Remove from '@material-ui/icons/Remove';
import SaveAlt from '@material-ui/icons/SaveAlt';
import Search from '@material-ui/icons/Search';
import ViewColumn from '@material-ui/icons/ViewColumn';
import PersonOutlineTwoToneIcon from '@material-ui/icons/PersonOutlineTwoTone';
import {Credentials} from '../../credentials.js'
import axios from 'axios'


const tableIcons = {
  Add: forwardRef((props, ref) => <AddBox {...props} ref={ref} />),
  Check: forwardRef((props, ref) => <Check {...props} ref={ref} />),
  Clear: forwardRef((props, ref) => <Clear {...props} ref={ref} />),
  Delete: forwardRef((props, ref) => <DeleteOutline {...props} ref={ref} />),
  DetailPanel: forwardRef((props, ref) => <ChevronRight {...props} ref={ref} />),
  Edit: forwardRef((props, ref) => <Edit {...props} ref={ref} />),
  Export: forwardRef((props, ref) => <SaveAlt {...props} ref={ref} />),
  Filter: forwardRef((props, ref) => <FilterList {...props} ref={ref} />),
  FirstPage: forwardRef((props, ref) => <FirstPage {...props} ref={ref} />),
  LastPage: forwardRef((props, ref) => <LastPage {...props} ref={ref} />),
  NextPage: forwardRef((props, ref) => <ChevronRight {...props} ref={ref} />),
  PreviousPage: forwardRef((props, ref) => <ChevronLeft {...props} ref={ref} />),
  ResetSearch: forwardRef((props, ref) => <Clear {...props} ref={ref} />),
  Search: forwardRef((props, ref) => <Search {...props} ref={ref} />),
  SortArrow: forwardRef((props, ref) => <ArrowDownward {...props} ref={ref} />),
  ThirdStateCheck: forwardRef((props, ref) => <Remove {...props} ref={ref} />),
  ViewColumn: forwardRef((props, ref) => <ViewColumn {...props} ref={ref} />)
  };



class ImageUpload extends Component {
  constructor(props) {
    super(props);
    this.state = {
      image: null,
      url: '',
      progress: 0,
      location:'',
      data:[],
      resultImg:''
    }
    this.handleChange = this
      .handleChange
      .bind(this);
      this.handleUpload = this.handleUpload.bind(this);
      this.handleLocation=this.handleLocation.bind(this);
  }
  handleLocation=(evt)=>{
    const{location}=this.state;
    this.setState({location:evt.target.value})
  }
handleSubmit=()=>{
  const{url,location}=this.state;
  const request={
    "location":location,
    "image":url
  }
    axios.post(`${Credentials.ENDPOINT}/liveRecognition`,request)
      .then((res)=>{
        console.log(res)
          console.log(res.data.details);
          console.log(res.data.lastpic);
        //  console.log(res[0]["lastpic"])
         this.setState({resultImg:res.data.lastpic})
         this.setState({data:[res.data.details]})
        // console.log(this.state.data[0]["details"])
      })

        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components        
      
  // console.log(url);
  // console.log(location);
}
  handleChange = e => {
    if (e.target.files[0]) {
      const image = e.target.files[0];
      this.setState(() => ({image}));
    }
  }
  handleUpload = () => {
      const {image} = this.state;
      const uploadTask = storage.ref(`images/${image.name}`).put(image);
      uploadTask.on('state_changed', 
      (snapshot) => {
        // progrss function ....
        const progress = Math.round((snapshot.bytesTransferred / snapshot.totalBytes) * 100);
        this.setState({progress});
      }, 
      (error) => {
           // error function ....
        console.log(error);
      }, 
    () => {
        // complete function ....
        storage.ref('images').child(image.name).getDownloadURL().then(url => {
            console.log(url);
            this.setState({url});
        })
    });
  }

  render() {

    const style = {
      height: '100vh',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'centre',
      justifyContent: 'centre',
      margintop:'20vh'
    };
    return (
      <div>
        <Container>
          {/* <Row className="uploadImageROW">
            <Col sm={12}>

                  <div className="uploadImage">
                  <p>
                  <input type="file" className="btn btn-file" onChange={this.handleChange}/>
                  </p>
                  <p>
                  <Button variant="secondary" onClick={this.handleUpload}>Upload</Button> 
                  </p>
                  <progress  value={this.state.progress} max="100"/>
                  </div>
              </Col>
              </Row> */}
              <Row className="title">
                  <Col md={{ span: 7, offset: 4 }} >
                    <h2 >Live Capture</h2>
                  </Col>
                </Row> 
              
              <Row className="ImageROW" style={{marginTop:"2vh"}} >
                <Col sm={6} >
                                  
                <div className="selectedImage">
                    <img src={this.state.url || 'http://via.placeholder.com/400x300'} alt="Uploaded images" height="300" width="400"/>
                    </div>
                </Col>
                <Col sm={6}>
                    <div className="loadedImage">
                    <img src={this.state.resultImg || 'http://via.placeholder.com/400x300'} alt="Uploaded images" height="300" width="400"/>
                    </div>
                </Col>  
              </Row>  
              <Row className="finalDetails">
                <Col sm={6}>
                <div className="uploadImage">
                  <p>
                  <input type="file" className="btn btn-file"  style={{marginLeft:"-2vh"}} onChange={this.handleChange}/>
                  </p>
                  <p>
                  <Button variant="secondary" onClick={this.handleUpload}>Upload</Button> 
                  </p>
                  <progress  value={this.state.progress} max="100"/>
                  </div>
                      <div className="inputImgDetails">
                      <Form>
                            <Form.Group className="mb-3" controlId="formLocation">
                              <Form.Label>Input Location:</Form.Label>
                              <Form.Control type="text" placeholder="Enter location" onChange={this.handleLocation} />
                              <Form.Text className="text-muted">
                                Enter Location Carefully
                              </Form.Text>
                              <Form.Label>Image URL:</Form.Label>
                              <Form.Control controlId="imgId" type="text"  readOnly value={this.state.url} />
                        </Form.Group>
                        </Form>
                        <Button variant="secondary" onClick={this.handleSubmit}>Submit</Button>
                      </div>
                </Col>
                </Row >
                <Row className="outputImgRow" style={{marginTop:"3vh"}}>
                  <Col sm={12}>
                      <div className="outputImgtable">
                            <MaterialTable
                                      icons={tableIcons}
                                      title="Suspect Recognition"
                                      columns={[
                                        { title: 'Criminal Id', field: 'sid' },
                                        { title: 'Criminal Name', field: 'name' },
                                        { title: 'ThreatLevel', field: 'threat'  },
                                        { title: 'Location', field: 'location' },
                                        { title: 'Time', field: 'last' },
                                        // { title: 'Cases', field: 'cases' }

                                        
                                      ]}
                                      data={this.state.data}
                                      // actions={[
                                      //   {
                                      //     icon: PersonOutlineTwoToneIcon,
                                      //     tooltip: 'View Profile',
                                      //     onClick: (event, rowData) => {
                                      //       console.log(rowData)  
                                      //       setModalInfo(rowData)
                                      //       console.log(rowData.criminalId)  
                                      //       toggleTrueFalse()       
                                      // }
                                      //   },
                                      // ]}
                                      options={{
                                        actionsColumnIndex: -1
                                      }}
                           />
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
  }
}

export default ImageUpload;
import './App.css';
import FileUpload from './components/FileUpload'
import TalkingImage from './components/TalkingImage'

import AppBar from '@mui/material/AppBar';
import { useState, useEffect } from "react";
import Button from '@mui/material/Button';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';

function App() {
  const [componentToShow, setComponentToShow] = useState(<FileUpload/>);
  const handleButtonClick = (component) => {
    setComponentToShow(component);
  };
  
  return (

    <div className="App"> 
      <AppBar position="static">
      <Toolbar variant="dense">
        <IconButton edge="start" color="inherit" aria-label="menu" sx={{ mr: 2 }}>
          {/* Add your menu icon here */}
        </IconButton>
        <Typography variant="h6" color="inherit" component="div" sx={{ flexGrow: 1 }}>
          Synthesized AI
        </Typography>
        <Button color="inherit" onClick={() => handleButtonClick(<TalkingImage />)}>
          Image Conversion
        </Button>
      </Toolbar>
    
    </AppBar>
    <div
    style={{
      marginLeft:'20px',
      marginTop:'200px'
    }}
    >
        {componentToShow}
      
        </div>
    </div>
  );
}

export default App;

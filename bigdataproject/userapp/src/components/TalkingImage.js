import * as React from 'react';
import { useState, useEffect } from "react";
import Button from '@mui/material/Button';

import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';

import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import TextareaAutosize from '@mui/base/TextareaAutosize';


export default function UploadVideos() {

    const [open, setOpen] = React.useState(false);
    const [progress, setProgress] = React.useState(0);
    const [buffer, setBuffer] = React.useState(10);
    const [language, setLanguage] = React.useState('');

    const handleChange = (event: SelectChangeEvent) => {
      console.log(event.target.value)
      setLanguage(event.target.value);
    };

    const [text, setText] = useState('');

    const handleTextChange = (event) => {
      setText(event.target.value);
    };

    const progressRef = React.useRef(() => {});

    const handleFileInputChange = (event) => {

      console.log(event.target.files[0])
      const data = new FormData();
      data.append('file', event.target.files[0]);
      data.append('filename',event.target.files[0].name);
      data.append('text',text);
      console.log("forwarding request ")
      console.log(data)

      let api = '/upload' + '/' + language

      fetch(api, {
        method: 'POST',
        body: data,
      }).then((response) => {
        console.log(response)
      });
    };

    const handleOpenImage = () => {
      const input = document.createElement("input");
      input.type = "file";
      input.accept = "image/*";
      input.multiple = false;
      input.onchange = handleFileInputChange;
      input.click();
    };


    React.useEffect(() => {
        const timer = setInterval(() => {
          progressRef.current();
        }, 500);
    
        return () => {
          clearInterval(timer);
        };
      }, []);

    
      React.useEffect(() => {
        progressRef.current = () => {
          if (progress > 100) {
            setProgress(0);
            setBuffer(10);
          } else {
            const diff = Math.random() * 10;
            const diff2 = Math.random() * 10;
            setProgress(progress + diff);
            setBuffer(progress + diff + diff2);
          }
        };
      });

  return (
    <Box
    sx={{
      display: 'flex',
      flexWrap: 'wrap',
      '& > :not(style)': {
        m: 10,
        width: 300,
        height: 400,
        marginLeft:'300px',
        marginBottom:'300px'
      },
    }}
  >

 <Paper elevation={10}  sx={{ marginLeft: '100px' , marginBottom:'100px' }} >

    <Button  onClick={handleOpenImage}
      variant="contained" component="label" 
          style={{
              width:'230px',
              marginTop:"10px"
          }}  >
          Image
      </Button>

      <TextareaAutosize
      aria-label="empty textarea"
      placeholder="Empty"
      style={{ width: 200, marginTop:'10px' }}
      value={text}
      onChange={handleTextChange}
    />

      <FormControl fullWidth
    sx={{ width: '100%' , marginTop:"5%"}}
   >
 
  <InputLabel id="demo-simple-select-label">Select Laguage</InputLabel>

  <Select
    labelId="demo-simple-select-label"
    id="demo-simple-select"
    value={language}
    label="Select Language"
    onChange={handleChange}
  >

    <MenuItem value={"Mandarin"}>Mandarin</MenuItem>
    <MenuItem value={"Hindi"}>Hindi</MenuItem>
    <MenuItem value={"Spanish"}>Spanish</MenuItem>
    <MenuItem value={"German"}>German</MenuItem>
    <MenuItem value={"French"}>French</MenuItem>

  </Select>


</FormControl>
    </Paper>


<Paper elevation={10} >
    <Button  
    variant="contained" component="label"
        style={{
            width:'230px',
            height:'230px',
            marginTop:"100px"

        }}
        
        >
        Download
      
      </Button>
    </Paper>
  </Box>

  );

}

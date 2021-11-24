import React, { useState } from 'react';

export default function TextBox(props) {
    return <span className="textBox">
    <label style={{marginRight: '5px'}}>{props.text}: </label>
    <input 
        onChange={(e) => props.change(e.target.value)} 
    type="text"></input> 
    </span>
}
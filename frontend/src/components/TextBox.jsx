import React, { useState } from 'react';

export default function TextBox(props) {
    return <>
    <label>{props.text}: </label>
    <input 
        onChange={(e) => props.change(e.target.value)} 
    type="text"></input> 
    </>
}
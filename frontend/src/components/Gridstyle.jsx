import React from 'react'
import { Sympmatrix } from './Sympmatrix'
import { useState } from 'react'
import { useRef } from 'react'

export const Gridstyle = () => {
    const [output, setoutput] = useState(false)
    const [matrix, setMatrix] = useState(
        Array.from({ length: 11 }, () => Array(12).fill(0))
      );
    const submit = () =>{
        console.log(matrix);
        setoutput(true);
        setMatrix(Array.from({ length: 11 }, () => Array(12).fill(0)));
        
    }
    
  return (
    <div>
        {
            output && 
            <>
                <div className='w- w-lvw h-lvh bg-white'>
                    output
                    <button type="button" onClick={()=>{setoutput(false)}}>click</button>
                </div>
            </>
        }
        {!output &&
        <>
        <Sympmatrix matrix={matrix} setMatrix={setMatrix}/>
        <div className="p-2 fixed w-58 break-words border bottom-10 right-10 bg-orange-300 cursor-pointer shadow-lg rounded-md flex justify-center items-center">
            <div className=' text-white ' onClick={submit}>Submit</div>
        </div>
        </>
        }
    </div>
  )
}

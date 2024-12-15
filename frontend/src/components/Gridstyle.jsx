import React from 'react'
import { Sympmatrix } from './Sympmatrix'
import { useState } from 'react'

export const Gridstyle = () => {
    const [matrix, setMatrix] = useState(
        Array.from({ length: 11 }, () => Array(12).fill(0))
      );
  return (
    <div>
        <Sympmatrix matrix={matrix} setMatrix={setMatrix}/>
        <div className="p-2 fixed w-58 break-words border bottom-10 right-10 bg-orange-300 cursor-pointer shadow-lg rounded-md flex justify-center items-center">
            <div className=' text-white '>Submit</div>
        </div>
    </div>
  )
}

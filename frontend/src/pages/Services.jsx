import { React, useState } from 'react';
import { Nav } from '../components/Nav';
import { Select } from '../components/Select';
import { Descstyle } from '../components/Descstyle'; // Assuming Descstyle is a component
import { Gridstyle } from '../components/Gridstyle'; // Assuming Gridstyle is a component


export const Services = () => {
    const [selec, setselec] = useState(true);  // Shows the Select component
    const [desc, setdesc] = useState(true);    // Determines whether to show Description or Grid

    return (
        <>
            {selec && (
                <Select selec={selec} setselec={setselec} desc={desc} setdesc={setdesc} />
            )}
            {!selec && (
                <div>
                    
                    {desc ? <> <Nav text={"Enter your Symptom Description"} /> <Descstyle /> </> : <><Nav  text={"Select your Symptoms "} /> <Gridstyle /> </>}
                    
                </div>
            )}
        </>
    );
};

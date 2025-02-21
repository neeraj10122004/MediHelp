import React from 'react';

const Record = ({ record }) => {
    const maxLength = 100;

    return (
        <article className="w-1/3 bg-slate-300 rounded-md p-4">
            <div className="flex gap-4">
                <div>{record.predictions}</div>
                <div>{record.date}</div>
            </div>
            <div>
                {record.llm && record.llm.length > maxLength
                    ? `${record.llm.substring(0, maxLength)}...`
                    : record.llm}
            </div>
            <button 
                className="bg-white mt-2 p-1 rounded hover:bg-gray-200"
                onClick={() => alert('Button clicked!')}
            >
                Show
            </button>
        </article>
    );
};

export default Record;


    


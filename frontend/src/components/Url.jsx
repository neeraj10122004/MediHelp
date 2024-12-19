import React from 'react'

export const Url = (link,snippet,title) => {
  return (
    <div>
        <a href={link}>{title}</a>
        <p>{link}</p>
        <div>
            {snippet}
        </div>
    </div>
  )
}

import React from 'react'
import {Routes, Route} from "react-router-dom"
import HomePage from './Pages/HomePage'
import ResultsPage from './Pages/ResultsPage'
const App = () => {
  return (
    <div>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path='/results' element={<ResultsPage />} />
      </Routes>
    </div>
  )
}

export default App

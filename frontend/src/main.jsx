import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import './i18n/config.js'

console.log('main.jsx loaded')
console.log('root element:', document.getElementById('root'))

try {
  const root = ReactDOM.createRoot(document.getElementById('root'))
  console.log('React root created')
  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>,
  )
  console.log('App rendered')
} catch (error) {
  console.error('Error rendering app:', error)
}

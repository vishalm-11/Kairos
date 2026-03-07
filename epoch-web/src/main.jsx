import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'
import { Ion } from 'cesium'

// Set Cesium token
const cesiumToken = import.meta.env.VITE_CESIUM_TOKEN
if (cesiumToken) {
  Ion.defaultAccessToken = cesiumToken
} else {
  console.warn('VITE_CESIUM_TOKEN not set. Cesium may not work properly.')
}

// Set Cesium base URL for assets
window.CESIUM_BASE_URL = '/cesium'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)

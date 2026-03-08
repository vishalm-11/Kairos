import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 30000,
})

export const getCountryData = (country) =>
  api.get(`/country/${encodeURIComponent(country)}`).then(r => r.data)

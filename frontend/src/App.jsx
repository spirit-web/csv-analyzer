// Hämtar verktyg från React
// useState är en React funktion som håller data trots att man uppdaterar skärmen
// useEffect är en React funktion som kör kod automatiskt när komponenten laddas
// axios är ett bibliotek för HTTP request där axios.get() motsvarar GET-requesten
import { useState, useEffect } from "react"
import axios from "axios"

// State variabler är det unika med React som uppdaterar skärmen
// useState([skapar variabeln observations som är en tom lista])
// setObservations är en funktion som uppdaterar listan
function App() {
  const [observations, setObservations] = useState ([])

  // useEffect (() 0> {...}, []) kör koden när sidan laddas
  // axios.get skickar en GET request till vår backend
  // setObservations(response.data) sparar listan med observationer i state vilket gör att React uppdatera skärmen
  useEffect(() => {
    axios.get("http://localhost:8000/observations/")
      .then(response => setObservations(response.data))
  }, [])

  // .map() loopar igenom listan och skapar ett HTML element för varje observation
  // key={obs.id} = React behöver ett id för varje element i en listan
  return (
    <div>
      <h1>CSV Analyzer</h1>
      {observations.map(obs => (
        <div key={obs.id}>
          <strong>{obs.filnamn}</strong>
          <p>{obs.anteckning}</p>
        </div>
      ))}
    </div>
  )
}

export default App

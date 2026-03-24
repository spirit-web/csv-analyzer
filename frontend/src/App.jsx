// Importerar useState och useEffect från React
// useState — håller data som uppdaterar skärmen automatiskt när den ändras
// useEffect — kör kod automatiskt när sidan laddas
import { useState, useEffect } from "react"
// axios — bibliotek för HTTP-requests mot backend
import axios from "axios"

function App() {
  // observations — lista med alla observationer från databasen
  const [observations, setObservations] = useState([])
  // filnamn — texten användaren skriver i filnamn-fältet
  const [filnamn, setFilnamn] = useState("")
  // anteckning — texten användaren skriver i antecknings-fältet
  const [anteckning, setAnteckning] = useState("")

  // Hämtar alla observationer från backend med GET-request
  // Sparar resultatet i observations-state så listan uppdateras på skärmen
  async function hamtaObservationer() {
    const svar = await axios.get("http://localhost:8000/observations/")
    setObservations(svar.data)
  }

  // Kör hamtaObservationer en gång när sidan laddas
  // Den tomma listan [] betyder "kör bara en gång, inte vid varje uppdatering"
  useEffect(() => {
    hamtaObservationer()
  }, [])

  // Skickar POST-request till backend när formuläret skickas
  // e.preventDefault() stoppar sidan från att laddas om vid formulärskickning
  // Efter skapandet töms fälten och listan hämtas på nytt
  async function skapaObservation(e) {
    e.preventDefault()
    await axios.post("http://localhost:8000/observations/", {
      filnamn:    filnamn,
      anteckning: anteckning
    })
    setFilnamn("")
    setAnteckning("")
    hamtaObservationer()
  }

  // Skickar DELETE-request till backend med observationens id
  // ${id} sätter in id-numret direkt i URL:en, t.ex. /observations/3
  // Hämtar sedan listan på nytt så den borttagna försvinner från skärmen
  async function taBortObservation(id) {
    await axios.delete(`http://localhost:8000/observations/${id}`)
    hamtaObservationer()
  }

  return (
    <div>
      <h1>CSV Analyzer</h1>

      {/* Formulär för att skapa ny observation */}
      {/* onSubmit kör skapaObservation när användaren klickar på knappen */}
      <form onSubmit={skapaObservation}>

        {/* value={filnamn} kopplar fältet till React-state */}
        {/* onChange uppdaterar state varje gång användaren skriver ett tecken */}
        <input
          placeholder="Filnamn"
          value={filnamn}
          onChange={e => setFilnamn(e.target.value)}
        />
        <input
          placeholder="Anteckning"
          value={anteckning}
          onChange={e => setAnteckning(e.target.value)}
        />
        <button type="submit">Skapa observation</button>
      </form>

      {/* Loopar igenom listan och visar varje observation */}
      {/* key={obs.id} krävs av React för att hålla koll på varje element i listan */}
      {observations.map(obs => (
        <div key={obs.id}>
          <strong>{obs.filnamn}</strong>
          <p>{obs.anteckning}</p>
          {/* onClick anropar taBortObservation med just den här observationens id */}
          <button onClick={() => taBortObservation(obs.id)}>
            Ta bort
          </button>
        </div>
      ))}
    </div>
  )
}

export default App
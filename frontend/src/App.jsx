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
  // redigeraId håller ID numret för den observation som redigeras just nu
  // null betyder att inget redigeras och att vi är i ett skapa nytt läge
  const [redigeraId, setRedigeraId] = useState(null)
  // statistik - som håller JSON från analysen
  const [statistik, setStatistik] = useState(null)
  // histogram som håller URL till bilden från analysen
  const [histogram, setHistogram] = useState(null)

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

// Hanterar både POST (skapa ny) och PUT (uppdatera befintlig)
// Om redigeraId är null skapas en ny observation
// Om redigeraId har ett värde uppdateras den observationen
async function skapaEllerUppdateraObservation(e) {
  e.preventDefault()

  if (redigeraId) {
    // PUT — uppdatera befintlig observation
    // Template literal sätter in redigeraId i URL:en, ex. /observations/3
    await axios.put(`http://localhost:8000/observations/${redigeraId}`, {
      filnamn:    filnamn,
      anteckning: anteckning
    })
    // Återställ till "skapa nytt"-läge efter uppdatering
    setRedigeraId(null)
  } else {
    // POST — skapa ny observation
    await axios.post("http://localhost:8000/observations/", {
      filnamn:    filnamn,
      anteckning: anteckning
    })
  }

  // Töm formulärfälten och hämta uppdaterad lista oavsett POST eller PUT
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

  // Fyller i formuläret med befintliga värden när användaren klickar "Redigera"
  // setRedigeraId sparar vilket id som redigeras så PUT-requesten vet vilken rad som ska uppdateras
  function startaRedigering(obs) {
    setFilnamn(obs.filnamn)
    setAnteckning(obs.anteckning)
    setRedigeraId(obs.id)
  }
  // Hanterar CSV uppladdningen
  async function analyseraCSV(e) {
    const fil = e.target.files[0]
    if (!fil) return

    const form = new FormData()
    form.append("fil", fil)

    // Hämtar statistik som JSON
    const statsvar = await axios.post(
      "http://localhost:8000/analysis/statistics", form
    )
    setStatistik(statsvar.data)

    // Hämtar histogram som en bild
    const bildsvar = await axios.post(
      "http://localhost:8000/analysis/histogram", form,
      { responseType: "blob" }
    )
    setHistogram(URL.createObjectURL(bildsvar.data))
  }

  return (
  <div>
    <h1>CSV Analyzer</h1>

    {/* Formulärets rubrik ändras beroende på läge */}
    {/* Om redigeraId finns visar vi "Redigera" annars "Ny observation" */}
    <h2>{redigeraId ? "Redigera observation" : "Ny observation"}</h2>

    {/* onSubmit kör nu skapaEllerUppdateraObservation */}
    <form onSubmit={skapaEllerUppdateraObservation}>
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

      {/* Knappens text ändras också beroende på läge */}
      <button type="submit">
        {redigeraId ? "Spara ändringar" : "Skapa observation"}
      </button>

      {/* Avbryt-knapp visas bara när man redigerar */}
      {/* Återställer formuläret till "skapa nytt"-läge utan att spara */}
      {redigeraId && (
        <button type="button" onClick={() => {
          setRedigeraId(null)
          setFilnamn("")
          setAnteckning("")
        }}>
          Avbryt
        </button>
      )}
    </form>
    {/* Fil-upload för CSV-analys */}
{/* onChange körs direkt när användaren väljer en fil */}
<div>
  <h2>Analysera CSV</h2>
  <input
    type="file"
    accept=".csv"
    onChange={analyseraCSV}
  />
</div>

{/* Visar statistik om den finns */}
{statistik && (
  <div>
    <h3>Statistik</h3>
    <p>Rader: {statistik.radata.rader}</p>
    <p>Kolumner: {statistik.radata.namn.join(", ")}</p>
    <p>Saknade värden: {JSON.stringify(statistik.datarening.saknade_varden)}</p>
    <p>Duplikat: {statistik.datarening.duplikat}</p>
  </div>
)}

{/* Visar histogram-bilden om den finns */}
{/* histogram-state håller en URL som <img> kan visa direkt */}
{histogram && (
  <img
    src={histogram}
    alt="Histogram"
    style={{ width: "100%", marginTop: "1rem" }}
  />
)}

    {/* Lista med observationer */}
    {observations.map(obs => (
      <div key={obs.id}>
        <strong>{obs.filnamn}</strong>
        <p>{obs.anteckning}</p>

        {/* Redigera-knapp skickar hela obs-objektet till startaRedigering */}
        <button onClick={() => startaRedigering(obs)}>
          Redigera
        </button>

        {/* Ta bort-knapp skickar bara obs.id till taBortObservation */}
        <button onClick={() => taBortObservation(obs.id)}>
          Ta bort
        </button>
      </div>
    ))}
  </div>
)
}

export default App
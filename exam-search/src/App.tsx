import React, { useState } from 'react'
import ExamRow from './components/ExamRow'

interface Exam {
  course_code: string
  exam_type: string
  start_time: string | null
  end_time: string | null
  location: string | null
}

function App() {
  const [exams, setExams] = useState<Exam[]>([])
  const [searchTerm, setSearchTerm] = useState('')
  const [loading, setLoading] = useState(false)
  const [searched, setSearched] = useState(false)

  const fetchExams = async (course_code: string) => {
    setLoading(true)
    const url = `https://exam-worker.max-51a.workers.dev/exams?course_code=${encodeURIComponent(course_code)}`
    const res = await fetch(url)
    const data = await res.json()
    setExams(data)
    setLoading(false)
    setSearched(true)
  }

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (searchTerm.trim()) {
      fetchExams(searchTerm.trim())
    }
  }

  return (
    <div className="min-h-screen bg-base-200 p-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6 text-center">Exam Search</h1>
        
        <form onSubmit={handleSearch} className="flex gap-2 justify-center mb-6">
          <input
            type="text"
            placeholder="Enter course code"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="input input-bordered w-full max-w-sm"
          />
          <button className="btn btn-primary px-6">Search</button>
        </form>

        {loading && (
          <div className="flex justify-center">
            <span className="loading loading-spinner text-primary" />
          </div>
        )}

        {!loading && searched && exams.length === 0 && (
          <div className="alert alert-warning shadow-lg mt-4 justify-center">
            <span>No exams found</span>
          </div>
        )}

        {!loading && exams.length > 0 && (
          <div className="overflow-x-auto">
            <table className="table table-zebra w-full shadow-lg">
              <thead>
                <tr>
                  <th>Course Code</th>
                  <th>Exam Type</th>
                  <th>Start Time</th>
                  <th>End Time</th>
                  <th>Location</th>
                  <th>Calendars</th>
                </tr>
              </thead>
              <tbody>
                {exams.map((exam, idx) => (
                  <ExamRow key={idx} exam={exam} />
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}

export default App

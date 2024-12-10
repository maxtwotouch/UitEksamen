import React from 'react'
import { FaGoogle, FaMicrosoft } from 'react-icons/fa'

interface Exam {
  course_code: string
  exam_type: string
  start_time: string | null
  end_time: string | null
  location: string | null
}

interface ExamRowProps {
  exam: Exam
}

function parseDateTime(dateStr: string): Date {
  return new Date(dateStr.replace(' ', 'T'))
}

function formatForGoogleCalendar(date: Date): string {
  const year = date.getUTCFullYear()
  const month = String(date.getUTCMonth() + 1).padStart(2, '0')
  const day = String(date.getUTCDate()).padStart(2, '0')
  const hours = String(date.getUTCHours()).padStart(2, '0')
  const minutes = String(date.getUTCMinutes()).padStart(2, '0')
  const seconds = String(date.getUTCSeconds()).padStart(2, '0')
  return `${year}${month}${day}T${hours}${minutes}${seconds}Z`
}

function formatForOutlook(date: Date): string {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')
  return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`
}

const ExamRow: React.FC<ExamRowProps> = ({ exam }) => {
  const title = `Exam: ${exam.course_code}`
  const location = exam.location || ''
  const details = `Exam Type: ${exam.exam_type}`

  if (!exam.start_time) {
    // If there's no start_time, we cannot create event links
    return (
      <tr>
        <td>{exam.course_code}</td>
        <td>{exam.exam_type}</td>
        <td>{exam.start_time || ''}</td>
        <td>{exam.end_time || ''}</td>
        <td>{exam.location}</td>
        <td></td>
      </tr>
    )
  }

  const startDate = parseDateTime(exam.start_time)
  
  let endDate: Date
  if (exam.end_time) {
    endDate = parseDateTime(exam.end_time)
  } else {
    // Default 2-hour event if no end_time
    endDate = new Date(startDate.getTime() + 4 * 60 * 60 * 1000)
  }

  const googleStart = formatForGoogleCalendar(startDate)
  const googleEnd = formatForGoogleCalendar(endDate)
  const outlookStart = formatForOutlook(startDate)
  const outlookEnd = formatForOutlook(endDate)

  const googleLink = `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${encodeURIComponent(
    title
  )}&dates=${googleStart}/${googleEnd}&location=${encodeURIComponent(
    location
  )}&details=${encodeURIComponent(details)}`

  const outlookLink = `https://outlook.live.com/calendar/0/deeplink/compose?path=/calendar/action/compose&rru=addevent&startdt=${encodeURIComponent(
    outlookStart
  )}&enddt=${encodeURIComponent(outlookEnd)}&subject=${encodeURIComponent(
    title
  )}&location=${encodeURIComponent(location)}&body=${encodeURIComponent(details)}`

  return (
    <tr>
      <td>{exam.course_code}</td>
      <td>{exam.exam_type}</td>
      <td>{exam.start_time}</td>
      <td>{exam.end_time}</td>
      <td>{exam.location}</td>
      <td>
        <div className="flex flex-col items-start gap-2">
          <span className="text-sm font-semibold">Add to calendar:</span>
          <div className="flex gap-4 items-center">
            {/* Google Calendar Icon with Tooltip */}
            <div className="tooltip" data-tip="Add to Google Calendar">
              <a
                href={googleLink}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-sm btn-circle btn-ghost text-red-500 hover:bg-red-100"
              >
                <FaGoogle size={18} />
              </a>
            </div>

            {/* Outlook Calendar Icon with Tooltip */}
            <div className="tooltip" data-tip="Add to Outlook Calendar">
              <a
                href={outlookLink}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-sm btn-circle btn-ghost text-blue-500 hover:bg-blue-100"
              >
                <FaMicrosoft size={18} />
              </a>
            </div>
          </div>
        </div>
      </td>
    </tr>
  )
}

export default ExamRow

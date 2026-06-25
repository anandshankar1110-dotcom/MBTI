// load QUESTIONS from JSON blob inserted by the template
const QUESTIONS = JSON.parse(document.getElementById('questions-data')?.textContent || '[]')

let current = 0
let answers = []
const total = QUESTIONS.length
const totalEl = document.getElementById('total')
const qnum = document.getElementById('qnum')
const questionBox = document.getElementById('questionBox')
const startBtn = document.getElementById('startBtn')
const testDiv = document.getElementById('test')
const introForm = document.getElementById('intro-form')
const resultDiv = document.getElementById('result')
const resultLinks = document.getElementById('resultLinks')
const btnA = document.getElementById('btnA')
const btnB = document.getElementById('btnB')

if (totalEl) {
  totalEl.innerText = total
}

if (startBtn) {
  startBtn.addEventListener('click', () => {
    const name = document.getElementById('name')?.value.trim() || ''
    const dob = document.getElementById('dob')?.value.trim() || ''
    const gender = document.getElementById('gender')?.value || ''

    if (name.length < 2) {
      alert('Please enter your name.')
      return
    }
    if (!dob) {
      alert('Please enter your date of birth.')
      return
    }
    if (!gender) {
      alert('Please select your gender.')
      return
    }

    if (introForm) introForm.classList.add('hidden')
    if (testDiv) testDiv.classList.remove('hidden')
    answers = []
    current = 0
    showQuestion()
  })
} else {
  console.warn('Start button not found in DOM')
}

function showQuestion() {
  if (!questionBox || !qnum) return

  qnum.innerText = current + 1
  const q = QUESTIONS[current]
  if (!q) {
    questionBox.innerText = 'No question available.'
    return
  }

  questionBox.innerHTML = `
    <strong>${q[0]}</strong>
    <div style="margin-top:12px">
      <div><strong>A:</strong> ${q[1]}</div>
      <div style="margin-top:8px"><strong>B:</strong> ${q[2]}</div>
    </div>
  `
}

function recordAndNext(choice) {
  answers.push(choice)
  current++
  if (current >= total) {
    submitAnswers()
  } else {
    showQuestion()
  }
}

if (btnA) {
  btnA.addEventListener('click', () => recordAndNext('a'))
}
if (btnB) {
  btnB.addEventListener('click', () => recordAndNext('b'))
}

async function submitAnswers() {
  const name = document.getElementById('name')?.value.trim() || ''
  const dob = document.getElementById('dob')?.value.trim() || ''
  const gender = document.getElementById('gender')?.value || ''

  const payload = { name, dob, gender, answers }
  const res = await fetch('/api/assess', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })

  if (!res.ok) {
    const txt = await res.text()
    alert('Error: ' + txt)
    return
  }

  const data = await res.json()
  showResult(data)
}

function showResult(data) {
  document.getElementById('rname').innerText = data.name || ''
  document.getElementById('ptype').innerText = data.pcode || ''
  document.getElementById('conf').innerText = data.confidence || ''
  document.getElementById('career').innerText = data.career || ''

  if (testDiv) testDiv.classList.add('hidden')
  if (resultDiv) resultDiv.classList.remove('hidden')
  if (resultLinks) resultLinks.innerHTML = ''

  if (data.pdf) {
    const byteCharacters = atob(data.pdf)
    const byteNumbers = new Array(byteCharacters.length)
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i)
    }
    const byteArray = new Uint8Array(byteNumbers)
    const blob = new Blob([byteArray], { type: 'application/pdf' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = data.pdf_filename || 'MBTI_Report.pdf'
    link.innerText = 'Download PDF report'
    link.className = 'btn primary'
    link.style.display = 'inline-block'
    link.style.marginTop = '10px'
    if (resultLinks) resultLinks.appendChild(link)
  }

  if (data.serial) {
    const s = document.createElement('div')
    s.innerText = 'Report Serial: ' + data.serial
    s.style.marginTop = '10px'
    if (resultLinks) resultLinks.appendChild(s)
  }

  if (data.report_url) {
    const rlink = document.createElement('a')
    rlink.href = data.report_url
    rlink.innerText = 'Open report (via QR/link)'
    rlink.target = '_blank'
    rlink.className = 'btn ghost'
    rlink.style.display = 'inline-block'
    rlink.style.marginTop = '10px'
    rlink.style.marginLeft = '12px'
    if (resultLinks) resultLinks.appendChild(rlink)
  }
}

// top-nav behavior: reveal sections and contact details only when clicked
document.addEventListener('DOMContentLoaded', () => {
  const links = document.querySelectorAll('.top-nav a')
  links.forEach(a => {
    a.addEventListener('click', (e) => {
      e.preventDefault()
      const href = a.getAttribute('href')
      if (!href || !href.startsWith('#')) return
      const target = document.querySelector(href)
      if (!target) return

      const details = target.querySelector('.details')
      if (details) {
        if (details.classList.contains('collapsed')) {
          details.classList.remove('collapsed')
          details.classList.add('show')
        } else if (details.classList.contains('show')) {
          details.classList.remove('show')
          details.classList.add('collapsed')
        } else {
          details.classList.add('show')
        }
      }

      target.scrollIntoView({ behavior: 'smooth', block: 'start' })
    })
  })
})

document.querySelectorAll('.lang-btn').forEach(b => {
  b.addEventListener('click', () => {
    const lang = b.getAttribute('data-lang')
    localStorage.setItem('mbti_lang', lang)
    window.location.href = '/'
  })
})

const feedbackForm = document.getElementById('feedbackForm')
const feedbackStatus = document.getElementById('feedbackStatus')

if (feedbackForm) {
  feedbackForm.addEventListener('submit', function (e) {
    e.preventDefault()
    if (feedbackStatus) feedbackStatus.innerText = 'Submitting...'
    setTimeout(() => {
      window.location.href = '/thankyou'
    }, 600)
  })
}

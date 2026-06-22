// load QUESTIONS from JSON blob inserted by the template
const QUESTIONS = JSON.parse(document.getElementById('questions-data').textContent || '[]')

let current = 0
let answers = []
const total = QUESTIONS.length
const totalEl = document.getElementById('total')
if (totalEl) totalEl.innerText = total

const startBtn = document.getElementById('startBtn')
const testDiv = document.getElementById('test')
// updated id in template: intro-form
const intro = document.getElementById('intro-form') || document.getElementById('intro')
const qnum = document.getElementById('qnum')
const questionBox = document.getElementById('questionBox')
const btnA = document.getElementById('btnA')
const btnB = document.getElementById('btnB')

if (startBtn) {
  startBtn.addEventListener('click', ()=>{
  const name = document.getElementById('name').value.trim()
  if(!name || name.length<2){alert('Enter a valid name');return}
    // guard for missing elements
    if (intro) intro.classList.add('hidden')
    if (testDiv) testDiv.classList.remove('hidden')
  showQuestion()
  })
} else {
  console.warn('Start button not found in DOM')
}

function showQuestion(){
  qnum.innerText = current+1
  const q = QUESTIONS[current]
  questionBox.innerHTML = `<strong>${q[0]}</strong><div style="margin-top:8px">A. ${q[1]}<br>B. ${q[2]}</div>`
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

      // If target has .details that are hidden (like contact), reveal them
      const details = target.querySelector('.details')
      if (details) {
        // toggle collapsed/show classes for animated reveal/hide
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

      // Smooth scroll to section
      target.scrollIntoView({behavior: 'smooth', block: 'start'})
    })
  })
})

function recordAndNext(choice){
  answers.push(choice)
  current++
  if(current>=total){
    submitAnswers()
  } else {
    showQuestion()
  }
}

btnA.addEventListener('click', ()=>recordAndNext('a'))
btnB.addEventListener('click', ()=>recordAndNext('b'))

async function submitAnswers(){
  const payload = {
    name: document.getElementById('name').value.trim(),
    dob: document.getElementById('dob').value.trim(),
    gender: document.getElementById('gender').value,
    answers
  }
  const res = await fetch('/api/assess', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})
  if(!res.ok){
    const txt = await res.text()
    alert('Error: '+txt)
    return
  }
  const data = await res.json()
  showResult(data)
}

function showResult(data){
  document.getElementById('rname').innerText = data.name || ''
  document.getElementById('ptype').innerText = data.pcode || ''
  document.getElementById('conf').innerText = data.confidence || ''
  document.getElementById('career').innerText = data.career || ''
  testDiv.classList.add('hidden')
  document.getElementById('result').classList.remove('hidden')
  if(data.pdf){
    const pdfBytes = atob(data.pdf)
    const len = pdfBytes.length
    const u8 = new Uint8Array(len)
    for (let i = 0; i < len; i++) {
      u8[i] = pdfBytes.charCodeAt(i)
    }
    const blob = new Blob([u8], { type: 'application/pdf' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = data.pdf_filename || 'MBTI_Report.pdf'
    link.innerText = 'Download PDF report'
    link.style.display = 'inline-block'
    link.style.marginTop = '10px'
    document.getElementById('result').appendChild(link)
  }
  if(data.serial){
    const s = document.createElement('div')
    s.innerText = 'Report Serial: ' + data.serial
    s.style.marginTop = '8px'
    document.getElementById('result').appendChild(s)
  }
  if(data.report_url){
    const rlink = document.createElement('a')
    rlink.href = data.report_url
    rlink.innerText = 'Open report (via QR/link)'
    rlink.target = '_blank'
    rlink.style.display = 'inline-block'
    rlink.style.marginLeft = '12px'
    document.getElementById('result').appendChild(rlink)
  }
}

document.querySelectorAll('.lang-btn').forEach(b=>{
        b.addEventListener('click', ()=>{
        const lang = b.getAttribute('data-lang')
        localStorage.setItem('mbti_lang', lang)
          // go back to home
        window.location.href = '/'
        })
    })

// ================== FEEDBACK PAGE FORM ==================
//const feedbackForm = document.getElementById("feedbackForm");
//const feedbackStatus = document.getElementById("feedbackStatus");

//if (feedbackForm) {
  //feedbackForm.addEventListener("submit", function (e) {
    //e.preventDefault();

    //feedbackStatus.innerText = "✅ Thanks! Feedback submitted successfully.";
    //feedbackForm.reset();
  //});
//}

// ================== FEEDBACK PAGE FORM ==================

const feedbackForm = document.getElementById("feedbackForm");
const feedbackStatus = document.getElementById("feedbackStatus");

if (feedbackForm) {
  feedbackForm.addEventListener("submit", function (e) {
    e.preventDefault();

    if (feedbackStatus) feedbackStatus.innerText = "Submitting...";

    setTimeout(() => {
      window.location.href = "/thankyou";
    }, 600);
  });
}

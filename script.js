/**
 * script.js — AI Resume Analyzer
 * Handles: drag-drop upload, loading overlay, animated counters,
 *          score ring, progress bars, Chart.js pie chart
 */

// ── Upload Zone ──────────────────────────────────────────────────────────────

const dropZone  = document.getElementById('dropZone');
const fileInput = document.getElementById('resumeFile');
const filePreview = document.getElementById('filePreview');
const fileNameEl  = document.getElementById('fileName');
const fileSizeEl  = document.getElementById('fileSize');

if (dropZone && fileInput) {

  // Drag events
  ['dragenter','dragover'].forEach(evt => {
    dropZone.addEventListener(evt, e => {
      e.preventDefault();
      dropZone.classList.add('dragover');
    });
  });

  ['dragleave','drop'].forEach(evt => {
    dropZone.addEventListener(evt, () => dropZone.classList.remove('dragover'));
  });

  dropZone.addEventListener('drop', e => {
    e.preventDefault();
    const files = e.dataTransfer?.files;
    if (files && files.length > 0) {
      fileInput.files = files;          // assign dropped files to input
      showFilePreview(files[0]);
    }
  });

  fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) showFilePreview(fileInput.files[0]);
  });

  function showFilePreview(file) {
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      showToast('Only PDF files are accepted.', 'danger');
      fileInput.value = '';
      filePreview.classList.remove('show');
      return;
    }
    fileNameEl.textContent = file.name;
    fileSizeEl.textContent = formatBytes(file.size);
    filePreview.classList.add('show');
  }

  function formatBytes(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  }
}

// ── Form Submit → Loading Overlay ────────────────────────────────────────────

const analyzeForm    = document.getElementById('analyzeForm');
const loadingOverlay = document.getElementById('loadingOverlay');

const loadingMessages = [
  { text: 'Extracting text from PDF…',         delay: 0    },
  { text: 'Running NLP skill analysis…',       delay: 900  },
  { text: 'Calculating match score…',          delay: 1800 },
  { text: 'Generating AI suggestions…',        delay: 2700 },
];

if (analyzeForm && loadingOverlay) {
  analyzeForm.addEventListener('submit', function(e) {
    const file = fileInput?.files[0];
    const role = document.getElementById('jobRole')?.value;

    if (!file) {
      e.preventDefault();
      showToast('Please upload your resume PDF first.', 'warning');
      return;
    }
    if (!role) {
      e.preventDefault();
      showToast('Please select a target job role.', 'warning');
      return;
    }

    // Show loading overlay
    loadingOverlay.classList.add('active');
    const stepsContainer = document.getElementById('loadingSteps');

    loadingMessages.forEach(msg => {
      setTimeout(() => {
        if (stepsContainer) {
          const step = document.createElement('div');
          step.className = 'loading-step done';
          step.innerHTML = `<i class="fas fa-check-circle me-2"></i>${msg.text}`;
          stepsContainer.appendChild(step);
        }
      }, msg.delay);
    });
  });
}

// ── Score Ring Animation ──────────────────────────────────────────────────────

function animateScoreRing() {
  const ring  = document.querySelector('.score-ring-fill');
  const numEl = document.querySelector('.score-number');

  if (!ring || !numEl) return;

  const score      = parseInt(ring.dataset.score) || 0;
  const circumference = 502; // 2 * π * r (r ≈ 80)
  const offset     = circumference - (score / 100) * circumference;

  // Ring colour
  const color = score >= 80 ? '#22c55e'
              : score >= 60 ? '#38bdf8'
              : score >= 40 ? '#f59e0b'
              :               '#ef4444';

  ring.style.stroke = color;

  setTimeout(() => {
    ring.style.strokeDashoffset = offset;
  }, 300);

  // Animated counter
  let current = 0;
  const duration = 1500;
  const step = score / (duration / 16);

  const timer = setInterval(() => {
    current = Math.min(current + step, score);
    numEl.textContent = Math.round(current) + '%';
    if (current >= score) clearInterval(timer);
  }, 16);
}

// ── Progress Bars ────────────────────────────────────────────────────────────

function animateProgressBars() {
  document.querySelectorAll('.progress-fill[data-width]').forEach(bar => {
    const target = bar.dataset.width;
    setTimeout(() => { bar.style.width = target; }, 400);
  });
}

// ── Staggered Badge Animation ─────────────────────────────────────────────────

function staggerBadges() {
  document.querySelectorAll('.skill-badge').forEach((badge, i) => {
    badge.style.animationDelay = `${i * 60}ms`;
  });
}

// ── Pie Chart (Chart.js) ──────────────────────────────────────────────────────

function initSkillChart() {
  const canvas = document.getElementById('skillChart');
  if (!canvas || typeof Chart === 'undefined') return;

  const matched = parseInt(canvas.dataset.matched) || 0;
  const missing = parseInt(canvas.dataset.missing) || 0;
  const extra   = parseInt(canvas.dataset.extra)   || 0;

  new Chart(canvas, {
    type: 'doughnut',
    data: {
      labels: ['Matched Skills', 'Missing Skills', 'Extra Skills'],
      datasets: [{
        data: [matched, missing, extra],
        backgroundColor: ['#22c55e', '#ef4444', '#38bdf8'],
        borderColor: ['#080b10'],
        borderWidth: 3,
        hoverOffset: 6,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '68%',
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            color: '#7a8ba0',
            font: { family: 'Space Grotesk', size: 11 },
            padding: 16,
            usePointStyle: true,
            pointStyleWidth: 8,
          },
        },
        tooltip: {
          backgroundColor: '#0e1420',
          borderColor: 'rgba(255,255,255,0.07)',
          borderWidth: 1,
          titleColor: '#e8edf5',
          bodyColor: '#7a8ba0',
          padding: 12,
        },
      },
    },
  });
}

// ── Toast Notifications ───────────────────────────────────────────────────────

function showToast(message, type = 'info') {
  const colors = {
    info:    { bg: 'rgba(56,189,248,.12)',  border: 'rgba(56,189,248,.3)',  text: '#7dd3fc', icon: 'fa-circle-info' },
    success: { bg: 'rgba(34,197,94,.12)',   border: 'rgba(34,197,94,.3)',   text: '#86efac', icon: 'fa-circle-check' },
    warning: { bg: 'rgba(245,158,11,.12)',  border: 'rgba(245,158,11,.3)',  text: '#fcd34d', icon: 'fa-triangle-exclamation' },
    danger:  { bg: 'rgba(239,68,68,.12)',   border: 'rgba(239,68,68,.3)',   text: '#fca5a5', icon: 'fa-circle-xmark' },
  };
  const c = colors[type] || colors.info;

  const toast = document.createElement('div');
  toast.style.cssText = `
    position:fixed; bottom:24px; right:24px; z-index:9999;
    background:${c.bg}; border:1px solid ${c.border}; color:${c.text};
    padding:14px 20px; border-radius:12px; font-size:.875rem;
    display:flex; align-items:center; gap:10px;
    backdrop-filter:blur(12px);
    animation: slideUp .3s ease;
    max-width: 320px;
  `;
  toast.innerHTML = `<i class="fas ${c.icon}"></i><span>${message}</span>`;
  document.body.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity .4s';
    setTimeout(() => toast.remove(), 400);
  }, 3500);
}

// ── Init on DOM Ready ─────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  animateScoreRing();
  animateProgressBars();
  staggerBadges();
  initSkillChart();

  // Auto-dismiss flash messages after 5 s
  document.querySelectorAll('.alert-custom').forEach(el => {
    setTimeout(() => {
      el.style.transition = 'opacity .5s';
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 500);
    }, 5000);
  });
});

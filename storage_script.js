
// --- LOCAL STORAGE LOGIC ---
function saveProgress() {
    const data = {
        edits: {},
        checks: {}
    };

    // Save Content Edits
    document.querySelectorAll('[contenteditable="true"]').forEach((el, index) => {
        data.edits[index] = el.innerText;
    });

    // Save Checks
    document.querySelectorAll('.icon-check').forEach((el, index) => {
        data.checks[index] = el.classList.contains('checked');
    });

    localStorage.setItem('gba_itinerary_v1', JSON.stringify(data));
}

function loadProgress() {
    const saved = localStorage.getItem('gba_itinerary_v1');
    if (!saved) return;

    const data = JSON.parse(saved);

    // Restore Edits
    document.querySelectorAll('[contenteditable="true"]').forEach((el, index) => {
        if (data.edits[index] !== undefined) el.innerText = data.edits[index];

        // Add Listener
        el.addEventListener('input', saveProgress);
    });

    // Restore Checks
    document.querySelectorAll('.icon-check').forEach((el, index) => {
        if (data.checks[index]) {
            el.classList.add('checked', 'fa-solid', 'fa-circle-check');
            el.classList.remove('fa-regular', 'fa-circle');
        }

        // Add Listener
        el.addEventListener('click', () => setTimeout(saveProgress, 100)); // Delay for toggle
    });
}

// --- DATE HIGHLIGHT LOGIC ---
function highlightDate() {
    const dates = {
        "d1": "2026-02-18",
        "d2": "2026-02-19",
        "d3": "2026-02-20",
        "d4": "2026-02-21",
        "d5": "2026-02-22",
        "d6": "2026-02-23"
    };

    const today = new Date().toISOString().split('T')[0];

    for (const [id, dateStr] of Object.entries(dates)) {
        if (today === dateStr) {
            // Find the nav link
            const link = document.querySelector(`a[href="#${id}"]`);
            if (link) {
                // Highlight
                link.classList.remove('bg-white', 'text-gray-700', 'border-gray-200');
                link.classList.add('bg-mag-navy', 'text-white', 'border-mag-navy', 'shadow-md');

                // Scroll nav into view
                link.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });

                // Scroll page to section (Optional, maybe too intrusive on reload?)
                // document.getElementById(id).scrollIntoView({ behavior: 'smooth' });
            }
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadProgress();

    // Init Listeners for fresh elements (if not loaded)
    document.querySelectorAll('[contenteditable="true"]').forEach(el => {
        el.addEventListener('input', saveProgress);
    });
    document.querySelectorAll('.icon-check').forEach(el => {
        el.addEventListener('click', () => setTimeout(saveProgress, 100));
    });

    highlightDate();
});

const API_URL = 'http://localhost:5000/api/releases';

document.addEventListener('DOMContentLoaded', () => {
    fetchReleases();
    document.getElementById('releaseForm').addEventListener('submit', handleFormSubmit);
});

// Create
async function handleFormSubmit(e) {
    e.preventDefault();

    const version = document.getElementById('version').value;
    const title = document.getElementById('title').value;
    const rawNotes = document.getElementById('rawNotes').value;
    
    const submitBtn = document.getElementById('submitBtn');
    const loadingState = document.getElementById('loadingState');
    
    submitBtn.disabled = true;
    loadingState.classList.remove('hidden');

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ version, title, raw_input: rawNotes })
        });

        if (response.ok) {
            document.getElementById('releaseForm').reset();
            await fetchReleases();
        } else {
            alert('Failed to generate release notes. Check backend logs.');
        }
    } catch (error) {
        console.error('Error Submitting Notes', error);
    } finally {
        submitBtn.disabled = false;
        loadingState.classList.add('hidden');
    }
}

// Read
async function fetchReleases() {
    const timeline = document.getElementById('timeline');
    
    try {
        const response = await fetch(API_URL);
        const data = await response.json();
        
        timeline.innerHTML = '';

        if (data.length === 0) {
            timeline.innerHTML = '<p class="empty-msg">No release notes compiled yet.</p>';
            return;
        }

        data.forEach(release => {
            const card = document.createElement('div');
            card.className = `release-card ${release.is_published ? 'published' : 'draft'}`;
            
            // Build structures for changelog categories
            const features = release.changelog.features.map(f => `<li>${f}</li>`).join('');
            const bugFixes = release.changelog.bug_fixes.map(b => `<li>${b}</li>`).join('');
            const maintenance = release.changelog.maintenance.map(m => `<li>${m}</li>`).join('');

            card.innerHTML = `
                <div class="card-header">
                    <h3>${release.version}: ${release.title}</h3>
                    <span class="badge">${release.is_published ? 'Published' : 'Draft'}</span>
                </div>
                <div class="card-body">
                    ${features ? `<h4>🚀 Features</h4><ul>${features}</ul>` : ''}
                    ${bugFixes ? `<h4>🐛 Bug Fixes</h4><ul>${bugFixes}</ul>` : ''}
                    ${maintenance ? `<h4>🔧 Maintenance</h4><ul>${maintenance}</ul>` : ''}
                </div>
                <div class="card-actions">
                    <button onclick="togglePublish('${release._id}', ${release.is_published})">
                        ${release.is_published ? 'Unpublish' : 'Publish'}
                    </button>
                    <button class="delete-btn" onclick="deleteRelease('${release._id}')">Delete</button>
                </div>
            `;
            timeline.appendChild(card);
        });
    } catch (error) {
        console.error('Error fetching timeline:', error);
        timeline.innerHTML = '<p class="error-msg">Error loading deployment data.</p>';
    }
}

// Update
async function togglePublish(id, currentState) {
    try {
        const response = await fetch(`${API_URL}/${id}`,{
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ is_published: !currentState })
        });

        if (response.ok) {
            fetchReleases();
        }
    } catch (error) {
        console.error('Error updating status:', error);
    }
}

// Delete
async function deleteRelease(id) {
    if (!confirm('Are you sure you want to permanently delete this release log?')) return;

    try {
        const response = await fetch(`${API_URL}/${id}`, { method: 'DELETE' });

        if (response.ok) {
            fetchReleases();
        }
    } catch (error) {
        console.error('Error deleting release item:', error);
    }
}
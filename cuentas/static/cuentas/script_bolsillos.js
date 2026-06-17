document.addEventListener('DOMContentLoaded', function() {
    initializeBolsillos();
});

// Inicialización general
function initializeBolsillos() {
    setupSearchFunctionality();
    setupPocketActions();
    // setupNavigationHighlight(); // Asegúrate de tener esta definida si la usas
}

// ============================================
// BÚSQUEDA Y FILTRO
// ============================================

function setupSearchFunctionality() {
    const searchInput = document.getElementById('searchInput');
    const pocketsList = document.getElementById('pocketsList');
    if (!searchInput || !pocketsList) return;

    const pocketItems = pocketsList.querySelectorAll('.pocket-item');

    searchInput.addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        pocketItems.forEach(item => {
            const title = item.querySelector('.pocket-title').textContent.toLowerCase();
            item.style.display = title.includes(searchTerm) ? '' : 'none';
        });
        updateEmptyState(pocketsList);
    });
}

function updateEmptyState(container) {
    const visibleItems = container.querySelectorAll('.pocket-item:not([style*="display: none"])');
    let emptyState = container.querySelector('.empty-state');
    if (visibleItems.length === 0) {
        if (!emptyState) {
            emptyState = document.createElement('div');
            emptyState.className = 'empty-state';
            emptyState.innerHTML = '<p>No hay bolsillos que coincidan con tu búsqueda</p>';
            container.appendChild(emptyState);
        }
    } else if (emptyState) {
        emptyState.remove();
    }
}

// ============================================
// ACCIONES DE BOLSILLOS (CORREGIDO)
// ============================================

function setupPocketActions() {
    const pocketsList = document.getElementById('pocketsList');
    if (!pocketsList) return;

    pocketsList.addEventListener('click', function(e) {
        const addBtn = e.target.closest('.add-pocket-btn');
        const removeBtn = e.target.closest('.remove-pocket-btn');
        const menuBtn = e.target.closest('.pocket-menu-btn');

        if (addBtn) abrirModalAccion(addBtn.dataset.id, 'agregar');
        else if (removeBtn) abrirModalAccion(removeBtn.dataset.id, 'retirar');
        else if (menuBtn) handlePocketMenu(menuBtn);
    });
}

function abrirModalAccion(id, accion) {
    const modal = document.getElementById('modalAccionDinero');
    const pocketIdInput = document.getElementById('pocketIdInput'); 
    const accionInput = document.getElementById('accionInput');
    const title = document.getElementById('modalAccionTitle');

    if (!modal || !pocketIdInput || !accionInput) {
        console.error("Error: Elementos del modal no encontrados en el HTML.");
        return;
    }

    pocketIdInput.value = id;
    accionInput.value = accion;
    title.textContent = accion === 'agregar' ? 'Agregar dinero' : 'Retirar dinero';
    modal.classList.add('active');
}

function cerrarModal(id) {
    const modal = document.getElementById(id);
    if (modal) modal.classList.remove('active');
}

// ============================================
// OTROS MODALES (CREAR BOLSILLO)
// ============================================

const btnCrearBolsillo = document.getElementById('btnCrearBolsillo');
const modalOverlay = document.getElementById('modalOverlay');

if (btnCrearBolsillo && modalOverlay) {
    btnCrearBolsillo.addEventListener('click', () => modalOverlay.classList.add('active'));
    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) modalOverlay.classList.remove('active');
    });
}

// ============================================
// FUNCIONES AUXILIARES
// ============================================

function formatCurrency(value) {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
    }).format(value);
}
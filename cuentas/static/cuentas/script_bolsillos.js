document.addEventListener('DOMContentLoaded', function() {
    initializeBolsillos();
});

// Inicialización general
function initializeBolsillos() {
    setupSearchFunctionality();
    setupPocketActions();
    setupNavigationHighlight();
}

// ============================================
// BÚSQUEDA Y FILTRO
// ============================================

function setupSearchFunctionality() {
    const searchInput = document.getElementById('searchInput');
    const filterBtn = document.querySelector('.filter-btn');
    const pocketsList = document.getElementById('pocketsList');
    const pocketItems = pocketsList.querySelectorAll('.pocket-item');

    // Búsqueda por nombre
    searchInput.addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();

        pocketItems.forEach(item => {
            const title = item.querySelector('.pocket-title').textContent.toLowerCase();
            if (title.includes(searchTerm)) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });

        // Mensaje si no hay resultados
        updateEmptyState(pocketsList);
    });

    // Botón de filtro (placeholder para futura funcionalidad)
    filterBtn.addEventListener('click', function() {
        console.log('Filtro activado');
    });
}

// Actualizar estado vacío
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
// ACCIONES DE BOLSILLOS
// ============================================

function setupPocketActions() {
    const pocketsList = document.getElementById('pocketsList');
    if (!pocketsList) return;

    pocketsList.addEventListener('click', function(e) {
        const addBtn = e.target.closest('.add-pocket-btn');
        const removeBtn = e.target.closest('.remove-pocket-btn');
        const menuBtn = e.target.closest('.pocket-menu-btn');

        if (addBtn) handleAddMoney(addBtn);
        else if (removeBtn) handleRemoveMoney(removeBtn);
        else if (menuBtn) handlePocketMenu(menuBtn);
    });
}

function handleAddMoney(button) {
    const pocketItem = button.closest('.pocket-item');
    const pocketTitle = pocketItem.querySelector('.pocket-title').textContent;
    alert(`Agregar dinero al bolsillo: ${pocketTitle}`);
}

function handleRemoveMoney(button) {
    const pocketItem = button.closest('.pocket-item');
    const pocketTitle = pocketItem.querySelector('.pocket-title').textContent;
    alert(`Retirar dinero del bolsillo: ${pocketTitle}`);
}

function handlePocketMenu(button) {
    const pocketItem = button.closest('.pocket-item');
    const pocketTitle = pocketItem.querySelector('.pocket-title').textContent;
    const menu = ['Ver detalles', 'Editar bolsillo', 'Ver historial', 'Eliminar bolsillo'];
    const option = prompt(
        `Opciones para ${pocketTitle}:\n\n${menu.map((m, i) => `${i + 1}. ${m}`).join('\n')}`, '1'
    );
    if (option) {
        const selectedOption = parseInt(option);
        if (selectedOption >= 1 && selectedOption <= menu.length) {
            console.log(`Seleccionado: ${menu[selectedOption - 1]}`);
        }
    }
}

// ============================================
// MODAL CREAR BOLSILLO
// ============================================

const btnCrearBolsillo = document.getElementById('btnCrearBolsillo');
const modalOverlay = document.getElementById('modalOverlay');
const modalClose = document.getElementById('modalClose');
const btnCancelar = document.getElementById('btnCancelar');

if (btnCrearBolsillo) {
    btnCrearBolsillo.addEventListener('click', () => {
        modalOverlay.classList.add('active');
    });
}

if (modalClose) {
    modalClose.addEventListener('click', () => {
        modalOverlay.classList.remove('active');
    });
}

if (btnCancelar) {
    btnCancelar.addEventListener('click', () => {
        modalOverlay.classList.remove('active');
    });
}

if (modalOverlay) {
    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) {
            modalOverlay.classList.remove('active');
        }
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

function calculatePercentage(current, total) {
    return Math.round((current / total) * 100);
}

// ============================================
// INIT
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    setupPocketActions();
});
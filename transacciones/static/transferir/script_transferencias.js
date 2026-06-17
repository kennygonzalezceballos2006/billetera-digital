document.addEventListener('DOMContentLoaded', function() {
    initializeTransferencias();
});

function initializeTransferencias() {
    setupSearch();
    setupFilterButton();
    setupHeaderButtons();
}

function setupSearch() {
    const searchInput = document.getElementById('searchInput');
    const transferRows = document.querySelectorAll('.transfer-row');

    searchInput.addEventListener('input', function(e) {
        const query = e.target.value.toLowerCase().trim();
        let visibleCount = 0;

        transferRows.forEach(row => {
            const contact = row.querySelector('.transfer-contact .movement-title').textContent.toLowerCase();
            const details = row.querySelector('.transfer-contact .movement-detail').textContent.toLowerCase();
            const type = row.querySelector('.movement-info:nth-child(3) .movement-title').textContent.toLowerCase();
            const amount = row.querySelector('.amount-value').textContent.toLowerCase();

            const matches = contact.includes(query) || details.includes(query) || type.includes(query) || amount.includes(query);
            row.style.display = matches ? '' : 'none';
            if (matches) visibleCount++;
        });

        updateEmptyState(visibleCount);
    });
}

function setupFilterButton() {
    const filterBtn = document.querySelector('.filter-btn');
    filterBtn.addEventListener('click', function() {
        console.log('Filtro activado');
        alert('Abrir panel de filtros');
    });
}

function setupHeaderButtons() {
    const addBtn = document.querySelector('.add-btn');
    const notificationBtn = document.querySelector('.notification-btn');

    if (addBtn) {
        addBtn.addEventListener('click', function() {
            console.log('Nueva transferencia');
            alert('Abrir formulario para nueva transferencia');
        });
    }

    if (notificationBtn) {
        notificationBtn.addEventListener('click', function() {
            console.log('Notificaciones');
            alert('Ver notificaciones');
        });
    }
}

function updateEmptyState(visibleCount) {
    const transfersList = document.getElementById('transfersList');
    let emptyState = document.querySelector('.empty-state');

    if (visibleCount === 0) {
        if (!emptyState) {
            emptyState = document.createElement('div');
            emptyState.className = 'empty-state';
            emptyState.textContent = 'No hay transferencias que coincidan con tu búsqueda.';
            transfersList.appendChild(emptyState);
        }
    } else if (emptyState) {
        emptyState.remove();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById("transferModal");
    const btnNueva = document.querySelector(".add-btn"); // Tu botón actual
    const spanCerrar = document.querySelector(".close-btn");

    // Abrir al hacer clic en "+ Nueva transferencia"
    if (btnNueva) {
        btnNueva.addEventListener('click', () => {
            modal.style.display = "block";
        });
    }

    // Cerrar al hacer clic en la X
    if (spanCerrar) {
        spanCerrar.addEventListener('click', () => {
            modal.style.display = "none";
        });
    }

    // Cerrar al hacer clic fuera del modal
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});
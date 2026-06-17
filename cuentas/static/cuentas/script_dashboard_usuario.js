/* ============================================
   SMARTWALLET - DASHBOARD USUARIO
   FUNCIONALIDAD - Dashboard Usuario
   ============================================ */

// ============================================
// Elementos del DOM
// ============================================
const navItems = document.querySelectorAll('.nav-item');
const notificationBtn = document.querySelector('.notification-btn');
const addBtn = document.querySelector('.add-btn');
const userProfile = document.querySelector('.user-profile');
const movementItems = document.querySelectorAll('.movement-item');

// ============================================
// NAVEGACIÓN - Cambio de item activo
// ============================================
navItems.forEach(item => {
    item.addEventListener('click', function(e) {
        // Obtener el href del enlace
        const href = this.getAttribute('href');

        // Si el href no es "#", permitir la navegación
        if (href && href !== '#') {
            // Remover clase active de todos los items
            navItems.forEach(nav => nav.classList.remove('active'));

            // Agregar clase active al item clickeado
            this.classList.add('active');

            // Log para debugging
            const navText = this.textContent.trim();
            console.log('Navegando a:', navText, '(' + href + ')');

            // Navegar a la página
            window.location.href = href;
        } else {
            // Para enlaces con "#", solo prevenir comportamiento por defecto
            e.preventDefault();
            
            // Remover clase active de todos los items
            navItems.forEach(nav => nav.classList.remove('active'));

            // Agregar clase active al item clickeado
            this.classList.add('active');

            const navText = this.textContent.trim();
            console.log('Opción no disponible:', navText);
        }
    });
});

// ============================================
// NOTIFICACIONES
// ============================================
notificationBtn.addEventListener('click', function() {
    const badge = this.querySelector('.notification-badge');

    // Simulación de lectura de notificación
    if (badge && badge.textContent !== '0') {
        badge.textContent = '0';
        badge.style.opacity = '0.5';

        // Mostrar mensaje en consola
        console.log('Notificación leída');

        // Restaurar después de 3 segundos (simulación)
        setTimeout(() => {
            badge.textContent = '1';
            badge.style.opacity = '1';
        }, 3000);
    }

    // Alert de demostración
    alert('📬 Centro de notificaciones\n\nNo tienes nuevas notificaciones en este momento.');
});

// ============================================
// BOTÓN AGREGAR
// ============================================
addBtn.addEventListener('click', function() {
    console.log('Abriendo modal de agregar...');

    // Simulación de modal
    const options = ['Transferencia', 'Recarga', 'Pago de servicios', 'Cancelar'];
    const userChoice = prompt(
        'Selecciona una acción:\n\n1. Transferencia\n2. Recarga\n3. Pago de servicios\n4. Cancelar\n\nEscribe el número:',
        '1'
    );

    if (userChoice) {
        const choice = parseInt(userChoice);
        switch(choice) {
            case 1:
                console.log('Iniciando transferencia...');
                alert('🏦 Transferencia\n\nEsta funcionalidad abrirá el formulario de transferencia.');
                break;
            case 2:
                console.log('Iniciando recarga...');
                alert('📱 Recarga\n\nEsta funcionalidad abrirá el formulario de recarga móvil.');
                break;
            case 3:
                console.log('Iniciando pago de servicios...');
                alert('💡 Pago de Servicios\n\nEsta funcionalidad abrirá el formulario de pago de servicios.');
                break;
            default:
                console.log('Operación cancelada');
        }
    }
});

// ============================================
// PERFIL DE USUARIO
// ============================================
userProfile.addEventListener('click', function() {
    console.log('Abriendo menú de perfil...');

    // Simulación de dropdown
    alert('👤 Perfil de Usuario\n\nUsuario: Juan D.\nEmail: juan.d@example.com\nCuenta activa');
});

// ============================================
// MOVIMIENTOS - Animación e interactividad
// ============================================
movementItems.forEach((item, index) => {
    // Efecto hover mejorado
    item.addEventListener('mouseenter', function() {
        this.style.transform = 'translateX(4px)';
        this.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.1)';
    });

    item.addEventListener('mouseleave', function() {
        this.style.transform = 'translateX(0)';
        this.style.boxShadow = 'none';
    });

    // Click en movimiento
    item.addEventListener('click', function() {
        const title = this.querySelector('.movement-title').textContent;
        const detail = this.querySelector('.movement-detail').textContent;
        const amount = this.querySelector('.amount-value').textContent;

        console.log(`Detalles del movimiento: ${title} - ${detail} - ${amount}`);

        // Simulación de vista de detalles
        showMovementDetails(title, detail, amount);
    });

    // Agregar animación de entrada
    setTimeout(() => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(10px)';
        item.style.transition = 'all 0.5s ease';

        setTimeout(() => {
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
        }, index * 100);
    }, 100);
});

// ============================================
// LINKS "VER TODOS"
// ============================================
const seeAllLinks = document.querySelectorAll('.see-all-link');

seeAllLinks.forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();

        const parent = this.closest('.section');
        let sectionType = 'información';

        if (parent.classList.contains('primary-card-section')) {
            sectionType = 'todas mis tarjetas';
        } else if (parent.classList.contains('recent-movements-section')) {
            sectionType = 'todos los movimientos';
        }

        console.log(`Viendo ${sectionType}...`);
        alert(`📋 Mostrando ${sectionType}\n\nEsta funcionalidad abrirá una nueva página o modal con el listado completo.`);
    });
});

// ============================================
// CARDS RESUMEN - Efectos interactivos
// ============================================
const summaryCards = document.querySelectorAll('.card');

summaryCards.forEach((card, index) => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-4px)';
        this.style.boxShadow = '0 8px 20px rgba(0, 0, 0, 0.12)';
    });

    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
        this.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.08)';
    });

    card.addEventListener('click', function() {
        const title = this.querySelector('.card-title').textContent;
        const amount = this.querySelector('.card-amount').textContent;

        console.log(`Card seleccionada: ${title} - ${amount}`);
    });

    // Agregar transición suave
    this.style.transition = 'all 0.3s ease';
});

// ============================================
// TARJETA DE CRÉDITO - Animación 3D
// ============================================
const creditCard = document.querySelector('.credit-card');

if (creditCard) {
    creditCard.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.02) rotateY(2deg)';
    });

    creditCard.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1) rotateY(0deg)';
    });

    creditCard.style.transition = 'transform 0.4s ease';
    creditCard.style.cursor = 'pointer';

    // Click para ver detalles
    creditCard.addEventListener('click', function() {
        console.log('Tarjeta de crédito seleccionada');
        alert('💳 Tarjeta: Mastercard\n\nÚltimos 4 dígitos: 4532\nSaldo disponible: $1.250.000\nFecha de vencimiento: 12/26');
    });
}

// ============================================
// GRÁFICO DONUT - Información interactiva
// ============================================
const chartLegendItems = document.querySelectorAll('.legend-item');

chartLegendItems.forEach(item => {
    item.style.cursor = 'pointer';
    item.style.transition = 'all 0.3s ease';

    item.addEventListener('mouseenter', function() {
        this.style.transform = 'translateX(4px)';
        this.style.backgroundColor = '#f8f9fa';
        this.style.padding = '8px';
        this.style.borderRadius = '8px';
    });

    item.addEventListener('mouseleave', function() {
        this.style.transform = 'translateX(0)';
        this.style.backgroundColor = 'transparent';
        this.style.padding = '0';
    });

    item.addEventListener('click', function() {
        const label = this.querySelector('.legend-label').textContent;
        const value = this.querySelector('.legend-value').textContent;
        const percent = this.querySelector('.legend-percent').textContent;

        console.log(`${label}: ${value} (${percent})`);
        alert(`📊 ${label}\n\nMonto: ${value}\nPorcentaje: ${percent}`);
    });
});

// ============================================
// FUNCIONES UTILITARIAS
// ============================================

/**
 * Muestra detalles de un movimiento
 * @param {string} title - Título del movimiento
 * @param {string} detail - Detalle adicional
 * @param {string} amount - Monto del movimiento
 */
function showMovementDetails(title, detail, amount) {
    const message = `
📊 Detalles del Movimiento

Operación: ${title}
Referencia: ${detail}
Monto: ${amount}

Estado: Completado
Fecha: Hoy, 10:30 a. m.
Categoría: Transferencia
    `;

    console.log(message);
    alert(message.trim());
}

/**
 * Actualiza el saldo disponible
 * @param {number} newBalance - Nuevo saldo
 */
function updateBalance(newBalance) {
    const balanceElements = document.querySelectorAll('.card-amount');
    if (balanceElements.length > 0) {
        balanceElements[0].textContent = `$${newBalance.toLocaleString()}`;
        console.log(`Saldo actualizado: $${newBalance.toLocaleString()}`);
    }
}

/**
 * Añade animación de pulsación
 * @param {Element} element - Elemento a animar
 */
function addPulseAnimation(element) {
    element.style.animation = 'pulse 0.3s ease-in-out';
}

// ============================================
// ANIMACIONES CSS DINÁMICAS
// ============================================
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
        100% {
            transform: scale(1);
        }
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);

// ============================================
// INICIALIZACIÓN AL CARGAR LA PÁGINA
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 SmartWallet Dashboard Usuario - Inicializado');

    // Animación de entrada para cards
    const cards = document.querySelectorAll('.card, .section');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.style.animation = 'slideIn 0.5s ease-in-out';
        }, index * 50);
    });

    // Log de información del usuario
    const userName = document.querySelector('.user-name').textContent;
    console.log(`Bienvenido ${userName}`);

    // Validar conexión simulada
    simulateDataSync();
});

// ============================================
// SINCRONIZACIÓN DE DATOS (SIMULADA)
// ============================================
function simulateDataSync() {
    console.log('🔄 Sincronizando datos del Dashboard Usuario...');

    setTimeout(() => {
        console.log('✅ Datos del Dashboard Usuario sincronizados correctamente');

        // Simular actualización en tiempo real cada 60 segundos
        setInterval(() => {
            console.log('📡 Verificando nuevas transacciones en Dashboard Usuario...');
        }, 60000);
    }, 500);
}

// ============================================
// MANEJO DE ERRORES Y LOGS
// ============================================
window.addEventListener('error', function(e) {
    console.error('Error en la aplicación Dashboard Usuario:', e.error);
});

// Log de cambios en el localStorage (si se utiliza)
const logStorageChange = (key, value) => {
    console.log(`📦 localStorage actualizado: ${key} = ${value}`);
};

// ============================================
// INTERACTIVIDAD ADICIONAL - TECLADO
// ============================================
document.addEventListener('keydown', function(e) {
    // ESC para cerrar modals (simulado)
    if (e.key === 'Escape') {
        console.log('Escape presionado - cerrar modal (si existe)');
    }

    // Ctrl/Cmd + K para búsqueda rápida
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        console.log('Búsqueda rápida abierta');
        alert('🔍 Búsqueda Rápida\n\nEsta funcionalidad abrirá un buscador global.');
    }

    // F12 o Ctrl+Shift+I para desarrollador
    if (e.key === 'F12' || (e.ctrlKey && e.shiftKey && e.key === 'I')) {
        console.log('Developer Tools');
    }
});

// ============================================
// SERVICIOS WORKER SIMULADO
// ============================================
if ('serviceWorker' in navigator) {
    // Aquí iría la lógica de Service Worker en una aplicación real
    console.log('Service Workers soportados en este navegador - Dashboard Usuario');
}

// ============================================
// DETECCIÓN DE MODO OFFLINE
// ============================================
window.addEventListener('online', function() {
    console.log('✅ Conexión restaurada - Dashboard Usuario');
    simulateDataSync();
});

window.addEventListener('offline', function() {
    console.warn('⚠️ Sin conexión a internet - Dashboard Usuario');
});

console.log('✅ Script de SmartWallet Dashboard Usuario cargado correctamente');

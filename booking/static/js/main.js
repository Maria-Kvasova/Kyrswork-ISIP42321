// 🎨 Анимация при прокрутке
document.addEventListener('DOMContentLoaded', function() {
    
    // ... ваш существующий код ...
    
    // Анимация появления элементов при прокрутке
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.animate-on-scroll, .service-card, .master-card');
        
        elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementTop < windowHeight - 100) {
                element.classList.add('visible');
            }
        });
    };
    
    // Запуск при загрузке и прокрутке
    animateOnScroll();
    window.addEventListener('scroll', animateOnScroll);
    
    // Эффект параллакса для hero-секции
    const hero = document.querySelector('.hero-section');
    if (hero) {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            hero.style.backgroundPositionY = `${scrolled * 0.5}px`;
        });
    }
    
    // Плавное появление навигации при прокрутке
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }
    
    console.log('✨ Дизайн обновлён! Анимации активны!');
});
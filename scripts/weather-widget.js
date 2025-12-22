// Script minimalista para exibir ícone e temperatura atuais na barra superior
(function () {
    const INDICATOR_SELECTOR = '[data-weather-indicator]';
    const ICON_SELECTOR = '[data-weather-icon]';
    const TEMP_SELECTOR = '[data-weather-temp]';
    const CACHE_KEY = 'tv-weather-cache-v1';
    const CACHE_TTL = 10 * 60 * 1000; // 10 minutos

    const WEATHER_MAP = {
        0: { day: ['☀️', 'Céu limpo'], night: ['🌙', 'Céu limpo'] },
        1: { day: ['🌤️', 'Parcialmente ensolarado'], night: ['🌤️', 'Parcialmente limpo'] },
        2: { day: ['⛅', 'Parcialmente nublado'], night: ['☁️', 'Parcialmente nublado'] },
        3: { day: ['☁️', 'Nublado'], night: ['☁️', 'Nublado'] },
        45: { day: ['🌫️', 'Nevoeiro'], night: ['🌫️', 'Nevoeiro'] },
        48: { day: ['🌫️', 'Nevoeiro'], night: ['🌫️', 'Nevoeiro'] },
        51: { day: ['🌦️', 'Garoa leve'], night: ['🌧️', 'Garoa leve'] },
        53: { day: ['🌦️', 'Garoa'], night: ['🌧️', 'Garoa'] },
        55: { day: ['🌧️', 'Garoa intensa'], night: ['🌧️', 'Garoa intensa'] },
        56: { day: ['🌧️', 'Chuvisco congelante'], night: ['🌧️', 'Chuvisco congelante'] },
        57: { day: ['🌧️', 'Chuvisco congelante'], night: ['🌧️', 'Chuvisco congelante'] },
        61: { day: ['🌧️', 'Chuva leve'], night: ['🌧️', 'Chuva leve'] },
        63: { day: ['🌧️', 'Chuva'], night: ['🌧️', 'Chuva'] },
        65: { day: ['🌧️', 'Chuva forte'], night: ['🌧️', 'Chuva forte'] },
        66: { day: ['🌨️', 'Chuva congelante'], night: ['🌨️', 'Chuva congelante'] },
        67: { day: ['🌨️', 'Chuva congelante'], night: ['🌨️', 'Chuva congelante'] },
        71: { day: ['🌨️', 'Neve leve'], night: ['🌨️', 'Neve leve'] },
        73: { day: ['🌨️', 'Neve'], night: ['🌨️', 'Neve'] },
        75: { day: ['❄️', 'Neve intensa'], night: ['❄️', 'Neve intensa'] },
        77: { day: ['❄️', 'Cristais de gelo'], night: ['❄️', 'Cristais de gelo'] },
        80: { day: ['🌦️', 'Pancadas leves'], night: ['🌧️', 'Pancadas leves'] },
        81: { day: ['🌦️', 'Pancadas'], night: ['🌧️', 'Pancadas'] },
        82: { day: ['🌧️', 'Pancadas fortes'], night: ['🌧️', 'Pancadas fortes'] },
        85: { day: ['🌨️', 'Pancadas de neve'], night: ['🌨️', 'Pancadas de neve'] },
        86: { day: ['❄️', 'Pancadas de neve forte'], night: ['❄️', 'Pancadas de neve forte'] },
        95: { day: ['⛈️', 'Tempestade'], night: ['⛈️', 'Tempestade'] },
        96: { day: ['⛈️', 'Tempestade com granizo'], night: ['⛈️', 'Tempestade com granizo'] },
        99: { day: ['⛈️', 'Tempestade com granizo'], night: ['⛈️', 'Tempestade com granizo'] }
    };

    function selectIndicator() {
        return document.querySelector(INDICATOR_SELECTOR);
    }

    function resolveWeatherIcon(code, isDay) {
        const entry = WEATHER_MAP[code];
        if (!entry) {
            return ['ℹ️', 'Condição desconhecida'];
        }
        return isDay ? entry.day : (entry.night || entry.day);
    }

    function applyWeather(indicator, iconEl, tempEl, payload) {
        tempEl.textContent = `${payload.temperature}°`;
        iconEl.textContent = payload.icon;

        const ariaParts = ['Clima atual'];
        if (payload.city) {
            ariaParts.push(`em ${payload.city}`);
        }
        ariaParts.push(`: ${payload.description.toLowerCase()}, ${payload.temperature} graus Celsius`);
        indicator.setAttribute('aria-label', ariaParts.join(' '));
        indicator.classList.add('is-ready');
    }

    async function fetchWeather() {
        const indicator = selectIndicator();
        if (!indicator) return;

        const iconEl = indicator.querySelector(ICON_SELECTOR);
        const tempEl = indicator.querySelector(TEMP_SELECTOR);
        if (!iconEl || !tempEl) return;

        try {
            const cachedRaw = sessionStorage.getItem(CACHE_KEY);
            if (cachedRaw) {
                const cached = JSON.parse(cachedRaw);
                if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
                    applyWeather(indicator, iconEl, tempEl, cached.data);
                    return;
                }
            }

            const locationResponse = await fetch('https://ipapi.co/json/');
            if (!locationResponse.ok) {
                throw new Error('Falha ao identificar localização');
            }

            const locationData = await locationResponse.json();
            const { latitude, longitude, city } = locationData;
            if (!latitude || !longitude) {
                throw new Error('Localização indisponível');
            }

            const weatherUrl = new URL('https://api.open-meteo.com/v1/forecast');
            weatherUrl.searchParams.set('latitude', latitude);
            weatherUrl.searchParams.set('longitude', longitude);
            weatherUrl.searchParams.set('current_weather', 'true');
            weatherUrl.searchParams.set('timezone', 'auto');

            const weatherResponse = await fetch(weatherUrl.toString());
            if (!weatherResponse.ok) {
                throw new Error('Falha ao obter clima');
            }

            const weatherData = await weatherResponse.json();
            const current = weatherData?.current_weather;
            if (!current) {
                throw new Error('Clima indisponível');
            }

            const { temperature, weathercode, is_day: isDay } = current;
            const roundedTemp = Math.round(Number(temperature));
            const [icon, description] = resolveWeatherIcon(Number(weathercode), Boolean(isDay));

            const payload = {
                temperature: Number.isFinite(roundedTemp) ? roundedTemp : '--',
                icon,
                description,
                city: city || ''
            };

            applyWeather(indicator, iconEl, tempEl, payload);
            sessionStorage.setItem(CACHE_KEY, JSON.stringify({ timestamp: Date.now(), data: payload }));
        } catch (error) {
            console.warn('[weather-widget] erro ao carregar clima:', error);
            const indicator = selectIndicator();
            if (indicator) {
                indicator.hidden = true;
            }
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', fetchWeather, { once: true });
    } else {
        fetchWeather();
    }
})();




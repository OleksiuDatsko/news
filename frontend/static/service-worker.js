/*
  Service Worker для Push-сповіщень
*/

self.addEventListener('push', (event) => {
    if (!event.data) {
        console.error('Push event but no data');
        return;
    }
	console.log('Push received:', event.data.text());

    const data = event.data.json();
    const title = data.title || 'Нове сповіщення';

    const options = {
        body: data.body || '',
        data: {
            url: data.url || '/'
        }
    };

    event.waitUntil(
        self.registration.showNotification(title, options)
    );
});

self.addEventListener('notificationclick', (event) => {
    event.notification.close();

    const urlToOpen = event.notification.data.url || '/';

    event.waitUntil(
        clients.matchAll({
            type: 'window',
            includeUncontrolled: true
        }).then((clientList) => {
            // Якщо вкладка з сайтом вже відкрита - фокусуємось на ній
            if (clientList.length > 0) {
                let client = clientList[0];
                for (let i = 0; i < clientList.length; i++) {
                    if (clientList[i].focused) {
                        client = clientList[i];
                    }
                }
                return client.focus().then(c => c.navigate(urlToOpen));
            }
            // Інакше - відкриваємо нову
            return clients.openWindow(urlToOpen);
        })
    );
});
import { api } from '$lib/services/api';

const VAPID_PUBLIC_KEY =
  'BFPSCKRzHlPa4WGSJykzj-eK4hsMek8u2exdJQ6JDDROOO8n83PZsnqPuJ_cnbFb9QoQewox6hfQ443jhwOHW94';

function urlBase64ToUint8Array(base64String: string) {
  const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
  const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');

  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);

  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

export async function subscribeToPush() {
  if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
    throw new Error('Push-сповіщення не підтримуються цим браузером.');
  }

  const registration = await navigator.serviceWorker.ready;

  let subscription = await registration.pushManager.getSubscription();

  if (subscription) {
    console.log('Користувач вже підписаний.');
    return subscription;
  }

  const permission = await Notification.requestPermission();
  if (permission !== 'granted') {
    throw new Error('Користувач не надав дозвіл на сповіщення.');
  }

  const applicationServerKey = urlBase64ToUint8Array(VAPID_PUBLIC_KEY);
  subscription = await registration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: applicationServerKey
  });

  try {
    await api.post('/notifications/subscribe', subscription.toJSON());
    console.log('Підписка успішно надіслана на сервер.');
  } catch (err) {
    console.error('Не вдалося надіслати підписку на сервер:', err);
    await subscription.unsubscribe();
    throw err;
  }

  return subscription;
}

export async function unsubscribeFromPush(): Promise<void> {
  if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
    return;
  }

  const registration = await navigator.serviceWorker.ready;
  const subscription = await registration.pushManager.getSubscription();

  if (!subscription) {
    console.log('Користувач не підписаний, нічого скасовувати.');
    return;
  }

  const endpoint = subscription.endpoint;
  const successfulUnsubscribe = await subscription.unsubscribe();

  if (successfulUnsubscribe) {
    console.log('Підписка успішно скасована в браузері.');

    try {
      await api.post('/notifications/unsubscribe', { endpoint });
      console.log('Відписка успішно надіслана на сервер.');
    } catch (err) {
      console.error('Помилка при видаленні підписки з сервера:', err);
    }
  } else {
    throw new Error('Не вдалося скасувати підписку в браузері.');
  }
}
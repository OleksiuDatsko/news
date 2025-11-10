import { userStore, adminStore } from '$lib/stores/authStore';
import { categoryStore } from '$lib/stores/categoryStore';
import { api, PUBLIC_ROUTES } from '$lib/services/api';
import { get } from 'svelte/store';
import { notificationStore, loadNotifications } from '$lib/stores/notificationStore';
import type { LayoutLoad } from './$types';
import type { IUser } from '$lib/types/user';
import type { IAdmin } from '$lib/types/admin';
import type { ICategory } from '$lib/types/category';

export const ssr = false;

export const load: LayoutLoad = async ({ fetch, url }) => {
  const currentPath = url.pathname;
  const isPublicRoute = PUBLIC_ROUTES.includes(currentPath);
  const promises = [];

  if (!isPublicRoute) {
    const currentUser = get(userStore);
    const currentAdmin = get(adminStore);
    const notificationsLoaded = get(notificationStore).loaded;

    if (!currentUser && !currentAdmin) {
      const authPromise = (async () => {
        const adminAuthPromise = api.get<{ admin: IAdmin }>('/admin/auth/me', fetch);
        const userAuthPromise = api.get<{ user: IUser }>('/auth/me', fetch);

        const [adminResult, userResult] = await Promise.allSettled([
          adminAuthPromise,
          userAuthPromise
        ]);

        adminStore.set(null);
        userStore.set(null);

        if (adminResult.status === 'fulfilled') {
          adminStore.set(adminResult.value.admin);
        } else if (userResult.status === 'fulfilled') {
          const { user } = userResult.value;
          const canSave = user?.permissions?.save_article;

          if (canSave && user) {
            try {
              const savedArticles = await api.get<number[]>('/articles/saved?ids=true', fetch);
              user.savedArticles = savedArticles;
            } catch (e) {
              console.error('Failed to load saved articles', e);
              user.savedArticles = [];
            }
          }

          userStore.set(user);

          if (user && !notificationsLoaded) {
            loadNotifications(fetch);
          }
        }
      })();
      promises.push(authPromise);
    }
  } else {
    userStore.set(null);
    adminStore.set(null);
  }

  const currentCategories = get(categoryStore);
  if (currentCategories.length === 0) {
    const categoryPromise = (async () => {
      try {
        const { categories } = await api.get<{ categories: ICategory[] }>('/categories/', fetch);
        categoryStore.set(categories);
      } catch (e) {
        console.error('Failed to load categories', e);
        categoryStore.set([]);
      }
    })();
    promises.push(categoryPromise);
  }

  await Promise.all(promises);
  return {};
};

<script lang="ts">
  import { adminStore } from '$lib/stores/authStore';

  const navItems = [
    {
      title: 'Управління Статтями',
      description: 'Створення, редагування та публікація новин.',
      href: '/_/articles'
    },
    {
      title: 'Управління Авторами',
      description: 'Додавання та редагування профілів авторів.',
      href: '/_/authors'
    },
    {
      title: 'Керування Категоріями',
      description: 'Редагування рубрик: Політика, Спорт тощо.',
      href: '/_/categories'
    },
    {
      title: 'Керування Підписками',
      description: 'Налаштування планів підписок.',
      href: '/_/subscriptions'
    },
    {
      title: 'Керування Користувачами',
      description: 'Перегляд списку та керування підписками.',
      href: '/_/users'
    },
    {
      title: 'Керування Рекламою',
      description: 'Налаштування банерів та перегляд статистики.',
      href: '/_/ads'
    },
    {
      title: 'Керування Адмін Користувачами',
      description: 'Перегляд списку адмінів та реєстрація нових.',
      href: '/_/admin-users'
    }
  ];
</script>

<svelte:head>
  <title>Адмін: Дашборд</title>
</svelte:head>

<div class="mb-8">
  <h1 class="text-3xl font-bold text-gray-900">Вітаємо, Адміністраторе!</h1>
  <p class="mt-1 text-lg text-gray-600">
    Ви увійшли як: <span class="font-medium text-gray-800">{$adminStore?.email}</span>
  </p>
</div>

<div class="flex flex-wrap gap-6">
  {#each navItems as item (item.href)}
    <a
      href={item.href}
      class="group bg-white p-6 rounded-lg shadow-lg hover:shadow-xl
                   border border-gray-100 hover:border-indigo-500
                   transition-all duration-300 ease-in-out transform hover:-translate-y-1"
    >
      <div class="mt-4">
        <h3
          class="text-lg font-semibold text-gray-900 group-hover:text-indigo-600 transition-colors duration-300"
        >
          {item.title}
        </h3>
        <p class="mt-1 text-sm text-gray-500">
          {item.description}
        </p>
      </div>

      <div class="mt-4 text-sm font-medium text-indigo-600 group-hover:text-indigo-700">
        Перейти <span class="group-hover:translate-x-1 transition-transform inline-block"
          >&rarr;</span
        >
      </div>
    </a>
  {/each}
</div>

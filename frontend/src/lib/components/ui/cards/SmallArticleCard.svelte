<script lang="ts">
  import type { IArticle } from '$lib/types/article';

  let { article }: { article: IArticle } = $props();

  function formatDate(dateString: string) {
    return new Date(dateString).toLocaleDateString('uk-UA', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }
</script>

<a href="/articles/{article.id}" class="font-medium text-indigo-600 hover:underline">
  {article.title}
</a>
<br />
<a href="/_/articles/{article.id}" class="text-sm text-gray-500 hover:underline"> Редагувати </a>
<div class="text-sm text-gray-500">
  <span>{article.status}</span> -
  <span>{formatDate(article.created_at)}</span>
  <br />
  <span>{article.author.first_name} {article.author.last_name}</span> -
  <span>{article.category.name}</span>
</div>

<script lang="ts">
  import { api } from '$lib/services/api';
  import { userStore } from '$lib/stores/authStore';
  import type { IComment } from '$lib/types/comment';
  import CommentItem from './CommentItem.svelte';
  import CommentForm from './CommentForm.svelte';
  import { onMount } from 'svelte';

  let { articleId }: { articleId: number } = $props();

  let comments = $state<IComment[]>([]);
  let isLoading = $state(true);
  let error = $state('');

  const canComment = $userStore?.permissions?.comment;

  onMount(async () => {
    try {
      const data = await api.get<{ comments: IComment[] }>(`/articles/${articleId}/comments`);
      comments = data.comments;
    } catch (e: any) {
      error = 'Не вдалося завантажити коментарі.';
      console.error(e);
    } finally {
      isLoading = false;
    }
  });

  function handleCommentPosted(newComment: IComment) {
    comments = [newComment, ...comments];
  }
</script>

<div class="mt-12 border-t pt-8">
  <h2 class="text-2xl font-bold mb-6">Коментарі ({comments.length})</h2>

  {#if canComment}
    <CommentForm {articleId} onCommentPosted={handleCommentPosted} />
  {:else if $userStore}
    <div class="p-4 bg-yellow-50 border border-yellow-200 rounded-md text-yellow-800 text-sm">
      Ваш поточний план підписки не дозволяє залишати коментарі.
    </div>
  {:else}
    <div class="p-4 bg-gray-100 border border-gray-200 rounded-md text-gray-700 text-sm">
      Будь ласка, <a href="/auth/login" class="font-medium text-indigo-600 hover:underline"
        >увійдіть</a
      >
      або
      <a href="/auth/register" class="font-medium text-indigo-600 hover:underline">зареєструйтеся</a
      >, щоб залишати коментарі.
    </div>
  {/if}

  <div class="mt-8 space-y-4">
    {#if isLoading}
      <p class="text-gray-500">Завантаження коментарів...</p>
    {:else if error}
      <p class="text-red-500">{error}</p>
    {:else if comments.length === 0 && canComment}
      <p class="text-gray-500">Ще немає коментарів. Будьте першим!</p>
    {:else if comments.length === 0}
      <p class="text-gray-500">Ще немає коментарів.</p>
    {:else}
      {#each comments as comment (comment.id)}
        <CommentItem {comment} />
      {/each}
    {/if}
  </div>
</div>

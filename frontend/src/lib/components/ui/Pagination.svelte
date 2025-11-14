<script lang="ts">
  import { goto } from '$app/navigation';
  import { page } from '$app/state';

  let {
    totalItems,
    perPage,
    currentPage,
    showTotal = true
  }: {
    totalItems: number;
    perPage: number;
    currentPage: number;
    showTotal?: boolean;
  } = $props();

  let totalPages = $derived(Math.ceil(totalItems / perPage));

  function onPageChange(newPage: number) {
    if (newPage < 1 || newPage > totalPages) {
      return;
    }
    const newParams = new URLSearchParams(page.url.searchParams);
    newParams.set('page', newPage.toString());
    console.log('Navigating to page:', newPage);
    goto(`?${newParams.toString()}`);
  }

  function createPaginationItems() {
    const items: (number | '...')[] = [];
    const maxPagesToShow = 5;
    const sidePages = 1;

    if (totalPages <= maxPagesToShow + sidePages) {
      for (let i = 1; i <= totalPages; i++) {
        items.push(i);
      }
    } else {
      items.push(1);
      if (currentPage > sidePages + 2) {
        items.push('...');
      }

      let start = Math.max(2, currentPage - 1);
      let end = Math.min(totalPages - 1, currentPage + 1);

      if (currentPage <= sidePages + 2) {
        start = 2;
        end = maxPagesToShow;
      } else if (currentPage >= totalPages - sidePages - 1) {
        start = totalPages - maxPagesToShow + 1;
        end = totalPages - 1;
      }

      for (let i = start; i <= end; i++) {
        items.push(i);
      }

      if (currentPage < totalPages - sidePages - 1) {
        items.push('...');
      }
      items.push(totalPages);
    }
    return items;
  }

  let paginationItems = $derived(createPaginationItems());
</script>

{#if totalPages > 1}
  <nav class="flex items-center justify-between border-t border-gray-200 px-4 py-3 sm:px-6 mt-6">
    <div class="flex-1 justify-between sm:flex sm:items-center">
      {#if showTotal}
        <div>
          <p class="text-sm text-gray-700">
            Показано
            <span class="font-medium">{(currentPage - 1) * perPage + 1}</span>
            -
            <span class="font-medium">{Math.min(currentPage * perPage, totalItems)}</span>
            з
            <span class="font-medium">{totalItems}</span>
            результатів
          </p>
        </div>
      {/if}
      <div>
        <ul class="isolate inline-flex -space-x-px rounded-md shadow-sm" aria-label="Pagination">
          <li
            class:disabled={currentPage === 1}
            class="relative inline-flex items-center rounded-l-md text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0"
            class:opacity-50={currentPage === 1}
            class:cursor-not-allowed={currentPage === 1}
          >
            <button
              onclick={() => onPageChange(currentPage - 1)}
              disabled={currentPage === 1}
              class="h-full w-full mx-2"
            >
              <span class="sr-only">Previous</span>
              &lsaquo;
            </button>
          </li>

          {#each paginationItems as item}
            {#if typeof item === 'number'}
              <li
                aria-current={item === currentPage ? 'page' : undefined}
                class="relative inline-flex items-center text-sm font-semibold ring-1 ring-inset ring-gray-300 focus:z-20 focus:outline-offset-0"
                class:z-10={item === currentPage}
                class:bg-indigo-600={item === currentPage}
                class:text-white={item === currentPage}
                class:focus-visible:outline-indigo-600={item === currentPage}
                class:text-gray-900={item !== currentPage}
                class:hover:bg-gray-50={item !== currentPage}
              >
                <button
                  onclick={() => onPageChange(item)}
                  disabled={item === currentPage}
                  class="h-full w-full px-4 py-2"
                >
                  {item}
                </button>
              </li>
            {:else}
              <li
                class="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-700 ring-1 ring-inset ring-gray-300"
              >
                ...
              </li>
            {/if}
          {/each}

          <li
            class:disabled={currentPage === totalPages}
            class="relative inline-flex items-center rounded-r-md text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0"
            class:opacity-50={currentPage === totalPages}
            class:cursor-not-allowed={currentPage === totalPages}
          >
            <button
              onclick={() => onPageChange(currentPage + 1)}
              disabled={currentPage === totalPages}
              class="h-full w-full m-2"
            >
              <span class="sr-only">Next</span>
              &rsaquo;
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
{/if}

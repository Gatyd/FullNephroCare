<template>
  <div class="flex items-center justify-between border-t border-gray-200 dark:border-gray-700 px-4 py-3 sm:px-6">
    <!-- Mobile view -->
    <div class="flex flex-1 justify-between sm:hidden">
      <button
        @click="previousPage"
        :disabled="currentPage === 1"
        class="relative inline-flex items-center px-4 py-2 text-sm font-medium rounded-md"
        :class="[
          currentPage === 1 
            ? 'text-gray-400 dark:text-gray-500 cursor-not-allowed' 
            : 'text-blue-600 dark:text-blue-400 hover:bg-gray-50 dark:hover:bg-gray-700'
        ]"
      >
        Précédent
      </button>
      <button
        @click="nextPage"
        :disabled="currentPage === totalPages"
        class="relative ml-3 inline-flex items-center px-4 py-2 text-sm font-medium rounded-md"
        :class="[
          currentPage === totalPages 
            ? 'text-gray-400 dark:text-gray-500 cursor-not-allowed' 
            : 'text-blue-600 dark:text-blue-400 hover:bg-gray-50 dark:hover:bg-gray-700'
        ]"
      >
        Suivant
      </button>
    </div>

    <!-- Desktop view -->
    <div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
      <div>
        <p class="text-sm text-gray-700 dark:text-gray-300">
          Affichage de
          <span class="font-medium">{{ startIndex }}</span>
          à
          <span class="font-medium">{{ endIndex }}</span>
          sur
          <span class="font-medium">{{ total }}</span>
          résultats
        </p>
      </div>

      <div>
        <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
          <!-- Previous Page -->
          <button
            @click="previousPage"
            :disabled="currentPage === 1"
            class="relative inline-flex items-center px-2 py-2 rounded-l-md border text-sm font-medium"
            :class="[
              currentPage === 1 
                ? 'bg-gray-100 dark:bg-gray-800 cursor-not-allowed' 
                : 'hover:bg-gray-50 dark:hover:bg-gray-700',
              'border-gray-300 dark:border-gray-600'
            ]"
          >
            <span class="sr-only">Précédent</span>
            <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
          </button>

          <!-- Page Numbers -->
          <template v-for="page in visiblePages" :key="page">
            <button
              v-if="page !== '...'"
              @click="goToPage(page)"
              :class="[
                page === currentPage
                  ? 'z-10 bg-blue-50 dark:bg-blue-900 border-blue-500 text-blue-600 dark:text-blue-200'
                  : 'bg-white dark:bg-gray-800 border-gray-300 dark:border-gray-600 text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700',
                'relative inline-flex items-center px-4 py-2 border text-sm font-medium'
              ]"
            >
              {{ page }}
            </button>
            <span
              v-else
              class="relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-700 dark:text-gray-400"
            >
              ...
            </span>
          </template>

          <!-- Next Page -->
          <button
            @click="nextPage"
            :disabled="currentPage === totalPages"
            class="relative inline-flex items-center px-2 py-2 rounded-r-md border text-sm font-medium"
            :class="[
              currentPage === totalPages 
                ? 'bg-gray-100 dark:bg-gray-800 cursor-not-allowed' 
                : 'hover:bg-gray-50 dark:hover:bg-gray-700',
              'border-gray-300 dark:border-gray-600'
            ]"
          >
            <span class="sr-only">Suivant</span>
            <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
            </svg>
          </button>
        </nav>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Pagination',

  props: {
    currentPage: {
      type: Number,
      required: true
    },
    perPage: {
      type: Number,
      required: true
    },
    total: {
      type: Number,
      required: true
    }
  },

  emits: ['update:currentPage'],

  computed: {
    totalPages() {
      return Math.ceil(this.total / this.perPage)
    },

    startIndex() {
      return ((this.currentPage - 1) * this.perPage) + 1
    },

    endIndex() {
      return Math.min(this.startIndex + this.perPage - 1, this.total)
    },

    visiblePages() {
      const delta = 2
      const range = []
      const rangeWithDots = []
      let l

      for (let i = 1; i <= this.totalPages; i++) {
        if (
          i === 1 || 
          i === this.totalPages || 
          i >= this.currentPage - delta && 
          i <= this.currentPage + delta
        ) {
          range.push(i)
        }
      }

      for (const i of range) {
        if (l) {
          if (i - l === 2) {
            rangeWithDots.push(l + 1)
          } else if (i - l !== 1) {
            rangeWithDots.push('...')
          }
        }
        rangeWithDots.push(i)
        l = i
      }

      return rangeWithDots
    }
  },

  methods: {
    previousPage() {
      if (this.currentPage > 1) {
        this.$emit('update:currentPage', this.currentPage - 1)
      }
    },

    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.$emit('update:currentPage', this.currentPage + 1)
      }
    },

    goToPage(page) {
      this.$emit('update:currentPage', page)
    }
  }
}
</script>
<script setup lang="ts">
import { UChip } from '#components'

interface Props {
  count: number
  animate?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  animate: true
})

const isVisible = computed(() => props.count > 0)
</script>

<template>
  <UChip
    v-if="isVisible"
    :class="{ 'animate-bounce-in': animate }"
    color="error"
    size="xs"
    :label="count.toString()"
    variant="solid"
    class="min-w-[20px] h-[20px] flex items-center justify-center"
  />
</template>

<style scoped>
.animate-bounce-in {
  animation: bounceIn 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

@keyframes bounceIn {
  0% {
    opacity: 0;
    transform: scale(0.3);
  }
  50% {
    opacity: 0.9;
    transform: scale(1.1);
  }
  70% {
    transform: scale(0.9);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
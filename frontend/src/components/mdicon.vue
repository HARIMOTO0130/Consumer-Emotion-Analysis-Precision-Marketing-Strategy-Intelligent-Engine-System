<template>
  <Icon
    :icon="fullIconName"
    :width="size"
    :height="size"
    :style="{color}"
    :rotate="rotate ? ` ${rotate}deg` : undefined"
  />
</template>

<script setup lang="ts">
import { Icon } from '@iconify/vue'

const props = defineProps({
  name: {
    type: String,
    required: true,
  },
  color: {
    type: String,
    default: '#000',
  },
  size: {
    type: [String, Number],
    default: '20',
  },
  rotate: {
    type: [String, Number],
    default: '0',
  },
})

const fullIconName = `material-symbols:${props.name}`
</script>
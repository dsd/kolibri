<template>

  <!-- z-index 7 - one beneath top menu bar for nested elevations -->
  <BaseToolbar style="z-index: 7;">
    <div class="container" :style="{ flexWrap: windowBreakpoint > 0 ? 'nowrap' : 'wrap' }">
      <TextTruncatorCss
        class="requirements"
        :text="overallStatusStrings.$tr('goal', { count: requiredCorrectAnswers })"
      />
      <span>
        <slot name="hint"></slot>
      </span>
    </div>
  </BaseToolbar>

</template>


<script>

  import commonCoreStrings from 'kolibri.coreVue.mixins.commonCoreStrings';
  import BaseToolbar from 'kolibri.coreVue.components.BaseToolbar';
  import TextTruncatorCss from 'kolibri.coreVue.components.TextTruncatorCss';
  import KResponsiveWindowMixin from 'kolibri-design-system/lib/KResponsiveWindowMixin';
  import { crossComponentTranslator } from 'kolibri.utils.i18n';
  import OverallStatus from './OverallStatus.vue';

  const overallStatusStrings = crossComponentTranslator(OverallStatus);

  export default {
    name: 'LessonMasteryBar',
    components: {
      BaseToolbar,
      TextTruncatorCss,
    },
    mixins: [KResponsiveWindowMixin, commonCoreStrings],
    props: {
      // typically this would be "m" from "m of n" mastery model
      requiredCorrectAnswers: {
        type: Number,
        required: true,
      },
    },
    data() {
      return {
        overallStatusStrings,
      };
    },
  };

</script>


<style lang="scss" scoped>

  .container {
    display: flex;
    justify-content: space-between;
    padding-top: 16px;
    padding-bottom: 8px;
  }

  .requirements {
    min-width: 0; // allow text to be shrinked and truncated
    margin-right: 8px;
  }

</style>

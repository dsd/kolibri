<template>

  <CoreBase
    :immersivePage="true"
    :immersivePagePrimary="true"
    immersivePageIcon="back"
    :immersivePageRoute="toolbarRoute"
    :appBarTitle="exam ? exam.title : null"
    :pageTitle="title"
    :authorized="userIsAuthorized"
    authorizedRole="adminOrCoach"
  >
    <QuestionLearnersReport
      @navigate="handleNavigation"
    />
  </CoreBase>

</template>


<script>

  import { mapState } from 'vuex';
  import commonCoach from '../common';
  import QuestionLearnersReport from '../common/QuestionLearnersReport';

  export default {
    name: 'ReportsQuizQuestionPage',
    components: {
      QuestionLearnersReport,
    },
    mixins: [commonCoach],
    computed: {
      ...mapState('questionDetail', ['title', 'exam']),
      toolbarRoute() {
        const backRoute = this.backRouteForQuery(this.$route.query);
        return backRoute || this.classRoute('ReportsQuizQuestionListPage', {});
      },
    },
    methods: {
      handleNavigation(params) {
        this.$router.push({
          name: this.name,
          params: {
            classId: this.$route.params.classId,
            quizId: this.$route.params.quizId,
            ...params,
          },
        });
      },
    },
  };

</script>


<style lang="scss" scoped></style>

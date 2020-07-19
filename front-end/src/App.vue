<template>
  <div id="app">
    <el-button @click="get_copilot" type="primary" style="margin-left: 16px;">open</el-button>

    <el-drawer title="I am the title" :visible.sync="drawer" :with-header="false">
      <span>Hi there!</span>
    </el-drawer>
  </div>
</template>

<script>
export default {
  data() {
    return {
      drawer: false,
      content:"",
      comp_output:"",
      language:"",
      question_df:"",
      question_time:"",
      answer_df:"",
      answer_time:"",
    };
  },
  mounted: function(){
    this.load_sample_data();
  },
  methods: {
    load_sample_data(){
      this.$axios.get("/sample_data.json").then(response =>{
          self.response_data = response.data[0];
          console.log(self.response_data)
          this.content = response_data.content;
          this.comp_output = response_data.comp_output;
          this.language = response_data.language;
      }
      )
    },
    get_copilot() {
      this.$axios
        .get("http://127.0.0.1:5000/api/get_recommendation", {
          params: {
            comp_output: this.comp_output,
            content: this.content,
            language: this.language,
          }
        })
        .then(response => {
          self.response_data = response.data;
          this.content = response_data.content;
          this.d4 = response_data.d4;
          this.$notify({
            title: "Search successful!",
            type: "success",
            message: "Got " + this.content + " hits in " + this.d4 + "s",
            duration: 5000
          });
        });
    }
  }
};
</script>

<style>
#app {
  font-family: Helvetica, sans-serif;
  text-align: center;
}
</style>
